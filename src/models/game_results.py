from enum import Enum

class GameResult(Enum):
    """Game result enumeration: WHITE_WINS, BLACK_WINS, DRAW and NO_WINNER
    """
    WHITE_WINS = "White wins!"
    BLACK_WINS = "Black wins!"
    DRAW = "DRAW!"
    NO_WINNER = ""
    
    def __str__(self) -> str:
        return self.value
