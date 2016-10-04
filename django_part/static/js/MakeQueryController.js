/**
 * Created by user on 30.09.16.
 */
angular.
  module('finderApp')
    .controller('MakeQueryCtrl',
      function MakeQueryCtrl($scope, QueryService, AuthorizationService, $rootScope) {
        $scope.mayBeNewQuery = function () {
          console.log($scope.query);
          if (typeof $scope.query != 'undefined') {
            QueryService.query({'status':1}).$promise
              .then(function (response) {
                var inside = false;
                $scope.links = response;
                for (var i = 0; i < $scope.links.length; i++) {
                  if ($scope.query == $scope.links[i]['query']) {
                      inside = true;
                      break
                  }
                }
                if (inside) {
                  console.log('inside');
                  window.location.href = 'http://127.0.0.1:8000/#!/query/' + $scope.query + '/';
                  $rootScope.checked = false;
                } else {
                  window.location.href = 'http://127.0.0.1:8000/#!/query/';
                  console.log('outside');
                  AuthorizationService.save({}, {'username':'booka', 'password':'tunnel777'});
                  QueryService.save({}, {'query':$scope.query, 'status':0});
                  $rootScope.checked = true;
                  socket.send(['query', $scope.query]);
                }
              });
          }
        };
      }
    );