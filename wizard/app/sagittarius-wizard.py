'''
A helper wizard for the Sagittarius Online Game Service.
Copyright: (c) 2015 William Gaul
License: MIT, see LICENSE for more details
'''
import os, httplib, urllib, json

from tornado import ioloop, web
from sockjs.tornado import SockJSConnection, SockJSRouter

import encrypt


DATA_FILE = 'recipes.dat'

def load_data():
	try:
		with open(DATA_FILE, 'r+') as f:
			return json.load(f)
	except IOError:
		return {}

def dump_data(data):
	with open(DATA_FILE, 'w') as f:
		json.dump(data, f)


########################################
# HANDLERS
########################################

def run_recipe(sock, recipe, id, password, **kwargs):
	headers = {
		'Content-type': 'application/x-www-form-urlencoded',
		'Accept': 'text/plain'
	}
	handle = "/" + recipe['action']

	def get_button_param(button):
		if button['type'] == 'returns':
			return 'rres=true'
		val = button['val']
		if button['enc']:
			val = encrypt.encrypt(val, password)
		return '{}={}'.format(button['key'], val)

	params = '&'.join([get_button_param(b) for b in recipe['buttons']])

	sock.out('Submitting to {}{}'.format(id, handle))
	sock.out('URL String: {}'.format(params))

	# Initialize connection!
	conn = httplib.HTTPConnection(id + ".appspot.com:80")
	conn.request('POST', handle, params, headers)
	resp = conn.getresponse().read()
	conn.close()

	# Handle response
	try:
		parsed = ''
		for part in json.JSONEncoder().iterencode(json.loads(resp)):
			parsed += ('"{}"'.format(encrypt.decrypt(part[1:-1], password)) if part.startswith('"~') else part)
		sock.out('Received data:\n{}'.format(json.dumps(json.loads(parsed), indent=4)))
	except (ValueError, KeyError, TypeError):
		sock.err('Error running recipe')

def save_recipe(sock, recipe, **kwargs):
	name = recipe['name']
	recipes = load_data()
	recipes[name] = recipe
	dump_data(recipes)
	sock.out('Successfully saved recipe "{}"'.format(name))

def delete_recipe(sock, recipe, **kwargs):
	name = recipe['name']
	recipes = load_data()
	if name in recipes:
		del recipes[name]
		dump_data(recipes)
		sock.out('Successfully deleted recipe "{}"'.format(name))
	else:
		sock.err('No recipe named "{}" has been saved'.format(name))


########################################
# MAIN APP
########################################

class IndexHandler(web.RequestHandler):
	def get(self):
		self.render('index.html')


class SockConnection(SockJSConnection):

	def on_message(self, message):
		payload = json.loads(message)
		{
			'run': run_recipe,
			'save': save_recipe,
			'delete': delete_recipe
		}[payload['endpoint']](self, **payload)

	def out(self, message):
		self.send(json.dumps({
			'message': message,
			'error': False
		}))

	def err(self, message):
		self.send(json.dumps({
			'message': message,
			'error': True
		}))


if __name__ == '__main__':
	TodoRouter = SockJSRouter(SockConnection, '/sock')
	web.Application([
		(r'/', IndexHandler),
		(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)})
	] + TodoRouter.urls).listen(8080)
	ioloop.IOLoop.instance().start()
