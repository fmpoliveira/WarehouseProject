import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action
from warehouse.cell import Cell


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()
        #TODO
        self.goal = None
        self.forklift = None
        self.exit = None

        self.rows = rows
        self.columns = columns
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)

        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == constants.FORKLIFT:
                    self.line_forklift = i
                    self.column_forklift = j
                if self.matrix[i][j] == constants.EXIT:
                    self.line_exit = i
                    self.column_exit = j

    def can_move_up(self) -> bool:
        # TODO
        if self.line_forklift - 1 >= self.rows:
            return False

        return self.matrix[self.line_forklift - 1][self.column_forklift] == constants.EMPTY

    def can_move_right(self) -> bool:
        # TODO
        if self.column_forklift + 1 >= self.columns:
            return False

        return self.matrix[self.line_forklift][self.column_forklift + 1] == constants.EMPTY

    def can_move_down(self) -> bool:
        # TODO
        if self.line_forklift + 1 >= self.rows:
            return False

        return self.matrix[self.line_forklift + 1][self.column_forklift] == constants.EMPTY

    def can_move_left(self) -> bool:
        # TODO
        if self.column_forklift - 1 >= self.columns:
            return False

        return self.matrix[self.line_forklift][self.column_forklift - 1] == constants.EMPTY

    def move_up(self) -> None:
        # TODO
        if self.can_move_up():
            self.matrix[self.line_forklift][self.column_forklift] = self.matrix[self.line_forklift - 1][self.column_forklift]
            self.line_forklift -= 1
            self.matrix[self.line_forklift][self.column_forklift] = 0

    def move_right(self) -> None:
        # TODO
        if self.can_move_right():
            self.matrix[self.line_forklift][self.column_forklift] = self.matrix[self.line_forklift][self.column_forklift + 1]
            self.column_forklift += 1
            self.matrix[self.line_forklift][self.column_forklift] = 0

    def move_down(self) -> None:
        # TODO
        if self.can_move_down():
            self.matrix[self.line_forklift][self.column_forklift] = self.matrix[self.line_forklift + 1][self.column_forklift]
            self.line_forklift += 1
            self.matrix[self.line_forklift][self.column_forklift] = 0

    def move_left(self) -> None:
        # TODO
        if self.can_move_left():
            self.matrix[self.line_forklift][self.column_forklift] = self.matrix[self.line_forklift][self.column_forklift - 1]
            self.column_forklift -= 1
            self.matrix[self.line_forklift][self.column_forklift] = 0

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.line_forklift or column != self.column_forklift):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())

    def set_forklift(self, line, column):
        self.forklift = Cell(line, column)

    def set_exit(self, line, column):
        self.exit = Cell(line, column)

    def set_goal(self, line, column):
        self.goal = Cell(line, column)
