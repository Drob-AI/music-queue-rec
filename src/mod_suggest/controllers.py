# Import the database object from the main app module
from src import FLASK
from src.playlistsRecomender import *
import json

print('nice')
data_set = dataProvider.import_folder( dir + '/dataProvider/data/dataset/yes_small/')
ids = list(set([song.id for playlist in data_set.train for song in playlist.songs]))

@FLASK.route("/")
def create_playlist():
    recomender = PlaylistGenerator(data_set=ids, playlist_size=10, hof_size = 20)

    hofs = recomender.start()

    # maximize the sum of the ids of all playlists:
    return json.dumps(list([list(hof) for hof in hofs]))