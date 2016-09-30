/**
 * Created by user on 30.09.16.
 */
angular.
  module('finderApp')
    .controller('MakeQueryCtrl',
      function MakeQueryCtrl($scope, QueryService, AuthorizationService) {
        $scope.mayBeNewQuery = function () {
          console.log($scope.query);
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
                  console.log('inside');
                  window.location.href = 'http://127.0.0.1:8000/#!/query/' + $scope.query + '/';
                  $scope.checked = false;
                } else {
                  window.location.href = 'http://127.0.0.1:8000/#!/query/';
                  console.log('outside');
                  AuthorizationService.save({}, {'username':'booka', 'password':'tunnel777'});
                  QueryService.save({}, {'query':$scope.query, 'status':'create'});
                  $scope.checked = true;
                  var socket = null;
                  var isopen = false;
                  var counter = 0;

                  socket = new WebSocket("ws://127.0.0.1:9000");
                  socket.binaryType = "arraybuffer";
                  socket.onopen = function () {
                    console.log("Connected!");
                    isopen = true;
                    socket.send($scope.query);
                  };
                  socket.onmessage = function (e) {
                    if (typeof e.data == "string") {
                      console.log("Text message received: " + e.data);
                      counter = counter + 1;
                      if (counter >= 1) {
                        for (var i = 1; i <= counter; i++) {
                          currentIndicator = "lamp" + i;
                          $scope.currentIndicator = true;
                        }
                      }
                      if (counter > 2) {
                        setTimeout(function () {
                          window.location.href = 'http://127.0.0.1:8000/#/query/' + $scope.query + '/';
                          $scope.checked = false;
                        }, 300);
                      }
                    }
                  };
                  socket.onclose = function (e) {
                    console.log("Connection closed.");
                    socket = null;
                    isopen = false;
                  }
                }
              });
          }
        };
      }
    );