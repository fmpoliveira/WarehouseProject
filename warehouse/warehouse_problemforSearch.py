
import copy

import constants
from agentsearch.problem import Problem
from warehouse.actions import *
from warehouse.cell import Cell
from warehouse.warehouse_state import WarehouseState


class WarehouseProblemSearch(Problem[WarehouseState]):

    def __init__(self, initial_state: WarehouseState, goal_position: Cell):
        super().__init__(initial_state)
        self.actions = [ActionDown(), ActionUp(), ActionRight(), ActionLeft()]
        self.goal_position = goal_position

    def get_actions(self, state: WarehouseState) -> list:
        valid_actions = []
        for action in self.actions:
            if action.is_valid(state):
                #print("Entrou no action is_valid")
                #print(action)
                valid_actions.append(action)
        return valid_actions

    def get_successor(self, state: WarehouseState, action: Action) -> WarehouseState:
        successor = copy.deepcopy(state)
        action.execute(successor)
        return successor

    def is_goal(self, state: WarehouseState) -> bool:
        # TODO
       # print(state.forklift.line, state.forklift.column)
       # print(self.goal_position)

        if state.forklift.line + 1 < state.rows or state.forklift.column + 1 < state.columns:
            if state.forklift.line == self.goal_position.line and state.forklift.column == self.goal_position.column:
                #print("Goal Position")
                #print("************")
                return True
            else:
                #print("False")
                #print("************")
                return False
        return False
        #print("Falhou o IF")
        #print("************")




        # Se for saida, o forklift tem de estar em cima. Se for objetivo, tem de estar ao lado
        #state self.lineforklift == ???
        #goal = self.goal_position
        #if state.matrix[self.goal_position.line, self.goal_position.column] == constants.EXIT:
         #   return True
        #if state.forklift == self.goal_position:
         #   return True

        #return False

