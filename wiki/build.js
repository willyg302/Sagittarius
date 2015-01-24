var metalsmith  = require('metalsmith');
var cleanCSS    = require('metalsmith-clean-css');
var collections = require('metalsmith-collections');
var define      = require('metalsmith-define');
var headings    = require('metalsmith-headings');
var less        = require('metalsmith-less');
var markdown    = require('metalsmith-markdown');
var permalinks  = require('metalsmith-permalinks');
var relative    = require('metalsmith-relative');
var templates   = require('metalsmith-templates');

metalsmith(__dirname)
	.source('src')
	.use(define({
		owner: {
			name: 'WillyG Productions',
			uri: 'http://willyg302.github.io/'
		}
	}))
	.use(less({
		pattern: 'less/main.less'
	}))
	.use(cleanCSS({
		files: 'css/*.css'
	}))
	.use(collections({
		starterKits: {
			pattern: 'starter-kits/**/*.md'
		}
	}))
	.use(markdown({
		gfm: true,
		smartypants: true,
		highlight: function(code, lang) {
			if (!lang) {
				return code;
			}
			try {
				return require('highlight.js').highlight(lang, code).value;
			} catch (e) {
				return code;
			}
		}
	}))
	.use(headings('h1'))
	.use(permalinks())
	.use(relative())
	.use(templates({
		engine: 'jade',
		directory: 'templates'
	}))
	.destination('build')
	.build(function(err) {
		err && console.log(err);
	});
