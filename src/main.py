from typing import Optional
from ui.console_interface import ConsoleInterface
from ui.user_interface import UserInterface
from ui.gui import GUI
import sys

def main() -> None:
    ui: Optional[UserInterface] = None
    
    if len(sys.argv) != 1:
        match sys.argv[1]:
            case "--console" | "-c": ui = ConsoleInterface()
            case "--ui" | "-u": ui = GUI()
            case _: ui = GUI()
    else:
        ui = ConsoleInterface()

    ui.run()
    
if __name__ == "__main__":
    main()