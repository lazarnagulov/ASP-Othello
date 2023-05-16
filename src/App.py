from Board import Board, Player, GameResult
import time

def main():
    game_board = Board()
    # start = time.time()
    while True:
        game_board.get_moves(game_board._current_player)
        print(f"Current Player: {game_board._current_player}")
        print(f"Score: {game_board.print_score()}")
        print(game_board)
      
        if game_board._legal_moves == {}:
            print(game_board.get_winner()) 
            break

        (x, y) = input(">>").split(",")
        # start = time.time()
        game_board.play((int(x),int(y)))
        # end = time.time()
        # print(end - start)        
        
    # print(game_board.get_moves())
    # game_board.play((5,4))
    # print(game_board)
    # # end = time.time()
    # print(end - start)
        
if __name__ == "__main__":
    main()