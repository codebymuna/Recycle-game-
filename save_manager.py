"""
save_manager.py

Handles saving and loading the player's game progress.
"""

import os

from items import (
    water_bottle,
    newspaper,
    drink_can,
    cardboard_box,
    paper_flyer,
    empty_bottle,
    metal_can,
    snack_wrapper
)


SAVE_FOLDER = "saves"
SAVE_FILE = "saves/savegame.txt"


# Dictionary used to find an item when loading the save file.
ITEMS = {
    "Water bottle": water_bottle,
    "Newspaper": newspaper,
    "Drink can": drink_can,
    "Cardboard box": cardboard_box,
    "Paper flyer": paper_flyer,
    "Empty bottle": empty_bottle,
    "Metal can": metal_can,
    "Snack wrapper": snack_wrapper
}


def save_game(player):
    """
    Save the player's progress to a text file.

    Parameters:
        player: The current Player object.
    """

    # Create the saves folder if it does not exist.
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    with open(SAVE_FILE, "w") as file:
        # Save basic player information.
        file.write(f"{player.name}\n")
        file.write(f"{player.age}\n")
        file.write(f"{player.health}\n")
        file.write(f"{player.points}\n")
        file.write(f"{player.coins}\n")

        # Save visited locations as one line.
        file.write(",".join(player.visited_locations) + "\n")

        # Save achievements as one line.
        file.write(",".join(player.achievements) + "\n")

        # Save inventory item names.
        inventory_names = []

        for item in player.inventory:
            inventory_names.append(item.name)

        file.write(",".join(inventory_names) + "\n")

    print("\nGame saved successfully!")


def load_game(player):
    """
    Load player progress from the save file.

    Parameters:
        player: The Player object that will receive the saved data.

    Returns:
        True if loading was successful, otherwise False.
    """

    if not os.path.exists(SAVE_FILE):
        print("\nNo saved game was found.")
        return False

    try:
        with open(SAVE_FILE, "r") as file:
            data = file.readlines()

        # Remove unnecessary spaces and newline characters.
        data = [line.strip() for line in data]

        # A valid save file needs at least 8 lines.
        if len(data) < 8:
            print("\nThe save file is damaged or incomplete.")
            return False

        # Load basic player information.
        player.name = data[0]
        player.age = int(data[1])
        player.health = int(data[2])
        player.points = int(data[3])
        player.coins = int(data[4])

        # Load visited locations.
        if data[5]:
            player.visited_locations = data[5].split(",")
        else:
            player.visited_locations = []

        # Load achievements.
        if data[6]:
            player.achievements = data[6].split(",")
        else:
            player.achievements = []

        # Load inventory.
        player.inventory = []

        if data[7]:
            for item_name in data[7].split(","):

                if item_name in ITEMS:
                    player.inventory.append(ITEMS[item_name])

        print("\nGame loaded successfully!")
        return True

    except (IndexError, ValueError):
        print("\nThe save file is damaged or invalid.")
        return False