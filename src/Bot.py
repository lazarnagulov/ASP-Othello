from structures import TreeNode, Tree
class Node(object):
    def __init__(self):
        self.children: list = []
        self.value = None


class Bot(object):
    MAX_INT = 9223372036854775807

    def __minimax(self, pos: Node, depth: int, alpha: int, beta: int, maximizingPlayer: bool) -> int:
        if depth == 0:
            return pos
        
        if maximizingPlayer:
            maxEval: int = - Bot.MAX_INT
            for child in pos.children:
                eval = self.__minimax(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval: int = Bot.MAX_INT
            for child in pos.children:
                eval = self.__minimax(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
            
        
        
    

