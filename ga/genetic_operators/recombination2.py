
import copy
import random
from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination


class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = ind1.num_genes

        copyInd1 = copy.deepcopy(ind1.genome)
        copyInd2 = copy.deepcopy(ind2.genome)

        child1 = []
        child2 = []

        # Primeiro child é gerado da seguinte forma:
        # Primeiro insere um elemento aleatório do ind1 e depois coloca um elemento aleatorio do ind2
        # Repete este processo aletório até atingir o tamanho pretendido
        while len(child1) != num_genes:
            rand1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
            value1 = ind1.genome[rand1]
            rand2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
            value2 = ind2.genome[rand2]
            if value1 not in child1:
                child1.append(value1)
                copyInd1.remove(value1)  # remover o valor em si
            if value2 not in child1:
                child1.append(value2)
                copyInd2.remove(value2)

        # Para formar o child2, junta os elementos que sobraram das cópias e aplica um shuffle
        child2 = copyInd1 + copyInd2
        random.shuffle(child2)

        ind1.genome = child1
        ind2.genome = child2

    def __str__(self):
        return "Recombination 2 (" + f'{self.probability}' + ")"
