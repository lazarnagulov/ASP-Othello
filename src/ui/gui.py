from enums.game_result import GameResult
from enums.player import Player
from enums.color import Color

from ui.component.tile import Tile
from models.board import Board
import sys

from .user_interface import UserInterface
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLabel, QHBoxLayout, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QEvent 

class GUI(UserInterface):    

    def __init__(self) -> None:
        self.app: QApplication = QApplication(sys.argv)      
        self.window: QWidget = QWidget()
        self.window.setFixedSize(400,400)
        self.current_player: QLabel = QLabel("Current Player: Black")
        self.current_score: QLabel = QLabel("Score - Black: 2, White: 2")

        self.stats_layout: QHBoxLayout = QHBoxLayout()
        self.stats_layout.addWidget(self.current_player)
        self.stats_layout.addStretch(1)
        self.stats_layout.addWidget(self.current_score)

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.addLayout(self.stats_layout)
        
        self.grid: QGridLayout = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        
        self.buttons: list[Tile] = []

        for row in range(8):
            for col in range(8):
                button: Tile = Tile(None)
                
                if (row + col) % 2 == 0:
                    button.setStyleSheet("background-color: green;")  
                else:
                    button.setStyleSheet("background-color: darkgreen;")
                
                if (row == 2 and col == 3) or (row == 3 and col == 2) \
                or (row == 4 and col == 5) or (row == 5 and col == 4):
                    button.set_color(Color.GRAY)
                
                if (row == 3 and col == 3) or (row == 4 and col == 4):
                    button.set_color(Color.WHITE)
                if (row == 3 and col == 4) or (row == 4 and col == 3):
                    button.set_color(Color.BLACK) 



                self.grid.addWidget(button, row, col)
                self.buttons.append(button)

        self.main_layout.addLayout(self.grid)

        self.window.setLayout(self.main_layout)
        self.window.setWindowTitle('Othello')

    def run(self) -> None:
        self.display_current_player(Player.BLACK)
        self.display_score(2,2)
        self.window.show()
        sys.exit(self.app.exec_())
    
    def display_current_player(self, current_player: Player) -> None: 
        self.current_player.setText(f"Current player: {current_player.name}")
    
    def display_score(self, white_tiles: int, black_tiles: int) -> None: 
        self.current_score.setText(f"Score - Black: {black_tiles}, White: {white_tiles}")
    
    def display_board(self, board: Board, legal_moves: dict[tuple[int, int], list[tuple[int, int]]]) -> None: 
        return None
    
    def display_result(self, result: GameResult) -> None: 
        return None
        
    
