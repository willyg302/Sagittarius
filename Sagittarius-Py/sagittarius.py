#!/usr/local/bin/python
# coding: utf-8

import os, urllib, jinja2, webapp2, json
from google.appengine.api import users, mail, app_identity
from google.appengine.ext import ndb

import encrypt


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

DEFAULT_DBOBJECT_TYPE = 'object'
DEFAULT_DBOBJECT_NAME = 'null'

SAGPASS = os.environ.get('SAGITTARIUS_PASSWORD', 'password')


class DBObject(ndb.Expando):
	"""The base model for an object in our database."""
	object_type = ndb.StringProperty()
	object_name = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now=True)


class MainPage(webapp2.RequestHandler):

	def get(self):
		template_values = {
			'appid': app_identity.get_application_id(),
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))


# Returns a dictionary with the requested object properties (or all if none specified)
def getObjectProperties(obj, projections):
	ret = {}
	if not projections:
		projections = obj._properties.keys()
	for p in projections:
		prop = str(getattr(obj, p[1:] if p.startswith('~') else p, 'null'))
		if p.startswith('~'):
			p = p[1:]
			prop = encrypt.encrypt(prop, SAGPASS)
		ret[p] = prop
	return ret

def generateQuery(filters):
	q = DBObject.query()
	for f in filters:
		if f.startswith('~'):
			f = encrypt.decrypt(f, SAGPASS)
		parts = f.split('::')
		q = q.filter(ndb.GenericProperty(parts[0]) == parts[1])
	#q = q.order(-DBObject.date) # We can't do this because only simple queries are allowed on Expandos
	return q


class GetAction(webapp2.RequestHandler):

	def post(self):
		ret = {}
		dbobjects = []

		limit = int(self.request.get('rlim', '20'))
		offset = int(self.request.get('roff', '0'))
		filters = self.request.get_all('f')
		projections = self.request.get_all('p')

		# Generate and run query
		q = generateQuery(filters)

		# Iterate over results
		for obj in q.iter(limit=limit, offset=offset):
			dbobjects.append(getObjectProperties(obj, projections))

		# Send response to user!
		ret['success'] = 'y' # Currently we just default to this being successful
		ret['dbobjects'] = dbobjects
		self.response.write("<resp>" + json.dumps(ret, separators=(',',':')) + "</resp>")


class AddAction(webapp2.RequestHandler):

	def post(self):
		ret = {}

		# Object attributes specified (if none, we add a "default object")
		attributes = self.request.get_all('a')
		if not attributes:
			attributes.append('object_type::' + DEFAULT_DBOBJECT_TYPE)
			attributes.append('object_name::' + DEFAULT_DBOBJECT_NAME)

		# Create our object
		obj = DBObject()
		for a in attributes:
			if a.startswith('~'):
				a = encrypt.decrypt(a, SAGPASS)
			parts = a.split('::')
			setattr(obj, parts[0], parts[1])
		obj.put()

		# Generate a quick response (for now, just success)
		ret['success'] = 'y'
		self.response.write("<resp>" + json.dumps(ret, separators=(',',':')) + "</resp>")


class ModAction(webapp2.RequestHandler):

	def post(self):
		ret = {}
		dbobjects = []

		limit = int(self.request.get('rlim', '20'))
		offset = int(self.request.get('roff', '0'))
		filters = self.request.get_all('f')
		projections = self.request.get_all('p')
		bReturn = self.request.get('rres', 'false')
		modifications = self.request.get_all('m')

		# Generate and run query
		q = generateQuery(filters)

		# Iterate over results and make modifications (We use fetch here because we're modifying in-loop)
		results = q.fetch(limit, offset=offset)
		for obj in results:
			for m in modifications:
				if m.startswith('~'):
					m = encrypt.decrypt(m, SAGPASS)
				parts = m.split('::')
				setattr(obj, parts[0], parts[1])
			#obj.put() # See below
			if bReturn != 'false':
				dbobjects.append(getObjectProperties(obj, projections))

		# Batch-put (this ensures near-atomicity)
		ndb.put_multi(results)

		# Send response to user!
		ret['success'] = 'y' # Currently we just default to this being successful
		if bReturn != 'false':
			ret['dbobjects'] = dbobjects
		self.response.write("<resp>" + json.dumps(ret, separators=(',',':')) + "</resp>")


class DelAction(webapp2.RequestHandler):

	def post(self):
		ret = {}
		dbobjects = []

		limit = int(self.request.get('rlim', '20'))
		offset = int(self.request.get('roff', '0'))
		filters = self.request.get_all('f')
		projections = self.request.get_all('p')
		bReturn = self.request.get('rres', 'false')

		# Generate and run query
		q = generateQuery(filters)

		# Iterate over results (We use fetch here because we batch-delete after)
		results = q.fetch(limit, offset=offset)
		if bReturn != 'false':
			for obj in results:
				dbobjects.append(getObjectProperties(obj, projections))

		# Batch-delete (this ensures near-atomicity)
		ndb.delete_multi([r.key for r in results])

		# Send response to user!
		ret['success'] = 'y' # Currently we just default to this being successful
		if bReturn != 'false':
			ret['dbobjects'] = dbobjects
		self.response.write("<resp>" + json.dumps(ret, separators=(',',':')) + "</resp>")


class SendMail(webapp2.RequestHandler):

	def post(self):
		subject = self.request.get('subj')
		content = self.request.get('mesg')
		sender = self.request.get('send', 'admin')
		receiver = self.request.get('recv')
		mail.send_mail(sender + "@" + app_identity.get_application_id() + ".appspotmail.com", receiver, subject, content)


application = webapp2.WSGIApplication([
	('/', MainPage),
	('/index.html', MainPage),
	('/dbget', GetAction),
	('/dbadd', AddAction),
	('/dbmod', ModAction),
	('/dbdel', DelAction),
	('/mail', SendMail),
], debug=True)