angular.
  module('finderApp').
  component('linksList', {
    templateUrl: '/static/js/links-list/links-list.template.html',
    controller: ['QueryService',
      function linksController(QueryService) {
        this.links = QueryService.query({'status':'done'});

      }
    ]
  });