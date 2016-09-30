angular.module('finderApp').component('linkDetail', {
    templateUrl: '/static/js/link-detail/link-detail.template.html',
    controller: function linksController($scope, ResultService, $routeParams) {
        $scope.currentPage = 0;
        $scope.itemsPerPage = 21;
        $scope.items = [];

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
    }
});