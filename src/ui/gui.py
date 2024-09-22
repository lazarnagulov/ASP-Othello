from enums.game_result import GameResult
from enums.player import Player
from enums.color import Color, get_color

from ui.component.game_window import GameWindow
from ui.user_interface import UserInterface
from models.board import Board
from game.game import Game

import sys

from PyQt5.QtWidgets import (
    QApplication, 
    QMessageBox
)

class GUI(UserInterface):    

    def __init__(self) -> None:        
        self.app: QApplication = QApplication(sys.argv)      
        self.window = GameWindow()
        
    def run(self) -> None:
        self.window.show()
        sys.exit(self.app.exec_())
         
    def display_current_player(self, current_player: Player) -> None: 
        self.current_player.setText(f"Current player: {current_player.name}")
    
    def display_score(self, white_tiles: int, black_tiles: int) -> None: 
        self.current_score.setText(f"Score - Black: {black_tiles}, White: {white_tiles}")
    
    def display_board(self, board: Board, legal_moves: dict[tuple[int, int], list[tuple[int, int]]]) -> None: 
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                occupied: int = board.is_occupied( (x,y))
                if occupied:
                    bit_color: int = board.get_tile_color((x,y))
                    self.buttons[x * Board.SIZE + y].set_color(get_color(bit_color))
                elif (x,y) in legal_moves:
                    self.buttons[x * Board.SIZE + y].set_color(Color.GRAY)
                else:
                    self.buttons[x * Board.SIZE + y].set_color(None)
    
    def display_result(self, result: GameResult) -> None: 
        result_box: QMessageBox = QMessageBox()
        result_box.setIcon(QMessageBox.Information)
        result_box.setText(f"{result}")
        result_box.setWindowTitle("Game Over")
        result_box.setStandardButtons(QMessageBox.Ok)
        
        result_box.exec_()
