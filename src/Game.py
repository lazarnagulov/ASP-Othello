from Board import Board, BoardSymbol, Player
import Matrix

class GameResult(object):
    """Game result enumeration
    """
    WHITE_WINS = "White wins!"
    BLACK_WINS = "Black wins!"
    DRAW = "DRAW!"
    NO_WINNER = ""
    
class Game(object):
    """Othello game class.
    """    
    legal_moves: dict[tuple[int, int], list[tuple[int, int]]] = []
    current_player: Player = Player.BLACK
    black_tiles: int = 2
    white_tiles: int = 2
    
    @staticmethod
    def print_board(board: Board) -> None:
        """Prints board.

        Args:
            board (Board): board
        """
        string_board: str = "# "
        for i in range(Board.SIZE):
            string_board += str(i) + " "
        string_board += "\n"
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if y == 0:
                    string_board += str(x) + " "
                occupied: int = board.get_tile(board.occupied, (x,y))
                if occupied:
                    color: int = board.get_tile(board.color, (x,y))
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

    
    @staticmethod
    def get_moves(board: Board, player: Player) -> dict[tuple[int, int], list[list[Player]]]:
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
            position (tuple[int, int]): position

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
            position (tuple[int, int]): position
            direction (tuple[int, int]): direction

        Returns:
            list[tuple[int, int]]: list of all opponents and their position
        """
        opponents: list[tuple[int, int]] = []
        current_position: tuple[int, int] = (position[0] + direction[0], position[1] + direction[1])
        opponent: Player = Player.get_opponent(player)

        while Game.__is_inside_board(current_position) and board.get_tile(board.occupied, current_position):
            if board.get_tile(board.color, current_position) == opponent:
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
            position (tuple[int, int]): position

        Returns:
            list[tuple[int, int]]: All opponents and their postion
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
            position (tuple[int, int]): postion

        Returns:
            list[tuple[int, int]]: Empty list if it is not possible, list of all oppoenents if it is.
        """
        if board.get_tile(board.occupied, position):
            return []
        
        return Game.__get_opponents(board, player, position)
        
    
    @staticmethod
    def get_winner(legal_moves: dict[tuple[int, int], list[tuple[int, int]]] = None) -> GameResult:
        """Gets winner if the game has ended.

        Args:
            legal_moves (dict[tuple[int, int], list[tuple[int, int]]], optional): Legal moves. Defaults to Game.legal_moves.

        Returns:
            GameResult: Game result
        """
        if not legal_moves:
            legal_moves = Game.legal_moves 
        if legal_moves != {}:
            return GameResult.NO_WINNER
        if Game.white_tiles > Game.black_tiles:
            return GameResult.WHITE_WINS
        elif Game.white_tiles < Game.black_tiles:
            return GameResult.BLACK_WINS
        elif Game.white_tiles == Game.black_tiles:
            return GameResult.DRAW
        return GameResult.NO_WINNER
    
    @staticmethod
    def play(board: Board, player: Player, position: tuple[int, int], legal_moves: dict[tuple[int, int], list[tuple[int, int]]] = None) -> bool:
        """Play a turn.

        Args:
            board (Board): board
            player (Player): player
            position (tuple[int, int]): position
            legal_moves (dict[tuple[int, int], list[tuple[int, int]]], optional): Legal moves. Defaults to Game.legal_moves.

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
        
        if player == Player.BLACK:
            Game.black_tiles += 1 + len(legal_moves[position])
            Game.white_tiles -= len(legal_moves[position])
        else:
            Game.black_tiles -= len(legal_moves[position])
            Game.white_tiles += 1 + len(legal_moves[position])
            
        return True

    @staticmethod
    def get_board_score(board: Board, player: Player) -> float:
        pass

    @staticmethod
    def print_turn():
        """Prints current player.
        """
        print(f"Current player: {BoardSymbol.get_symbol(Game.current_player)}")

    @staticmethod
    def print_score():
        """Prints current score.
        """
        print(f"{BoardSymbol.get_symbol(Player.WHITE)}: {Game.white_tiles} - {BoardSymbol.get_symbol(Player.BLACK)}: {Game.black_tiles}")

    @staticmethod
    def switch_player() -> None:
        """Switches players.
        """
        Game.current_player = Player.get_opponent(Game.current_player)
        
        