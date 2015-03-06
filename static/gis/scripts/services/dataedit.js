'use strict';

angular.module('socialjusticeApp')
  .factory('dataEdit', function($resource,djResource,config) {
   return djResource(config.route('dataEdit'), null,
       {
           'create': { method:'POST' }
       });
   });
