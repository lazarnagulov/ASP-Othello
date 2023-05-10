from Board import Board, Player
import time

def main():
    game_board = Board()
    # start = time.time()
    print(game_board)
    
    while True:
        print(game_board.get_moves())
        (x, y) = input(">>").split(",")
        game_board.play((int(x),int(y)))
        print(game_board)
        
        
    # print(game_board.get_moves())
    # game_board.play((5,4))
    # print(game_board)
    # # end = time.time()
    # print(end - start)
        
if __name__ == "__main__":
    main()