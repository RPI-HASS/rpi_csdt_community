'use strict';

angular.module('socialjusticeApp')
  .service('config', function config() {
      var makeConfig = function() {
        var config = {
          map: {
            maxZoomLevelLoading: 12,
            startLocation: [42.000, -91.000]
          },
          routes: {
              dataSource: '/fake_data/dataSource/:id.json',
              dataFeed: '/fake_data/dataFeed.json?dataSource=:dataSourceId'
          },
          route: function(name, values) {
              var route = this.routes[name];
              if(values !== undefined) {
                for(var key in values) {
                  route = route.replace(':'+key, values[key]);
                }
              }
              if(this.serverRoot !== undefined) {
                return this.serverRoot + route;
              }
              return route;
          },
          makeConfig: makeConfig
        };
          // If there is a global configuration available, merge it an overwrite defaults
      if(window.config !== undefined) {
        var merge = function(cur, old) {
          var res = old;
          for(var v in cur) {
            if(typeof cur[v] === 'object') {
              res[v] = merge(cur[v], old[v]);
            } 
            else {
              res[v] = cur[v];
            }
          }
          return res;
        };
        config = merge(window.config, config);
      }
      return config;
  };
      return makeConfig();
  });
