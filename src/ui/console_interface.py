from models.player import Player
from models.board_symbol import BoardSymbol, get_symbol
from models.game_result import GameResult
from game.board import Board

from .user_interface import UserInterface

class ConsoleInterface(UserInterface):
    
    def display_current_player(board, current_player: Player) -> None:
        print(f"Current player: {get_symbol(current_player)}")
   
    def display_score(board, white_tiles: int, black_tiles: int) -> None:
        print(f"{get_symbol(Player.WHITE)}: {white_tiles} - {get_symbol(Player.BLACK)}: {black_tiles}")
        
    def display_board(self, board: Board, legal_moves: dict[tuple[int, int], list[tuple[int, int]]]) -> None:
        string_board: str = "# "
        for i in range(Board.SIZE):
            string_board += str(i) + " "
        string_board += "\n"
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if y == 0:
                    string_board += str(x) + " "
                occupied: int = board.is_occupied( (x,y))
                if occupied:
                    color: int = board.get_tile_color((x,y))
                    if color == Player.WHITE:
                        string_board += BoardSymbol.WHITE + " "
                    else:
                        string_board += BoardSymbol.BLACK + " "
                elif (x,y) in legal_moves:
                    string_board += BoardSymbol.LEGAL_MOVE + " "
                else:
                    string_board += BoardSymbol.EMPTY + " "
            string_board += "\n"

        print(string_board)
    
    def display_result(self, result: GameResult) -> None: ...
        