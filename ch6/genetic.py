import random
import datetime
import copy

class Chromosone:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness

class Genetic:
    def __init__(self, gene_set, mutate, fitness, display, optimal_fitness, length):
        self.gene_set = gene_set
        self.fitness = fitness
        self.display = display
        self.mutate = mutate
        self.optimal_fitness = optimal_fitness
        self.length = length
    
    def get_fitness(self, genes):
        return self.fitness(genes)
        
    def _mutate(self, parent):
        return self.mutate(parent, self.gene_set)
        
    def _generate_parent(self):
        genes = [random.choice(self.gene_set) for x in range(self.length)]
        fitness = self.fitness(genes)
        return Chromosone(genes, fitness)
    
    def solve(self, display_on=True):
        self.start_time = datetime.datetime.now()
        best = self._generate_parent()
        if display_on:
            self.display(best, self.start_time)
        fitness = best.fitness
        while fitness != self.optimal_fitness:
            candidate_genes = self._mutate(best)
            candidate = Chromosone(candidate_genes, self.get_fitness(candidate_genes))
            if candidate.fitness > fitness:
                fitness = candidate.fitness
                best = candidate
                if display_on:
                    self.display(best, self.start_time)
        return best