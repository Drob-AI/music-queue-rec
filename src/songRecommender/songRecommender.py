from recsys.algorithm.factorize import SVD

svd = SVD()
svd.load_data(filename='./data/movielens/ratings.dat',
            sep='::',
            format={'col':0, 'row':1, 'value':2, 'ids': int})