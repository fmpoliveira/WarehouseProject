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
        self.paths_forklifts = {}
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
                index = self.genome[i] - len(self.genome)

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
            forklift = self.problem.forklifts[index + 1]
            aux.insert(0, forklift)
            aux.insert(len(aux), self.problem.agent_search.exit)
            self.weight += self.compute_weight(aux)
            self.problem.path.append(aux)

        self.fitness = self.weight

        return self.fitness

    def compute_weight(self, arr):
        total = self.weight
        is_reversed = False
        list_actions = []

        if arr[0] not in self.paths_forklifts:
            self.paths_forklifts[arr[0]] = []

        for i in range(len(arr) - 1):
            initial_position = arr[i]
            next_position = arr[i + 1]
            key_cell = Pair(initial_position, next_position)

            if key_cell not in self.problem.agent_search.solution_by_pair:
                key_cell = Pair(next_position, initial_position)
                is_reversed = True

            list_cell = self.problem.agent_search.get_solution_by_pair(key_cell)

            list_actions = copy.deepcopy(list_cell.actions)

            #if is_reversed:
                #self.reverse_actions(list_actions)

            self.paths_forklifts[arr[0]].append(list_actions)

            is_reversed = False

            total += list_cell.cost

        # adiciona o novo valor à lista ordenada de maior para menor
        if total not in self.problem.agent_search.weight_values:
            self.problem.agent_search.weight_values.append(total)
            self.problem.agent_search.weight_values.sort(reverse=True)

        if total not in self.values:
            self.values.append(total)
            self.values.sort(reverse=True)

        return total

    def reverse_actions(self, list_actions):
        list_reversed = []
        for action in list_actions:
            if action == "UP":
                list_reversed.append("DOWN")
            elif action == "DOWN":
                list_reversed.append("UP")
            elif action == "LEFT":
                list_reversed.append("RIGHT")
            else:
                list_reversed.append("LEFT")

        return list_reversed

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
        pass

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        string += '\nFitness: ' + f'{self.fitness}' + "\n\n"
        string += '\nWorst Fitness ' + str(self.problem.agent_search.weight_values[0]) + "\n\n"
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:

        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.weight = self.weight
        new_instance.values = self.values
        new_instance.paths_forklifts = self.paths_forklifts
        # TODO done
        return new_instance
