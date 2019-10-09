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

class EvFuncs:
    def __init__(self, genes, individual, initialize, fitness, mutate, sample, vis=None):
        self._genes = genes
        self._individual = individual
        self._initialize = initialize
        self._fitness = fitness
        self._mutate = mutate
        self._sample = sample
        self._vis = vis
        
    def initialize(self, lambda_):
        return self._initialize(lambda_, self._genes, self._individual, self._fitness)
    
    def mutate(self, ind, gen):
        return self._mutate(ind, gen, self._fitness, self._individual)
    
    def sample(self, population, mu, gen):
        return self._sample(population, mu, gen, self._fitness)
    
    def visualize(self, ind, start_time):
        return self._vis(ind, start_time)
            

class ES():
    #Evolutionary strategies
    def __init__(self, ev_funcs, mu, lambda_, plus=True, timer=10, optimal_fitness=None):
        self.ev_funcs = ev_funcs
        self.mu = mu
        self.lambda_ = lambda_
        #(mu, lambda_) algorithm if False, mu+lambda_ algorithm if true
        self.plus = plus
        self.population = []
        if timer is None:
            self.timer = np.inf
        else:
            self.timer = timer
        if optimal_fitness is None:
            self.optimal_fitness = np.inf
        else:
            self.optimal_fitness = optimal_fitness
        
    def solve(self):
        self.gen = 0
        start_time = time.time()
        self.population = self.ev_funcs.initialize(self.lambda_)
        best = self.population[0]
        while self.optimal_fitness > best.fitness  and time.time() < start_time + self.timer:
            old_best = best
            for individual in self.population:
                if individual > best:
                    best = individual
            if self.mu < len(self.population):
                keep = self.ev_funcs.sample(self.population, self.mu, self.gen)
            else:
                keep = self.population
            new_pop = []
            for individual in keep:
                for i in range(self.lambda_//self.mu):
                    new_pop.append(self.ev_funcs.mutate(individual, self.gen))
            if self.plus:
                new_pop.extend(keep)
            self.population = new_pop
            self.gen += 1
            if self.ev_funcs._vis is not None and old_best != best:
                self.ev_funcs.visualize(best, start_time)
        return best   

class GenFuncs:
    def __init__(self, genes, individual, initialize, fitness, crossover, mutate, sample, vis=None):
        self._genes = genes
        self._individual = individual
        self._initialize = initialize
        self._fitness = fitness
        self._crossover = crossover
        self._mutate = mutate
        self._sample = sample
        self._vis = vis
        
    def initialize(self, pop_size):
        return self._initialize(pop_size, self._genes, self._individual, self._fitness)
    
    def mutate(self, ind, gen):
        return self._mutate(ind, gen, self._fitness, self._individual)
    
    def crossover(self, pop, gen):
        return self._crossover(pop, gen, self._fitness, self._individual)
    
    def sample(self, population, pop_size, gen):
        return self._sample(population, pop_size, gen, self._fitness)
    
    def visualize(self, ind, start_time):
        return self._vis(ind, start_time)

class GenAlg():
    #Evolutionary strategies
    def __init__(self, gen_funcs, pop_size, timer=10, optimal_fitness=None):
        self.gen_funcs = gen_funcs
        self.pop_size = pop_size
        self.population = []
        if timer is None:
            self.timer = np.inf
        else:
            self.timer = timer
        if optimal_fitness is None:
            self.optimal_fitness = np.inf
        else:
            self.optimal_fitness = optimal_fitness

        
    def solve(self):
        self.gen = 0
        start_time = time.time()
        self.population = self.gen_funcs.initialize(self.pop_size)
        best = self.population[0]
        while self.optimal_fitness > best.fitness  and time.time() < start_time + self.timer:
            old_best = best
            for individual in self.population:
                if individual > best:
                    best = individual
            for i in pop_size//2:
                parents = self.gen_funcs.sample(self.population, 2, self.gen)
            
            new_pop = []
            self.population = new_pop
            self.gen += 1
            if self.gen_funcs._vis is not None and old_best != best:
                self.gen_funcs.visualize(best, start_time)
        return best   