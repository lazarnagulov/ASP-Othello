from typing import Optional
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

    interface.run()
    
if __name__ == "__main__":
    main()