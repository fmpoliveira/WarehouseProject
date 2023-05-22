import constants
from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()
        self._lines_goal_matrix = None
        self._cols_goal_matrix = None

    def compute(self, state: WarehouseState) -> float:
        # TODO
        h = 0
        for i in range(state.rows):
            for j in range(state.columns):
                # Blank is ignored so that the heuristic is admissible
                if state.matrix[i][j] != 0:
                    #h += abs(i - self._lines_goal_matrix[state.matrix[i][j]]) + abs(j - self._cols_goal_matrix[state.matrix[i][j]])
                    h += 1
                    #print("h= " + h)
        return h

    def __str__(self):
        return "# TODO"

