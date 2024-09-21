from .player import Player

class BoardSymbol:
    """BoardSyombol enumeration. WHITE, BLACK EMPTY and LEGAL_MOVE
    """
    WHITE = "○"
    BLACK = "●"
    EMPTY = "□"
    LEGAL_MOVE = "■"
    
    def __add__(self, other: str) -> str:
        return self.value + other
    
    def __str__(self) -> str:
        return self.value
    
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
