from Game import Board, BoardSymbol, Player, Game
import time

def main():
    game_board: Board = Board()
    # bot = Bot()
    
    while True:
        Game.print_turn()
        Game.legal_moves = Game.get_moves(game_board, Game.current_player)
        Game.print_score()
        Game.print_board(game_board)
        while True:
            try:
                op = input(">> ")
                if op == "end":
                    return
                (x,y) = op.split(",")
            except:
                print("Invalid input!")
            if Game.play(game_board, Game.current_player, (int(x),int(y))):
               break  
        Game.switch_player()
        
if __name__ == "__main__":
    main()