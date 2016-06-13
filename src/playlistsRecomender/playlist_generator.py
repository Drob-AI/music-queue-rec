import dataProvider
import os

data_set = dataProvider.import_folder( './dataProvider/data/dataset/yes_small/')

print(data_set.train[0].songs)