angular.module('finderApp').component('linkDetail', {
    templateUrl: '/static/js/link-detail/link-detail.template.html',
    controller: function linksController($scope, ResultService, $routeParams, $rootScope) {
        $scope.currentPage = 0;
        $scope.itemsPerPage = 21;
        $scope.items = [];
        $rootScope.checked = false;

        ResultService.query({'query__query': $routeParams.linkQuery}, function (response) {
                $scope.items = response;
            });

        $scope.firstPage = function () {
            return $scope.currentPage == 0;
        };
        $scope.lastPage = function () {
            var lastPageNum = Math.ceil($scope.items.length / $scope.itemsPerPage - 1);
            return $scope.currentPage == lastPageNum;
        };
        $scope.numberOfPages = function () {
            return Math.ceil($scope.items.length / $scope.itemsPerPage);
        };
        $scope.startingItem = function () {
            return $scope.currentPage * $scope.itemsPerPage;
        };
        $scope.pageBack = function () {
            $scope.currentPage = $scope.currentPage - 1;
        };
        $scope.pageForward = function () {
            $scope.currentPage = $scope.currentPage + 1;
        };
        $scope.makeZip = function () {
            var checkedValue = ['zip', window.location.href.split('/').slice(-1)[0]];
            var inputElements = document.getElementsByClassName('messageCheckbox');
            for(var i=0; i<inputElements.length; ++i){
                if(inputElements[i].checked){
                    checkedValue.push(inputElements[i].value);
                }
            }
            console.log(window.location.href.split('/').slice(-1)[0]);
            socket.send(checkedValue);
        }

    }
});