import math

import copy

from ga.genetic_algorithm import GeneticAlgorithm
from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual


class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes
        copyInd1 = copy.deepcopy(ind1.genome)
        copyInd2 = copy.deepcopy(ind2.genome)
        child1 = []
        child2 = []
        # Primeiro child fica com a primeira terço do ind2 e o segundo child fica com primeira terço do ind1
        # Removemos esses elementos das copias
        # Juntamos os elementos dos originais num array
        # Aleatoriamente geramos um numero que corresponde ao index do array com todos
        # Vamos adicionando a cada ind novo esse elemento caso não tenha, até ambos se encontrarem completos

        index_cut = math.floor(num_genes / 3)

        child1 = copyInd2[:index_cut]
        child2 = copyInd1[:index_cut]

        del copyInd1[:index_cut]
        del copyInd2[:index_cut]

        all_individuals_left = copyInd1 + copyInd2

        while len(child1) != num_genes:
            rand1 = GeneticAlgorithm.rand.randint(0, len(all_individuals_left) - 1)
            value1 = all_individuals_left[rand1]
            if value1 not in child1:
                child1.append(value1)
                del all_individuals_left[rand1]  # apaga o elemento por index

        while len(child2) != num_genes:
            rand2 = GeneticAlgorithm.rand.randint(0, len(all_individuals_left) - 1)
            value2 = all_individuals_left[rand2]
            if value2 not in child2:
                child2.append(value2)
                del all_individuals_left[rand2]

        ind1.genome = child1
        ind2.genome = child2

    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"
