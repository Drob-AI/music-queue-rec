angular.module('playlist', ['ngRoute', 'ngResource', 'angularjs-dropdown-multiselect']).
    config(function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: '/views/root.html',
            controller: 'RootController'
        }).when('/playlist', {
            templateUrl: '/views/playlist.html',
            controller: 'PlaylistController'
        })
    });