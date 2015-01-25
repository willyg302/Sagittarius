project = 'Sagittarius'

def build_wiki():
	'''Build the wiki'''
	with ok.root('wiki'):
		ok.node('build.js')
	# Delete extra Metalsmith junk
	ok.node('gulp wiki-post-clean', module=True)

def publish_wiki():
	'''Publish the wiki to GitHub Pages'''
	ok.node('gulp deploy', module=True)

def serve_wiki():
	'''Serve the wiki locally'''
	with ok.root('wiki'):
		ok.node('http-server build/', module=True)

def install():
	# Base stuff for Gulp
	ok.npm('install')
	# Metalsmith and additional stuff for wiki
	with ok.root('wiki'):
		ok.npm('install')

def default():
	pass
