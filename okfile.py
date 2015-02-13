import os

project = 'Sagittarius'


########################################
# STARTER KITS
########################################

def build_sk_java():
	with ok.root('starter-kits/java'):
		ok.maven('compile').maven('package')

def build_sk_javascript():
	with ok.root('starter-kits/javascript'):
		ok.npm('run build')


########################################
# WIKI
########################################

def build_wiki():
	'''Build the wiki'''
	with ok.root('wiki'):
		ok.node('build.js')
	# Delete extra Metalsmith junk
	ok.node('gulp wiki-post-clean', module=True)
	# Add the downloads
	ok.node('gulp wiki-zip-sks', module=True)

def publish_wiki():
	'''Publish the wiki to GitHub Pages'''
	ok.node('gulp deploy', module=True)

def serve_wiki():
	'''Serve the wiki locally'''
	with ok.root('wiki'):
		ok.node('http-server build/', module=True)


########################################
# WIZARD
########################################

def build_wizard():
	'''Build the wizard'''
	ok.run(test_wizard)
	with ok.root('wizard'):
		ok.node('gulp', module=True)
	# Kick off install of build if needed
	if not os.path.isdir('wizard/dist/node_modules'):
		with ok.root('wizard/dist'):
			ok.npm('install')

def test_wizard():
	'''Test the wizard'''
	reporter = 'node_modules/jshint-stylish/stylish.js'
	with ok.root('wizard'):
		ok.node('jsxhint --reporter {} --exclude **/__tests__/** app/js/.'.format(reporter), module=True)
		# Run Jest
		ok.npm('test')

def serve_wizard():
	'''Serve the wizard locally'''
	with ok.root('wizard/dist'):
		ok.node('index.js')


########################################
# MAIN
########################################

def install():
	# Base stuff for Gulp
	ok.npm('install')
	# JavaScript starter kit
	with ok.root('starter-kits/javascript'):
		ok.npm('install')
	# Metalsmith and additional stuff for wiki
	with ok.root('wiki'):
		ok.npm('install')
	# Wizard
	with ok.root('wizard'):
		ok.npm('install').bower('install')

def default():
	pass
