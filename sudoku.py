class Cell:
    """One individual cell on the Sudoku board"""

    def __init__(self, column_number, row_number, number, game):
        # Whether or not to include the cell in the backtracking
        self.solved = True if number > 0 else False
        self.number = number  # the current value of the cell
        # Which numbers the cell could potentially be
        self.possibilities = set(range(1, 10)) if not self.solved else []
        self.row = row_number  # the index of the row the cell is in
        self.column = column_number  # the index of the column the cell is in
        self.current_index = 0  # the index of the current possibility
        self.game = game  # the sudoku game the cell belongs to
        if not self.solved:  # runs the possibility checker
            self.find_possibilities()

    def check_area(self, area):
        """Checks to see if the cell's current value is a valid sudoku move"""
        values = [item for item in area if item != 0]
        return len(values) == len(set(values))

    def set_number(self):
        """changes the number attribute and also changes the cell's value in the larger puzzle"""
        if not self.solved:
            self.number = self.possibilities[self.current_index]
            self.game.puzzle[self.row][self.column] = self.possibilities[self.current_index]

    def handle_one_possibility(self):
        """If the cell only has one possibility, set the cell to that value and mark it as solved"""
        if len(self.possibilities) == 1:
            self.solved = True
            self.set_number()

    def find_possibilities(self):
        """filter the possible values for the cell"""
        for item in self.game.get_row(self.row) + self.game.get_column(self.column) + self.game.get_box(self.row, self.column):
            if not isinstance(item, list) and item in self.possibilities:
                self.possibilities.remove(item)
        self.possibilities = list(self.possibilities)
        self.handle_one_possibility()

    def is_valid(self):
        """checks to see if the current number is valid in its row, column, and box"""
        for unit in [self.game.get_row(self.row), self.game.get_column(self.column), self.game.get_box(self.row, self.column)]:
            if not self.check_area(unit):
                return False
        return True

    def increment_value(self):
        """move number to the next possibility while the current number is invalid and there are possibilities left"""
        while not self.is_valid() and self.current_index < len(self.possibilities) - 1:
            self.current_index += 1
            self.set_number()


class SudokuSolver:
    """contains logic for solving a sudoku puzzle -- even very difficult ones using a backtracking algorithm"""

    def __init__(self, puzzle):
        self.puzzle = puzzle  # the 2d list of spots on the board
        self.solve_puzzle = []  # 1d list of the Cell objects
        # the size of the boxes within the puzzle -- 3 for a typical puzzle
        self.box_size = int(len(self.puzzle) ** .5)
        self.backtrack_coord = 0  # what index the backtracking is currently at

    def get_row(self, row_number):
        """Get the full row from the puzzle based on the row index"""
        return self.puzzle[row_number]

    def get_column(self, column_number):
        """Get the full column"""
        return [row[column_number] for row in self.puzzle]

    def find_box_start(self, coordinate):
        """Get the start coordinate for the small sudoku box"""
        return coordinate // self.box_size * self.box_size

    def get_box_coordinates(self, row_number, column_number):
        """Get the numbers of the small sudoku box"""
        return self.find_box_start(column_number), self.find_box_start(row_number)

    def get_box(self, row_number, column_number):
        """Get the small sudoku box for an x and y coordinate"""
        start_y, start_x = self.get_box_coordinates(row_number, column_number)
        box = []
        for i in range(start_x, self.box_size + start_x):
            box.extend(self.puzzle[i][start_y:start_y+self.box_size])
        return box

    def initialize_board(self):
        """create the Cells for each item in the puzzle and get its possibilities"""
        for row_number, row in enumerate(self.puzzle):
            for column_number, item in enumerate(row):
                self.solve_puzzle.append(
                    Cell(column_number, row_number, item, self))

    def move_forward(self):
        """Move forwards to the next cell"""
        while self.backtrack_coord < len(self.solve_puzzle) - 1 and self.solve_puzzle[self.backtrack_coord].solved:
            self.backtrack_coord += 1

    def backtrack(self):
        """Move forwards to the next cell"""
        self.backtrack_coord -= 1
        while self.solve_puzzle[self.backtrack_coord].solved:
            self.backtrack_coord -= 1

    def set_cell(self):
        """Set the current cell to work on"""
        cell = self.solve_puzzle[self.backtrack_coord]
        cell.set_number()
        return cell

    def reset_cell(self, cell):
        """set a cell back to zero"""
        cell.current_index = 0
        cell.number = 0
        self.puzzle[cell.row][cell.column] = 0

    def decrement_cell(self, cell):
        """runs the backtracking algorithm"""
        while cell.current_index == len(cell.possibilities) - 1:
            self.reset_cell(cell)
            self.backtrack()
            cell = self.solve_puzzle[self.backtrack_coord]
        cell.current_index += 1

    def change_cells(self, cell):
        """move forwards or backwards based on the validity of a cell"""
        if cell.is_valid():
            self.backtrack_coord += 1
        else:
            self.decrement_cell(cell)

    def solve(self):
        """run the other functions necessary for solving the sudoku puzzle"""
        self.move_forward()
        cell = self.set_cell()
        cell.increment_value()
        self.change_cells(cell)

    def run_solve(self):
        """runs the solver until we are at the end of the puzzle"""
        while self.backtrack_coord <= len(self.solve_puzzle) - 1:
            self.solve()


def solve(puzzle):
    solver = SudokuSolver(puzzle)
    solver.initialize_board()
    solver.run_solve()
    return solver.puzzle


puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

print(solve(puzzle))

solution = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]]
