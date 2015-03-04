'use strict';

/**
* @ngdoc function
* @name socialjusticeApp.controller:AboutCtrl
* @description
* # AboutCtrl
* Controller of the socialjusticeApp
*/
angular.module('socialjusticeApp')
  .controller('ChartsCtrl', function ($scope) {
   

        $scope.config = {
            title: 'DataSets',
            tooltips: true,
            labels: false,
            mouseover: function() {},
            mouseout: function() {},
            click: function() {},
            legend: {
                display: true,
                //could be 'left, right'
                position: 'right'
            }
        };

        $scope.data = {
            series: ['Farmer Market', 'Retail Stores', 'Obesity'],
            data: [{
                x: 'Troy',
                y: [10, 50, 30],
                tooltip: 'this is tooltip'
            }, {
                x: 'Cohoes',
                y: [25, 10, 15]
            }, {
                x: 'Albany',
                y: [21,43,3]
            }, {
                x: 'Latham',
                y: [39, 0, 16]
            }]
        };
  });