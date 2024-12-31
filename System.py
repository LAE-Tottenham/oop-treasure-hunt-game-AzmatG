import questionary
import os
import platform
from art import text2art
import time
import sys
import getch


def clear_console():
    if platform.system() == "Windows":
        os.system("cls")  
    else:
        os.system("clear")  
def message(sentence, delay):
    for char in sentence:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
def get_name():
    response = questionary.text(
    "What is your name?",
    validate=lambda text: text.isalpha() or "Please enter a valid name!"
    ).ask()
    confirm = questionary.confirm(f"{response}... Is this correct?").ask()
    if confirm:
        return response
    else:
        return get_name()
def game_over():
    Art = text2art("GAME OVER!")
    print(Art)
def menu():
    clear_console()
    Art = text2art("WELOCOME TO\n             TSUBAKI")
    print(Art)
    response = questionary.select(
        "What would you like to do",
        choices=[
            "Start Game!",
            "Tutorial!",
            "Leave..."
        ]
    
    ).ask()
    if response == "Start Game!":
        return "starting game"
    if response == "Tutorial!":
        message("The main purpose of the game is to complete all levels of the maze and kill the boss, ending the game. To access your loadout, press 'i' in the lobby\nYou will be reminded of this in the maze so do not worry. Be careful though! You only get one life!\nAnything else is self explanatory so I will leave you be.\nHave fun!", 0.03)
        print("\npress any key to continue...")
        Input = getch.getch()
        
        if Input:

            return menu()
    if response == "Leave...":
        print("Leaving...")
        time.sleep(3)
def good_end(player):
    clear_console()
    message(f"And so, Salé's curse was lifted, and no longer would the 5...No 4 Great Entities ruin the land of fear-stricken people...", 0.05)
    message("\nThere was \n", 0.05)
    message("HOPE", 0.3)
    time.sleep(3)
    message(f"\nThe warrior...The hero of Tsubaki...{player.get_name()} would not stop here", 0.1)
    time.sleep(3)
    message("\nAfter all...", 0.05)
    message("\nThere was 4 left...", 0.3)
    art = text2art("Good Ending")
    message(art, 0.01)
def choose_end(player, boss):
    clear_console()
    message("\n...", 0.5)
    message(f"{boss.get_name()} looked down at you with an unreadable gaze...\n", 0.1)
    message(f"Warrior...\nThats what they call people like you in this land right?", 0.1)
    message(f"\nYou looked at {boss.get_name()} with shock... \nHe could talk?", 0.1)
    time.sleep(1)
    message("Your strength is admirable...", 0.1)
    message("\nI'll give you a choice warrior...", 0.2)
    message("\nJoin me or...", 0.2)
    time.sleep(1)
    message("DIE\n", 1)
    join = questionary.confirm("Warning! This Choice will determine the ending of the game!... Would you join the Raiju").ask()
    if join:
        message(f"\nAh...I knew you could be trusted...", 0.05)
        message("\nCome. We have many things to discuss", 0.1)
        time.sleep(3)
        message(f"\n\nAnd so, the journey of {player.get_name()} ended. The fallen hero of Tsubaki, A villain who would eventually cause its destruction\n", 0.1)
        art = text2art("Bad Ending")
        message(art, 0.01)
    else:
        message("...\n", 0.5)
        message("Ah, i see...Die\n", 0.1)
        message(f"With a heavy strike, {boss.get_name()} ended your life\n", 0.1)
        art = text2art("Neutral Ending")
        message(art, 0.01)