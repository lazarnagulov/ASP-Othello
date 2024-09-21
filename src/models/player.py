from enum import Enum


class Player(Enum):
    """Player enumaration. BLACK and WHITE. They can only be binary units (0 and 1).
    """
    BLACK = 0
    WHITE = 1
    
    def __eq__(self, other: object) -> bool:
        return self.value == other


def get_opponent(player: Player) -> Player:
    """Gets player's oppoenent.

    Args:
        player (Player): player

    Returns:
        Player: player's opponent
    """
    return Player.BLACK if player == Player.WHITE else Player.WHITE
