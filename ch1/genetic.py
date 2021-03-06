import random
import datetime
import copy
import time
import statistics

class Chromosone:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness

class Genetic:
    def __init__(self, gene_set, target, fitness, display):
        self.gene_set = gene_set
        self.fitness = fitness
        self.length = len(target)
        self.target = target
        self.display = display
    
    def get_fitness(self, genes):
        return self.fitness(genes, self.target)
        
    def _mutate(self, parent):
        index = random.randrange(0, len(parent.genes))
        parent_genes = copy.copy(parent.genes)
        new_gene = random.choice(self.gene_set)
        while new_gene == parent_genes[index]:
            new_gene = random.choice(self.gene_set)
        parent_genes[index] = new_gene
        fitness = self.get_fitness(parent_genes)
        return Chromosone(parent_genes, fitness)
        
    def _generate_parent(self):
        genes = [random.choice(self.gene_set) for x in range(self.length)]
        fitness = self.fitness(genes, self.target)
        return Chromosone(genes, fitness)
    
    def solve(self, display_on=True):
        start_time = datetime.datetime.now()
        best = self._generate_parent()
        if display_on:
            self.display(best, start_time)
        fitness = best.fitness
        while fitness < self.length:
            candidate = self._mutate(best)
            if candidate.fitness > fitness:
                fitness = candidate.fitness
                best = candidate
                if display_on:
                    self.display(best, start_time)
        return best    
    