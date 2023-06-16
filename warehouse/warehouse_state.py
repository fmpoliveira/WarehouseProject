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
        # TODO done
        self.goal = None
        self.forklift = None
        self.exit = None

        self.rows = rows
        self.columns = columns
        self.matrix = np.copy(matrix).astype(int)

        self.line_forklift = None
        self.column_forklift = None
        self.line_exit = None
        self.column_exit = None

    def can_move_right(self) -> bool:
        # TODO done
        if self.forklift.column + 1 >= self.columns:
            return False
        if self.matrix[self.forklift.line][self.forklift.column + 1] == constants.EMPTY:
            return True
        if self.matrix[self.forklift.line][self.forklift.column + 1] == constants.EXIT:
            return True

        return False

    def can_move_up(self) -> bool:
        # TODO done
        if self.forklift.line - 1 >= self.rows:
            return False
        if self.matrix[self.forklift.line - 1][self.forklift.column] == constants.EMPTY:
            return True
        if self.matrix[self.forklift.line - 1][self.forklift.column] == constants.EXIT:
            return True

        return False

    def can_move_down(self) -> bool:
        # TODO done
        if self.forklift.line + 1 >= self.rows:
            return False
        if self.matrix[self.forklift.line + 1][self.forklift.column] == constants.EMPTY:
            return True
        if self.matrix[self.forklift.line + 1][self.forklift.column] == constants.EXIT:
            return True

        return False

    def can_move_left(self) -> bool:
        # TODO done
        if self.forklift.column - 1 >= self.columns:
            return False
        if self.matrix[self.forklift.line][self.forklift.column - 1] == constants.EMPTY:
            return True
        if self.matrix[self.forklift.line][self.forklift.column - 1] == constants.EXIT:
            return True

        return False

    def move_up(self) -> None:
        # TODO done
        if self.can_move_up():
            self.matrix[self.forklift.line][self.forklift.column] = self.matrix[self.forklift.line - 1][
                self.forklift.column]
            self.set_forklift(self.forklift.line - 1, self.forklift.column)
            self.matrix[self.forklift.line][self.forklift.column] = constants.FORKLIFT

    def move_right(self) -> None:
        # TODO done
        if self.can_move_right():
            self.matrix[self.forklift.line][self.forklift.column] = self.matrix[self.forklift.line][
                self.forklift.column + 1]
            self.set_forklift(self.forklift.line, self.forklift.column + 1)
            self.matrix[self.forklift.line][self.forklift.column] = constants.FORKLIFT

    def move_down(self) -> None:
        # TODO done
        if self.can_move_down():
            self.matrix[self.forklift.line][self.forklift.column] = self.matrix[self.forklift.line + 1][
                self.forklift.column]
            self.set_forklift(self.forklift.line + 1, self.forklift.column)
            self.matrix[self.forklift.line][self.forklift.column] = constants.FORKLIFT

    def move_left(self) -> None:
        # TODO done
        if self.can_move_left():
            self.matrix[self.forklift.line][self.forklift.column] = self.matrix[self.forklift.line][
                self.forklift.column - 1]
            self.set_forklift(self.forklift.line, self.forklift.column - 1)
            self.matrix[self.forklift.line][self.forklift.column] = constants.FORKLIFT

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
            constants.EMPTY: constants.COLOREMPTY,
            constants.EXIT: constants.COLOREXIT
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
        self.line_forklift = line
        self.column_forklift = column

    def set_exit(self, line, column):
        self.exit = Cell(line, column)
        self.line_exit = line
        self.column_forklift = column

    def set_goal(self, line, column):
        self.goal = Cell(line, column)
