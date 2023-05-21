from Board import Board, Player
from Game import Game, GameResult
import time

class Bot(object):
    POSITIVE_INFINITY = float("inf")
    NEGATIVE_INFINITY = float("-inf")
    MAX_DEPTH: int = 10
    
    hashed_boards: dict[tuple[int, int], float] = {}

    def __minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool, player: Player) -> tuple[float, tuple[int, int]]:
        moves: dict[tuple[int, int], list[tuple[int, int]]] = Game.get_moves(board, player)
        
        if depth == 0 or Game.has_ended(board):
            board_hash: tuple[int, int] = (board.color, board.occupied)
            if Bot.hashed_boards.get(board_hash):
                return Bot.hashed_boards[board_hash]
            else:
                score: float = Game.get_board_score(board, player)
                Bot.hashed_boards[board_hash] = score
                return score
        
        if maximizingPlayer:
            max_eval: int = Bot.NEGATIVE_INFINITY
            eval: int = Bot.NEGATIVE_INFINITY
            for move in moves:
                next_state: Board = board.deepcopy()
                Game.play(next_state, player, move, moves, True)
                if Bot.hashed_boards.get(next_state):
                    eval = Bot.hashed_boards[next_state]
                else:
                    eval = self.__minimax(next_state, depth - 1, alpha, beta, False, Player.get_opponent(player))
                if eval > max_eval:
                    max_eval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval: int = Bot.POSITIVE_INFINITY
            eval: int = Bot.POSITIVE_INFINITY
            for move in moves:
                next_state: Board = board.deepcopy()
                Game.play(next_state, player, move, moves, True)
                if Bot.hashed_boards.get(next_state):
                    eval = Bot.hashed_boards[next_state]
                else:   
                    eval = self.__minimax(next_state, depth - 1, alpha, beta, True, Player.get_opponent(player))
                if eval < min_eval:
                    min_eval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval        
    
    def bot_move(self, board: Board, time_limit: float = 1.25) -> tuple[int, int]:
        start_time: float = time.time()
        moves: dict[tuple[int, int], list[tuple[int, int]]] = Game.get_moves(board, Player.WHITE)
        
        best_score: int = Bot.NEGATIVE_INFINITY
        best_move: tuple[int, int] = ()
        depth: int = 1
        
        for move in moves:
            next_state: Board = board.deepcopy()
            Game.play(next_state, Player.WHITE, move, moves, True)

            score = self.__minimax(next_state, depth, Bot.NEGATIVE_INFINITY, Bot.POSITIVE_INFINITY, False, Player.BLACK)
            if score > best_score:
                best_score = score
                best_move = move
            
            if time.time() - start_time >= time_limit or depth > Bot.MAX_DEPTH:
                break
            
            depth += 1
        
        print(f"Time: {time.time() - start_time}")
        print(f"Depth: {depth}")
        print(f"Move: {best_move}")
        
        return best_move
        