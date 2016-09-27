angular.
  module('finderApp').
  component('linkDetail', {
    templateUrl: '/static/js/link-detail/link-detail.template.html',
    controller: ['ResultService', '$routeParams',
      function linksController(ResultService, $routeParams) {
        this.links = ResultService.query({'query__query': $routeParams.linkQuery});
      }
    ]

  });




