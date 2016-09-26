/**
 * Created by user on 23.09.16.
 */
linksApp.controller('allLinks',
    function QuestionController($scope, $http){

        $http.get('/api/query/').success(function(data) {
            $scope.links = data;
            console.log(data);
        });

    }
);