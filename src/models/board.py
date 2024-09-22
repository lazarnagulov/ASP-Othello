from models.player import Player
from models.board_symbol import BoardSymbol
import game
import util.matrix as Matrix

class Board:
    """
    Othello board class. Board is represented by two 64 bit binary numbers. Occupied are all occupied positions on board (1 if occupied 0 if not)
    and color are all tiles position on board (1 if tile is white, 0 if tile is black). 
    """
    SIZE: int = 8
    """
    Othello board size = 8
    """
    
    def __init__(self) -> None:
        """
        Create board with starting tiles.         
        """
        self.occupied: int = 0
        self.color: int = 0
        
        self.set_tile((3,3), Player.WHITE)
        self.set_tile((3,4), Player.BLACK)
        self.set_tile((4,4), Player.WHITE)
        self.set_tile((4,3), Player.BLACK)

    
    def is_occupied(self, position: tuple[int, int]) -> bool:
        """Checks if board is occupied in position.

        Args:
            position (tuple[int, int]): position (row, column)

        Returns:
            bool: True if position is occupied 
        """
        return bool((self.occupied & Matrix.DECODE_MATRIX[position[0]][position[1]]) >> (position[0] * 8 + position[1])) 

    def get_tile_color(self, position: tuple[int, int]) -> int:
        """Gets the color in position.

        Args:
            position (tuple[int, int]): position (row, column)

        Returns:
            int: Returns player in position. If position is empty, returns -1
        """
        if self.is_occupied(position):
            return (self.color & Matrix.DECODE_MATRIX[position[0]][position[1]]) >> (position[0] * 8 + position[1])
        return -1
        
    def replace_opponent(self, position: tuple[int, int]) -> None:
        """Reverse tile on position. Does nothing if position is empty.

        Args:
            position (tuple[int, int]): position (row, column)
        """
        self.color ^= Matrix.DECODE_MATRIX[position[0]][position[1]]
    
    def set_tile(self, position: tuple[int, int], player: Player) -> None:
        """Occupies tile on position.

        Args:
            position (tuple[int, int]): position (row, column)
            player (Player): player
        """
        self.occupied |= Matrix.DECODE_MATRIX[position[0]][position[1]]
        if player == Player.WHITE:
            self.color |= Matrix.DECODE_MATRIX[position[0]][position[1]]    
            
    def deepcopy(self) -> 'Board':
        """Deepcopies Board object.

        Returns:
            Board: copied board
        """
        new_board = Board()
        new_board.color = self.color
        new_board.occupied = self.occupied
        return new_board