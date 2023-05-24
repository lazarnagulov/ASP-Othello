from Game import Board, BoardSymbol, Player, Game, GameResult
from Bot import Bot

def main():
    # print("\t---> OTHELLO <---")
    # print("Commands:")
    # print("\tstart pvp - starts player vs player")
    # print("\tstart pvb - starts player vs bot")
    # print("\tstart bvb - start bot vs bot")
    # print("\texit - exits program")

    # while True:
    #     try:    
    #         op: str = input(">> ")
    #         if op == "exit":
    #             return
    #         (op1, op2) = op.split(" ")
    #         if op1 != "start":
    #             print("Invalid input")
    #             continue
    #         elif op2 == "pvp":
    #             pass # start pvp mod
    #         elif op2 == "pvb":
    #             pass # start pvb mod
    #         elif op2 == "bvb":
    #             pass # start bvb mod
    #         else:
    #             print("Invalid input")
    #             continue
    #     except:
    #         print("Invalid input")
    
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