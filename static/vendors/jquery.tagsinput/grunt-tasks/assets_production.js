module.exports = function(grunt) {
   grunt.registerTask('asset:production',
   [
      'cssmin:plugin',
      'uglify:plugin'
   ]);
};
