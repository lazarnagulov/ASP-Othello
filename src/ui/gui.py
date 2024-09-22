from models.game_result import GameResult
from models.player import Player
from models.board import Board
import sys

from .user_interface import UserInterface
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLabel, QHBoxLayout, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QEvent 

class GUI(UserInterface):    

    def __init__(self) -> None:
        self.app: QApplication = QApplication(sys.argv)      
        self.window: QWidget = QWidget()
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
        
        self.buttons: list[QPushButton] = []

        for row in range(8):
            for col in range(8):
                button: QPushButton = QPushButton()
                
                if (row + col) % 2 == 0:
                    button.setStyleSheet("background-color: green;")  
                else:
                    button.setStyleSheet("background-color: darkgreen;")

                self.grid.addWidget(button, row, col)
                self.buttons.append(button)

        self.main_layout.addLayout(self.grid)

        self.window.setLayout(self.main_layout)
        self.window.setWindowTitle('Othello')
        self.window.resize(400, 400)

        self.window.show()
            
    def run(self) -> None:
        return None

    
    def display_current_player(self, current_player: Player) -> None: 
        self.current_player.text = current_player.name
    
    def display_score(board, white_tiles: int, black_tiles: int) -> None: 
        return None
    
    def display_board(self, board: Board, legal_moves: dict[tuple[int, int], list[tuple[int, int]]]) -> None: 
        return None
    
    def display_result(self, result: GameResult) -> None: 
        return None
        
    
