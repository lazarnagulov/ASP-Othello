import copy

class Player(object):
    WHITE = "○"
    BLACK = "●"
    EMPTY = "□"
    LEGAL_MOVE = "■"
    
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
        self._current_player: Player = Player.BLACK
        self._black_tiles: int = 2
        self._white_tiles: int = 2

        self._board[3][3] = Player.WHITE
        self._board[3][4] = Player.BLACK
        self._board[4][4] = Player.WHITE
        self._board[4][3] = Player.BLACK
    
        self._legal_moves: dict[list[tuple[int, int]]] = self.__find_legal_moves(self._current_player)
        
    def __str__(self):
        board: str = "# "
        for i in range(Board.SIZE):
            board += str(i) + " "
        board += "\n"
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if j == 0:
                    board += str(i) + " "
                if (i,j) in self._legal_moves:
                    board += Player.LEGAL_MOVE + " "
                    continue
                board += self._board[i][j] + " "
            board += "\n"
        return board
    
    def __hash__(self):
        hash_in_str: str = (''.join(''.join(row) for row in self._board)).replace(Player.EMPTY, '0').replace(Player.BLACK, '1').replace(Player.WHITE, '2')
        return int(hash_in_str, 3)
    
    def __is_legal_move(self, player: Player, position: tuple[int, int]) -> bool:
        opponents: list[tuple[int, int]] = []
        if self.get_board_value(position) != Player.EMPTY:
            return (False, [])
        
        opponents = self.__get_opponents(position, player)
        return (len(opponents) > 0, opponents)
    
    def __get_opponents(self, position: tuple[int, int], player: Player) -> list[tuple[int,int]]:
        opponents: list[tuple[int, int]] = []
        for direction in Board.DIRECTIONS:
            opps: list[tuple[int, int]] = self.__get_opponents_in_direction(position, player, direction)
            if not opps:
                continue
            opponents += opps

        return opponents
            
    def __get_opponents_in_direction(self, position: tuple[int, int], player: Player, direction: tuple[int,int]) -> list[tuple[int, int]]:
        opponents: list[tuple[int, int]] = []
        current_position = (position[0] + direction[0], position[1] + direction[1])
        opponent: Player = Player.get_opponent(player)
        
        while self.__is_inside_board(current_position) and self.get_board_value(current_position) != Player.EMPTY:
            if self.get_board_value(current_position) == opponent:
                opponents += [current_position] 
                current_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            else:
                return opponents
        return []

    def __is_inside_board(self, move: tuple[int, int]) -> bool:
        return (move[0] >= 0 and move[0] < Board.SIZE) and (move[1] >= 0 and move[1] < Board.SIZE)
    
    def __find_legal_moves(self, player: Player) -> dict[list[tuple[int, int]]]:
        moves: dict[list[tuple[int, int]]] = {}
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                is_legal = self.__is_legal_move(player, (i,j))
                if is_legal[0]:
                    moves[(i,j)] = is_legal[1]

        return moves
    
    def get_heuristic(self, board: list[list[str]]) -> float:
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
        
        temp = self._legal_moves
        
        player_tiles = len(temp)
        opponent_tiles = len(self.get_moves(opponent))
        
        self._legal_moves = temp
        
        if player_tiles > opponent_tiles:
            score_mobility = (100.0 * player_tiles)/(player_tiles + opponent_tiles)
        elif player_tiles < opponent_tiles:
            score_mobility = -(100.0 * player_tiles)/(player_tiles + opponent_tiles)
        else:
            score_mobility = 0
        
        return 10 * score_parity + 801.724 * score_corner + 382.026 * score_corcer_closeness + 78.922 * score_mobility + 74.396 * score_frontier + 10 * score
    
    def get_moves(self, player: Player) -> dict[tuple[int, int], list[list[Player]]]:
        moves_dict: dict[list[tuple[int,int]]] = self.__find_legal_moves(player)       

        self._legal_moves.clear()
        self._legal_moves = moves_dict

        return moves_dict
    
    def deepcopy(self):
        return copy.deepcopy(self)
    
    def print_score(self) -> str:
        return f"{Player.WHITE}: {self._white_tiles} - {Player.BLACK}: {self._black_tiles}"
    
    def switch_players(self) -> None:
        self._legal_moves.clear()
        self._current_player = Player.get_opponent(self._current_player)
        
    def get_board_value(self, coords: tuple[int, int]) -> str:
        return self._board[coords[0]][coords[1]]
    
    def set_board_value(self, coords: tuple[int, int], value: Player):
        self._board[coords[0]][coords[1]] = value