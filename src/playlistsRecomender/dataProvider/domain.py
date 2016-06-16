class Song:
    occurance_count = 0
    external_id = 0
    tags = []
    
    def __init__(self, song_id, title, artist):
        self.id = song_id
        self.title = title
        self.artist = artist
        
class Tag:
    occurance_count = 0
    songs = []
    
    def __init__(self, tag_id, name):
        self.id = tag_id
        self.name = name
        
class Playlist:
    songs = []
    playlist_tags = {}
    
    def tags(self):
        if len(self.playlist_tags) > 0:
            return self.playlist_tags
            
        self.playlist_tags = {}
        
        songs_tags = map(songs, lambda song: song.tags)
        tags = reduce(songs_tags, lambda tag_list, song_tags: tag_list + songs_tags, []);
        for tag in tags: 
            if tag in playlist_tags:
                playlist_tags[tag] += 1
            else: 
                playlist_tags[tag] = 1
        return playlist_tags
        
class Dataset:
    def __init__(self, tags, songs, train_playlists, test_playlists):
        self.tags = tags
        self.songs = songs
        self.train = train_playlists
        self.test = test_playlists