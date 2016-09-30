/**
 * Created by user on 30.09.16.
 */
angular.
  module('finderApp')
  .filter('startFrom', function() {
    return function(input, start) {
      start = +start;
      return input.slice(start);
    }
  });