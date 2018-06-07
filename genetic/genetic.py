""" Written by Jose and Neil,
 directly copied and pasted into this file by Yoav"""

import deap
from deap import base, tools, algorithms
from network.network import evaluate_fitness, FitnessValue
import random


class Genetic:
    """ Wrapper class for deap genetic algorithms
    """

    def __init__(self, beginning_networks, data, numgens=10000):
        """ Initialize genetic class

            :param: self: current genetic class
            :param: beginning_networks: first neural networks to start evolving
            :param: data: array/list/data structure of useful replay data
        """
        # our parameters
        self.finalCount = 10
        # How many individuals do we want in the end?
        # weight domain (for mutations)
        self.__weightMAX = 1
        self.__weightMIN = -1

        # deap algorithm arguments
        self.networks = beginning_networks
        self.data = data
        self.toolbox = base.Toolbox()
        self.tournsize = 2
        # number of parents selected from each generation
        self.genSize = 10
        self.cxpb = 1.0
        # probability of mating two individuals
        self.mutpb_indiv = 1.0
        # probability of mutating an individual
        # 1.0 because we want to maybe mutate a weight,
        # not maybe mutate an entire individual.
        # 1.0 means that no individual will be exempt
        # from its weights being mutated.
        self.mutpb_weight = 0.2
        # probability of mutating a weight
        self.ngen = numgens
        # 10000 is probably far too low/high.
        # I pulled it out of a hat.
        # TODO see if there's a standard value or
        # if we just need to do trial & error
        # to balance time & performance.

    def begin(self, X, Y):
        """
        Toolbox needs aliases: mate, mutate, select, evaluate
        Data from replays passed in as param X and Y(see NN evaluate fitness)
        """
        self.toolbox.register("mate", crossover)
        # TODO write custom crossover function
        self.toolbox.register("mutate"
                              , mutate  # defined below
                              , mutProb=self.mutpb_weight
                              , weightMIN=self.__weightMIN
                              , weightMAX=self.__weightMAX)
        self.toolbox.register("select"
                              , tools.selTournament
                              # ...(individuals, k, tournsize, fit_attr='fitness')
                              , tournsize=self.tournsize
                              , fit_attr='fitness')
        self.toolbox.register("evaluate", evaluate, paramX=X, paramY=Y)

        population = self.networks
        cxpb = self.cxpb
        # probability of mating two individuals
        mutpb = self.mutpb_indiv
        # probability of mutating an individual
        ngen = self.ngen
        halloffame = deap.tools.HallOfFame(self.finalCount)
        # Object that keeps track of the x best individuals.
        # x = self.finalCount = number of individuals we want in the end

        deap.algorithms.eaSimple(population, self.toolbox, cxpb, mutpb, ngen, halloffame = halloffame)

        return halloffame


def mutate(individual, mutProb, weightMIN, weightMAX):
    """
    Mutates an individual, in-place.
    For each weight, maybe assigns new value between
         [ weightMIN, weightMAX ].
    :param individual: the neural network to be mutated
    :param mutProb: the probability of mutating a given weight
    :param weightMIN: minimum value of a weight
    :param weightMAX: maximum value of a weight
    """
    LAYERS = individual.get_num_layers()
    # TODO I think I saw a bug in get_weights in network.py.
    # Shouldn't an error be raised if layer >= self.num_layers
    # not layer > self.num_layers?
    # Jose is new to Python, so he could be wrong.
    # If he's wrong, change LAYERS-1 to LAYERS.

    # for all layers
    for l in range(LAYERS):

        weights = individual.get_weights(l)
        # numpy array copy of this layer's weights

        # for all weights in this layer
        for w in range(len(weights)):
            for n in range(len(weights[w])):
                if random.uniform(0, 1) <= mutProb:
                    # randomize the weight
                    weights[w][n] = random.uniform(weightMIN, weightMAX)

        individual.set_weights(l, weights)
        individual.fitness = FitnessValue(0)
        # set weights for one layer
    return individual,


def crossover(parent1, parent2):
    # Assuming both individuals have same number of layers?
    # Crossing over an entire layer's weights since there is no way currently to get
    # or set individual weights

    # randomize layer to cross over
    num_layers = parent1.num_layers
    crossoverLayer = random.randint(0, num_layers - 1)

    # crossover entire layer's weights
    parent1_weights = parent1.get_weights(crossoverLayer)
    parent1.set_weights(crossoverLayer, parent2.get_weights(crossoverLayer))
    parent2.set_weights(crossoverLayer, parent1_weights)

    return parent1, parent2


def evaluate(individual, paramX, paramY):
    return evaluate_fitness(individual, paramX, paramY)