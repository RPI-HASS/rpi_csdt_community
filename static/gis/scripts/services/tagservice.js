'use strict';

angular.module('socialjusticeApp')
  .service('tagService', function($resource,config) {
   return $resource(config.route('tagService'), null,{
      query: {method: 'GET', isArray: true, transformResponse: function(TagData) {
        var d = JSON.parse(TagData);
        var tagArray=d.tags;
        return tagArray;
    }}
   });
   });