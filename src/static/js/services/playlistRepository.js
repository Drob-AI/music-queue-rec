angular.module('playlist').
    service('DatasetRepository', ['$q', '$http', function ($q, $http) {

      function generatePlaylist(data) {
          return $http({
              method: 'GET',
              url: 'http://localhost:5000/create-playlist?plalist-size=10&categories=1&user-id=900',
          }).then(function (result) {
              return result;
          });
      }

      function getArtists() {
          return $http({
              method: 'GET',
              url: 'http://localhost:5000/get-artists'
          }).then(function (result) {
              var a = _.keys(result);
              return _.map(result.data, function (entry) {
                  return {
                      label: entry.name,
                      id: entry.id
                  };
              })
          });
      }

      function getTags() {
          return $http({
              method: 'GET',
              url: 'http://localhost:5000/get-tags'
          }).then(function (result) {
              return _.map(result.data, function (entry) {
                  return {
                      label: entry.name,
                      id: entry.id
                  };
              })
          });
      }

      return {
        generate: generatePlaylist,
        getArtists: getArtists,
        getTags: getTags
      }

    }]);