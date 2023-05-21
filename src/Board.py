import Matrix
import sys

class Player(object):
    """Player enumaration. BLACK and WHITE. They can only be binary units (0 and 1).
    """
    BLACK = 0
    WHITE = 1

    @staticmethod
    def get_opponent(player):
        """Gets player's oppoenent.

        Args:
            player (Player): player

        Returns:
            Player: player's opponent
        """
        return Player.BLACK if player == Player.WHITE else Player.WHITE

class BoardSymbol(object):
    """BoardSyombol enumeration. WHITE, BLACK EMPTY and LEGAL_MOVE
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
    Othello board class. Board is represented by two 64 bit binary numbers. Occupied are all occupied positions on board (1 if occupied 0 if not)
    and color are all tiles position on board (1 if tile is white, 0 if tile is black). 
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

    
    def __hash__(self):
        hash_value: int = 0
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                occupied: int = self.get_tile(self.occupied, (x,y))
                if occupied:
                    color: int = self.get_tile(self.color, (x,y))
                    if color == 1:
                        hash_value ^= -1
                    else:
                        hash_value ^= 1
                else:
                    hash_value ^= 0
        return hash_value

    def get_tile(self, board: int, position: tuple[int, int]) -> int:
        """Checks occupied or color number, depending on board argument. Color only works on occupied positions.

        Args:
            board (int): board.color or board.occupied\n
            position (tuple[int, int]): postion on board (row, column)

        Returns:
            int: Returns bit on `8*row + column` position, which represents occupation or tile on board.
        """
        
        offset: int = position[0] * 8 + position[1] 
        
                
        if sys.byteorder == "little":
            return (board & Matrix.DECODE_MATRIX[position[0]][position[1]]) >> offset
        else:
            return (board & Matrix.DECODE_MATRIX[position[0]][position[1]]) << offset
            
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

    def deepcopy(self):
        """Deepcopies Board object.

        Returns:
            Board: copied board
        """
        new_board = Board()
        new_board.color = self.color
        new_board.occupied = self.occupied
        return new_board
        