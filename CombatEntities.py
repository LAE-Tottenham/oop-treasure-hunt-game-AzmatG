import questionary
from rich.console import Console
from rich.progress import Progress
from rich import print
from BaseEntity import Entity
from Items import Item, Weapon, Armour, HealingItem, CreateRandomWeapon
from System import clear_console
import getch 
import random
console = Console()

class Player(Entity):
    def __init__(self, name, hp, DMG, stamina):
        super().__init__(name, hp, DMG, stamina)
        self.currentweapon = ""
        self.currentarmour = ""
        self.inventory = []
        self.gold = 0
    def equip(self, item):
        if type(item) == Weapon:
            if self.currentweapon == "":
                self.set_DMG(item.get_DMG())
                self.currentweapon = item
            else:
                self.set_DMG(self.currentweapon.get_DMG()*-1)
                self.set_DMG(item.get_DMG())
                self.currentweapon = item
        elif type(item) == Armour:
            if self.currentarmour == "":
                self.set_hp(item.get_def())
                self.currentarmour = item
                
            else:
                self.set_hp(self.currentarmour.get_def()*-1)
                self.set_hp(item.get_def())
                self.currentarmour = item
                
        else:
            input("This is not a compatible usage of the equip function")
        
        
        pass
    def pick_up(self, object):
        if len(self.inventory)<15:
            self.inventory.append(object)
        else:
            raise Exception("Inventory is already full")
    def get_gold(self, enemy):
        self.gold += enemy.gold 
    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
        else:
            raise Exception("Not enough Gold")
    def drop_item(self, object):
        if object in self.inventory:
            self.inventory.remove(object)
        else:
            raise Exception("An issue occured")
    def heal(self, item):
        self.set_hp(item.get_heal())
        self.inventory.remove(item)
        if self.get_hp() > self.get_max_hp():
            self.normalise_hp()
    def get_max_health(self):
        if self.currentarmour != "":
            return self.get_max_hp() + self.currentarmour.get_def()
        return self.get_max_hp()
    
    def defend(self):

        self.set_guard(True)

    def view_stats(self):
    
        with Progress(console=console) as progress:
            progress.add_task("[bold red]HP", total=self.get_max_health(), completed=self.get_hp())
            progress.add_task("[bold green]Stamina", total=self.get_max_stamina(), completed=self.get_stamina())
            progress.add_task("[bold purple]DMG", total=self.get_max_DMG(), completed=self.get_DMG())
            
    def view_enemy(self, enemy):
        with Progress(console=console) as progress:
            progress.add_task("[bold red]HP", total=enemy.get_max_hp(), completed=enemy.get_hp())
            progress.add_task("[bold green]Stamina", total=enemy.get_max_stamina(), completed=enemy.get_stamina())
            progress.add_task("[bold purple]DMG", total=enemy.get_max_DMG(), completed=enemy.get_DMG())
    def loadout(self):
        clear_console()
        print(f"You currently have {self.gold} Gold!")
        response = questionary.select(
            "What would you like to check?",
            choices=[
                "Check Current Loadout",
                "Check Items",
                "Check Weapons",
                "Check Armour",
                "Equip from inventory",
                "Drop Items",
                "Back..."
            ]).ask() 
        
        if response == "Check Current Loadout":
            clear_console()
            if self.currentweapon == "":
                print("You currently have no weapons equiped!")
            if self.currentweapon:
                print(f"Your current Weapon is: [bold red]{self.currentweapon.get_desc()}[/bold red]")
            if self.currentarmour == "":
                print("You currently have no armour equiped!")

            if self.currentarmour:
                print(f"Your current Armour is: [bold purple]{self.currentarmour.get_desc()}[/bold purple]")
            PlayerInput = getch.getch()
            if PlayerInput:
                return self.loadout()
            
        elif response == "Check Items":
            clear_console()
            items = []
            for item in self.inventory:
                if isinstance(item, HealingItem):
                    items.append(item)
            if len(items) == 0:
                print("Nothing to see here...")
            for item in items:
                print(f"[bold blue]{item.get_desc()}[/bold blue]")
            PlayerInput = getch.getch()
            if PlayerInput:
                return self.loadout()
        elif response == "Check Weapons":
            clear_console()
            weapons = []
            for item in self.inventory:
                if isinstance(item, Weapon) and item != self.currentweapon:
                    weapons.append(item)
            if len(weapons) == 0:
                print("Nothing to see here...")
            for item in weapons:
                print(f"[bold red]{item.get_desc()}[/bold red]")
            PlayerInput = getch.getch()
            if PlayerInput == '\n' or PlayerInput == '\r':
                return self.loadout()
        elif response == "Check Armour":
            clear_console()
            armour = []
            for item in self.inventory:
                if isinstance(item, Armour) and item != self.currentarmour:
                    armour.append(item)
            if len(armour) == 0:
                print("Nothing to see here...")
            for item in armour:
                print(f"[bold purple]{item.get_desc()}[/bold purple]")
            PlayerInput = getch.getch()
            if PlayerInput == '\n' or  PlayerInput == '\r':
                return self.loadout()
        if response == "Equip from inventory":
            clear_console()
            
            
            response = questionary.select(
                "What would you like to equip?",
                choices=[
                    "Weapon",
                    "Armour",
                    "Back"
                ]
            ).ask()
            if response == "Weapon":
                clear_console()
                if self.currentweapon == "":
                    print("You currently have no weapons equiped!")
                
                else:
                    print(f"Your current Weapon is: [bold red]{self.currentweapon.get_desc()}[/bold red]")
                
                weapons = [item for item in self.inventory if isinstance(item, Weapon) and item != self.currentweapon]
                choices = [item.get_desc() for item in self.inventory if isinstance(item, Weapon) and item != self.currentweapon]
                if len(weapons) == 0:
                    print("Nothing to see here...") 
                    PlayerInput = getch.getch()
                    if PlayerInput:
                        return self.loadout()
                response = questionary.select(
                    "Available Weapons...",
                    choices=[item.get_desc() for item in self.inventory if isinstance(item, Weapon) and item != self.currentweapon]
                ).ask()
                clear_console()
                chosen_weapon = weapons[choices.index(response)]
                self.equip(chosen_weapon)
                print(f"You have now equiped The [bold red]{chosen_weapon.get_name()}[/bold red]")
                PlayerInput = getch.getch()
                if PlayerInput:
                    return self.loadout()
            elif response == "Armour":
                clear_console()
                if self.currentarmour == "":
                    print("You currently have no armour equiped!")
                else:
                    print(f"Your current Armour is: [bold purple]{self.currentarmour.get_desc()}[/bold purple]")
                armours = [item for item in self.inventory if isinstance(item, Armour)]
                choices = [item.get_desc() for item in self.inventory if isinstance(item, Armour)]
                if len(armours) == 0:
                    print("Nothing to see here...") 
                    PlayerInput = getch.getch()
                    if PlayerInput:
                        return self.loadout()
                response = questionary.select(
                    "Available Armour...",
                    choices=[item.get_desc() for item in self.inventory if isinstance(item, Armour)]
                    ).ask()
                clear_console()
                chosen_armour = armours[choices.index(response)]
                self.equip(chosen_armour)
                print(f"You have now equiped The [bold purple]{chosen_armour.get_name()}[/bold purple]")
                PlayerInput = getch.getch()

                if PlayerInput:
                    return self.loadout()
            else:
                return self.loadout()
        if response == "Drop Items":

            if len(self.inventory) > 0:
                items = [item for item in self.inventory if item != self.currentarmour and item != self.currentweapon]
                choices = [item.get_name() for item in self.inventory if item != self.currentarmour and item != self.currentweapon]
                choices.append("Back")
                response = questionary.select(
                    "What would you like to drop",
                    choices=choices
                ).ask()
                if response == "Back":
                    return self.loadout()
                chosen_item = items[choices.index(response)]
                self.drop_item(chosen_item)
                print(f"You have dropped {response}")
                PlayerInput = getch.getch()
                if PlayerInput:
                    return self.loadout()
            else:

                print("You have no items!")
                PlayerInput = getch.getch()
                if PlayerInput:
                    return self.loadout()
                
        else:
            pass
class Enemy(Entity):
    def __init__(self, level):
        if level == 0:

            names = ["Skeleton", "Goblin", "Skeleton with a Helmet"]
            name = names[random.randint(0, len(names)-1)]
            hp = 200
            DMG = 10
            stamina = 100
            self.gold = 15
        if level == 1:

            names = ["Large Skeleton", "Ogre", "Shrouded Figure"]
            name = names[random.randint(0, len(names)-1)]
            hp = 300
            DMG = 20
            stamina = 100
            self.gold = 50
        if level == 2:

            names = ["Sneaky Goblin", "Skeleton Warrior", "Green Laekan"]
            name = names[random.randint(0, len(names)-1)]
            hp = 400
            DMG = 20
            stamina = 100
            self.gold = 100
        if level == 3:

            names = ["Undead Corpse", "Faller", "Vampire", "Beast"]
            name = names[random.randint(0, len(names)-1)]
            hp = 500
            DMG = 30
            stamina = 150
            self.gold = 200

        if level == 4:
            names = ["Madness of Stereo", "Sary Never Clear", "Griefer", "Ashquan", "Kaiden"]
            name = names[random.randint(0, len(names)-1)]
            hp = 1000
            DMG = 50
            stamina = 200
            self.gold = 500
        super().__init__(name, hp, DMG, stamina)
    def defend(self):
        self.set_guard(True)
        
    def random_move(self):
        move_prob = [70, 20, 10] # attack defend or nothing
        prob_total = 100 - random.randint(0, 100)
        i = len(move_prob) - 1
        for prob in move_prob:
            if prob_total <= move_prob[i]:
                return i
            else:
                prob_total -= move_prob[i]
                i -= 1
    
        
class Boss(Entity):
    def __init__(self):
        names = ["Leader of The Raiju, Nosferatu Zodd", "Bringer of Calamity, Ashen One", "Solo Leveller"]
        name = names[random.randint(0, len(names)-1)] 
        hp = 2000
        DMG = 50
        stamina = 300
        super().__init__(name, hp, DMG, stamina)
    def heal(self):
        self.set_hp(10)
    def defend(self):
        self.get_guard = True
    def big_attack(self, player):
        player.set_hp(self.get_DMG()*-5 if not player.get_guard() else self.get_DMG()*-2)  
    def random_move(self):
        move_prob = [70, 25, 5] #attack defend or big attack
        prob_total = 100 - random.randint(0, 100)
        i = len(move_prob) - 1
        for prob in move_prob:
            if prob_total <= move_prob[i]:
                return i
            else:
                prob_total -= move_prob[i]
                i -= 1

player = Player("Ryan", 200, 20, 100)
enemy = Enemy(1)
boss = Boss()


random_dagger = CreateRandomWeapon(0)
random_stick = CreateRandomWeapon(3)
dagger1 = random_dagger.make_weapon()
dagger2 = random_dagger.make_weapon()
armour1 = Armour(2)
armour2 = Armour(1)
Heal1 = HealingItem(2)
player.pick_up(Heal1)
player.pick_up(dagger1)
player.pick_up(dagger2)
player.pick_up(armour1)
player.pick_up(armour2)
#print(enemy.random_move())

#print(player.view_stats())
#print(player.currentweapon.get_desc())
#player.loadout()
