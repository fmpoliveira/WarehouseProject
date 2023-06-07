import random

from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual
import numpy as np


class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        # TODO
        self.forklifts = agent_search.forklifts
        self.products = agent_search.products
        self.agent_search = agent_search
        self.minDistance = 1000000

    def generate_individual(self) -> "WarehouseIndividual":
        # TODO
        length_individual = (len(self.forklifts) + len(self.products)) - 1
        new_individual = WarehouseIndividual(self, length_individual)
        while len(new_individual.genome) != length_individual:
            # We start on 1 until length_individual, but when we starr the search for the object we will subtract 1 to the number
            rand_num = random.randint(1, length_individual)
            if rand_num not in new_individual.genome:
                new_individual.genome.append(rand_num)
        return new_individual

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

