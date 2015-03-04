'use strict';

angular.module('socialjusticeApp')
    .service('polygonService', function($resource,config) {
     return $resource(config.route('polygonService'), null,{
        query: {method: 'GET', isArray: false, transformResponse: function(pData) {
          var Data = JSON.parse(pData);
          return Data;
      }}
   });
   });
