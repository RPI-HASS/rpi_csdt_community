'use strict';

angular.module('socialjusticeApp')
.controller('addTagCtrl',function($scope,$resource,$modal) {
	// Pre-fetch an external template populated with a custom scope
	$scope.csvfile='Gulf_Coast_Area_Geographies.xls';
	var myOtherModal  = $modal({scope: $scope, template: 'views/modal/tags.html', show: false});
	// Show when some event occurs (use $promise property to ensure the template has been loaded)
	$scope.showModal = function() {
		myOtherModal.$promise.then(myOtherModal.show);
	};
	$scope.hideModal = function() {
		myOtherModal.$promise.then(myOtherModal.hide);
	};
	$scope.downloadAllDataSet=function(){
		console.log('ddddd');
		// We can pass the tagObject in the function to get the particular dataSet
		var load=$resource('http://www2.census.gov/acs/2005_Gulf_Coast_Area_Data_Profiles/Gulf_Coast_Area_Geographies.xls');
		load.get({})
        .$promise.then(function(tagobj,headers){
            console.log(tagobj);
            console.log(headers);
            $scope.d=tagobj;
        });
        console.log($scope.d);
        $scope.damn='Gulf_Coast_Area_Geographies.xls';
		
   	}; 
	
});

