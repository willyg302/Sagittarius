var metalsmith  = require('metalsmith');
var collections = require('metalsmith-collections');
var define      = require('metalsmith-define');
var markdown    = require('metalsmith-markdown');
var permalinks  = require('metalsmith-permalinks');
var templates   = require('metalsmith-templates');

metalsmith(__dirname)
	.source('src')
	.use(define({
		owner: {
			name: 'WillyG Productions',
			uri: 'http://willyg302.github.io/'
		}
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
	.use(permalinks())
	.use(templates({
		engine: 'jade',
		directory: 'templates'
	}))
	.destination('build')
	.build(function(err) {
		err && console.log(err);
	});
