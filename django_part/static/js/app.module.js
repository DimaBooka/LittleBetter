var finderApp = angular.module('finderApp', [
  'ngRoute',
  'services',
]);

angular.
  module('finderApp')
    .controller('MakeQueryCtrl',
      function MakeQueryCtrl($scope, QueryService, CreateService, ClientService) {
        $scope.getlog = function () {
          if (typeof $scope.query != 'undefined') {
            QueryService.query({'status':'done'}).$promise
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
                  window.location.href = 'http://127.0.0.1:8000/#!/query/' + $scope.query + '/';
                  $scope.checked = false;
                } else {
                  window.location.href = 'http://127.0.0.1:8000/#!/query/';
                  CreateService.save({}, {'query':$scope.query, 'status':'create'});
                  $scope.checked = true;
                  ClientService($scope);
                }
              });
          }
        };
      }
    )
    .filter('startFrom', function() {
      return function(input, start) {
        start = +start;
        return input.slice(start);
      }
    });