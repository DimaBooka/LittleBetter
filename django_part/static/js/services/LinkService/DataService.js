
 angular.module('services.LinkService', ['ngResource'])

     .factory('QueryService', ['$resource',
        function($resource) {
          return $resource('/api/query/:id', {'id': '@id'}, {
            query: {
              method: 'GET',
              params: {done: 'done'},
              isArray: false
            }
          });
        }
      ])

      .factory('ResultService', ['$resource',
        function($resource) {
          return $resource('/api/result/:id', {'id': '@id'}, {
            query: {
              method: 'GET',
              params: {done: 'done'},
              isArray: false
            }
          });
        }
      ]);

