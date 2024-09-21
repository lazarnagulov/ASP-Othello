from models.game_result import GameResult
from models.player import Player
from game.board import Board

from .user_interface import UserInterface

class GUI(UserInterface):
    def display_current_player(self, current_player: Player) -> None: 
        return None
    def display_score(board, white_tiles: int, black_tiles: int) -> None: 
        return None
    def display_board(self, board: Board, legal_moves: dict[tuple[int, int], list[tuple[int, int]]]) -> None: 
        return None
    
    def display_result(self, result: GameResult) -> None: 
        return None
