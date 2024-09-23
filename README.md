# Othello
Project for Algorithms and Data Structures course.
## Overview
Welcome to the Othello game project! This Python implementation originally featured a console-only mode for Player vs Bot. It has now been updated to include two modes of play: **Player vs Player** and **Player vs Bot**. The project also offers two interfaces: a **Console Interface** and a **Graphical User Interface (GUI)**, providing an enhanced gaming experience.

![Othello Board](img/othello_board.jpg)

### Interfaces
- **Graphical User Interface (GUI)**

  ![Othello GUI](img/othello_gui.png)

- **Console Interface**

  ![Othello Console](img/othello_console.png)

## Recent Updates
- **21.9.2024**: Revisited and updated the project.
- **23.9.2024**: Added GUI and Player vs Player mode.

## Usage
To run the application, ensure you have **PyQt5** installed:

```bash
pip install -r requirements.txt 
```

## Launching the Application
Run the application with the following command for the default option (GUI: Player vs Bot):
```
python3 ./src/main.py
```

## Command Options

You can customize your game mode with the following command-line options:
- Console - vs Bot
```
python3 ./src/main.py [--console | -c] [--bot | -b]
```
- Console - vs Player
```
python3 ./src/main.py [--console | -c] [--player | -p]
```
- GUI - vs Bot
```
python3 ./src/main.py [--gui | -g] [--bot | -b]
```
- GUI - vs Player
```
python3 ./src/main.py [--gui | -g] [--player | -p]
```
## Dependencies
- **PyQt5**: Required for the GUI.

## References
- [Othello](https://en.wikipedia.org/wiki/Reversi)
- [Heuristic Function for Othello](https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/)
