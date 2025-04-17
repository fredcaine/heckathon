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

            with open(f"savefiles/savefile-{i}.txt", "r") as savefile:
                values = savefile.read()
            
            print(f"""Savefile {i}:

                  {values}""")

        savedec = input("\n\nNow, you can make your decision. Which savefile would you like to load?\n\n\n\n")
    
    elif savedec not in ("1", "2", "3", "4"):
        savedec = input(f"You try to load save {savedec}, but it doesn't exist. Choose something else.\n\n\n\n")

    else:
        break
    
savefile = f"savefiles/savefile-{savedec}.txt"

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

print("""At any time in this playthrough, you can use the following commands:-

      1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
      2) scene -- This prints out the current scene using coloured ASCII art.
      3) help -- This will print out this exact string of text you are seeing right now!
      4) credits -- This will tell you the collaborators on this game, and what they've contributed.
      5) exit/quit -- These will quit out of the game. Don't worry, your progress will be saved to the savefile you chose.
      6) save -- This will manually save your progress (including what room you're in, your health, your level, etc.). Don't worry though, the game will auto-save every time you take damage, go to a new room, etc..\n""")

import builtins as b  # looks wonky but i need to do this

stdinput = input

def scenemaker():
    enemysprites = []
    for enemy in player.cur_room_class.contained_enemies: enemysprites.append(sprites[" ".join(enemy.identify_type().split(sep=" ")[1:])])
    print(create_scene(sprites[player.cur_room], enemysprites, sprites[player.playertype], sprites[player.weapon]))

special_commands_func = {
        "exit": lambda: exit(),
        "quit": lambda: exit(),
        "save": lambda: player.save(),
        "scene": lambda: scenemaker()}

special_commands = {
        "stats": "You might want to exit, then run the program again on this savefile to refresh these, but anyway...\n\n" + player.stats,
        "help": """At any time in this playthrough, you can use the following commands.
    1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
    2) scene -- This prints out the current scene using coloured ASCII art.
    3) help -- This will print out this exact string of text you are seeing right now!
    4) credits -- This will tell you the collaborators on this game, and what they've contributed.
    5) exit/quit -- These will quit out of the game. Don't worry, your progress will be saved to whatever savefile you chose.
    6) save -- This will manually save your progress (including what room you're in, your health, your level, etc.). Don't worry though, the game will auto-save every time you take damage, go to a new room, etc..\n""",
    "credits": """
    All the code        --          Fredrick Wans   8U
    All the sprites     --          Hassan Saheb    8K
    Emotional support   --          Ahmed Sayed     8N  (also was in charge of pissing off Fredrick, (me))\n\n"""}


def custom_input(prompt=""):  # so that scene works

    prompt = "\033[0m" + prompt
    while True:
        user_input = stdinput(prompt).strip().lower()
        if user_input in special_commands.keys():
            print(special_commands[user_input])
            continue
        elif user_input in special_commands_func.keys():
            special_commands_func[user_input]()
            continue
        return user_input

b.input = custom_input

def stdmvmt():
    mvmtdecision = input("""\n\nYou can now move in any direction.

                         a) Up.
                         b) Down.
                         c) Left.
                         d) Right.\n\n\n""")


    while True:
        if mvmtdecision in ("a", "b", "c", "d"):
            break
        else:
            mvmtdecision = input("\nJust use the letter alone. Don't include brackets or anything.\n\n\n")
    return mvmtdecision

cur_room = save.get("checkpoint")

if cur_room != None:
    print(f"\nYou left off last time in a {save.get('checkpoint')} room.")
else:
    print("\n\nYou wake up in a completely empty room; all by yourself. Four doors appear at your front, back, left and right. You realise that you'll be stuck here quite a while...")
    cur_room = "start"
    player.save()

difficulty = (player.level // 3.5) + 1

rooms = (lambda: ShootRoom(difficulty, player),
         lambda: DungeonRoom(randint(15,25), difficulty, player),
         lambda: DungeonRoom(randint(15,25), difficulty, player),
         lambda: TripleDoorRoom(difficulty, player),
         lambda: TripleDoorRoom(difficulty, player),
         lambda: TripleDoorRoom(difficulty, player),
         lambda: EmptyRoom(player),
         lambda: EmptyRoom(player),
         lambda: EmptyRoom(player))
formatted_rooms = ("shoot", "dungeon", "dungeon", "triple door", "triple door", "triple door", "empty", "empty", "empty")


if cur_room == "dungeon":
    room = DungeonRoom(randint(15,25), difficulty, player)
elif cur_room == "triple door":
    room = TripleDoorRoom(difficulty, player)
elif cur_room == "shoot":
    room = ShootRoom(difficulty, player)
elif cur_room == "empty":
    room = EmptyRoom(player)

while True:

    stdmvmt()
    roomchoice = randint(0,8)
    formatted_room = formatted_rooms[roomchoice]
    room = rooms[roomchoice]()
    player.save()
