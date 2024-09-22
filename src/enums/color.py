from enum import Enum
from enums.player import Player

class Color(Enum):
    BLACK = "black"
    WHITE = "white"
    GRAY = "gray"


def get_color(player: int) -> Color:
    match player:
        case Player.BLACK.value: return Color.BLACK
        case Player.WHITE.value: return Color.WHITE
        case _: raise Exception("Unreachable...")