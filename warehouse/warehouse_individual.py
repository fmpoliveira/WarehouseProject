import copy

import numpy as np

from ga.individual_int_vector import IntVectorIndividual
from warehouse.cell import Cell
from warehouse.pair import Pair


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.weight = None  # sum of the path since the start of the forklift until the exit
        self.values = []
        # TODO

    def compute_fitness(self) -> float:
        # TODO
        self.weight = 0
        aux = []
        index = None

        forklifts_count = len(self.problem.forklifts) - 1

        for i in range(self.num_genes):
            # produto
            if self.genome[i] <= len(self.problem.products):
                product_index = self.genome[i] - 1
                product = self.problem.products[product_index]  # get the product cell
                aux.append(product)

            # forklift
            else:
                # exemplo: [2,4,5,1,3]
                # com o valor que está no array para o forklift (5) tiramos o tamanho dos produtos (5), logo vai buscar o 1 index
                index = self.genome[i] - len(self.problem.products)
                forklift = self.problem.forklifts[index]

                # adiciona o forklift no inicio
                aux.insert(0, forklift)

                # adiciona o saida no final
                aux.insert(len(aux), self.problem.agent_search.exit)

                self.weight = self.compute_weight(aux)

                forklifts_count -= 1
                aux = []

        # if it only has 1 forklift
        if len(self.problem.forklifts) == 1:
            forklift = self.problem.forklifts[0]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            self.weight = self.compute_weight(aux)
            self.problem.path.append(aux)

            # if it has more than 1 forklift and count for the index is the first one
        elif forklifts_count == 0 and len(self.problem.forklifts) > 1:
            # TODO
            # INDEX ESTÁ MAU
            forklift = self.problem.forklifts[index + 1]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            self.weight = self.compute_weight(aux)
            self.problem.path.append(aux)

        self.fitness = self.values[0]

        return self.fitness

    def compute_weight(self, arr):
        total = self.weight
        for i in range(len(arr) - 1):
            initial_position = arr[i]
            next_position = arr[i + 1]
            key_cell = Pair(initial_position, next_position)

            if key_cell not in self.problem.agent_search.solution_by_pair:
                key_cell = Pair(next_position, initial_position)
                # TODO
                # SENAO tiver o par temos que trocar ordem

            list_cell = self.problem.agent_search.get_solution_by_pair(key_cell)



            total += list_cell.cost


        print("TOTAL WEIGHT", total)
        # adiciona o novo valor à lista ordenada de maior para menor
        self.values.append(total)
        self.values.sort(reverse=True)
        return total

    # def compute_weight(self, arr):
    #     total = 0
    #     i = 0
    #
    #     for path in self.problem.path:
    #         for i in range(len(path) - 1):
    #             initial_position = path[i]
    #             next_position = path[i + 1]
    #             for pair_agent in self.problem.agent_search.pairs:
    #                 if (pair_agent.cell1 == initial_position and pair_agent.cell2 == next_position) or \
    #                         (pair_agent.cell2 == initial_position and pair_agent.cell1 == next_position):
    #                     total += pair_agent.value
    #                     break
    #
    #     return total

    def compute_path(self):
        aux = []

        forklifts_count = len(self.problem.forklifts) - 1

        for i in range(self.num_genes):
            # is forklift

            if self.genome[i] > len(self.problem.products):
                #  a primeiro que encontra é um forklift e o aux está como None
                if i == 0:
                    aux = []
                    forklift = self.problem.forklifts[0]
                    aux.append(forklift)
                    aux.insert(len(aux), self.problem.agent_search.exit)
                    self.problem.path.append(aux)
                    aux = []

                else:
                    forklift = self.problem.forklifts[forklifts_count]
                    aux.insert(0, forklift)
                    aux.insert(len(aux), self.problem.agent_search.exit)
                    self.problem.path.append(aux)
                    forklifts_count = forklifts_count - 1
                    aux = []
            # product
            else:
                product_index = self.genome[i] - 1
                product = self.problem.products[product_index]  # get the product cell
                aux.append(product)

        if len(self.problem.forklifts) == 1:
            forklift = self.problem.forklifts[0]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            self.problem.path.append(aux)

        # if it has more than 1 forklift and count for the index is the first one
        elif forklifts_count == 0 and len(self.problem.forklifts) > 1:
            forklift = self.problem.forklifts[forklifts_count]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            self.problem.path.append(aux)

    def obtain_all_path(self):
        # TODO
        return self.problem.path, len(self.problem.path)

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
