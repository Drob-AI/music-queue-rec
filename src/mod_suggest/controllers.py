# Import the database object from the main app module
from src import FLASK
from src.playlistsRecomender import *
import json

print('nice')
data_set = dataProvider.import_folder( dir + '/dataProvider/data/dataset/yes_small/')

@FLASK.route("/")
def delete_dataset_info():
    recomender = PlaylistGenerator(data_set=data_set)
    hof = recomender.start()
    print(list(hof));

    # maximize the sum of the ids of all playlists:
    return json.dumps(list(hof))