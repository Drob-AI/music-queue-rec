import os
import gaPlaylistGenerator as gaGenerator
import numpy
import random
from ngrams import *
from deap import creator, base, tools, algorithms
import os
from threading import Thread

# max 9
THREADS_NUMBER = 3
dir = os.path.dirname(os.path.realpath(__file__))
GA_PARAMS = [
        # Creates less different playlists with not bad prob
        {
            'cxpb':0.7,
            'mutpb':0.3,
            'ngen':200,
            # 'verbose':True,
            'verbose':False,
            'gen_size':300
        },
        {
            'cxpb':0.7,
            'mutpb':0.9,
            'ngen':100,
            # 'verbose':True,
            'verbose':False,
            'gen_size':300
        },
        {
            'cxpb':0.4,
            'mutpb':0.9,
            'ngen':100,
            # 'verbose':True,
            'verbose':False,
            'gen_size':400
        },
        {
            'cxpb':0.4,
            'mutpb':0.9,
            'ngen':100,
            # 'verbose':True,
            'verbose':False,
            'gen_size':400
        },
        {
            'cxpb':0.8,
            'mutpb':0.3,
            'ngen':300,
            # 'verbose':True,
            'verbose':False,
            'gen_size':300
        },
        {
            'cxpb':0.7,
            'mutpb':0.3,
            'ngen':600,
            # 'verbose':True,
            'verbose':False,
            'gen_size':300
        },
        {
            'cxpb':0.7,
            'mutpb':0.3,
            'ngen':600,
            # 'verbose':True,
            'verbose':False,
            'gen_size':300
        },
        {
            'cxpb':0.7,
            'mutpb':0.4,
            'ngen':200,
            # 'verbose':True,
            'verbose':False,
            'gen_size':3000
        },
        {
            'cxpb':0.7,
            'mutpb':0.5,
            'ngen':100,
            # 'verbose':True,
            'verbose':False,
            'gen_size':2000
        },]
class PlaylistGenerator:
    def __init__(self, data_set, fitness_weights = (1.0,),
        playlist_size = 15,  hof_size = 5):

        self.ids = data_set
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
        self.toolbox.register("mate", self.__cross)
        self.toolbox.register("mutate", self.__mutate_playlist, indpb=1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        self.hofs = []
        for i in range(THREADS_NUMBER):
            self.hofs.append(tools.HallOfFame(hof_size))

        print(self.hofs)
        self.ga_algorithms = algorithms.eaSimple

        self.ngramMetric = Ngrams()

    def start(self):

        threads = []
        for i in range(0, THREADS_NUMBER):
            params = (GA_PARAMS[i]['gen_size'], self.toolbox, tools, self.ga_algorithms,
                                    self.hofs[i], dict((k, GA_PARAMS[i][k]) for k in ('cxpb', 'mutpb', 'ngen', 'verbose')))

            threads.append(Thread(target=gaGenerator.ga_start_silent, args=params))
            # threads.append(Thread(target=gaGenerator.ga_start_with_debug, args=params))
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

    def __cross(self, pl1, pl2):
        crossed = tools.cxTwoPoint(pl1, pl2)
        self.__mutate_reapeats(crossed[0])
        self.__mutate_reapeats(crossed[1])
        return crossed

    def __mutate_reapeats(self, pl):
        for song in pl:
            indexes = [i for i, x in enumerate(pl) if x == song]

            if(len(indexes) > 1):
                indexes = indexes[1:]

                for index in indexes:
                    new_song = self.__create_new_playlist()
                    while (new_song in pl):
                        new_song = self.__create_new_playlist()

                    pl[index] = new_song

    def __mutate_playlist(self, playlist, indpb):
        if(random.random() < 0.6):
            for index, id in enumerate(playlist):
                if(random.random() < 0.3):
                    new_song = self.__create_new_playlist()
                    if(new_song not in playlist):
                        playlist[index] = new_song

        if(random.random() < indpb):
            i , j = random.randint(0, len(playlist) - 1), random.randint(0, len(playlist) - 1)
            playlist[i], playlist[j] = playlist[j], playlist[i]

        return playlist,
