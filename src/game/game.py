from game.board import Board
from typing import Optional
from models.board_symbol import BoardSymbol, get_symbol
from models.game_results import GameResult
from models.player import Player, get_opponent
import util.matrix as Matrix

class Game:
    """Othello game static class. It stores all possible moves, current player and number of tiles for each player.
    """    
    legal_moves: dict[tuple[int, int], list[tuple[int, int]]] = {}
    current_player: Player = Player.BLACK
    black_tiles: int = 2
    white_tiles: int = 2
    
    @staticmethod
    def get_moves(board: Board, player: Player) -> dict[tuple[int, int], list[tuple[int, int]]]:
        """Gets all possible moves for player.

        Args:
            board (Board): board
            player (Player): player

        Returns:
            dict[tuple[int, int], list[list[Player]]]: All possible moves (position) : [opponents]
        """
        moves: dict[tuple[int,int],list[tuple[int,int]]] = {}
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                opponents: list[tuple[int, int]] = Game.__is_legal_move(board, player, (x,y))
                if opponents:
                    moves[(x,y)] = opponents
        
        return moves
        
    @staticmethod
    def __is_inside_board(position: tuple[int, int]) -> bool:
        """Checks if position is inside of board

        Args:
            position (tuple[int, int]): position (row, column)

        Returns:
            bool: True if position is inside, False if it is not.
        """
        return (position[0] >= 0 and position[0] < Board.SIZE) and (position[1] >= 0 and position[1] < Board.SIZE)
    
    @staticmethod
    def __get_opponents_in_dir(board: Board, player: Player, position: tuple[int, int], direction: tuple[int, int]) -> list[tuple[int, int]]:
        """Gets all opponents in direction

        Args:
            board (Board): board
            player (Player): player
            position (tuple[int, int]): position (row, column)
            direction (tuple[int, int]): direction - Matrix.DIRECTIONS

        Returns:
            list[tuple[int, int]]: list of all opponents and their position
        """
        opponents: list[tuple[int, int]] = []
        current_position: tuple[int, int] = (position[0] + direction[0], position[1] + direction[1])
        opponent: Player = get_opponent(player)

        while Game.__is_inside_board(current_position) and board.is_occupied(current_position):
            if board.get_tile_color(current_position) == opponent:
                opponents += [current_position]
                current_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            else:
                return opponents
        
        return []

    
    @staticmethod
    def __get_opponents(board: Board, player: Player, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Gets all opponents.

        Args:
            board (Board): board
            player (Player): player
            position (tuple[int, int]): position (row, column)

        Returns:
            list[tuple[int, int]]: All opponents and their positions
        """
        opponents: list[tuple[int, int]] = []
        for direction in Matrix.DIRECTIONS:
            opps: list[tuple[int, int]] = Game.__get_opponents_in_dir(board, player, position, direction)    
            if not opps:
                continue
            opponents += opps
        return opponents        
    
    @staticmethod
    def __is_legal_move(board: Board, player: Player, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Checks if move is possible to make.

        Args:
            board (Board): board
            player (Player): player
            position (tuple[int, int]): postion (row, column)

        Returns:
            list[tuple[int, int]]: Empty list if it is not possible, list of all oppoenents if it is.
        """
        if board.is_occupied(position):
            return []
        
        return Game.__get_opponents(board, player, position)
        
    @staticmethod
    def has_ended(board: Board) -> bool:
        if Game.get_moves(board, Player.BLACK) == {}:
            return True
        elif Game.get_moves(board, Player.WHITE) == {}:
            return True
        
        return False
    
    @staticmethod
    def print_status(board: Board):
        Game.__print_current_player()
        Game.__print_score()
        Game.__print_board(board)
    
    @staticmethod
    def get_winner() -> GameResult:
        """Gets winner if the game has ended.

        Returns:
            GameResult: Game result
        """
        if Game.white_tiles > Game.black_tiles:
            return GameResult.WHITE_WINS
        elif Game.white_tiles < Game.black_tiles:
            return GameResult.BLACK_WINS
        elif Game.white_tiles == Game.black_tiles:
            return GameResult.DRAW
        return GameResult.NO_WINNER
    
    @staticmethod
    def play(board: Board, player: Player, position: tuple[int, int], legal_moves: Optional[dict[tuple[int, int], list[tuple[int, int]]]] = None, bot: bool = False) -> bool:
        """Play a turn.

        Args:
            board (Board): board
            player (Player): player
            position (tuple[int, int]): position (row, column)
            legal_moves (dict[tuple[int, int], list[tuple[int, int]]], optional): Legal moves. Defaults to Game.legal_moves.
            bot (bool): True if bot calls method. Defaults to False
        Returns:
            bool: True if move is possible to make, False if it is not
        """
        if not legal_moves:
            legal_moves = Game.legal_moves
        if position not in legal_moves:
            print("Cannot make that move!")
            return False
        
        board.set_tile(position, player)
        for opponent in legal_moves[position]:
            board.replace_opponent(opponent)
        
        if not bot:
            if player == Player.BLACK:
                Game.black_tiles += 1 + len(legal_moves[position])
                Game.white_tiles -= len(legal_moves[position])
            else:
                Game.black_tiles -= len(legal_moves[position])
                Game.white_tiles += 1 + len(legal_moves[position])

        return True

    @staticmethod
    def get_board_score(board: Board, player: Player) -> float:
        """Calculate board score.

        Args:
            board (Board): board
            player (Player): player

        Returns:
            float: score
        """
        opponent: Player = get_opponent(player)
        player_tiles: int = 0
        opponent_tiles: int = 0
        my_front_tiles: int = 0
        opp_front_tiles: int = 0
        p: float = 0
        c: float = 0
        l: float = 0
        m: float = 0
        f: float = 0
        d: float = 0

        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if board.get_tile_color((i,j)) == player:
                    d += Matrix.HEURISTIC_MATRIX[i][j]
                    player_tiles += 1
                elif board.get_tile_color((i,j)) == opponent:
                    d -= Matrix.HEURISTIC_MATRIX[i][j]
                    opponent_tiles += 1
                if board.is_occupied((i,j)):
                    for direction in Matrix.DIRECTIONS:
                        x = i + direction[0]
                        y = j + direction[1]
                        if x >= 0 and x < 8 and y >= 0 and y < 8 and not board.is_occupied((x,y)):
                            if board.get_tile_color((i, j)) == player:
                                my_front_tiles += 1
                            elif board.get_tile_color((i,j)) == opponent:
                                opp_front_tiles += 1
                            break
                        
        if player_tiles > opponent_tiles:
            p = (100.0 * player_tiles) / (player_tiles + opponent_tiles)
        elif player_tiles < opponent_tiles:
            p = -(100.0 * opponent_tiles) / (player_tiles + opponent_tiles)
        else:
            p = 0

        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0
            
        player_tiles = 0
        opponent_tiles = 0

        if board.get_tile_color((0,0)) == player:
            player_tiles += 1
        elif board.get_tile_color((0,0)) == opponent:
            opponent_tiles += 1

        if board.get_tile_color((0,7)) == player:
            player_tiles += 1
        elif board.get_tile_color((0,7)) == opponent:
            opponent_tiles += 1

        if board.get_tile_color((7,0)) == player:
            player_tiles += 1
        elif board.get_tile_color((7,0)) == opponent:
            opponent_tiles += 1

        if board.get_tile_color((7,7)) == player:
            player_tiles += 1
        elif board.get_tile_color((7,7)) == opponent:
            opponent_tiles += 1
        c = 25 * (player_tiles - opponent_tiles)

        player_tiles = 0
        opponent_tiles = 0

        if not board.is_occupied((0, 0)):
            if board.get_tile_color((0, 1)) == player:
                player_tiles += 1
            elif board.get_tile_color((0, 1)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((1, 1)) == player:
                player_tiles += 1
            elif board.get_tile_color((1, 1)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((1, 0)) == player:
                player_tiles += 1
            elif board.get_tile_color((1, 0)) == opponent:
                opponent_tiles += 1

        if not board.is_occupied((0, 7)):
            if board.get_tile_color((0, 6)) == player:
                player_tiles += 1
            elif board.get_tile_color((0, 6)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((1, 6)) == player:
                player_tiles += 1
            elif board.get_tile_color((1, 6)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((1, 7)) == player:
                player_tiles += 1
            elif board.get_tile_color((1, 7)) == opponent:
                opponent_tiles += 1

        if not board.is_occupied((7, 0)):
            if board.get_tile_color((7, 1)) == player:
                player_tiles += 1
            elif board.get_tile_color((7, 1)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((6, 1)) == player:
                player_tiles += 1
            elif board.get_tile_color((6, 1)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((6, 0)) == player:
                player_tiles += 1
            elif board.get_tile_color((6, 0)) == opponent:
                opponent_tiles += 1

        if not board.is_occupied((7, 7)):
            if board.get_tile_color((6, 7)) == player:
                player_tiles += 1
            elif board.get_tile_color((6, 7)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((6, 6)) == player:
                player_tiles += 1
            elif board.get_tile_color((6, 6)) == opponent:
                opponent_tiles += 1

            if board.get_tile_color((7, 6)) == player:
                player_tiles += 1
            elif board.get_tile_color((7, 6)) == opponent:
                opponent_tiles += 1

        l = -12.5 * (player_tiles - opponent_tiles)
        
        player_tiles = len(Game.get_moves(board, player))
        opponent_tiles = len(Game.get_moves(board, opponent))

        if player_tiles > opponent_tiles:
            m = (100.0 * player_tiles) / (player_tiles + opponent_tiles)
        elif player_tiles < opponent_tiles:
            m = -(100.0 * opponent_tiles) / (player_tiles + opponent_tiles)
        else:
            m = 0

        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
        return score

    @staticmethod
    def __print_current_player():
        """Prints current player.
        """
        print(f"Current player: {get_symbol(Game.current_player)}")

    @staticmethod
    def __print_score():
        """Prints current score.
        """
        print(f"{get_symbol(Player.WHITE)}: {Game.white_tiles} - {get_symbol(Player.BLACK)}: {Game.black_tiles}")

    @staticmethod
    def switch_player() -> None:
        """Switches current player.
        """
        Game.current_player = get_opponent(Game.current_player)
    
    @staticmethod
    def __print_board(self) -> str:
        string_board: str = "# "
        for i in range(Board.SIZE):
            string_board += str(i) + " "
        string_board += "\n"
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if y == 0:
                    string_board += str(x) + " "
                occupied: int = self.is_occupied( (x,y))
                if occupied:
                    color: int = self.get_tile_color((x,y))
                    if color == Player.WHITE:
                        string_board += BoardSymbol.WHITE + " "
                    else:
                        string_board += BoardSymbol.BLACK + " "
                elif (x,y) in Game.legal_moves:
                    string_board += BoardSymbol.LEGAL_MOVE + " "
                else:
                    string_board += BoardSymbol.EMPTY + " "
            string_board += "\n"

        print(string_board)
        