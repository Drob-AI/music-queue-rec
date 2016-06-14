import random
import json
import numpy

from deap import creator, base, tools, algorithms

# towns = []
# n = 100
# for i in range(n):
#     x = random.randrange(0, 10)
#     y = random.randrange(0, 10)
    # new_town = (x, y)
#     towns.append(new_town)

# with open('data.json', 'w') as outfile:
#     json.dump(towns, outfile)

with open('data.json') as data_file:
    towns = json.load(data_file)
# print(towns)

def distance(point1, point2):
    return numpy.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def eval_one_max(individual):
    distances = [distance(individual[ind- 1], individual[ind]) if (ind > 0) else 0
                for ind, point in enumerate(individual)]
    return sum(distances),

def create_new_point():
    return numpy.random.permutation(towns)[0]

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
toolbox.register("attr_float",create_new_point)
# Structure initializers

toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_float, len(towns))

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_one_max)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate_path, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)
hof = tools.HallOfFame(1, similar=similar_hof)

def main():
    pop = toolbox.population(n=2000)
    hof = tools.HallOfFame(1, similar=similar_hof)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.1, ngen=300,
                                   stats=stats, halloffame=hof, verbose=True)


main()