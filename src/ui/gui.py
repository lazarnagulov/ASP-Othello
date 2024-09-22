from enums.game_result import GameResult

from ui.component.game_window import GameWindow
from ui.user_interface import UserInterface

import sys

from PyQt5.QtWidgets import (
    QApplication, 
    QMessageBox
)

class GUI(UserInterface):    

    def __init__(self) -> None:        
        argv: list[str] = sys.argv
        self.app: QApplication = QApplication(argv)      
        self.window = GameWindow(argv)
        
    def run(self) -> None:
        self.window.show()
        sys.exit(self.app.exec_())
