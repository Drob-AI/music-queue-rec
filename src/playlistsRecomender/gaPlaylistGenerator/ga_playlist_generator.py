import numpy

def ga_playlist_generator(populations, toolbox, tools, ga_algorithms, hof,  params):

    pop = toolbox.population(n=populations)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    params['halloffame'] = hof
    params['stats'] = stats
    print('started')
    print(params)
    pop, log = ga_algorithms(pop, toolbox, **params)