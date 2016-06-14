import dataProvider
import os
import gaPlaylistGenerator as gaGenerator
import numpy
import random

from deap import creator, base, tools, algorithms

print(gaGenerator.ga_playlist_generator)

data_set = dataProvider.import_folder( './dataProvider/data/dataset/yes_small/')

ids = list(set([song.id for playlist in data_set.train for song in playlist.songs]))
print(len(ids));

def eval_one_max(playlist):
    return sum(playlist),

def create_new_playlist():
    return numpy.random.permutation(ids)[0]

def mutate_path(path, indpb):
    if(random.random() < indpb):
        i , j = random.randint(0, len(path) - 1), random.randint(0, len(path) - 1)
        path[i], path[j] = path[j], path[i]

    return path,

def similar_hof(ind, hofer):
    return eval_one_max(ind) == eval_one_max(hofer)

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float",create_new_playlist)
# Structure initializers

toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_float, 10)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_one_max)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate_path, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3);
hof = tools.HallOfFame(1, similar=similar_hof)
ga_algorithms = algorithms.eaSimple
params = {
    'cxpb':0.8,
    'mutpb':0.1,
    'ngen':300,
    'verbose':True
}

gaGenerator.ga_playlist_generator(1, toolbox, tools, ga_algorithms, hof, params)