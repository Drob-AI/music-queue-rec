import dataProvider
import os
import gaPlaylistGenerator as gaGenerator
import numpy
import random
from ngrams import *
from deap import creator, base, tools, algorithms
import os
from threading import Thread


THREADS_NUMBER = 1
dir = os.path.dirname(os.path.realpath(__file__))

class PlaylistGenerator:
    def __init__(self, data_set, fitness_weights = (1.0,),
                 playlist_size = 15, cross_pb = 0.7,
                 mutate_pb = 0.3,  hof_size = 5,
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

        self.hofs = []
        for i in range(THREADS_NUMBER):
            self.hofs.append(tools.HallOfFame(hof_size))

        self.ga_algorithms = algorithms.eaSimple
        self.params = {
            'cxpb':cross_pb,
            'mutpb':mutate_pb,
            'ngen':number_gen,
            'verbose':True
            # 'verbose':False
        }
        self.ngramMetric = Ngrams()

    def start(self):

        threads = []
        for i in range(0, THREADS_NUMBER):
            params = (self.gen_size, self.toolbox, tools, self.ga_algorithms,
                                    self.hofs[i], self.params)
            # threads.append(Thread(target=gaGenerator.ga_start_silent, args=params))
            threads.append(Thread(target=gaGenerator.ga_start_with_debug, args=params))
            threads[i].start()

        for thread in threads:
            thread.join()

        # gaGenerator.ga_start_silent(self.gen_size, self.toolbox, tools, self.ga_algorithms,
        #     self.hof, self.params)
        self.hofs = sorted(list([playlist for hof in self.hofs for playlist in list(hof)]),
                        key=lambda pl: self.__eval_one_max(pl), reverse=True)


        recomended_playlists = [self.hofs[0]]
        for playlist in self.hofs:
            if(all(self.__playlist_distance(playlist, prev_playlist) < 0.5 for prev_playlist in recomended_playlists)):
                recomended_playlists.append(playlist)

        print([self.__eval_one_max(pl) for pl in recomended_playlists])
        return recomended_playlists;

    def __playlist_distance(self, playlist1, playlist2):
        return float(sum([song1 == playlist2[i] for i, song1 in enumerate(playlist1)])) / len(playlist1)

    def __eval_one_max(self, playlist):
        return self.ngramMetric.scoreFromOneDimensionalArrayOfNumbers(playlist),

    def __create_new_playlist(self):
        random_index = random.randrange(0, len(self.ids))
        return self.ids[random_index]

    def __mutate_playlist(self, playlist, indpb):
        if(random.random() < 0.6):
            for index, id in enumerate(playlist):
                if(random.random() < 0.3):
                    new_song = self.__create_new_playlist()
                    playlist[index] = new_song

        if(random.random() < indpb):
            i , j = random.randint(0, len(playlist) - 1), random.randint(0, len(playlist) - 1)
            playlist[i], playlist[j] = playlist[j], playlist[i]

        return playlist,
