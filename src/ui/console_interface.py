from models.player import Player
from models.board_symbol import BoardSymbol, get_symbol
from models.game_result import GameResult
from game.game import Game
from game.bot import Bot
from models.board import Board
from typing import Optional

from .user_interface import UserInterface

class ConsoleInterface(UserInterface):

    def run(self) -> None:
        
        game_board: Board = Board()
        bot: Bot = Bot()    
    
        while True:
            Game.legal_moves = Game.get_moves(game_board, Game.current_player)
            self.display_score(Game.white_tiles, Game.black_tiles)
            self.display_board(game_board, Game.legal_moves)
            if Game.has_ended(game_board):
                self.display_score(Game.white_tiles, Game.black_tiles)
                self.display_board(game_board, Game.legal_moves)
                self.display_result(Game.get_winner())
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
                        self.display_score(Game.white_tiles, Game.black_tiles)
                        self.display_board(game_board, Game.legal_moves)
                        break  
                except:
                        print("Invalid input!")
                        continue
            
            bot_move: Optional[tuple[int, int]] = bot.bot_move(game_board)
            if bot_move:
                Game.play(game_board, Game.current_player, bot_move, Game.get_moves(game_board, Player.WHITE))
            else:
                self.display_result(Game.get_winner())
                break
            
            Game.switch_player()            
    
    def display_current_player(board, current_player: Player) -> None:
        print(f"Current player: {get_symbol(current_player)}")
   
    def display_score(board, white_tiles: int, black_tiles: int) -> None:
        print(f"{get_symbol(Player.WHITE)}: {white_tiles} - {get_symbol(Player.BLACK)}: {black_tiles}")
        
    def display_board(self, board: Board, legal_moves: dict[tuple[int, int], list[tuple[int, int]]]) -> None:
        string_board: str = "# "
        for i in range(Board.SIZE):
            string_board += str(i) + " "
        string_board += "\n"
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if y == 0:
                    string_board += str(x) + " "
                occupied: int = board.is_occupied( (x,y))
                if occupied:
                    color: int = board.get_tile_color((x,y))
                    if color == Player.WHITE:
                        string_board += BoardSymbol.WHITE + " "
                    else:
                        string_board += BoardSymbol.BLACK + " "
                elif (x,y) in legal_moves:
                    string_board += BoardSymbol.LEGAL_MOVE + " "
                else:
                    string_board += BoardSymbol.EMPTY + " "
            string_board += "\n"

        print(string_board)
    
    def display_result(self, result: GameResult) -> None: 
        print(result)
        
         
