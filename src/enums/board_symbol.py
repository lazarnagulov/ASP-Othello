from enum import Enum
from .player import Player

class BoardSymbol(Enum):
    """BoardSyombol enumeration. WHITE, BLACK EMPTY and LEGAL_MOVE
    """
    WHITE = "○"
    BLACK = "●"
    EMPTY = "□"
    LEGAL_MOVE = "■"
    
    def __add__(self, other: str) -> str:
        return self + other
    
def get_symbol(player: Player) -> BoardSymbol:
    """Converts player to symbol.
    
    Args:
        player (Player): player

    Returns:
        BoardSymbol: player's symbol
    """
    if player == Player.BLACK:
        return BoardSymbol.BLACK
    else:
        return BoardSymbol.WHITE
