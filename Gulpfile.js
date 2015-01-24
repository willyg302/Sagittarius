var gulp       = require('gulp');
var deploy     = require('gulp-gh-pages');


var paths = {
	deploy: __dirname + '/wiki/build/**/*'
};

gulp.task('deploy', function() {
	return gulp.src(paths.deploy)
		.pipe(deploy());
});
