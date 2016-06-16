import recsys.algorithm
from recsys.algorithm.factorize import SVD

recsys.algorithm.VERBOSE = True

svd = SVDNeighbourhood()
svd.load_data(filename='../data/traindata.dat',
            sep=',',
            format={'col':0, 'row':1, 'value':2, 'ids': int})

k = 100
svd.compute(k=k, min_values=1, pre_normalize=None, mean_center=True, post_normalize=True)
print(svd.recommend(1, only_unknowns=False, is_row=False))