/*
 * This file is part of e-Giełda.
 * Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
 *
 * e-Giełda is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.
 */

var gulp = require('gulp');

var concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    sourcemaps = require('gulp-sourcemaps'),

    fs = require('fs'),
    path = require('path'),
    es = require('event-stream'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),

    less = require('gulp-less'),
    minifyCss = require('gulp-minify-css');

/*
 * JavaScript
 */
gulp.task('lint', function () {
    return gulp.src('assets/js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

function getFolders(dir){
    return fs.readdirSync(dir)
        .filter(function(file){
            return fs.statSync(path.join(dir, file)).isDirectory();
        });
}

function getJsTask(func) {
    var folders = getFolders('assets/js');
    var tasks = folders.map(func);
    return es.concat.apply(null, tasks);
}

gulp.task('js', function() {
    return getJsTask(function(folder) {
        return gulp.src(path.join('assets/js', folder, '/*.js'))
            .pipe(sourcemaps.init())
            .pipe(concat(folder + '.js'))
            .pipe(sourcemaps.write())
            .pipe(gulp.dest('dist/js'));
    });
});

gulp.task('js-minified', function() {
    return getJsTask(function(folder) {
        return gulp.src(path.join('assets/js', folder, '/*.js'))
            .pipe(concat(folder + '.min.js'))
            .pipe(uglify())
            .pipe(gulp.dest('dist/js'));
    });
});

/*
 * LESS
 */
gulp.task('less', function () {
    return gulp.src('assets/less/*.less')
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('dist/css'));
});

gulp.task('less-minified', function () {
    return gulp.src('assets/less/*.less')
        .pipe(less())
        .pipe(minifyCss({keepSpecialComments: 0}))
        .pipe(rename(function (path) {
            path.basename += '.min';
        }))
        .pipe(gulp.dest('dist/css'));
});

/*
 * Misc
 */
gulp.task('assets', function () {
    return es.concat(
        // Semantic UI assets
        gulp.src('vendor/Semantic-UI/src/themes/default/assets/**/*.*')
            .pipe(gulp.dest('dist')),

        // jQuery datetimepicker
        gulp.src('node_modules/jquery-datetimepicker/jquery.datetimepicker.js')
            .pipe(uglify())
            .pipe(gulp.dest('dist/js')),
        gulp.src('node_modules/jquery-datetimepicker/jquery.datetimepicker.css')
            .pipe(minifyCss({keepSpecialComments: 0}))
            .pipe(gulp.dest('dist/css'))
    );
});

gulp.task('watch', function () {
    var semanticPath = 'vendor/Semantic-UI/src/**/';

    gulp.watch('assets/js/*/*.js', ['lint', 'js']);
    gulp.watch(['assets/less/**/*.less',
        semanticPath + '*.less', semanticPath + '*.variables', semanticPath + '*.overrides'],
        ['less']);
});

gulp.task('build-dev', ['lint', 'js', 'less', 'assets']);
gulp.task('build-dist', ['lint', 'js-minified','less-minified', 'assets']);
gulp.task('build', ['build-dev', 'build-dist']);
gulp.task('default', ['build-dev', 'watch']);
