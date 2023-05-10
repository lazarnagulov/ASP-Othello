class Player(object):
    WHITE = "W"
    BLACK = "B"
    EMPTY = "."
    
    @staticmethod
    def get_opponent(player):
        return Player.BLACK if player == Player.WHITE else Player.WHITE

class Board(object):
    DIRECTIONS: list = [(0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
    SIZE: int = 8    

    def __init__(self):
        self._board: list[list[Player]] = [[Player.EMPTY for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        self._possible_moves: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self._current_player: Player = Player.BLACK
        
        self._board[3][3] = Player.WHITE
        self._board[3][4] = Player.BLACK
        self._board[4][4] = Player.WHITE
        self._board[4][3] = Player.BLACK
        
    def __str__(self):
        board: str = ""
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                board += self._board[i][j]
            board += "\n"
        return board

    def __is_inside_board(self, move: tuple[int, int]) -> bool:
        return (move[0] >= 0 and move[0] < Board.SIZE) and (move[1] >= 0 and move[1] < Board.SIZE)
        
    def get_moves(self):
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if self.get_board_value((x,y)) == self._current_player:
                    self.__get_possible_moves((x,y))
        
        moves: list[tuple[int, int]] = []
        for move in self._possible_moves:
            moves.append(move)
            
        return moves
    
    def play(self, move):
        if not self._possible_moves.get(move):
            return
        print(self._possible_moves)
        print(self._possible_moves[move])
        self.set_board_value(move, self._current_player)
        for x,y in self._possible_moves[move]:
            self.set_board_value((x,y), self._current_player)
        
        self._possible_moves.clear()        
        self._current_player = Player.get_opponent(self._current_player)        
    
    def __get_possible_moves(self, move: tuple): 
        for direction in Board.DIRECTIONS:
            opponents: list[tuple[int, int]] = self.__get_opponents(move, direction)

                            
    def __get_opponents(self, move: tuple, direction: tuple) -> list[tuple[int, int]]:
        opponents: list[tuple[int, int]] = []
        current_position: list[int, int] = [move[0] + direction[0], move[1] + direction[1]]
        while self.__is_inside_board(current_position):
            if self.get_board_value(current_position) == Player.get_opponent(self._current_player):
                opponents += [tuple(current_position)]
            elif self.get_board_value(current_position) == Player.EMPTY and opponents != []:
                self._possible_moves[tuple(current_position)] = opponents
                return opponents
            else:
                return opponents
            
            
            current_position[0] += direction[0]
            current_position[1] += direction[1]

        
        return opponents            
   
        
    def get_board_value(self, coords: tuple[int, int]) -> str:
        return self._board[coords[0]][coords[1]]
    
    def set_board_value(self, coords: tuple[int, int], value: Player):
        self._board[coords[0]][coords[1]] = value