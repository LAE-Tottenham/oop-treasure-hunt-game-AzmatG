import getch
from System import clear_console
from Trader import Trader
from CombatEntities import Player
import time
import questionary
from Maze import Maze



class Lobby():
    def __init__(self, player, maze, trader):
        self.player = player
        self.maze = maze
        self.trader = trader
        self.met_trader = False
    def make_lobby(self):
        lobby = [[True, True, True, True, True, True, True],
                    [True, False, False, False, False, False, True],
                    ["=", "=", False, False, False, False, True],
                    ["@", False, False, False, False, False, True],
                    ["=", "=", False, False, False, False, True],
                [True, False, False, False, False, False, True],
                [True, False, False, False, False, False, True],
                [True, False, False, False, False, False, True],    
                [True, False, False, False, False, False, True],
                    [True, "-", "|", False, "|", "-", True],
                    [True, True, "|", "#", "|", True, True],
                    ]
        
        return lobby
    def move(self):
        lobby = self.make_lobby()
        playerX, playerY = 3, 1
        TraderX, TraderY = 0, 3
        mazeX, mazeY = 3, 10
        lobby[playerY][playerX] = "◈"
        
        def IsValidMove(maze, positionX, positionY):
            if positionY == TraderY and positionX == TraderX:
                return True
            elif positionX == mazeX and positionY == mazeY:
                return True
            return 0 < positionX < 7 and 0 < positionY < 10 and not maze[positionY][positionX]
        while True:
            clear_console()
            self.PrintLobby(lobby)
            PlayerInput = getch.getch()
            
            if PlayerInput == "w":
                if IsValidMove(lobby, playerX, playerY-1):
                    lobby[playerY][playerX] = False
                    playerY = playerY-1
                    lobby[playerY][playerX] = "◈"
                    clear_console()
                    self.PrintLobby(lobby)
            if PlayerInput == "a":
                if IsValidMove(lobby, playerX-1, playerY):
                    lobby[playerY][playerX] = False
                    playerX = playerX-1
                    lobby[playerY][playerX] = "◈"
                    clear_console()
                    self.PrintLobby(lobby)
            if PlayerInput == "s":
                if IsValidMove(lobby, playerX, playerY+1):
                    lobby[playerY][playerX] = False
                    playerY = playerY+1
                    lobby[playerY][playerX] = "◈"
                    clear_console()
                    self.PrintLobby(lobby)
            if PlayerInput == "d":
                if IsValidMove(lobby, playerX+1, playerY):
                    lobby[playerY][playerX] = False
                    playerX = playerX+1
                    lobby[playerY][playerX] = "◈"
                    clear_console()
                    self.PrintLobby(lobby)
            if (playerY, playerX) == (TraderY, TraderX):
                clear_console()
                if not self.met_trader:
                    self.trader.give_intro()
                    self.met_trader = True
                    input()
                    clear_console()
                self.trader.events(self.player)

                lobby[playerY][playerX] = "@"
                playerX += 1
                lobby[playerY][playerX] = "◈"
                clear_console()
                self.PrintLobby(lobby)
            if PlayerInput == "i":
                self.player.loadout()
            if (playerY, playerX) == (mazeY, mazeX):
                clear_console()
                enter = questionary.confirm("You cant leave until you find the exit. Would you like to enter the Maze?").ask()
                if enter:
                    if self.maze.level > 0:
                        range = ["0", "1", "2", "3", "4"]

                        level = questionary.select(
                            "Which level would you like to start from",
                            choices=range
                        ).ask()
                        self.maze.level = int(level)
                    self.maze.PlayerExplore()
                    if not self.maze.ending and not self.maze.dead:
                        lobby[mazeY][mazeX] = "#"
                        playerY -= 1
                        lobby[playerY][playerX] = "◈"
                        clear_console()
                        self.PrintLobby(lobby) 
                    else:
                        break
                    

                
                
            
    def ConvertCell(self, cell):
        if isinstance(cell, str):
            return cell
        elif cell: 
            return "□" 
        else:
            return " "
    def PrintLobby(self, lobby):
        final_lobby = []
        for row in lobby:
            converted_row = [self.ConvertCell(cell) for cell in row]
            final_lobby.append(converted_row)
        for row in final_lobby:
            print("  ".join(x for x in row))