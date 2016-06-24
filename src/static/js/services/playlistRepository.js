angular.module('playlist').
    service('DatasetRepository', ['$q', '$http', function ($q, $http) {

      function generatePlaylist(data) {
          return $http({
              method: 'POST',
              url: 'http://localhost:5000/create-playlist',
              data: data
          }).then(function (result) {
              return result;
          });
      }

      function getArtists() {
          return $http({
              method: 'GET',
              url: 'http://localhost:5000/get-artists'
          }).then(function (result) {
            return result.data;
          });
      }

      function getTags() {
          return $http({
              method: 'GET',
              url: 'http://localhost:5000/get-tags'
          }).then(function (result) {
            return result.data;
          });
      }

      return {
        generate: generatePlaylist,
        getArtists: getArtists,
        getTags: getTags
      }

    }]);