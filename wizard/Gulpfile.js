var gulp       = require('gulp');
var less       = require('gulp-less');
var minifycss  = require('gulp-minify-css');
var uglify     = require('gulp-uglify');

var browserify = require('browserify');
var del        = require('del');
var reactify   = require('reactify');
var buffer     = require('vinyl-buffer');
var vinyl      = require('vinyl-source-stream');


var paths = {
	assets: [
		'./app/img/**/*.*',
		'./app/index.html',
		'./app/encrypt.py',
		'./app/README.md',
		'./app/recipes.dat',
		'./app/requirements.txt',
		'./app/sagittarius-wizard.py'
	],
	app: './app',
	dist: './dist',
	package: ['./dist/**/*.*', '!./dist/env/**/*.*'],
	css: './app/less/main.less',
	js: './app/js/app.js'
};

gulp.task('clean', function(cb) {
	del(paths.package, cb);
});

gulp.task('copy-assets', function() {
	return gulp.src(paths.assets, {base: paths.app})
		.pipe(gulp.dest(paths.dist));
});

gulp.task('compile-css', function() {
	return gulp.src(paths.css)
		.pipe(less())
		.pipe(minifycss())
		.pipe(gulp.dest(paths.dist));
});

gulp.task('compile-js', function() {
	return browserify(paths.js)
		.transform(reactify)
		.bundle()
		.pipe(vinyl('main.js'))
		.pipe(buffer())
		.pipe(uglify())
		.pipe(gulp.dest(paths.dist));
});

gulp.task('default', ['clean'], function() {
	gulp.start('copy-assets', 'compile-css', 'compile-js');
});
