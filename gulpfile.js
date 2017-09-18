var gulp = require('gulp'),
    configLocal = require('./gulp-config.json'),
    merge = require('merge'),
    bower = require('gulp-bower'),
    rename = require('gulp-rename'),
    scsslint = require('gulp-scss-lint'),
    sass = require('gulp-sass'),
    cleanCSS = require('gulp-clean-css'),
    eslint = require('gulp-eslint'),
    isFixed = require('gulp-eslint-if-fixed'),
    babel = require('gulp-babel'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify'),
    browserSync = require('browser-sync').create();

var configDefault = {
  src: {
    scss: './src/scss',
    js: './src/js'
  },
  dist: {
    css: './static/css',
    js: './static/js',
    fonts: './static/fonts'
  },
  components: {
    base: './src/components',
    athena: './src/components/athena-framework',
    fontAwesome: './src/components/font-awesome'
  },
  sync: false,
  syncTarget: 'http://localhost/'
},
config = merge(configDefault, configLocal);

gulp.task('bower', function() {
  bower({ cmd: 'update' })
    .pipe(gulp.dest(config.components.base))
    .on('end', function() {
        gulp.src(config.components.fontAwesome + '/fonts/*')
          .pipe(gulp.dest(config.dist.fonts + '/font-awesome'));

        gulp.src(config.components.athena + '/dist/fonts/*/**')
          .pipe(gulp.dest(config.dist.fonts));

        gulp.src(config.components.athena + '/dist/js/framework.min.js')
          .pipe(gulp.dest(config.dist.js));
    });
});

gulp.task('eslint', function() {
  return gulp.src(config.src.js + '/**/*.js')
    .pipe(eslint({fix: true}))
    .pipe(eslint.format())
    .pipe(isFixed(config.src.js));
});

gulp.task('babel', ['eslint'], function() {
  var components = [
    config.src.js + '/frontend-script.js'
  ];

  return gulp.src(components)
    .pipe(babel())
    .pipe(uglify())
    .pipe(rename('script.min.js'))
    .pipe(gulp.dest(config.dist.js));
});

gulp.task('babel-admin', ['eslint'], function() {
  var components = [
    config.src.js + '/backend-script.js'
  ];

  return gulp.src(components)
    .pipe(babel())
    .pipe(uglify())
    .pipe(rename('manager.min.js'))
    .pipe(gulp.dest(config.dist.js));
});

gulp.task('js', ['eslint', 'babel', 'babel-admin']);

gulp.task('scss-lint', function() {
  return gulp.src(config.src.scss + '/*.scss')
    .pipe(scsslint({
      'maxBuffer': 400 * 1024
    }));
});

gulp.task('scss', function() {
  return gulp.src(config.src.scss + '/style.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSS({compatibility: 'ie >= 8'}))
    .pipe(rename('style.min.css'))
    .pipe(gulp.dest(config.dist.css))
    .pipe(browserSync.stream());
});

gulp.task('css', ['scss-lint', 'scss']);

gulp.task('watch', function() {
  gulp.watch(config.src.scss+ '/*.scss', ['css']);
  gulp.watch(config.src.js + '/**/*.js', ['js']);
});

gulp.task('default', ['bower', 'css', 'js']);
