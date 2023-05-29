import constants
from agentsearch.heuristic import Heuristic
from warehouse.cell import Cell
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()
        self._lines_goal_matrix = None
        self._cols_goal_matrix = None

    def compute(self, state: WarehouseState) -> float:
        # TODO
        goal_position = state.goal
        forklift_position = state.forklift
        return abs(goal_position.column - forklift_position.column) + abs(goal_position.line - forklift_position.line)


    def __str__(self):
        return "# TODO"

