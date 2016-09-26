/**
 * Created by user on 26.09.16.
 */
linksApp.controller('allLinks',
    function QuestionController($scope, $http){

        $http.get('/api//').success(function(data) {
            $scope.links = data;
            console.log(data);
        });

    }
);