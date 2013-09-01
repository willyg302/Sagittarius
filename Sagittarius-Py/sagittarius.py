#!/usr/local/bin/python
# coding: utf-8

import os, urllib, jinja2, webapp2, json
from google.appengine.api import users, mail, app_identity
from google.appengine.ext import ndb

import encrypt
from utils import DynamicPropertyMixin


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

DEFAULT_DBOBJECT_TYPE = 'object'
DEFAULT_DBOBJECT_NAME = 'null'

SAGPASS = os.environ.get('SAGITTARIUS_PASSWORD', 'password')


class DBObject(ndb.Expando, DynamicPropertyMixin):
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

def enableCORS(requestHandler):
	requestHandler.response.headers['Access-Control-Allow-Origin'] = '*'
	requestHandler.response.headers['Access-Control-Allow-Methods'] = 'POST'


class GetAction(webapp2.RequestHandler):

	def post(self):
		enableCORS(self)
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
		enableCORS(self)
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
		enableCORS(self)
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
		enableCORS(self)
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
		enableCORS(self)
		subject = self.request.get('subj')
		content = self.request.get('mesg')
		sender = self.request.get('send', 'admin')
		receiver = self.request.get('recv')
		mail.send_mail(sender + "@" + app_identity.get_application_id() + ".appspotmail.com", receiver, subject, content)
		# Send a quick success response (in reality, we should probably kick back errors, if any)
		ret = {}
		ret['success'] = 'y'
		self.response.write("<resp>" + json.dumps(ret, separators=(',',':')) + "</resp>")


class Leaderboard(webapp2.RequestHandler):

	def getLeaderboard(self, lb_name, limit, offset):
		ret = {}
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			data = json.loads(str(getattr(lb, 'data')))
			if (offset < len(data)):
				upto = min(len(data), limit + offset)
				ret['data'] = data[offset:upto]
		ret['success'] = 'y'
		return ret

	def addLeaderboard(self, lb_name, sort, maxsize):
		ret = {}
		lb = DBObject()
		setattr(lb, 'object_type', 'leaderboard')
		setattr(lb, 'object_name', lb_name)
		setattr(lb, 'sort', sort)
		setattr(lb, 'maxsize', maxsize)
		lb.set_text_prop('data', '[]')
		lb.put()
		ret['success'] = 'y'
		return ret

	def postToLeaderboard(self, lb_name, score, scoreid):
		ret = {}
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			data = json.loads(str(getattr(lb, 'data')))
			descending = (str(getattr(lb, 'sort')) == 'desc')
			maxsize = int(getattr(lb, 'maxsize'))
			data.append({'score': score, 'sid': scoreid})
			data = sorted(data, key=lambda k: k['score'], reverse=descending)[:maxsize]
			#setattr(lb, 'data', json.dumps(data, separators=(',',':')))
			lb.set_text_prop('data', json.dumps(data, separators=(',',':')))
			lb.put()
		ret['success'] = 'y'
		return ret

	def purgeLeaderboard(self, lb_name):
		ret = {}
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			#setattr(lb, 'data', '[]')
			lb.set_text_prop('data', '[]')
			lb.put()
		ret['success'] = 'y'
		return ret

	def deleteLeaderboard(self, lb_name):
		ret = {}
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			lb.key.delete()
		ret['success'] = 'y'
		return ret

	def post(self):
		enableCORS(self)
		ret = {}
		action = self.request.get('act')
		lb_name = self.request.get('n', 'leaderboard')

		if action == 'get':
			limit = int(self.request.get('rlim', '20'))
			offset = int(self.request.get('roff', '0'))
			ret = self.getLeaderboard(lb_name, limit, offset)
		elif action == 'add':
			sort = self.request.get('s', 'desc')
			maxsize = int(self.request.get('m', '50'))
			ret = self.addLeaderboard(lb_name, sort, maxsize)
		elif action == 'post':
			score = int(self.request.get('score'))
			scoreid = self.request.get('sid')
			ret = self.postToLeaderboard(lb_name, score, scoreid)
		elif action == 'purge':
			ret = self.purgeLeaderboard(lb_name)
		elif action == 'del':
			ret = self.deleteLeaderboard(lb_name)

		self.response.write("<resp>" + json.dumps(ret, separators=(',',':')) + "</resp>")


application = webapp2.WSGIApplication([
	('/', MainPage),
	('/index.html', MainPage),
	('/dbget', GetAction),
	('/dbadd', AddAction),
	('/dbmod', ModAction),
	('/dbdel', DelAction),
	('/mail', SendMail),
	('/ldbds', Leaderboard),
], debug=True)