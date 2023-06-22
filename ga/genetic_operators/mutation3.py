import copy
import random

from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation


class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        # TODO done
        # 1. Selecione aleatoriamente um valor do array original.
        # 2. Remova esse valor do array original
        # 3. Shuffle do array original
        # 4. Inserir o valor selecionado aleatoriamente numa posição aleatória do array shuffled
        # 5. Devolver o array resultante
        
        num_genes = len(ind.genome)
        rand_pos = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        save_1 = ind.genome[rand_pos]
        ind.genome.pop(rand_pos)
        random.shuffle(ind.genome)
        rand_pos_insert = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        ind.genome.insert(rand_pos_insert, save_1)

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
