'use strict';

angular.module('socialjusticeApp')
	.service('dataSource', function dataSource($resource, config) {
			return $resource(config.route('dataSource'), null, {
				query: {
					method: 'GET',
					isArray: true, 
					transformResponse:function(data){
										data = JSON.parse(data);
										return data.results;
			}
		}
	});
  });
