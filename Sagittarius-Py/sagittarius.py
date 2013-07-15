#!/usr/local/bin/python
# coding: utf-8
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import app_identity

import jinja2
import webapp2


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
        #q = q.order(-DBObject.date)

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
        # Object properties specified
        properties = self.request.get_all('p')
        if not properties:
            properties.append('object_type::' + DEFAULT_DBOBJECT_TYPE)
            properties.append('object_name::' + DEFAULT_DBOBJECT_NAME)

        obj = DBObject()
        for p in properties:
            parts = p.split('::')
            if (parts[0] == 'object_type'):
                obj.object_type = parts[1]
            elif (parts[0] == 'object_name'):
                obj.object_name = parts[1]
            else:
                setattr(obj, parts[0], parts[1])

        obj.put()
        # @TODO: Response?
        #self.response.write("<resp>Added: " + obj.to_dict() + "</resp>")


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
    ('/mail', SendMail),
], debug=True)