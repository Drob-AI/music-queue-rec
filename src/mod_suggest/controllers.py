# Import the database object from the main app module
from src import FLASK
from src.playlistsRecomender import *
import json
from flask import request
from src.songRecommender import *
from src.data import tracks
from src.data import tags
from src.data import authors

print('nice')
# data_set = dataProvider.import_folder( dir + '/dataProvider/data/dataset/yes_small/')
# ids = list(set([song.id for playlist in data_set.train for song in playlist.songs]))

@FLASK.route("/create-playlist")
def create_playlist():
    playlist_size = request.args.get('plalist-size', '')
    user_id = int(request.args.get('user-id', ''))
    categories = [int(id) for id in request.args.get('categories','').split(',')]

    svd_reccomended = recommendFor(user_id)
    print(svd_reccomended)
    # svd_reccomended = songs
    ids = [s['id'] for s in svd_reccomended]

    recomender = PlaylistGenerator(data_set=ids, playlist_size=int(playlist_size), hof_size = 35)
    hofs = recomender.start()

    recommended = list([list(hof) for hof in hofs])
    translated = [[tracks[song] for song in playlist] for playlist in recommended ]
    # maximize the sum of the ids of all playlists:
    print(translated[0], translated[1])
    return json.dumps(translated)



@FLASK.route("/")
def root():
    return FLASK.send_static_file('index.html')

@FLASK.route('/<path:path>')
def static_proxy(path):
	# send_static_file will guess the correct MIME type
	return FLASK.send_static_file(path)

@FLASK.route('/get-artists')
def get_artists():
	return json.dumps(authors)

@FLASK.route('/get-tags')
def get_tags():
	return json.dumps(tags)