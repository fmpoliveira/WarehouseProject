import random

from ga.genetic_algorithm import GeneticAlgorithm
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation


class Mutation3(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        rand_pos = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        print("rand_pos", rand_pos)

        save_1 = ind.genome[rand_pos]

        print("save_1", save_1)

        print("genome", ind.genome)

        ind.genome.pop(rand_pos)

        print("genome_ remove", ind.genome)

        random.shuffle(ind.genome)

        print("genome shuffle", ind.genome)

        rand_pos_insert = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        print("rand_pos_insert", rand_pos_insert)

        ind.genome.insert(rand_pos_insert, save_1)

        print("genome insert", ind.genome)

    def __str__(self):
        return "Mutation 3 (" + f'{self.probability}' + ")"
