from typing import Protocol
from enums.player import Player
from enums.game_result import GameResult
from models.board import Board


class UserInterface(Protocol):
    def run(self) -> None: ...
    