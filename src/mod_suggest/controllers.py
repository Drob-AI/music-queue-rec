# Import the database object from the main app module
from src import FLASK
from src.playlistsRecomender import *
import json

print('nice')
data_set = dataProvider.import_folder( dir + '/dataProvider/data/dataset/yes_small/')

@FLASK.route("/")
def create_playlist():
    recomender = PlaylistGenerator(data_set=data_set, number_gen = 300,
                                    playlist_size=10, gen_size = 100, mutate_pb = 0.7,
                                    hof_size = 10)

    hofs = recomender.start()

    # maximize the sum of the ids of all playlists:
    return json.dumps(list([list(hof) for hof in hofs]))