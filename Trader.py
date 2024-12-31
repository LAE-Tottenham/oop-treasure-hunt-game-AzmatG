
#Buy weapons, armour and health potions => TradeEvent()
#A place to talk and get infomation => TalkEvent()
#A place to get side quests, simpke things like getting a certain weapon QuestGiverEvent()
#attributes => none
#methods => GiveIntro() TradeEvent() TalkEvent() QuestGiverEvent()
import questionary
from rich import print
from System import clear_console
from CombatEntities import Player
import time
from Items import CreateRandomWeapon, Armour, HealingItem
clear_console()
class Trader():
    def __init__(self):
        self.name = "Hanayome"
        self.quests = []
        
        self.weapons = [(CreateRandomWeapon(1).make_weapon(), 1), (CreateRandomWeapon(2).make_weapon(), 2), (CreateRandomWeapon(2).make_weapon(), 2), (CreateRandomWeapon(3).make_weapon(), 3)]
        self.display_weapons  = []
        for x in self.weapons:
            if x[1] == 1:
                self.display_weapons.append(f"{x[0].get_desc()} || 100 Gold")
            if x[1] == 2:
                self.display_weapons.append(f"{x[0].get_desc()} || 500 Gold")
            if x[1] == 3:
                self.display_weapons.append(f"{x[0].get_desc()} || 1000 Gold")
        self.display_weapons.append("Back")
        self.armour = [(Armour(1), 1), (Armour(2), 2)]
        self.display_armour = []
        for x in self.armour:
            if x[1] == 1:
                self.display_armour.append(f"{x[0].get_desc()} || 100 Gold")
            if x[1] == 2:
                self.display_armour.append(f"{x[0].get_desc()} || 500 Gold")
        self.display_armour.append("Back")
    def give_intro(self):
        print(f"[bold green]Hello Travellor[/bold green]! My name is [bold blue]{self.name}[/bold blue]. [bold yellow]The Worlds best Tradesman[/bold yellow]. Whatever you want, I'll cater! Whether it be [bold red]strengthening yourself[/bold red], buying a few [bold green]safety precautions[/bold green] or finding some neat [bold purple]quests[/bold purple] Im here for you! If a [bold blue]chat[/bold blue] is all you need, Ill be here too. Pleasure to make your aquaintance")
    def events(self, player):
        
        action = questionary.select(
            "What would you like to do?",
            choices= [
            "Strengthen self",
            "Potions",
            "Quests",
            "Talk", 
            "Maybe later..."
            ]
        ).ask()
        if action == "Strengthen self":
            clear_console()
            print("Ah, seeking greater power! Lets see what I can do for you...")
            self.buy_arms(player)
            return self.events(player)
        elif action == "Potions":
            clear_console()
            print("Looking for potions, are you? I've got just the thing!")
            self.buy_potions(player)
            return self.events(player)
        elif action == "Quests":
            clear_console()
            print("Ah, A thirst for adventure compels you ey? Let me sort you out!")
            self.quest_giver_event(player)
            return self.events(player)
        elif action == "Talk":
            clear_console()
            print("[bold]A chat it is!")
            self.talk_event(player)
            return self.events(player)
        elif action == "Maybe later...":
            clear_console()
            print("I see.. Maybe next time!")

    def talk_event(self, player):
        response = questionary.select(
            "What should we talk about!",
            choices= [
                "What is this place?",
                "What are Raiju?",
                "Why do people keep going into mazes?",
                "How do we get rid of the Raiju?",
                "How do I get Gold?",
                "Hello!",
                "Back"
                ]
        ).ask()
        if response == "What is this place?":
            print("We are a humble village, Salé, in the outskirts of [bold purple]Tsubaki[/bold purple]. While we may not be as extravagent or powerful as other villages , our strong sense of [bold yellow]community[/bold yellow] helps us thrive. We make a living off of passing trade with travellors such as [bold green]you[/bold green]. Its peaceful...Though, things has started to change recently... we fear for the worst since the arrival of the [bold red]Raiju.")
            input()
            clear_console()
            return self.talk_event(player)
        elif response == "What are Raiju?":
            print("[bold red]The Raiju[/bold red]... They're not like us. One day, a new world addition to the [bold]five great mysteries of Tsubaki[/bold] appeared abruptly. A maze. Grand yet desolate. Its achitecture truly unparalleled. A true wonder. It was met with curiosity at first. We were not sure of what to think. However, after the [bold red]Mayor[/bold red] went inside... We don't speak of what happened. Its all their fault. The [bold]Raiju. They dont belong in our realm.")
            input()
            clear_console()
            return self.talk_event(player)
        elif response == "Why do people keep going into mazes?":
            print("To change our reality. No matter how overwhelming the task, humans like us, we [bold yellow]struggle[/bold yellow], we [bold yellow]fight[/bold yellow] and [bold yellow]never yield[/bold yellow]. All in hopes of carving a beautiful future for the next generation, entrusting the same task to them... Too much?")
            input()
            clear_console()
            return self.talk_event(player)
        elif response == "How do we get rid of the Raiju?":
            print("We dont know. We've sent countless recon groups into the maze, none of them have made it back. However, a great being is sensed at the end of the maze, we assume if [bold red]'He'[/bold red] is slayed, all will revert back to how it was, how it should be.")
            input()
            clear_console()
            return self.talk_event(player)
        elif response == "How do I get Gold?":
            print("Well, without a job, theres only one way. Being a Maze Hunter. We do not know why but, The Raiju love carrying around gold... If your considering going, be careful yeah?")
            print("Also, before I forget. Bring a couple items from the maze to me and I'll take it from you for Gold!")
            input()
            
            return self.talk_event(player)
        elif response == "Hello!":
            print("[bold purple]Hi?...... I know i said I'd chat with you but, this really isnt what i had in mind")
            input()
            clear_console()
            return self.talk_event(player)
        else:
            clear_console()
            return self.events(player)

    def quest_giver_event(self, player):
        
        response = questionary.select(
            "Here are the Available Quests:",
            
            choices=[
                "Bring me a Stick of any Kind || 1000 Gold",
                "Bring me An Abyssal Blade || 500 Gold",
                "Bring me 夜の剣 || 500 Gold",
                "Bring me a Broken Dagger || 100 Gold",
                "Back"
            ]
        ).ask()
        if response == "Bring me a Stick of any Kind || 1000 Gold":
            sticks = ["Stick of Doom", "Brownest Stick", "Stick of Calamity", "STICKY situation", "Simple Stick"]
            have_item = False
            for item in player.inventory:
                if item.get_name() in sticks:
                    have_item = True
                    break
            if have_item:
                player.gold += 1000
                print("Wow... Ive heard a lot about the Sticks but...Seeing one in person truly is a marvel. Thank you. Take this...\n+1000 Gold!")
                time.sleep(3)
            else:
                print("You do not have a Stick... Perhaps take a look in the upper levels of the maze?")
                time.sleep(3)
            clear_console()
            return self.events(player)
        
        if response == "Bring me An Abyssal Blade || 500 Gold":
            have_item = False
            for item in player.inventory:
                if item.get_name() == "Abyssal Blade":
                    have_item = True
                    break
            if have_item:
                player.gold += 500
                print("It is a beauty isn't it? Here, Take this\n+500 Gold!")
                time.sleep(3)
            else:
                print("You do not have an Abyssal Blade... Perhaps take a look in the middle levels of the maze?")
                time.sleep(3)
            clear_console()
            return self.events(player)
        if response == "Bring me 夜の剣 || 500 Gold":
            have_item = False
            for item in player.inventory:
                if item.get_name() == "夜の剣":
                    have_item = True
                    break
            if have_item:
                player.gold += 500
                print("The blade of the Night, 夜の剣. it doesn't get much better than this... Here, Take this\n+500 Gold!")
                time.sleep(3)
            else:
                print("You do not have a 夜の剣... Perhaps take a look in the middle levels of the maze?")
                time.sleep(3)
            clear_console()
            return self.events(player)
        if response == "Bring me a Broken Dagger || 100 Gold":
            have_item = False
            for item in player.inventory:
                if item.get_name() == "Broken Dagger":
                    have_item = True
                    break
            if have_item:
                player.gold += 100
                print("A Broken Dagger... No doubt left behind by a fallen hunter... I'll make sure to deliver this to their family...thank you") 
                print("100 Gold!")
                time.sleep(3)
            else:
                print("You do not have a Broken Dagger... Perhaps take a look in the Lower levels of the maze?")
                time.sleep(3)
            clear_console()
            return self.events(player)
        if response == "Back":
            return self.events(player)
    def buy_arms(self, player):
        
        response = questionary.select(
            "Have a look!",
            choices = [
            "Weaponry",
            "Armour",
            "Back"
            ]
        ).ask()

        if response == "Weaponry":
            response = questionary.select(
                "Have A look!",
                choices=self.display_weapons
            ).ask()
            response_index = self.display_weapons.index(response)
            if response_index != len(self.display_weapons)-1:
                chosen_weapon = self.weapons[response_index][0]

            if response_index ==0:
                if player.gold >= 100:
                    verify = questionary.confirm("Are you Sure?").ask()
                    if verify:
                        player.gold -= 100
                        player.pick_up(chosen_weapon)
                        print(f"You purchased the {chosen_weapon.get_name()}!")
                else:
                    print("You do not have enough Gold!")
                
            if response_index == 1:
                if player.gold >= 500:
                    verify = questionary.confirm("Are you Sure?").ask()
                    if verify:
                        player.gold -= 300
                        player.pick_up(chosen_weapon)
                        print(f"You purchased the {chosen_weapon.get_name()}!")
                else:
                    print("You do not have enough Gold!")
                
            if response_index == 2:
                if player.gold >= 500:
                    verify = questionary.confirm("Are you Sure?").ask()
                    if verify:
                        player.gold -= 300
                        player.pick_up(chosen_weapon)
                        print(f"You purchased the {chosen_weapon.get_name()}!")
                else:
                    print("You do not have enough Gold!")
                
            if response_index == 3:
                if player.gold >= 1000:
                    verify = questionary.confirm("Are you Sure?").ask()
                    if verify:
                        player.gold -= 1000
                        print(f"You purchased the {chosen_weapon.get_name()}!")
                else:
                    print("You do not have enough Gold!")
                
            if response_index == 4:
                return self.buy_arms(player)
            time.sleep(3)
            clear_console()
            return self.buy_arms(player)
        elif response == "Armour":
            
            response = questionary.select(
            "Have a look!",
            choices=self.display_armour
            ).ask()
            response_index = self.display_armour.index(response)
            if response_index == 0:
                if player.gold >= 100:
                    verify = questionary.confirm("Are you Sure?").ask()
                    if verify:
                        player.gold -= 100
                        player.pick_up(self.armour[0][0])
                        print("You purchased the Cat Disguise!")
                else:
                    print("You do not have enough Gold!")
            if response_index == 1:
                if player.gold >= 100:
                    verify = questionary.confirm("Are you Sure?").ask()
                    if verify:
                        player.gold -= 500
                        player.pick_up(self.armour[1][0])
                        print("You purchased the Typical School Uniform!")
                else:
                    print("You do not have enough Gold!")

            if response_index == 2:
                return self.buy_arms(player)
            time.sleep(3)
            clear_console()
            return self.buy_arms(player)
        else:
            return self.events(player)
        
    def buy_potions(self, player):

        choices = [HealingItem(0), HealingItem(1), HealingItem(2)]
        display = [f"{HealingItem(0).get_desc()} || 25 Gold", f"{HealingItem(1).get_desc()} || 100 Gold", f"{HealingItem(2).get_desc()} || 150 Gold"]

        display.append("Back")
        response = questionary.select(
            "Have a look!",
            choices = display
        ).ask() 
        index = display.index(response)
        if index == 0:
            confirm = questionary.confirm("Are you sure?").ask()
            if confirm:
                print(f"You purchased the {choices[index].get_name()}!")
                player.gold -= 25
                player.pick_up(choices[index])
        if index == 1:
            confirm = questionary.confirm("Are you sure?").ask()
            if confirm:
                print(f"You purchased the {choices[index].get_name()}!")
                player.gold -= 100
                player.pick_up(choices[index])
        if index == 2:
            confirm = questionary.confirm("Are you sure?").ask()
            if confirm:
                print(f"You purchased the {choices[index].get_name()}!")
                player.gold -= 150
                player.pick_up(choices[index])
        if index == 3:
            return self.events(player)
        time.sleep(3)
        clear_console()
        return self.events(player)
    
player = Player("Izhaan", 100, 10, 100)
player.gold += 0
trader = Trader()
#trader.give_intro()
#trader.events(player)
