angular.
  module('finderApp')
    .config(['$locationProvider' ,'$routeProvider', '$httpProvider',
    function config($locationProvider, $routeProvider, $httpProvider) {
      $locationProvider.hashPrefix('');
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
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