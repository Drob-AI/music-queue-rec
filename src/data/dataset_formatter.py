import json

USER_LISTENS = '../../dataset/idomaar/relations/events.idomaar'
USER_LIKES = '../../dataset/idomaar/relations/love.idomaar'
PLAYLISTS = '../../dataset/idomaar/entities/playlist.idomaar'

MAX_USERS = 5000

LISTENS_PLAYTIME_FIELD = 3
LISTENS_RELATIONS_FIELD = 4

LIKE_USER_FIELD = 2
LIKE_OBJECT_FIELD = 3

TEST_PERCENTAGE = 0.2

all_users = {};
all_songs = {};

likes = {}

def get_like(raw_like):
    data_entries = [x for x in raw_like.split(' ') if x]
    # print data_entries
    like_entry = data_entries[LIKE_USER_FIELD] + data_entries[LIKE_OBJECT_FIELD]
    like_json = json.loads(like_entry); 
    user = like_json["subjects"][0]["id"]
    song = like_json["objects"][0]["id"]
    
    return {"user": user, "song": song}

def get_user_likes():
    users_count = 0
    users = {}
    with open(USER_LIKES, 'r') as likes_file:
        for line in likes_file:
            entry = get_like(line)
            
            if (not users.has_key(entry["user"])) and users_count >= MAX_USERS:
                continue

            all_users[entry["user"]] = True;
                
            if not users.has_key(entry["user"]):
                users[users_count] = True
                users_count += 1
            
            if not likes.has_key(entry["user"]):
                likes[entry["user"]] = {}

            if not likes[entry["user"]].has_key(entry["song"]):
                likes[entry["user"]][entry["song"]] = True
    return users;


def get_user_and_song(raw_listen):
    data_entries = [x for x in raw_listen.split('\t') if x]
    # print data_entries
    playtime = json.loads(data_entries[LISTENS_PLAYTIME_FIELD])["playtime"]
    relations = json.loads(data_entries[LISTENS_RELATIONS_FIELD])
    
    user = relations["subjects"][0]["id"]
    song = relations["objects"][0]["id"]
    isPlay = playtime > 0;
    value = 1
    
    if isPlay:
        value = 1
    elif likes.has_key(user) and likes[user].has_key(song) and likes[user][song]:
        value = 0
    else:
        value = -1
    
    return {"user": user, "song": song, "value": value}
    
def get_user_listens(users):
    dataset = {}
    with open(USER_LISTENS, 'r') as listens:
        for line in listens:
            entry = get_user_and_song(line)
            if not users.has_key(entry["user"]):
                continue

                
            if not dataset.has_key(entry["user"]):
                dataset[entry["user"]] = {}

            if not dataset[entry["user"]].has_key(entry["song"]):
                dataset[entry["user"]][entry["song"]] = 0
                
            all_songs[entry["song"]] = True;

            dataset[entry["user"]][entry["song"]] += entry["value"];
    
    return dataset;
    

def get_playlist(raw_playlist):
    data_entries = [x for x in raw_playlist.split('\t') if x]
    raw_track_data = json.loads(data_entries[4])['objects']
    raw_track_data = filter(lambda x: x != [], raw_track_data)
    return map((lambda x: x['id']), raw_track_data)
    

def get_playlist_data():
    playlists = []
    with open(PLAYLISTS, 'r') as playlist_file:
        for line in playlist_file:
            entry = get_playlist(line)
            if (len(entry) > 0):
                playlists.append(entry);
    
    return playlists;

def read_playlist_data():
    playlists = get_playlist_data();
    playlistData = open('playlist.dat', 'w')
    for playlist in playlists:
         playlistData.write(str(reduce(lambda x, y: str(x) + ' ' + str(y) , playlist)) + '\n')
    playlistData.close();


def read_train_data():
    users = get_user_likes()
    listens = get_user_listens(users)

    trainingData = open('traindata.dat', 'w')

    i = 0
    trainSize = MAX_USERS * TEST_PERCENTAGE;

    for user in listens.keys():
        for song in listens[user].keys():
            trainingData.write(str(user) + ',' + str(song) + ',' + str(listens[user][song]) + '\n')

    trainingData.close()

read_playlist_data()