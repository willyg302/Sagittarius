#!/usr/local/bin/python
# coding: utf-8

import os, urllib, jinja2, webapp2
from google.appengine.api import users, mail, app_identity
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEFAULT_DBOBJECT_TYPE = 'object'
DEFAULT_DBOBJECT_NAME = 'null'


class DBObject(ndb.Expando):
    """The base model for an object in our database."""
    object_type = ndb.StringProperty()
    object_name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            #'sagpass': os.environ.get('SAGITTARIUS_PASSWORD', 'PASS'),
            'appid': app_identity.get_application_id(),
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class GetAction(webapp2.RequestHandler):

    def post(self):
        ret = ''
        limit = int(self.request.get('rlim', '20'))
        offset = int(self.request.get('roff', '0'))

        # Our optional filters (possibly none at all)
        filters = self.request.get_all('f')

        # Projections (possibly none)
        projections = self.request.get_all('p')

        # Generate and run query
        q = DBObject.query()
        for f in filters:
            parts = f.split('::')
            q = q.filter(ndb.GenericProperty(parts[0]) == parts[1])
        #q = q.order(-DBObject.date) # We can't do this because only simple queries are allowed on Expandos

        # Iterate over results
        for obj in q.iter(limit=limit, offset=offset):
            if not projections:
                projections = obj._properties.keys()
            for p in projections:
                ret += ("<" + p + ">" + str(getattr(obj, p, 'null')) + "</" + p + ">")
            ret += '\n'

        # Send response to user!
        self.response.write("<resp>" + ret + "</resp>")


class AddAction(webapp2.RequestHandler):

    def post(self):
        ret = ''

        # Object attributes specified (if none, we add a "default object")
        attributes = self.request.get_all('a')
        if not attributes:
            attributes.append('object_type::' + DEFAULT_DBOBJECT_TYPE)
            attributes.append('object_name::' + DEFAULT_DBOBJECT_NAME)

        # Create our object
        obj = DBObject()
        for a in attributes:
            parts = a.split('::')
            setattr(obj, parts[0], parts[1])
        obj.put()

        # Generate a quick response
        for k in obj._properties.keys():
            ret += ("<" + k + ">" + str(getattr(obj, k, 'null')) + "</" + k + ">")
        self.response.write("<resp>Added object: " + ret + "</resp>")


class ModAction(webapp2.RequestHandler):

    def post(self):
        ret = ''
        limit = int(self.request.get('rlim', '20'))
        offset = int(self.request.get('roff', '0'))

        # Our optional filters (possibly none at all)
        filters = self.request.get_all('f')

        # Projections (possibly none), and whether to return results at all
        projections = self.request.get_all('p')
        bReturn = self.request.get('rres', 'false')

        # Modifications to make (possibly none)
        modifications = self.request.get_all('m')

        # Generate and run query
        q = DBObject.query()
        for f in filters:
            parts = f.split('::')
            q = q.filter(ndb.GenericProperty(parts[0]) == parts[1])
        #q = q.order(-DBObject.date) # We can't do this because only simple queries are allowed on Expandos

        # Iterate over results and make modifications (We use fetch here because we're modifying in-loop)
        results = q.fetch(limit, offset=offset)
        for obj in results:
            for m in modifications:
                parts = m.split('::')
                setattr(obj, parts[0], parts[1])
            obj.put()
            if bReturn == 'false':
                continue
            if not projections:
                projections = obj._properties.keys()
            for p in projections:
                ret += ("<" + p + ">" + str(getattr(obj, p, 'null')) + "</" + p + ">")
            ret += '\n'

        # Send response to user!
        if ret == '':
            ret = 'Success!'
        self.response.write("<resp>" + ret + "</resp>")


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
    ('/mail', SendMail),
], debug=True)