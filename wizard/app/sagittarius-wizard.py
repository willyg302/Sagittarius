'''
A helper wizard for the Sagittarius Online Game Service.
Copyright: (c) 2015 William Gaul
License: MIT, see LICENSE for more details
'''
import httplib, urllib, json

from flask import Flask, render_template, request

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

def run_recipe(recipe, id, password):
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

	print handle, params

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
		return parsed
	except (ValueError, KeyError, TypeError):
		return json.dumps({})

def save_recipe(recipe):
	recipes = load_data()
	recipes[recipe['name']] = recipe
	dump_data(recipes)
	return True

def delete_recipe(recipe):
	recipes = load_data()
	del recipes[recipe['name']]
	dump_data(recipes)
	return True


########################################
# MAIN APP
########################################

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
	req = request.get_json()
	return run_recipe(req['data'], req['id'], req['pass'])

@app.route('/recipe', methods=['POST'])
def recipe():
	req = request.get_json()
	return {
		'save': save_recipe,
		'delete': delete_recipe
	}[req['action']](req['data'])


if __name__ == '__main__':
	app.run(port=8080)
