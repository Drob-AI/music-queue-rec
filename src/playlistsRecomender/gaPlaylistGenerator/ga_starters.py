import numpy

def ga_start_with_debug(populations, toolbox, tools, ga_algorithms, hof,  params):
    pop = toolbox.population(n=populations)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    params['halloffame'] = hof
    params['stats'] = stats
    pop, log = ga_algorithms(pop, toolbox, **params)

def ga_start_silent(populations, toolbox, tools, ga_algorithms, hof,  params):
    pop = toolbox.population(n=populations)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    params['halloffame'] = hof
    pop, log = ga_algorithms(pop, toolbox, **params)