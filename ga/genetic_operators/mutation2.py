from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
import random


class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        rand_pos = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        save_1 = ind.genome[rand_pos]

        for i in range(num_genes - 1):
            if ind.genome[i] == rand_pos:
                ind.genome[i] = save_1
                ind.genome[rand_pos] = rand_pos

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
