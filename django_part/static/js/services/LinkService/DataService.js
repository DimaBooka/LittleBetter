
 angular.module('services.LinkService', ['ngResource'])
     .config(function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
     })
     .factory('QueryService', ['$resource',
        function($resource) {
          return $resource('/api/query/:id', {'id': '@id'}, {
            query: {
              method: 'GET',
              params: {},
              isArray: true
            }, stripTrailingSlashes: false
          });
        }
     ])

     .factory('ResultService', ['$resource',
        function($resource) {
          return $resource('/api/result/:id', {'id': '@id'}, {
            query: {
              method: 'GET',
              params: {},
              isArray: true
            }
          });
        }
     ])

     .factory('CreateService', ['$resource',
        function($resource) {
          return $resource('/api/query/', {}, {
            save: {
              method: 'POST',
            },
          });
        }
     ])

     .factory('ClientService', [
        function(query) {
          return function (scope) {

            var socket = null;
            var isopen = false;
            var counter = 0;

            socket = new WebSocket("ws://127.0.0.1:9000");
            socket.binaryType = "arraybuffer";

            socket.onopen = function () {
              console.log("Connected!");
              isopen = true;
              socket.send(scope.query);
            };

            socket.onmessage = function (e) {
              if (typeof e.data == "string") {
                console.log("Text message received: " + e.data);
                counter = counter + 1;
                if (counter >= 1) {
                  for (var i = 1; i <= counter; i++) {
                    var ProgressBar = document.getElementById("lamp" + i);
                    ProgressBar.innerHTML = '<span class="done" ></span>';
                  }
                }
                if (counter > 2) {
                  setTimeout(function () {
                    window.location.href = 'http://127.0.0.1:8000/#!/query/' + scope.query + '/';
                    scope.checked = false;
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
        }
     ]);

