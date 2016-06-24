# Import the database object from the main app module
from src import FLASK
from src.playlistsRecomender import *
from flask import jsonify, request, json
import json

print('nice')
data_set = dataProvider.import_folder( dir + '/dataProvider/data/dataset/yes_small/')
ids = list(set([song.id for playlist in data_set.train for song in playlist.songs]))

@FLASK.route("/")
def root():
    return FLASK.send_static_file('index.html')

@FLASK.route('/<path:path>')
def static_proxy(path):
	# send_static_file will guess the correct MIME type
	return FLASK.send_static_file(path)

@FLASK.route('/get-artists')
def get_artists():
	songs = dataProvider.read_songs( dir + '/dataProvider/data/dataset/yes_small/song_hash.txt')
	artists = []
	insertedArtists = []
	for s in songs:
		if s.artist not in insertedArtists:
			artist = {
				"id": s.id,
				"label": s.artist
			}
			artists.append(artist)
			insertedArtists.append(s.artist)
	return jsonify(artists)

@FLASK.route('/get-tags')
def get_tags():
	tagHashes = dataProvider.read_tags( dir + '/dataProvider/data/dataset/yes_small/tag_hash.txt')
	tags = []
	for t in tagHashes:
		tag = {
			"id": t.id,
			"label": t.name
		}
		tags.append(tag)
	return jsonify(tags)

@FLASK.route('/create-playlist', methods = ['POST'])
def createPlaylist():
	song_file = file(dir + '/dataProvider/data/dataset/yes_small/song_hash.txt', 'r')
	selectedArtists = request.get_json().get('artists')
	selectedTags = request.get_json().get('tags')	
	lines = song_file.readlines()
	tracks = {}
    
	for line in lines:
		tokens = line.strip().split('\t')
		tracks[int(tokens[0])] = {
			"id": int(tokens[0]),
			"name": tokens[1],
			"artists": tokens[2]
		}
	song_file.close()

    # selectedArtists = request.get_json().get('artists')

	selectedIds = [d['id'] for d in selectedArtists] + [d['id'] for d in selectedTags]
	recomender = PlaylistGenerator(data_set=ids, playlist_size=10, hof_size = 20)
	hofs = recomender.start()
    # maximize the sum of the ids of all playlists:
	return json.dumps(list([list([tracks[l].get('name') for l in hof]) for hof in hofs]))