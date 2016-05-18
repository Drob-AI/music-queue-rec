from domain import *

PLAYLISTS_TEST_FILE = 'test.txt'
PLAYLISTS_TRAIN_FILE = 'train.txt'
TAGS_FILE = 'tag_hash.txt'
SONGS_FILE = 'song_hash.txt'
SONG_TAGS_FILE = 'tags.txt'

def index_by_id(lst):
    index = {}
    for entry in lst:
        index[entry.id] = entry
        
    return index;

def read_songs(path):
    song_file = file(path, 'r')
    songs = []
    
    lines = song_file.readlines()
    
    for line in lines:
        tokens = line.strip().split('\t')
        song = Song(int(tokens[0]), tokens[1], tokens[2])
        songs += [song]
    
    song_file.close()
        
    return songs

def read_tags(path):
    tag_file = file(path, 'r')
    tags = []
    
    lines = tag_file.readlines()
    
    for line in lines:
        tokens = line.strip().split(', ')
        tag = Tag(int(tokens[0]), tokens[1])
        tags += [tag]
        
    tag_file.close()
    
    return tags
    
def tag_songs(path, songs, tag_index):
    song_tags_file = file(path, 'r')
    
    lines = song_tags_file.readlines()
    
    for i in xrange(0, len(lines)):
        line = lines[i].strip()
        song = songs[i]
        if line == '#':
            continue
        tags = map(lambda raw_tag: tag_index[int(raw_tag)], line.split(' '))
        
        for tag in tags:
            tag.songs += [song]
            
        song.tags = tags        
    
    song_tags_file.close();
    
    return songs

def string_as_numberlist(raw_str):
    return map(lambda raw_num: int(raw_num), raw_str.strip().split(' '))
    
def update_alt_ids(alt_id_string, songs):
    alt_ids = string_as_numberlist(alt_id_string)
    for i in xrange(0, len(songs)):
        songs[i].external_id = alt_ids[i]
    
def update_occurances(occurance_string, songs):
    occurances = string_as_numberlist(occurance_string)
    for i in xrange(0, len(songs)):
        songs[i].occurance_count = occurances[i]
    
def read_playlists(path, songs, song_index, update):
    playlists_file = file(path, 'r')
    lines = playlists_file.readlines()
    
    if update:
        update_alt_ids(lines[0], songs)
        update_occurances(lines[1], songs)
    
    playlists = []
    
    for i in xrange(2, len(songs)):
        song_ids = string_as_numberlist(lines[i])
        playlist = Playlist()
        for song_id in song_ids:
            playlist.songs += [song_index[song_id]]
        playlists += [playlist]
    
    return playlists
        

def import_folder(dataset_path):
    songs = read_songs(dataset_path + SONGS_FILE)
    tags = read_tags(dataset_path + TAGS_FILE)
    song_index = index_by_id(songs)
    tag_index = index_by_id(tags)
    
    tag_songs(dataset_path + SONG_TAGS_FILE, songs, tag_index)
    
    test_playlists = read_playlists(dataset_path + PLAYLISTS_TEST_FILE, songs, song_index, False)
    train_playlists = read_playlists(dataset_path + PLAYLISTS_TRAIN_FILE, songs, song_index, True)
    
    return Dataset(tag_index, song_index, train_playlists, test_playlists)