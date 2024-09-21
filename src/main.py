from game.game import Board, Player, Game
from typing import Optional
from game.bot import Bot
from ui.console_interface import ConsoleInterface
from ui.user_interface import UserInterface
from ui.gui import GUI
import sys

def main() -> None:
    interface: Optional[UserInterface] = None
    
    if len(sys.argv) != 1:
        match sys.argv[1]:
            case "--console" | "-c": interface = ConsoleInterface()
            case "--ui" | "-u": interface = GUI()
            case _: interface = GUI()
    else:
        interface = ConsoleInterface()

    game_board: Board = Board()
    bot: Bot = Bot()    
   
    while True:
        Game.legal_moves = Game.get_moves(game_board, Game.current_player)
        interface.display_score(Game.white_tiles, Game.black_tiles)
        interface.display_board(game_board, Game.legal_moves)
        if Game.has_ended(game_board):
            interface.display_score(Game.white_tiles, Game.black_tiles)
            interface.display_board(game_board, Game.legal_moves)
            interface.display_result(Game.get_winner())
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
                    interface.display_score(Game.white_tiles, Game.black_tiles)
                    interface.display_board(game_board, Game.legal_moves)
                    break  
            except:
                    print("Invalid input!")
                    continue
        
        bot_move: Optional[tuple[int, int]] = bot.bot_move(game_board)
        if bot_move:
            Game.play(game_board, Game.current_player, bot_move, Game.get_moves(game_board, Player.WHITE))
        else:
            interface.display_result(Game.get_winner())
            break
        
        Game.switch_player()            
    
    
if __name__ == "__main__":
    main()