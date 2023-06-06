import copy

import numpy as np

from ga.individual_int_vector import IntVectorIndividual
from warehouse.cell import Cell


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.weight = None  # sum of the path since the start of the forklift until the exit

        # TODO

    def compute_fitness(self) -> float:
        # TODO
        print(self.genome)
        self.weight = 0
        a = []

        # for pair in self.problem.agent_search.pairs:
        # print(pair.cell1, pair.cell2)

        x = Cell(1, 2)
        y = Cell(2, 2)

        print(x.compareWithReversedCells(y))

        if (len(self.problem.forklifts) == 1):
            forklift = self.problem.forklifts[0]
            a.insert(0, forklift)

        for i in range(self.num_genes):
            if self.genome[i] <= len(self.problem.products):
                product_index = self.genome[i] - 1
                product = self.problem.products[product_index]  # get the product cell
                a.append(product)
            # confirmamos queé um forklift
            else:
                # TODO
                if len(a) == 0:
                    self.weight += 0 #confirmar com o professor se o peso é o caminho total dos dois
                #else:
                    #a.insert(0, )
                #


        a.insert(len(a), self.problem.agent_search.exit)

        # temos que fazer o tamanho do array menos 1 porque senão faz uma iteração a mais
        for i in range(len(a) - 1):
            initial_position = a[i]
            next_position = a[i + 1]
            for pair_agent in self.problem.agent_search.pairs:
                if (pair_agent.cell1 == initial_position and pair_agent.cell2 == next_position) or \
                        (pair_agent.cell2 == initial_position and pair_agent.cell1 == next_position):
                    print("Success!!!", pair_agent, initial_position, next_position)
                    self.weight += pair_agent.value
                    break
            print("------")

        print(self.weight)
        return 0

    def obtain_all_path(self):
        # TODO
        pass

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        # TODO
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        # TODO
        return new_instance
