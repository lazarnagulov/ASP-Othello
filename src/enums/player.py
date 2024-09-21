from enum import Enum, auto

class Player(Enum):
    """Player enumaration. BLACK and WHITE. They can only be binary units (0 and 1).
    """
    BLACK = auto
    WHITE = auto

def get_opponent(player) -> Player:
    """Gets player's oppoenent.

    Args:
        player (Player): player

    Returns:
        Player: player's opponent
    """
    return Player.BLACK if player == Player.WHITE else Player.WHITE
