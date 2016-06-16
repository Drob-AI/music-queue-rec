import dataProvider
import os
import gaPlaylistGenerator as gaGenerator
import numpy
import random

from deap import creator, base, tools, algorithms
import os

dir = os.path.dirname(os.path.realpath(__file__))

class PlaylistGenerator:
    def __init__(self, data_set, fitness_weights = (1.0,),
                 playlist_size = 15, cross_pb = 0.7,
                 mutate_pb = 0.3,  hof_size=5,
                 number_gen = 100, gen_size = 300):
        # self.data_set = dataProvider.import_folder( dir + '/dataProvider/data/datasset/yes_small/')
        self.data_set = data_set;
        self.ids = list(set([song.id for playlist in self.data_set.train for song in playlist.songs]))
        self.gen_size = gen_size

        creator.create("FitnessMax", base.Fitness, weights=fitness_weights)
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        # Attribute generator
        self.toolbox.register("attr_float", self.__create_new_playlist)
        # Structure initializers

        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
            self.toolbox.attr_float, playlist_size)

        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.__eval_one_max)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", self.__mutate_playlist, indpb=mutate_pb)
        self.toolbox.register("select", tools.selTournament, tournsize=3);
        self.hof = tools.HallOfFame(hof_size)
        self.ga_algorithms = algorithms.eaSimple
        self.params = {
            'cxpb':cross_pb,
            'mutpb':mutate_pb,
            'ngen':number_gen,
            # 'verbose':True
            'verbose':False
        }

    def start(self):
        # gaGenerator.ga_start_with_debug(self.gen_size, self.toolbox, tools, self.ga_algorithms,
        #                             self.hof, self.params)
        gaGenerator.ga_start_silent(self.gen_size, self.toolbox, tools, self.ga_algorithms,
            self.hof, self.params)
        return self.hof;

    def __eval_one_max(self, playlist):
        # print(playlist,reduce(lambda x, y: x - y, playlist) )
        # return reduce(lambda x, y: x - y, playlist),
        return sum(playlist),

    def __create_new_playlist(self):
        return numpy.random.permutation(self.ids)[0]

    def __mutate_playlist(self, playlist, indpb):
        if(random.random() < 0.4):
            for index, id in enumerate(playlist):
                if(random.random() < 0.3):
                    playlist[index] = self.__create_new_playlist()

        if(random.random() < indpb):
            i , j = random.randint(0, len(playlist) - 1), random.randint(0, len(playlist) - 1)
            playlist[i], playlist[j] = playlist[j], playlist[i]

        return playlist,
