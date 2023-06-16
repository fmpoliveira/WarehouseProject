import copy

import numpy as np

from ga.individual_int_vector import IntVectorIndividual
from warehouse.actions import ActionDown, ActionUp, ActionLeft, ActionRight
from warehouse.cell import Cell
from warehouse.pair import Pair


class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.weight = None  # sum of the path since the start of the forklift until the exit
        self.steps_values = []  # guarda os custos para todos os forklifts
        self.worst_value = None  # guarda o custo do forklift com o pior caminho
        self.all_paths_forklifts = []  # guarda o caminho todo que os forklifts percorrem
        self.forklifts_and_products = {}  # guarda as cells com os produtos que vai buscar e a saida

        # TODO - done

    def compute_fitness(self) -> float:
        # TODO done
        self.weight = 0
        self.worst_value = 0
        self.steps_values = []
        self.all_paths_forklifts = []
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
                self.compute_weight_for_path_of_forklift(aux, index)
                forklifts_count -= 1
                aux = []

        # if it only has 1 forklift
        if len(self.problem.forklifts) == 1:
            self.compute_weight_for_path_of_forklift(aux, 0)

            # if it has more than 1 forklift and count for the index is the first one
        elif forklifts_count == 0 and len(self.problem.forklifts) > 1:
            self.compute_weight_for_path_of_forklift(aux, index + 1)

        self.fitness = self.worst_value

        return self.fitness

    def compute_weight_for_path_of_forklift(self, arr, index):
        forklift = self.problem.forklifts[index]
        arr.insert(0, forklift)
        arr.insert(len(arr), self.problem.agent_search.exit)
        self.forklifts_and_products[forklift] = arr
        self.weight = self.compute_weight(arr)

    def compute_weight(self, arr):
        total = self.weight
        is_reversed = False
        line_path = [arr[0]]

        for i in range(len(arr) - 1):
            initial_position = arr[i]
            next_position = arr[i + 1]
            pair_key = Pair(initial_position, next_position)

            if pair_key not in self.problem.agent_search.solution_by_pair:
                pair_key = Pair(next_position, initial_position)
                is_reversed = True

            list_solution_by_pair = self.problem.agent_search.get_solution_by_pair(pair_key)

            if is_reversed:
                list_cells_reversed = list_solution_by_pair.all_path_cells[
                                      ::-1]  # reverte o array com as celulas todas do par
                line_path.extend(
                    list_cells_reversed[1:])  # copia as células todas com exceção da primeira
            else:
                line_path.extend(
                    list_solution_by_pair.all_path_cells[1:])  # copia as células todas com exceção da primeira

            total += list_solution_by_pair.cost
            is_reversed = False

        self.all_paths_forklifts.append(line_path)

        # guarda os steps para cada forklift
        self.steps_values.append(len(line_path))
        # penalizar colisões
        # COLISOES: MESMA CELULA
        # if len(self.problem.forklifts) > 1:
        #    for forklift_index, forklift_cell in enumerate(self.problem.forklifts):
        #        for pair_key in self.paths_forklifts.keys():
        #            solution_for_pair = self.problem.agent_search.get_solution_by_pair(pair_key)
        #            self.teste[forklift_index].extend(solution_for_pair.all_path_cells)

        # adiciona o novo valor à lista ordenada de maior para menor
        if total > self.problem.agent_search.worst_global_weight:
            self.problem.agent_search.worst_global_weight = total

        # se o total calculado for maior que o pior resultado possivel nesta iteração, troca
        if total > self.worst_value:
            self.worst_value = total

        return total

    def obtain_all_path(self):
        # TODO - done
        max_steps = max(self.steps_values)
        return self.all_paths_forklifts, max_steps + 1  # para incluir a saida

    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str(self.genome) + "\n\n"
        string += '\nWorst Fitness ' + str(self.problem.agent_search.worst_global_weight) + "\n\n"
        string += 'Forklifts Path: \n\n'

        i = 0
        for forklift in self.forklifts_and_products.values():
            for index in range(len(forklift)):
                if index < len(forklift) - 1:
                    string += f"{forklift[index]} -> "
                else:
                    string += "S \n\n"
            string += 'Steps: ' + str(self.steps_values[i]) + '\n\n'
            i += 1
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        new_instance.weight = self.weight
        new_instance.worst_value = self.worst_value
        new_instance.all_paths_forklifts = self.all_paths_forklifts
        new_instance.forklifts_and_products = self.forklifts_and_products
        new_instance.steps_values = self.steps_values
        # TODO done
        return new_instance
