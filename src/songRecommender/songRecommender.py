import recsys.algorithm
# Path hack.
# import sys, os
# sys.path.insert(0, os.path.abspath('..'))
# from src.data import tracks
# from src.data import all_tags
import sys, os
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE
sys.path.insert(0, os.path.abspath('..'))

from recsys.algorithm.factorize import SVD
from recsys.algorithm.factorize import SVDNeighbourhood

recsys.algorithm.VERBOSE = True

svd = SVD()
svd.load_data(filename='./src/data/traindata.dat',
            sep=',',
            format={'col':0, 'row':1, 'value':2, 'ids': int})

k = 100
svd.compute(k=k, min_values=5, pre_normalize=None, mean_center=True, post_normalize=True)

def hasTags(rec, tags):
    return len(set(tags).intersection(set(rec['tags']))) > 0

def hasAuthors(rec, authors):
    return len(set(authors).intersection(set(rec['artists']))) > 0

def recommendFor(user, tags=[], authors=[]):
    tags = set(tags)
    authors = set(authors)
    recommendations = svd.recommend(1, only_unknowns=False, is_row=False, n = 1000)
    rec_tracks = map(lambda rec: tracks[rec[0]], recommendations)
    if (len(tags) > 0):
        rec_tracks = filter(lambda track: hasTags(track, tags), rec_tracks)
    if (len(authors) > 0):
        rec_tracks = filter(lambda track: hasAuthors(track, authors), rec_tracks)
    return rec_tracks;

def test():
    data = Data()
    format = {'col':0, 'row':1, 'value':2, 'ids': int}
    svd = SVD(Sk=2)
    data.load('./src/data/traindata.dat', sep=',', format=format)
    train, test = data.split_train_test(percent=80) # 80% train, 20% test
    svd.set_data(train)

    k = 100
    svd.compute(k=k, min_values=1, pre_normalize=None, mean_center=True, post_normalize=True)

    rmse = RMSE()
    mae = MAE()
    i = 0

    total = len(test.get())
    for rating, item_id, user_id in tests:
        i = i + 1
        print str(i) + '/' + str(total);
        try:
            pred_rating = svd.predict(item_id, user_id)
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)
        except KeyError:
            continue

    print 'RMSE=%s' % rmse.compute()
    print 'MAE=%s' % mae.compute()

# test()
