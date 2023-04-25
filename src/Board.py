class Board(object):
    
    def __init__(self):
        self._board: list[list[str]] = [["." for _ in range(8)] for _ in range(8)]
        self._board[3][3] = "W"
        self._board[3][4] = "B"
        self._board[4][4] = "W"
        self._board[4][3] = "B"
        
    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self._board[i][j] , end="")
            print()
    
    def get_board_value(self, row, column):
        return self._board[row][column]
    
    def set_board_value(self, row, column, value):
        self._board[row][column] = value