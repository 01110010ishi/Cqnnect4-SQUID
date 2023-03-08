class Board:

    def __init__(self):
        self.ROWS = 6
        self.COLUMNS = 7
        self._grid = []
        self.clear()
        self.four = None

    # Clear the board
    def clear(self):
        self._grid = [[None for i in range(self.COLUMNS)] for j in range(self.ROWS)]

        # Check in all directions if a player has won (4 connected)

    def check_player_wins(self, player):

        # Check horizontal
        for c in range(self.COLUMNS - 3):
            for r in range(self.ROWS):
                if self._grid[r][c] == player and self._grid[r][c + 1] == player and self._grid[r][c + 2] == player and \
                        self._grid[r][c + 3] == player:
                    self.four = 'horizontal'
                    return True

        # Check vertical
        for c in range(self.COLUMNS):
            for r in range(self.ROWS - 3):
                if self._grid[r][c] == player and self._grid[r + 1][c] == player and self._grid[r + 2][c] == player and \
                        self._grid[r + 3][c] == player:
                    self.four = 'vertical'
                    return True

        # Check positive diagonal
        for c in range(self.COLUMNS - 3):
            for r in range(self.ROWS - 3):
                if self._grid[r][c] == player and self._grid[r + 1][c + 1] == player and self._grid[r + 2][
                    c + 2] == player and self._grid[r + 3][c + 3] == player:
                    self.four = 'diagonal+'
                    return True

        # Check negative diagonal
        for c in range(self.COLUMNS - 3):
            for r in range(3, self.ROWS):
                if self._grid[r][c] == player and self._grid[r - 1][c + 1] == player and self._grid[r - 2][
                    c + 2] == player and self._grid[r - 3][c + 3] == player:
                    self.four = 'diagonal-'
                    return True

        return False

    # A player adds a new chip to a column of the board
    # The first free row is calculated, if the column is
    # full -1 is returns, otherwise the row to which the
    # chip has been added
    def add_chip(self, player, column):
        for row in range(self.ROWS):
            cell_value = self._grid[row][column - 1]
            if cell_value is None:
                self._grid[row][column - 1] = player
                print('now adding chip')
                return row
        return -1

    def remove_qpiece(self, col, row):
        self._grid[row][col - 1] = None
