
 angular.module('services.LinkService', ['ngResource'])
     .config(function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
     })
     .factory('QueryService', ['$resource',
        function($resource) {
          return $resource('/api/query/:id', {'id': '@id'}, {});
        }
     ])

     .factory('ResultService', ['$resource',
        function($resource) {
          return $resource('/api/result/:id', {'id': '@id'}, {});
        }
     ]);