'use strict';

var config = {
    // Base directory of everything
    'base': '/static/js/create/',
    // REST endpoints
    'application_api': '/api/application/:id',
    'theme_api': '/api/theme/:id',
    'category_api': '/api/category/:id'
};

// Declare app level module which depends on views, and components
angular.module('community.create', ['ngRoute', 'ngResource',])
.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {
        controller: 'MainController',
        templateUrl: config['base'] + 'create.html',
        reloadOnSearch: false
    })
    .otherwise({redirectTo: '/'});
}])
.factory('themeResource', ['$resource', function($resource) {
    return $resource(config['theme_api']);
}])
.factory('categoryResource', ['$resource', function($resource) {
    return $resource(config['category_api']);
}])
.factory('applicationResource', ['$resource', function($resource) {
    return $resource(config['application_api']);
}])
.controller('MainController', ['$scope', '$routeParams', '$location', 'applicationResource',
    'themeResource', 'categoryResource', '$q',
    function($scope, $routeParams, $location, applicationResource, themeResource, categoryResource, $q) {
    var applications = {};
    $scope.activeTheme = $routeParams['theme'];
    // Fetch all the categories for this theme
    $scope.getApplication = function(id) {
        return applications[id];
    }
    $scope.appComparator = function(app1, app2){
        return this.getApplication(app1).rank - this.getApplication(app2).rank;
    }
    $scope.applications = applicationResource.query(function() {
        for(var index in $scope.applications) {
            var application = $scope.applications[index];
            applications[application.id] = application;
        }
    });
    $scope.categories = categoryResource.query();
    $q.all([
        $scope.applications.$promise,
        $scope.categories.$promise
    ]).then(
        function() {
            var myself = $scope;
            $scope.categories.forEach(function(category){
                category.applications.sort(function(app1, app2){myself.appComparator(app1, app2);});
            });
    });
    $scope.themes = themeResource.query(function() {
        var theme = $location.search()['theme'];
        if(theme == undefined)
            $scope.setTheme($scope.themes[0].id);
        else
            $scope.setTheme(theme);
    });

    $scope.setTheme = function(id) {
        var selectedTheme = null;
        for(var i=0; i < $scope.themes.length; i += 1) {
            if($scope.themes[i].id == id) {
                selectedTheme = $scope.themes[i];
                $location.search('theme', id);
                break;
            }
        }
        $scope.activeTheme = selectedTheme;
    }
}]);
