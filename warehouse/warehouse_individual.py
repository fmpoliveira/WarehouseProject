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

        aux = []

        forklifts_count = len(self.problem.forklifts) - 1

        for i in range(self.num_genes):
            # is product
            if self.genome[i] <= len(self.problem.products):
                product_index = self.genome[i] - 1
                product = self.problem.products[product_index]  # get the product cell
                aux.append(product)

            # is forklift
            else:
                # TODO
                if len(aux) == 0:
                    self.weight += 0  # confirmar com o professor se o peso é o caminho total dos dois
                    forklifts_count = forklifts_count - 1
                else:
                    if forklifts_count > 0:
                        # get the forklift
                        forklift = self.problem.forklifts[forklifts_count]
                        aux.insert(0, forklift)
                        aux.insert(len(aux), self.problem.agent_search.exit)
                        total = self.compute_weight(aux)
                        print("total", total)
                        self.weight += total
                        aux = []
                        forklifts_count = forklifts_count - 1

        # if it only has 1 forklift
        if len(self.problem.forklifts) == 1:
            forklift = self.problem.forklifts[0]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            total = self.compute_weight(aux)
            print("total", total)
            self.weight += total
            if self.problem.minDistance > self.weight:
                self.problem.minDistance = self.weight

        # if it has more than 1 forklift and count for the index is the first one
        elif forklifts_count == 0 and len(self.problem.forklifts) > 1:
            forklift = self.problem.forklifts[forklifts_count]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            total = self.compute_weight(aux)
            print("total", total)
            self.weight += total
            if self.problem.minDistance > self.weight:
                self.problem.minDistance = self.weight


        # for i in range(len(a) - 1):
        #     initial_position = a[i]
        #     next_position = a[i + 1]
        #     for pair_agent in self.problem.agent_search.pairs:
        #         if (pair_agent.cell1 == initial_position and pair_agent.cell2 == next_position) or \
        #                 (pair_agent.cell2 == initial_position and pair_agent.cell1 == next_position):
        #             print("Success!!!", pair_agent, initial_position, next_position)
        #             self.weight += pair_agent.value
        #             break
        #     print("------")

        print(self.weight)

        self.fitness = self.weight if self.weight <= self.problem.minDistance else 0

        return self.fitness



    def compute_weight(self, arr):
        total = self.weight
        for i in range(len(arr) - 1):
            initial_position = arr[i]
            next_position = arr[i + 1]
            for pair_agent in self.problem.agent_search.pairs:
                if (pair_agent.cell1 == initial_position and pair_agent.cell2 == next_position) or \
                        (pair_agent.cell2 == initial_position and pair_agent.cell1 == next_position):
                    #print("Success!!!", pair_agent, initial_position, next_position)
                    total += pair_agent.value
                    break
            #print("------")

        return total

    def obtain_all_path(self):
        # TODO
        pass

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        string += '\nFitness: ' + f'{self.fitness}'
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.weight = self.weight
        # TODO done
        return new_instance
