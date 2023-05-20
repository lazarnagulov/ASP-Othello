from Board import Board, Player
from Game import Game, GameResult
import time

class Node(object):
    def __init__(self, board: Board, moves: list = None, value: float= None):
        self.board: Board = None
        self.moves: list[Node] = moves
        self.value: float = value


class Bot(object):
    POSITIVE_INFINITY = float("inf")
    NEGATIVE_INFINITY = float("-inf")

    def __minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool, player: Player) -> float:
        moves: dict[tuple[int, int], list[tuple[int, int]]] = Game.get_moves(board, player)
        #TODO: end game condition
        if depth == 0:
            #TODO: heruistic 
            return 0
        
        if maximizingPlayer:
            maxEval: int = Bot.NEGATIVE_INFINITY
            for move in moves:
                next_state: Board = board.deepcopy()
                Game.play(next_state, player, move, moves)
                eval = self.__minimax(next_state, depth - 1, alpha, beta, False, Player.get_opponent(player))
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval: int = Bot.POSITIVE_INFINITY
            for move in moves:
                next_state: Board = board.deepcopy()
                Game.play(next_state, player, move, moves)                
                eval = self.__minimax(next_state, depth - 1, alpha, beta, True, Player.get_opponent(player))
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval        
    

