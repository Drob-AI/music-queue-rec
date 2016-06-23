import recsys.algorithm
# Path hack.
# import sys, os
# sys.path.insert(0, os.path.abspath('..'))
from src.data import tracks
from src.data import all_tags

from recsys.algorithm.factorize import SVD

recsys.algorithm.VERBOSE = True

svd = SVD()
svd.load_data(filename='./src/data/traindata.dat',
            sep=',',
            format={'col':0, 'row':1, 'value':2, 'ids': int})

k = 150
svd.compute(k=k, min_values=1, pre_normalize=None, mean_center=True, post_normalize=True)
# print(svd.recommend(1, only_unknowns=False, is_row=False))

def hasTags(rec, tags):
    return len(set(tags).intersection(set(rec['tags']))) > 0

def hasAuthors(rec, authors):
    return len(set(authors).intersection(set(rec['artists']))) > 0

def recommendFor(user, tags=[], authors=[]):
    tags = set(tags)
    authors = set(authors)
    recommendations = svd.recommend(1, only_unknowns=False, is_row=False)
    rec_tracks = map(lambda rec: tracks[rec[0]], recommendations)
    if (len(tags) > 0):
        rec_tracks = filter(lambda track: hasTags(track, tags), rec_tracks)
    if (len(authors) > 0):
        rec_tracks = filter(lambda track: hasAuthors(track, authors), rec_tracks)
    return rec_tracks;

print recommendFor(1)