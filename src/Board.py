import Matrix
import sys

class Player(object):
    """Player enumaration
    """
    BLACK = 0
    WHITE = 1

    @staticmethod
    def get_opponent(player):
        """Gets player's oppoenent

        Args:
            player (Player): player

        Returns:
            Player: player's opponent
        """
        return Player.BLACK if player == Player.WHITE else Player.WHITE

class BoardSymbol(object):
    """BoardSyombol enumeration
    """
    WHITE = "○"
    BLACK = "●"
    EMPTY = "□"
    LEGAL_MOVE = "■"
    
    @staticmethod
    def get_symbol(player: Player):
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

class Board(object):
    """
    Othello board class
    """
    SIZE: int = 8
    """
    Othello board size = 8
    """
    
    def __init__(self):
        """
        Create board with starting tiles.
        """
        self.occupied: int = 0
        self.color: int = 0
        
        self.set_tile((3,3), Player.WHITE)
        self.set_tile((3,4), Player.BLACK)
        self.set_tile((4,4), Player.WHITE)
        self.set_tile((4,3), Player.BLACK)

    def get_tile(self, board: int, position: tuple[int, int]) -> int:
        """Check if position on board is occuptied or which player is in that position.\n
        Arguments
            board (int): board.color or board.occupied\n
            position (tuple[int, int]): position on board
        Returns
            int: 1 if position is occupied / white is on that postion and 0 if position is not occupied / black is on that position 
        """
        if sys.byteorder == "little":
            return (board & Matrix.DECODE_MATRIX[position[0]][position[1]]) >> (position[0] * 8 + position[1])
        else:
            return (board & Matrix.DECODE_MATRIX[position[0]][position[1]]) << (position[0] * 8 + position[1])
            
    def replace_opponent(self, position: tuple[int, int]) -> None:
        """Reverse tile on position. Does nothing if position is empty.

        Args:
            position (tuple[int, int]): position
        """
        self.color ^= Matrix.DECODE_MATRIX[position[0]][position[1]]
    
    def set_tile(self, position: tuple[int, int], player: Player) -> None:
        """Occupies tile on position

        Args:
            position (tuple[int, int]): position
            player (Player): player
        """
        self.occupied |= Matrix.DECODE_MATRIX[position[0]][position[1]]
        if player == Player.WHITE:
            self.color |= Matrix.DECODE_MATRIX[position[0]][position[1]]                            

    def deepcopy(self):
        """Deepcopies Board object.

        Returns:
            Board: copied board
        """
        new_board = Board()
        new_board.color = self.color
        new_board.occupied = self.occupied
        return new_board
        