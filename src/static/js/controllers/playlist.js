angular.module('playlist').
    controller('PlaylistController', ['$scope', 'DatasetRepository', function ($scope, DatasetRepository) {
        
        DatasetRepository.getArtists().then(function (result) {
            $scope.allArtists = result;
        });

        DatasetRepository.getTags().then(function (result) {
            $scope.allTags = result;
         });

        $scope.selectedArtists = [];
        $scope.selectedTags = [];

        $scope.createPlaylist = function() {
        	var selectedArtistsAndTags = {artists: $scope.selectedArtists, tags: $scope.selectedTags};
			DatasetRepository.generate(selectedArtistsAndTags).then(function (result) {
            	$scope.generatedPlaylist = result.data;
         	});

    	}
    }]);