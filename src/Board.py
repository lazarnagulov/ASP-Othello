import copy
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
    HEURISTIC_MATRIX: list[list[int]] = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]

    def __init__(self):
        self._board: list[list[Player]] = [[Player.EMPTY for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        self._possible_moves: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self._current_player: Player = Player.BLACK
        self._black_tiles: int = 2
        self._white_tiles: int = 2

        self._board[3][3] = Player.WHITE
        self._board[3][4] = Player.BLACK
        self._board[4][4] = Player.WHITE
        self._board[4][3] = Player.BLACK
    
    def __str__(self):
        board: str = ""
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                board += self._board[i][j] + " "
            board += "\n"
        return board

    def __is_inside_board(self, move: tuple[int, int]) -> bool:
        return (move[0] >= 0 and move[0] < Board.SIZE) and (move[1] >= 0 and move[1] < Board.SIZE)
        
    def get_moves(self):
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if self._board[x][y] == self._current_player:
                    self.__get_possible_moves((x,y))
        # for pos in self._current_player_postions:
        #     self.__get_possible_moves(pos)
            
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
        for x, y in self._possible_moves[move]:
            self.set_board_value((x,y), self._current_player)
        
        if self._current_player == Player.BLACK:
            self._black_tiles += 1 + len(self._possible_moves[move])
            self._white_tiles -= len(self._possible_moves[move])
        else:
            self._black_tiles -= len(self._possible_moves[move])
            self._white_tiles += 1 + len(self._possible_moves[move])
        
        self._possible_moves.clear()        
        self._current_player = Player.get_opponent(self._current_player)        
    
    def __get_possible_moves(self, move: tuple): 
        for direction in Board.DIRECTIONS:
            self.__get_opponents(move, direction)

                            
    def __get_opponents(self, move: tuple, direction: tuple) -> list[tuple[int, int]]:
        opponents: list[tuple[int, int]] = []
        current_position: list[int, int] = [move[0] + direction[0], move[1] + direction[1]]
        while self.__is_inside_board(current_position):
            if self.get_board_value(current_position) == Player.get_opponent(self._current_player):
                opponents += [tuple(current_position)]
            elif self.get_board_value(current_position) == Player.EMPTY and opponents != []:
                self._possible_moves[tuple(current_position)] = opponents
                return 
            else:
                return 
            current_position[0] += direction[0]
            current_position[1] += direction[1]
        
        return
   
    def __get_heuristic(self, board: list[list[str]]) -> float:
        player_tiles: int = 0
        opponent_tiles: int = 0
        
        player_front: int = 0
        opponent_front: int = 0
        
        player = self._current_player
        opponent = Player.get_opponent(self._current_player)
        
        score_parity: float = 0
        score_frontier: float = 0
        score_corner: float = 0
        score_corcer_closeness: float = 0
        score_mobility: float = 0
        score: float = 0
        
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if board[i][j] == player:
                    player_tiles += 1
                    score += Board.HEURISTIC_MATRIX[i][j]
                elif board[i][j] == opponent:
                    opponent_tiles += 1
                    score -= Board.HEURISTIC_MATRIX[i][j]
                if board[i][j] != Player.EMPTY:
                    for direction in Board.DIRECTIONS:
                        x, y = i + direction[0], j + direction[1]
                        if self.__is_inside_board((x,y)) and board[x][y] == Player.EMPTY:
                            if board[i][j] == player:
                                player_front += 1
                            else:
                                opponent_front += 1
                            break
       
        if player_tiles > opponent_tiles:
            score_parity = (100.0 * player_tiles)/(player_tiles + opponent_tiles)
        elif player_tiles < opponent_tiles:
            score_parity = -(100.0 * player_tiles)/(player_tiles + opponent_tiles)
        else:
            score_parity = 0

        if player_front > opponent_front:
            score_frontier = (100.0 * player_front)/(player_front + opponent_front)
        elif player_front < opponent_front:
            score_frontier = -(100.0 * player_front)/(player_front + opponent_front)
        else:
            score_frontier = 0
        
        player_tiles = opponent_tiles = 0
        if board[0][0] == player:
            player_tiles += 1
        elif board[0][0] == opponent:
            opponent_tiles += 1
        if board[0][7] == player:
            player_tiles += 1
        elif board[0][7] == opponent:
            opponent_tiles += 1
        if board[7][0] == player:
            player_tiles += 1
        elif board[7][0] == opponent:
            opponent_tiles += 1
        if board[7][7] == player:
            player_tiles += 1
        elif board[7][7] == opponent:
            opponent_tiles += 1
        score_corner = 25 * (player_tiles - opponent_tiles)
        
        player_tiles = opponent_tiles = 0
        if board[0][0] == Player.EMPTY:
            if board[0][1] == player:
                player_tiles += 1
            elif board[0][1] == opponent:
                opponent_tiles += 1
            if board[1][1] == player:
                player_tiles += 1
            elif board[1][1] == opponent:
                opponent_tiles += 1
            if board[1][0] == player:
                player_tiles += 1
            elif board[1][0] == opponent:
                opponent_tiles += 1
                
        if board[0][7] == Player.EMPTY:
            if board[0][6] == player:
                player_tiles += 1
            elif board[0][6] == opponent:
                opponent_tiles += 1
            if board[1][6] == player:
                player_tiles += 1
            elif board[1][6] == opponent:
                opponent_tiles += 1
            if board[1][7] == player:
                player_tiles += 1
            elif board[1][7] == opponent:
                opponent_tiles += 1
        
        if board[7][0] == Player.EMPTY:
            if board[7][1] == player:
                player_tiles += 1
            elif board[7][1] == opponent:
                opponent_tiles += 1
            if board[6][1] == player:
                player_tiles += 1
            elif board[6][1] == opponent:
                opponent_tiles += 1
            if board[6][0] == player:
                player_tiles += 1
            elif board[6][0] == opponent:
                opponent_tiles += 1
        
        if board[7][7] == Player.EMPTY:
            if board[6][7] == player:
                player_tiles += 1
            elif board[6][7] == opponent:
                opponent_tiles += 1
            if board[6][6] == player:
                player_tiles += 1
            elif board[6][6] == opponent:
                opponent_tiles += 1
            if board[7][6] == player:
                player_tiles += 1
            elif board[7][6] == opponent:
                opponent_tiles += 1
        score_corcer_closeness = -12.5 * (player_tiles - opponent_tiles)
        
        if self._possible_moves == []:
            player_tiles = len(self.get_moves())
        else:
            player_tiles = len(self._possible_moves)
            
        self.switch_players()
        opponent_tiles = len(self.get_moves())
        self.switch_players()
        
        if player_tiles > opponent_tiles:
            score_mobility = (100.0 * player_tiles)/(player_tiles + opponent_tiles)
        elif player_tiles < opponent_tiles:
            score_mobility = -(100.0 * player_tiles)/(player_tiles + opponent_tiles)
        else:
            score_mobility = 0
        
        return 10 * score_parity + 801.724 * score_corner + 382.026 * score_corcer_closeness + 78.922 * score_mobility + 74.396 * score_frontier + 10 * score
        
    def board_copy(self):
        return [[i for i in row] for row in self._board]
        
    def switch_players(self) -> None:
        self._current_player = Player.get_opponent(self._current_player)
        
    def get_board_value(self, coords: tuple[int, int]) -> str:
        return self._board[coords[0]][coords[1]]
    
    def set_board_value(self, coords: tuple[int, int], value: Player):
        self._board[coords[0]][coords[1]] = value