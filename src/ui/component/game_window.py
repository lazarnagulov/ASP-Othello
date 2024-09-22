from typing import Optional, cast
from enums.game_result import GameResult
from enums.player import Player
from enums.color import Color, get_color

from ui.user_interface import UserInterface
from ui.component.tile import Tile
from models.board import Board
from game.bot import Bot
from game.game import Game

import sys

from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QHBoxLayout, 
    QLabel, 
    QHBoxLayout, 
    QGridLayout, 
    QVBoxLayout,
    QMessageBox
)

class GameWindow(QWidget):    

    def __init__(self) -> None:
        super().__init__()
        self.game_board: Board = Board()
        self.bot: Bot = Bot()
        Game.legal_moves = Game.get_moves(self.game_board, Game.current_player)
        
        self.app: QApplication = QApplication(sys.argv)      
        self.setFixedSize(400,400)
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
                button: Tile = Tile(None, (row, col))
                
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
                
                button.clicked.connect(self.handle_click)

                self.grid.addWidget(button, row, col)
                self.buttons.append(button)

        self.main_layout.addLayout(self.grid)

        self.setLayout(self.main_layout)
        self.setWindowTitle('Othello')

    def handle_click(self) -> None:
        if(not Game.play(self.game_board, Game.current_player, cast(Tile, self.sender()).position)):
            return
        Game.switch_player()
        Game.legal_moves = Game.get_moves(self.game_board, Game.current_player)
        self.display_current_player(Game.current_player)
        self.display_board(self.game_board, Game.legal_moves)
        self.display_score(Game.white_tiles, Game.black_tiles) 
        if Game.has_ended(self.game_board):
            self.display_result(Game.get_winner())
        
    def run(self) -> None:
        self.show()
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
