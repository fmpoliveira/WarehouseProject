from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
import random


class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        # TODO done
        num_genes = len(ind.genome)
        rand_pos = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        save_1 = ind.genome[rand_pos]
        rand_aux = rand_pos  # se a posição for zero, temos que aumentar o numero, uma vez que o valor min de um elemento do genorma é 1

        if rand_pos == 0:
            rand_aux += 1

        for i in range(num_genes - 1):
            if ind.genome[i] == rand_aux:
                ind.genome[i] = save_1
                ind.genome[rand_pos] = rand_aux

    def __str__(self):
        return "Mutation 2 (" + f'{self.probability}' + ")"
