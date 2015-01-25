var gulp       = require('gulp');
var deploy     = require('gulp-gh-pages');

var del        = require('del');


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
	]
};

gulp.task('deploy', function() {
	return gulp.src(paths.deploy)
		.pipe(deploy());
});

gulp.task('wiki-post-clean', function(cb) {
	del(paths.wikiClean, cb);
});
