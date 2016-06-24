# Import the database object from the main app module
from src import FLASK
from src.playlistsRecomender import *
import json
from flask import request
# from src.songRecommender import *

print('nice')
# data_set = dataProvider.import_folder( dir + '/dataProvider/data/dataset/yes_small/')
# ids = list(set([song.id for playlist in data_set.train for song in playlist.songs]))

@FLASK.route("/")
def create_playlist():
    ids = [{'artists': [345988], 'id': 2758462, 'tags': [], 'name': u'Technomind/_/Smoothed+Brown+Noise'}, {'artists': [129], 'id': 35036, 'tags': [], 'name': u'%5Bunknown%5D/_/Joven+y+bonita+%5BBR-Screener%5D+Castellano+(www.estrenakos.com)'}, {'artists': [189343], 'id': 3844123, 'tags': [122106, 127210, 14348, 14371, 127207], 'name': u'kukui/_/%E5%85%89%E3%81%AE%E8%9E%BA%E6%97%8B%E5%BE%8B'}, {'artists': [133003], 'id': 1032288, 'tags': [134092, 238672, 189631, 220708, 134090], 'name': u'%ED%8B%B0%EC%95%84%EB%9D%BC/_/%EB%8A%90%EB%82%8C+%EC%95%84%EB%8B%88%EA%B9%8C'}, {'artists': [133003], 'id': 1032277, 'tags': [238672, 54087, 1831, 134092, 106467], 'name': u'%ED%8B%B0%EC%95%84%EB%9D%BC/_/%EB%82%98+%EC%96%B4%EB%96%A1%ED%95%B4'}, {'artists': [133003], 'id': 1032297, 'tags': [94263, 134092, 133846, 133886, 94231], 'name': u'%ED%8B%B0%EC%95%84%EB%9D%BC/_/%EC%95%84%ED%8C%8C'}, {'artists': [261461], 'id': 2085350, 'tags': [], 'name': u'Orange+Caramel/_/%EA%B9%8C%ED%83%88%EB%A0%88%EB%82%98+Catallena'}, {'artists': [189343], 'id': 1509645, 'tags': [81211, 14348, 14405, 43966, 103848], 'name': u'kukui/_/%E7%A9%BA%E8%9D%89%E3%83%8E%E5%BD%B1'}, {'artists': [133003], 'id': 1032285, 'tags': [238672, 26712, 1831, 133886, 134090], 'name': u'%ED%8B%B0%EC%95%84%EB%9D%BC/_/%EB%84%98%EB%B2%84%EB%82%98%EC%9D%B8+(No.9)+(Club+Ver.)'}, {'artists': [133003], 'id': 1032353, 'tags': [134092, 54087, 81223, 133846, 134090], 'name': u'%ED%8B%B0%EC%95%84%EB%9D%BC/_/Sugar+Free'}]
    print(ids)
    playlist_size = request.args.get('plalist-size', '')
    categories = [int(id) for id in request.args.get('categories','').split(',')]
    recomender = PlaylistGenerator(data_set=ids, playlist_size=int(playlist_size), hof_size = 35)
    hofs = recomender.start()

    # maximize the sum of the ids of all playlists:
    return json.dumps(list([list(hof) for hof in hofs]))