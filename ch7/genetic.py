import time
import random
import numpy as np
from math import ceil

class Individual():
    def __init__(self, genome, fitness):
        self.genome = genome
        self.fitness = fitness
    def __gt__(self, other):
        return self.fitness > other.fitness
    def __eq__(self, other):
        return self.fitness == other.fitness and self.genome == other.genome

class ES():
    #Evolutionary strategies
    def __init__(self, mu, lambda_, initialize, fitness, mutate, sample, plus=True, optimal_fitness=None, timer=10, visualizer=None, individual=Individual):
        self.mu = mu
        self.lambda_ = lambda_
        self.individual_class = individual
        self.initialize = initialize
        self.fitness = fitness
        self.mutate = mutate
        self.sample = sample
        #(mu, lambda_) algorithm if False, mu+lambda_ algorithm if true
        self.plus = plus
        self.population = []
        if timer is None:
            self.timer = np.inf
        else:
            self.timer = timer
        self.visualizer = visualizer
        if optimal_fitness is None:
            self.optimal_fitness = np.inf
        else:
            self.optimal_fitness = optimal_fitness
        
    def solve(self):
        self.gen = 0
        start_time = time.time()
        self.population = self.initialize(self.lambda_, self.fitness, self.individual_class)
        best = self.population[0]
        while self.optimal_fitness > best.fitness  and time.time() < start_time + self.timer:
            old_best = best
            for individual in self.population:
                if individual > best:
                    best = individual
            if self.mu < len(self.population):
                keep = self.sample(self.population, self.mu, self.gen)
            else:
                keep = self.population
            new_pop = []
            for individual in keep:
                for i in range(ceil(self.lambda_/self.mu)):
                    new_pop.append(self.mutate(individual, self.fitness, self.individual_class, self.gen))
            if self.plus:
                new_pop.extend(keep)
            self.population = new_pop
            self.gen += 1
            if self.visualizer is not None and old_best != best:
                self.visualizer(best, start_time)
        return best   
