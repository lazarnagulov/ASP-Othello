from Game import Board, Player, Game
from Bot import Bot

def main():
    game_board: Board = Board()
    bot: Bot = Bot()
   
    while True:
        Game.legal_moves = Game.get_moves(game_board, Game.current_player)
        Game.print_status(game_board)
        if Game.has_ended(game_board):
            Game.print_status(game_board)
            print(Game.get_winner())
            break

        while True:
            try:
                print("Input: <row>,<column>")
                op: str = input(">> ")
                if op == "exit":
                    return
                (x,y) = op.split(",")
            
                if Game.play(game_board, Game.current_player, (int(x),int(y))):
                    Game.switch_player()
                    Game.print_status(game_board)
                    break  
            except:
                    print("Invalid input!")
                    continue
        
        bot_move: tuple[int, int] = bot.bot_move(game_board)
        if bot_move:
            Game.play(game_board, Game.current_player, bot_move, Game.get_moves(game_board, Player.WHITE))
        else:
            print(Game.get_winner())
            break
        
        Game.switch_player()            
    
    
if __name__ == "__main__":
    main()