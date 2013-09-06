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
# Note that this is where END TILDES are handled
def getObjectProperties(obj, projections):
	ret = {}
	if not projections:
		projections = obj._properties.keys()
	for p in projections:
		prop = str(getattr(obj, p[:-1] if p.endswith('~') else p, 'null'))
		if p.endswith('~'):
			p = p[:-1]
			prop = encrypt.encrypt(prop, SAGPASS)
		ret[p] = prop
	return ret

def generateQuery(filters):
	q = DBObject.query()
	for f in filters:
		parts = f.split('::')
		q = q.filter(ndb.GenericProperty(parts[0]) == parts[1])
	#q = q.order(-DBObject.date) # We can't do this because only simple queries are allowed on Expandos
	return q


class Request(webapp2.Request):

	def preprocess_value(self, value):
		if value.startswith('~'):
			value = encrypt.decrypt(value, SAGPASS)
		# Mustache substitutions!
		value = value.replace('{{IP}}', self.remote_addr)
		return value

	def get_all(self, argument_name, default_value=None):
		ret = super(Request, self).get_all(argument_name, default_value)
		return [self.preprocess_value(r) for r in ret]


class RequestHandler(webapp2.RequestHandler):

	def __init__(self, request=None, response=None):
		super(RequestHandler, self).__init__(request, response)
		self.response_obj = {'success': 'y'} # We say that we are successful by default

	def post(self):
		self.response.headers['Access-Control-Allow-Origin'] = '*'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST'

	def fail(self, msg):
		self.response_obj['success'] = msg

	def send_response(self):
		self.response.write(json.dumps(self.response_obj, separators=(',',':')))


class GetAction(RequestHandler):

	def post(self):
		super(GetAction, self).post()
		dbobjects = []

		limit = int(self.request.get('rlim', '20'))
		offset = int(self.request.get('roff', '0'))
		filters = self.request.get_all('f')
		projections = self.request.get_all('p')

		q = generateQuery(filters)
		for obj in q.iter(limit=limit, offset=offset):
			dbobjects.append(getObjectProperties(obj, projections))

		self.response_obj['dbobjects'] = dbobjects
		self.send_response()


class AddAction(RequestHandler):

	def post(self):
		super(AddAction, self).post()

		# Object attributes specified (if none, we add a "default object")
		attributes = self.request.get_all('a')
		if not attributes:
			attributes.append('object_type::' + DEFAULT_DBOBJECT_TYPE)
			attributes.append('object_name::' + DEFAULT_DBOBJECT_NAME)

		obj = DBObject()
		for a in attributes:
			parts = a.split('::')
			setattr(obj, parts[0], parts[1])
		obj.put()

		self.send_response()


class ModAction(RequestHandler):

	def post(self):
		super(ModAction, self).post()
		dbobjects = []

		limit = int(self.request.get('rlim', '20'))
		offset = int(self.request.get('roff', '0'))
		filters = self.request.get_all('f')
		projections = self.request.get_all('p')
		bReturn = self.request.get('rres', 'false')
		modifications = self.request.get_all('m')

		q = generateQuery(filters)

		# Iterate over results and make modifications (We use fetch here because we're modifying in-loop)
		results = q.fetch(limit, offset=offset)
		for obj in results:
			for m in modifications:
				parts = m.split('::')
				setattr(obj, parts[0], parts[1])
			#obj.put() # See below
			if bReturn != 'false':
				dbobjects.append(getObjectProperties(obj, projections))

		# Batch-put (this ensures near-atomicity)
		ndb.put_multi(results)

		if bReturn != 'false':
			self.response_obj['dbobjects'] = dbobjects
		self.send_response()


class DelAction(RequestHandler):

	def post(self):
		super(DelAction, self).post()
		dbobjects = []

		limit = int(self.request.get('rlim', '20'))
		offset = int(self.request.get('roff', '0'))
		filters = self.request.get_all('f')
		projections = self.request.get_all('p')
		bReturn = self.request.get('rres', 'false')

		q = generateQuery(filters)

		# Iterate over results (We use fetch here because we batch-delete after)
		results = q.fetch(limit, offset=offset)
		if bReturn != 'false':
			for obj in results:
				dbobjects.append(getObjectProperties(obj, projections))

		# Batch-delete (this ensures near-atomicity)
		ndb.delete_multi([r.key for r in results])

		if bReturn != 'false':
			self.response_obj['dbobjects'] = dbobjects
		self.send_response()


class SendMail(RequestHandler):

	def post(self):
		super(SendMail, self).post()

		subject = self.request.get('subj')
		content = self.request.get('mesg')
		sender = self.request.get('send', 'admin')
		receiver = self.request.get('recv')

		mail.send_mail(sender + "@" + app_identity.get_application_id() + ".appspotmail.com", receiver, subject, content)

		# Send a quick success response (in reality, we should probably kick back errors, if any)
		self.send_response()


class Leaderboard(RequestHandler):

	def getLeaderboard(self, lb_name, limit, offset):
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			data = json.loads(str(getattr(lb, 'data')))
			if (offset < len(data)):
				upto = min(len(data), limit + offset)
				self.response_obj['data'] = data[offset:upto]

	def addLeaderboard(self, lb_name, sort, maxsize):
		lb = DBObject()
		setattr(lb, 'object_type', 'leaderboard')
		setattr(lb, 'object_name', lb_name)
		setattr(lb, 'sort', sort)
		setattr(lb, 'maxsize', maxsize)
		lb.set_text_prop('data', '[]')
		lb.put()

	def postToLeaderboard(self, lb_name, score, scoreid):
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			data = json.loads(str(getattr(lb, 'data')))
			descending = (str(getattr(lb, 'sort')) == 'desc')
			maxsize = int(getattr(lb, 'maxsize'))
			data.append({'score': score, 'sid': scoreid})
			data = sorted(data, key=lambda k: k['score'], reverse=descending)[:maxsize]
			lb.set_text_prop('data', json.dumps(data, separators=(',',':')))
			lb.put()

	def purgeLeaderboard(self, lb_name):
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			lb.set_text_prop('data', '[]')
			lb.put()

	def deleteLeaderboard(self, lb_name):
		q = DBObject.query().filter(ndb.GenericProperty('object_type') == 'leaderboard').filter(ndb.GenericProperty('object_name') == lb_name)
		lb = q.get() # LB should be unique
		if lb != None:
			lb.key.delete()

	def post(self):
		super(Leaderboard, self).post()
		action = self.request.get('act')
		lb_name = self.request.get('n', 'leaderboard')

		if action == 'get':
			limit = int(self.request.get('rlim', '20'))
			offset = int(self.request.get('roff', '0'))
			self.getLeaderboard(lb_name, limit, offset)
		elif action == 'add':
			sort = self.request.get('s', 'desc')
			maxsize = int(self.request.get('m', '50'))
			self.addLeaderboard(lb_name, sort, maxsize)
		elif action == 'post':
			score = int(self.request.get('score'))
			scoreid = self.request.get('sid')
			self.postToLeaderboard(lb_name, score, scoreid)
		elif action == 'purge':
			self.purgeLeaderboard(lb_name)
		elif action == 'del':
			self.deleteLeaderboard(lb_name)

		self.send_response()


class Webapp(webapp2.WSGIApplication):

	request_class = Request


application = Webapp([
	('/', MainPage),
	('/index.html', MainPage),
	('/dbget', GetAction),
	('/dbadd', AddAction),
	('/dbmod', ModAction),
	('/dbdel', DelAction),
	('/mail', SendMail),
	('/ldbds', Leaderboard),
], debug=True)