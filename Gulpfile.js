var gulp       = require('gulp');
var deploy     = require('gulp-gh-pages');
var zip        = require('gulp-zip');

var del        = require('del');
var merge      = require('merge-stream');
var path       = require('path');


var paths = {
	deploy: __dirname + '/wiki/build/**/*',
	wikiClean: [
		__dirname + '/wiki/build/less',
		__dirname + '/wiki/build/getting-started/css',
		__dirname + '/wiki/build/getting-started/img',
		__dirname + '/wiki/build/getting-started/less',
		__dirname + '/wiki/build/modules/css',
		__dirname + '/wiki/build/modules/img',
		__dirname + '/wiki/build/modules/less',
		__dirname + '/wiki/build/wizard/css',
		__dirname + '/wiki/build/wizard/img',
		__dirname + '/wiki/build/wizard/less'
	],
	sks: {
		all: ['java', 'javascript', 'unrealscript'],
		src: __dirname + '/starter-kits',
		dest: __dirname + '/wiki/build/starter-kits'
	}
};

gulp.task('deploy', function() {
	return gulp.src(paths.deploy)
		.pipe(deploy());
});

gulp.task('wiki-post-clean', function(cb) {
	del(paths.wikiClean, cb);
});

gulp.task('wiki-zip-sks', function() {
	var tasks = paths.sks.all.map(function(sk) {
		return gulp.src(path.join(paths.sks.src, sk, '/**/*'))
			.pipe(zip("sagittarius-" + sk + ".zip"))
			.pipe(gulp.dest(path.join(paths.sks.dest, sk)));
	});
	return merge(tasks);
});
