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

    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),

    less = require('gulp-less'),
    minifyCss = require('gulp-minify-css');

gulp.task('lint', function () {
    return gulp.src('assets/js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('scripts', function () {
    return gulp.src('assets/js/*.js')
        .pipe(concat('all.js'))
        .pipe(gulp.dest('dist'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist'));
});

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
            path.basename += ".min";
        }))
        .pipe(gulp.dest('dist/css'));
});

gulp.task('assets', function () {
    return gulp.src('vendor/Semantic-UI/src/themes/default/assets/**/*.*')
        .pipe(gulp.dest('dist'));
});

gulp.task('watch', function () {
    gulp.watch('assets/js/*.js', ['lint', 'scripts']);
    gulp.watch('assets/less/*.less', ['less']);
});

gulp.task('default', ['lint', 'less', 'scripts', 'assets', 'watch']);
gulp.task('build-dist', ['less-minified']);
