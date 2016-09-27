angular.
  module('finderApp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/query', {
          template: '<links-list></links-list>'
        }).
        when('/query/:linkQuery', {
          template: '<link-detail></link-detail>'
        }).
        otherwise('/query');
    }
  ]);