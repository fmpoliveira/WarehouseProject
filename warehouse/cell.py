class Cell:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return False
        return self.line == other.line and self.column == other.column

    def compareWithReversedCells(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return False
        return (self.line == other.line and self.column == other.column) or (self.line == other.column and self.column == other.line)

    def __str__(self) -> str:
        return f"{self.line}-{self.column}"