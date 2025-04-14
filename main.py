from playerclass import *
from roomdefinitions import *
from random import *
from sprites import *
from ast import literal_eval
from sys import exit

savedec = input("""Before you begin, a wizard appears to you and says something strange about savefiles. Though your character is confused as to what he is talking about, perhaps you might understand.

        He asks which savefile you would like to load.

            1) Save 1
            2) Save 2
            3) Save 3
            4) Save 4
            5) List the stats of each save.\n\n\n\n""")

while True:

    if savedec == "5":

        for i in range(1,5):

            with open(f"savefile-{i}.txt", "r") as savefile:
                values = savefile.read()
            
            print(f"""Savefile {i}:

                  {values}""")

        savedec = input("\n\nNow, you can make your decision. Which savefile would you like to load?\n\n\n\n")
    
    elif savedec not in ("1", "2", "3", "4"):
        savedec = input(f"You try to load save {savedec}, but it doesn't exist. Choose something else.\n\n\n\n")

    else:
        break
    
savefile = f"savefile-{savedec}.txt"

with open(savefile, "r") as save:
    save = save.read()
    save = literal_eval(save)

if save.get("playertype") == "TBD":

    playertype = input("""You will soon embark on your journey, fighting the horrible Glitch.
            A kind wizard appears next to you. He asks what class you would like to play.
        He gives you the following four options, and tells you to respond with your choice's corresponding letter.

                   a) Barbarian
                   b) Tank
                   c) Healer
                   d) Warrior
                Choose wisely, as your choice determines your strength, and the weapons that you will be using.\n\n""").lower()

    while True:
        if playertype in ("a", "b", "c", "d"):
            player = Player({"a": "barbarian", "b": "tank", "c": "healer", "d": "warrior"}.get(playertype), save, savefile)
            break
        else:
            playertype = input("\nHe tells you to just use the letter alone. Don't include brackets or anything.\n\n")

else:
    player = Player(save.get("playertype"), save, savefile)

scene = ""

print("""At any time in this playthrough, you can use the following commands.
      1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
      2) scene -- This prints out the current scene using coloured ASCII art.
      3) help -- This will print out this exact string of text you are seeing right now!
      4) exit/quit -- These will quit out of the game. Don't worry, your progress will be saved to the savefile you chose.\n""")

import builtins as b  # looks wonky but i need to do this

stdinput = input

special_commands_func = {
    "exit": exit,
    "quit": exit}

special_commands = {
    "stats": player.stats,
    "scene": scene,
    "help": """At any time in this playthrough, you can use the following commands.
    1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
    2) scene -- This prints out the current scene using coloured ASCII art.
    3) help -- This will print out this exact string of text you are seeing right now!
    4) exit/quit -- These will quit out of the game. Don't worry, your progress will be saved to whatever savefile you chose.\n"""}

def custom_input(prompt=""):
    
    while True:
        user_input = stdinput(prompt).strip().lower()
        if user_input in special_commands.keys():
            print(special_commands[user_input])
            continue
        elif user_input in special_commands_func.keys():
            special_commands[user_input]
            continue
        return user_input

b.input = custom_input

def stdmvmt():
    mvmtdecision = input("""\n\nYou can now move in any direction. You can also see a map of the rooms you've been to.

                         a) Up.
                         b) Down.
                         c) Left.
                         d) Right.
                         e) Map.\n\n""")
    while True:
        try:
            mvmtdecision = {"a": "up", "b": "down", "c": "left", "d": "right", "e": "map"}[mvmtdecision]
            break
        except TypeError:
            mvmtdecision = input("\nJust use the letter alone. Don't include brackets or anything.\n\n")

    if mvmtdecision == "e":
        pass

    return mvmtdecision

print("\n\nYou wake up in a completely empty room; all by yourself. Four doors appear at your front, back, left and right. You realise that you'll be stuck here quite a while...")

while True:

    stdmvmt()
    difficulty = player.level // 2.5
    room = choice((ShootRoom(difficulty, player),
                   DungeonRoom(randint(15,25), difficulty, player),
                   DungeonRoom(randint(15,25), difficulty, player),
                   TripleDoorRoom(difficulty, player),
                   EmptyRoom(player)))
