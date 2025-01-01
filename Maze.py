import random
from System import clear_console, game_over, message, good_end, choose_end
import getch 
from rich import print
from collections import deque 
from Items import CreateRandomWeapon, Weapon, Armour, HealingItem, Item
from CombatEntities import Player, Enemy, Boss
import questionary
from CombatTurnStateMachine import CombatTurnStateMachine
import time


class Maze:
    def __init__(self, player):
        self.level = 0
        self.mazeSize = 15 
        self.startX, self.startY = 2*random.randint(0, self.mazeSize//2 - 1) + 1, 2*random.randint(0, self.mazeSize//2 - 1) + 1
        self.maze = self.Generate()
        self.min_distance = self.mazeSize//2
        self.exitX, self.exitY  = None, None
        self.player = player
        self.chestweights = [
            #C   S   G
            [90, 10, 0],  #0
            [70, 30, 0],  #1
            [60, 30, 10], #2
            [50, 35, 15], #3
            [30, 50, 20]  #4
        ]

        
        self.ending = False
        self.enclosed_areas = None
        self.dead = False
    def CleanUp(self):
        self.maze = self.Generate()

    def Generate(self):

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        maze = [[True]*self.mazeSize for x in range(self.mazeSize)]
        
        stack = [(self.startX, self.startY)]
        while len(stack) > 0:
            currentX, currentY = stack[-1]
            if (maze[currentY][currentX]):
                maze[currentY][currentX] = False
            random.shuffle(directions)
            
            neighbours = []
            
            for dir in directions:
                midX, midY = currentX + dir[0], currentY + dir[1]
                newX, newY = midX + dir[0], midY + dir[1]
                
                if 0 <= newX < self.mazeSize and 0 <= newY < self.mazeSize and maze[newY][newX] and maze[midY][midX]:
                    neighbours.append((newX, newY, midX, midY))

            if neighbours:
                newX, newY, midX, midY = random.choice(neighbours)
                maze[newY][newX] = False
                maze[midY][midX] = False
                stack.append((newX, newY))

            else:

                stack.pop()            

        return maze
    
    def EndPos(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        bfs_queue = deque([(self.startX, self.startY)])
        distanceLevels = {(self.startX, self.startY): 0}
        current_distance = 0
        result = []
        max_retries = 10
        retries = 0
        while bfs_queue:
            nextLevel = []

            for i in range(len(bfs_queue)):
                currentX, currentY = bfs_queue.popleft()

                if current_distance > self.min_distance:
                    result.append((currentX, currentY))

                random.shuffle(directions)

                for dir in directions:

                    newX, newY = currentX + dir[0], currentY + dir[1]

                    if 0 < newX < self.mazeSize and 0 < newY < self.mazeSize and not self.maze[newY][newX] and (newX, newY) not in distanceLevels:
                        distanceLevels[(newX, newY)] = current_distance + 1
                        nextLevel.append((newX, newY))

            bfs_queue.extend(nextLevel)
            current_distance += 1 

        exits = []
        for cell in result:
            wall_count = 0
            for dir in directions:
                neighbourX, neighbourY = cell[0] + dir[0], cell[1] + dir[1]

                if 0 <= neighbourX < self.mazeSize and 0 <= neighbourY < self.mazeSize and self.maze[neighbourY][neighbourX]:
                    wall_count += 1

            if wall_count == 3:
                exits.append(cell)
        while len(exits) <= 1 and retries < max_retries:
            self.CleanUp()  
            retries += 1
            return self.EndPos()

        exit = random.choice(exits)
        exits.remove(exit)
        self.exitX, self.exitY = exit[0], exit[1]
        self.enclosed_areas = exits
    
    def ConvertCell(self, cell):
        if isinstance(cell, str):
            return cell
        elif cell: 
            return "□" 
        else:
            return " "
        
    def PrintMaze(self, maze):
        final_maze = []
        for row in maze:
            converted_row = [self.ConvertCell(cell) for cell in row]
            final_maze.append(converted_row)
        for row in final_maze:
            print("  ".join(x for x in row))

    def SpawnEnemy(self):

        maze = self.maze
        no_of_enemies = 3 + self.level
        enemy_locations = []
        
        for cell in maze:
            enemyX, enemyY = random.randint(1, self.mazeSize-1), random.randint(1, self.mazeSize-1)
            if not maze[enemyY][enemyX] and enemyX != self.startX and enemyY != self.startY:
                enemy_locations.append((enemyX, enemyY))
                enemyX, enemyY = random.randint(1, self.mazeSize-1), random.randint(1, self.mazeSize-1)
            if len(enemy_locations) == no_of_enemies:
                break
        return enemy_locations
    
    def WeightedChance(self):
        weights = self.chestweights[self.level] 
        weight_total = 100 - random.randint(0, 100)
        i = len(weights) - 1
        for x in weights:
            if weight_total <= weights[i]:
                return i
            else:
                weight_total -= weights[i]
                i -= 1

    def Chests(self):
        result = []
        no_of_chests = round(len(self.enclosed_areas)/2)
        for x in self.enclosed_areas:
            result.append(((x), self.WeightedChance()))
            if len(result) == no_of_chests:
                break
        return result    
    
    def generate_chest_loot(self, type):

        items = []
        if type == 0:
            items.append(CreateRandomWeapon(1).make_weapon())
            items.append(CreateRandomWeapon(0).make_weapon())
            items.append(CreateRandomWeapon(0).make_weapon())
            items.append(Armour(0))
            items.append(HealingItem(0))
        if type == 1:
            items.append(CreateRandomWeapon(1).make_weapon())
            items.append(CreateRandomWeapon(2).make_weapon())
            items.append(CreateRandomWeapon(2).make_weapon())
            items.append(Armour(1))
            items.append(HealingItem(1))
        if type == 2:
            items.append(CreateRandomWeapon(3).make_weapon())
            items.append(CreateRandomWeapon(3).make_weapon())
            items.append(CreateRandomWeapon(2).make_weapon())
            items.append(Armour(2))
            items.append(HealingItem(2))
        return items
    def view_chest(self, items):
            clear_console()
            if len(items) == 0:
                pass
            
            print("Chest Contents:")
            
            weapons = [item for item in items if isinstance(item, Weapon)]
            display_weapons = [item.get_desc() for item in items if isinstance(item, Weapon)]
            for item in items:
                print(item.get_desc())
                    
            response = questionary.select(
                "What would you like to do?",
                choices=[
                    "Select from Weapons",
                    "Pick up Armour",
                    "Pick up Healing Item",
                    "Pick up all",
                    "Check self",
                    "Return to maze"
                ]
            ).ask()
            if response == "Select from Weapons":
                clear_console()
                display_weapons.append("Back")
                response = questionary.select(
                    "Which weapon would you like pick up?",
                    choices=display_weapons
                ).ask()
                if response == "Back":
                    return self.view_chest(items)
                chosen_weapon = weapons[display_weapons.index(response)]
                try:
                    self.player.pick_up(chosen_weapon)
                    items.remove(chosen_weapon)
                    print(f"You picked up [bold red]{chosen_weapon.get_name()}[/bold red]")
                    PlayerInput = getch.getch()
                    if PlayerInput:
                        return self.view_chest(items)
                except:
                    print("[bold red]You do not have enough space in your inventory to perform this action![/bold red]")
                    PlayerInput = getch.getch()
                    if PlayerInput:
                        return self.view_chest(items)
                
            elif response == "Pick up Armour":
                clear_console()
                for item in items:
                    if isinstance(item, Armour):
                        try:
                            self.player.pick_up(item)
                            items.remove(item)
                            print(f"You picked up [bold purple]{item.get_name()}[/bold purple]")
                            PlayerInput = getch.getch()
                            if PlayerInput:
                                return self.view_chest(items)
                        except:
                            print("[bold red]You do not have enough space in your inventory to perform this action![/bold red]")
                            PlayerInput = getch.getch()
                            if PlayerInput:
                                return self.view_chest(items)
            elif response == "Pick up Healing Item":
                clear_console()
                for item in items:
                    if isinstance(item, HealingItem):
                        try:
                            self.player.pick_up(item)
                            items.remove(item)
                            print(f"You picked up [bold blue]{item.get_name()}[/bold blue]")
                            PlayerInput = getch.getch()
                            if PlayerInput:
                                return self.view_chest(items)
                        except:
                            print("[bold red]You do not have enough space in your inventory to perform this action![/bold red]")
                            PlayerInput = getch.getch()
                            if PlayerInput:
                                return self.view_chest(items)
                
            elif response == "Pick up all":
                clear_console()
                try:
                    for item in items:
                        self.player.pick_up(item)
                    print("You picked everything up!")   
                    PlayerInput = getch.getch()
                    if PlayerInput:
                        pass
                except:
                    print("[bold red]You do not have enough space in your inventory to perform this action![/bold red]")
                    PlayerInput = getch.getch()
                    if PlayerInput:
                        return self.view_chest(items)
            elif response == "Check self":
                self.player.loadout()
                return self.view_chest(items)
            else:
                pass
    def NextLevel(self):
        
        self.startX, self.startY = 2*random.randint(0, self.mazeSize//2 - 1) + 1, 2*random.randint(0, self.mazeSize//2 - 1) + 1
        self.maze = self.Generate()
        self.min_distance = self.mazeSize//2
        self.exitX, self.exitY  = None, None
        self.enclosed_areas = None

    def TriggerBossBattle(self):
        boss = Boss()
        state = CombatTurnStateMachine(self.player, boss, True)
        while True:
            status = state.Check_Battle_Status()
            if status == "win":
                message(f"{boss.get_name()} wobbled and fell to their knees...\n", 0.2)
                message(f"You slowly walked over to them, bloodied and battered", 0.1)
                message(f"\nYou looked down at them, with a face of pity, before swiftly ending them in one swift blow...", 0.3)
                message(f"\nThe battle was over...", 0.1)
                good_end(self.player)
            if status == "lose":
                choose_end(self.player, boss)
            
            player_move = state.Choose()
            state.TransitionState()
            state.ImplementPlayer(player_move)   

            status = state.Check_Battle_Status()
            if status == "win":
                message(f"{boss.get_name()} wobbled and fell to their knees...\n", 0.2)
                message(f"You slowly walked over to them, bloodied and battered", 0.1)
                message(f"\nYou looked down at them, with a face of pity, before swiftly ending them in one swift blow...", 0.3)
                message(f"\nThe battle was over...", 0.1)
                good_end(self.player)
                
            if status == "lose":
                choose_end(self.player, boss)
            state.ImplementEnemyMove()

    def PlayerExplore(self):
        #set up maze and generate needed assets
        clear_console()
        self.mazeSize = 15 + self.level*4
        self.maze = self.Generate()
        enemies = self.SpawnEnemy()
        self.EndPos()
        chests = self.Chests()
        playerX, playerY = self.startX, self.startY
        
        #validation 
        def IsValidMove(maze, positionX, positionY):
            if positionX == self.exitX and positionY == self.exitY and not have_key:
                return False
            return 0 < positionX < self.mazeSize and 0 < positionY < self.mazeSize and not maze[positionY][positionX] or isinstance(maze[positionY][positionX], str)
        
        #initialise all entities
        have_key = False
        self.maze[self.startY][self.startX] = "◈"
        self.maze[self.exitY][self.exitX] = "E"
        chest_type = {}
        for x in chests:
            chestX, chestY = x[0][0], x[0][1]
            self.maze[chestY][chestX] = "T"
            chest_type[(chestX, chestY)] = x[1]
        key =  random.choice(list(chest_type.keys()))
        input("Note: '◈' is the player\n'E' is the exit\nenemies are random and invisible\n'T' is Treasure\nPress 'I' at any time to access your loadout")
        #maze exploration while loop
        
        alive = True
        while True:
            clear_console()
            if not alive:
                
                game_over()
                self.dead = True
                break
                
            else:    
                clear_console()
                
                self.PrintMaze(self.maze)
                print(f"LEVEL {self.level}")
                PlayerInput = getch.getch()
                
                
                for enemy in enemies:
                    if playerX == enemy[0] and playerY == enemy[1]:
                        clear_console()
                        print("You encountered an enemy!\nGet ready for Combat!")
                        enemies.remove((playerX, playerY))
                        enemy = Enemy(self.level)
                        state = CombatTurnStateMachine(self.player, enemy, False)
                        input()
                        while True:
                            status = state.Check_Battle_Status()
                            if status == "win":
                                self.player.reset()
                                self.player.get_gold(enemy)
                                print(f"For fighting {enemy.get_name()}, you were awarded {enemy.gold} Gold!")
                                input()
                                break
                            if status == "lose":
                                
                                alive = False
                                input()
                                break
                            player_move = state.Choose()
                            state.TransitionState()
                            state.ImplementPlayer(player_move)
                            status = state.Check_Battle_Status()

                            if status == "win":
                                self.player.reset()
                                self.player.get_gold(enemy)
                                print(f"For fighting {enemy.get_name()}, you were awarded {enemy.gold} Gold!")
                                input()
                                break
                            if status == "lose":
                                
                                alive = False
                                input()
                                break
                            if status == "run away":
                                print("You Ran Away and was awarded nothing...")
                                input()
                                break
                            state.ImplementEnemyMove()


                if PlayerInput == "i":
                    self.player.loadout()
                    
                if PlayerInput == "w":
                    if IsValidMove(self.maze, playerX, playerY-1):
                        self.maze[playerY][playerX] = False
                        playerY = playerY-1
                        self.maze[playerY][playerX] = "◈"
                        clear_console()
                        self.PrintMaze(self.maze)
                elif PlayerInput == "a":
                    if IsValidMove(self.maze, playerX-1, playerY):
                        self.maze[playerY][playerX] = False
                        playerX = playerX-1
                        self.maze[playerY][playerX] = "◈"
                        clear_console()
                        self.PrintMaze(self.maze)
                    
                elif PlayerInput == "s":
                    if IsValidMove(self.maze, playerX, playerY+1):
                        self.maze[playerY][playerX] = False
                        playerY = playerY+1
                        self.maze[playerY][playerX] = "◈"
                        clear_console()
                        self.PrintMaze(self.maze)
                    
                elif PlayerInput == "d":
                    if IsValidMove(self.maze, playerX+1, playerY):
                        self.maze[playerY][playerX] = False
                        playerX= playerX+1
                        self.maze[playerY][playerX] = "◈"
                        clear_console()
                        self.PrintMaze(self.maze)

                if (playerX, playerY) == (self.exitX, self.exitY):
                    if self.level == 4:
                        Boss = questionary.confirm("Warning, The next level is a Boss Battle. Are you sure you want to Continue?").ask()
                        
                        if Boss:
                            self.ending = True
                            self.TriggerBossBattle()
                            break
                        else:
                            break

                    self.level += 1
                    self.mazeSize += 4
                    print("Well done! You have completed the maze!")
                    again = questionary.confirm("Would you like to go to the next level?").ask()
                    if again:
                        self.NextLevel()
                        return self.PlayerExplore()
                    else:
                        self.mazeSize = 15
                        self.startX, self.startY = 2*random.randint(0, self.mazeSize//2 - 1) + 1, 2*random.randint(0, self.mazeSize//2 - 1) + 1
                        self.maze = self.Generate()
                        self.exitX, self.exitY  = None, None
                        self.enclosed_areas = None
                        break
                    

                if (playerX, playerY) in chest_type:
                    
                    type = chest_type[(playerX, playerY)]
                    
                    chest_items = self.generate_chest_loot(type)

                    open_chest = questionary.confirm("You found a chest! Would you like to Open it?").ask()
                    if open_chest:
                        self.view_chest(chest_items)
                        if (playerX, playerY) == key:
                            input("In a corner of the Chest you found A key!⚿ You can now Leave!")
                            have_key = True
                        del chest_type[(playerX, playerY)]
                    else:
                        pass

player = Player("Ryan", 50, 2, 100)

maze = Maze(player)











 