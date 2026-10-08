"""
game.py

Contains the main Game class.

The Game class controls the main loop, menus, exploration,
recycling, scoring, achievements, and win condition.
"""

from player import Player
from locations import LOCATIONS, RECYCLING_STATIONS
from events import travel_event
from save_manager import save_game, load_game


# The player needs this many points to win.
WINNING_SCORE = 50


class Game:
    """Control the Helsinki Eco Adventure."""

    def __init__(self):
        """Create a new game."""

        self.player = None
        self.running = True

    # --------------------------------------------------------
    # GAME START
    # --------------------------------------------------------

    def start(self):
        """Ask for player information and start the game."""

        print("""
==================================================
          HELSINKI ECO ADVENTURE 
==================================================

Welcome, Eco Explorer!

Your mission is to explore nature, collect litter,
recycle it correctly, and become a Helsinki Eco Hero.

Your goal is to earn at least 50 recycling points.
""")

        name = self.get_name()
        age = self.get_age()

        self.player = Player(name, age)

        print(f"\nWelcome to the adventure, {self.player.name}!")

        self.run()

    # --------------------------------------------------------
    # INPUT FUNCTIONS
    # --------------------------------------------------------

    def get_name(self):
        """Ask for and return the player's name."""

        while True:
            name = input("Enter your name: ").strip()

            if name:
                return name

            print("Please enter a name.")

    def get_age(self):
        """Ask for and return a valid player age."""

        while True:
            age_input = input("Enter your age: ").strip()

            if age_input.isdigit():
                age = int(age_input)

                # The game is designed for K12 players.
                if 6 <= age <= 18:
                    return age

            print("Please enter an age between 6 and 18.")

    # --------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------

    def run(self):
        """Run the main game loop."""

        while self.running and self.player.is_alive():

            self.show_menu()

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.explore()

            elif choice == "2":
                self.recycle()

            elif choice == "3":
                self.show_map()

            elif choice == "4":
                self.show_status()

            elif choice == "5":
                self.show_help()

            elif choice == "6":
                self.save()

            elif choice == "7":
                self.load()

            elif choice == "8":
                self.quit_game()

            else:
                print("\nPlease choose a number from 1 to 8.")

            # Check whether the player has won.
            if self.player.has_won(WINNING_SCORE):
                self.victory()
                break

        # Check if the player lost all health.
        if not self.player.is_alive():
            self.game_over()

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    def show_menu(self):
        """Display the main menu."""

        print("""
================ MAIN MENU ================

1. Explore a location
2. Recycle collected items
3. View map
4. View player status
5. How to play
6. Save game
7. Load game
8. Quit

============================================
""")

    # --------------------------------------------------------
    # EXPLORE
    # --------------------------------------------------------

    def explore(self):
        """Let the player choose and explore a location."""

        self.show_map()

        while True:
            choice = input(
                "Choose a location number (or 0 to cancel): "
            ).strip()

            if choice == "0":
                return

            if choice.isdigit():
                location_number = int(choice)

                if 1 <= location_number <= len(LOCATIONS):
                    location = LOCATIONS[location_number - 1]
                    self.explore_location(location)
                    return

            print("Please enter a valid location number.")

    def explore_location(self, location):
        """
        Explore a chosen location and collect recyclable items.

        Parameters:
            location: The selected Location object.
        """

        print(f"\nYou arrive at: {location.name}")
        print(location.description)

        # Record the location as visited.
        self.player.visit_location(location.name)

        # Check for a random travel event.
        travel_event(self.player)

        # Check whether the player has lost all health.
        if not self.player.is_alive():
            return

        if not location.has_items():
            print("\nThere is no litter left here.")
            return

        # Keep collecting until the player chooses to stop
        # or there are no items left.
        while location.items:

            print("\nItems you found:")

            for number, item in enumerate(location.items, start=1):
                print(
                    f"{number}. {item.name} "
                    f"({item.material}) - {item.points} points"
                )

            choice = input(
                "\nEnter an item number to collect, "
                "or press Enter to leave: "
            ).strip()

            if choice == "":
                break

            if not choice.isdigit():
                print("Please enter a number.")
                continue

            item_number = int(choice)

            if not 1 <= item_number <= len(location.items):
                print("That item number is not available.")
                continue

            # Remove the item from the location.
            item = location.items.pop(item_number - 1)

            # Add it to the player's inventory.
            self.player.add_item(item)

            print(f"\nYou collected the {item.name}!")

            self.check_achievements()

        if not location.items:
            print("\nYou collected everything from this location!")

    # --------------------------------------------------------
    # RECYCLING
    # --------------------------------------------------------

    def recycle(self):
        """Allow the player to recycle items."""

        if not self.player.inventory:
            print("\nYour inventory is empty.")
            print("Explore a location and collect some litter first.")
            return

        print("\n========== RECYCLING STATIONS ==========")

        for material, station in RECYCLING_STATIONS.items():
            print(f"{material.title()}: {station}")

        while self.player.inventory:

            print("\nYour inventory:")

            for number, item in enumerate(
                self.player.inventory,
                start=1
            ):
                print(
                    f"{number}. {item.name} "
                    f"({item.material}) - {item.points} points"
                )

            choice = input(
                "\nChoose an item number to recycle, "
                "or press Enter to stop: "
            ).strip()

            if choice == "":
                break

            if not choice.isdigit():
                print("Please enter a number.")
                continue

            item_number = int(choice)

            if not 1 <= item_number <= len(self.player.inventory):
                print("That item number is not in your inventory.")
                continue

            item = self.player.inventory[item_number - 1]

            self.recycle_item(item, item_number - 1)

            # Check for victory after every successful recycling.
            if self.player.has_won(WINNING_SCORE):
                return

    def recycle_item(self, item, inventory_index):
        """
        Recycle one item.

        The player must choose the correct recycling station.

        Parameters:
            item: The RecyclableItem object.
            inventory_index: The item's position in the inventory.
        """

        materials = list(RECYCLING_STATIONS.keys())

        print(f"\nWhere should the {item.name} go?")

        for number, material in enumerate(materials, start=1):
            print(f"{number}. {material.title()}")

        while True:

            choice = input("Choose a recycling station: ").strip()

            if not choice.isdigit():
                print("Please enter a number.")
                continue

            station_number = int(choice)

            if not 1 <= station_number <= len(materials):
                print("Please choose a valid station.")
                continue

            chosen_material = materials[station_number - 1]

            # Check whether the selected material is correct.
            if chosen_material != item.material:

                print("\nNot quite! That is not the correct station.")
                print("Try again.")

                continue

            station = RECYCLING_STATIONS[item.material]

            print(
                f"\nCorrect! You put the {item.name} "
                f"in the {station}."
            )

            # Award points and eco-coins.
            self.player.add_points(item.points)
            self.player.add_coins(2)

            # Remove the recycled item from inventory.
            self.player.inventory.pop(inventory_index)

            print(
                f"+{item.points} recycling points!"
            )
            print("+2 eco-coins!")

            print(
                f"Total points: {self.player.points}"
            )

            self.check_achievements()

            return

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    def show_map(self):
        """Display the available locations."""

       # print("\n=============== MAP ===============")

        print("""
================ HELSINKI MAP ================

                 🌲
              1. FOREST
            [Recycling]

                  |
                  |
                  v

🌊 2. LAKE --------+-------- 3. PARK 🌳
     [Recycling]            [Recycling]
                  |
                  |
                  v

              🏖️ 4. BEACH
                [Recycling]

===============================================
""")

        for number, location in enumerate(LOCATIONS, start=1):

            if location.name in self.player.visited_locations:
                status = "Visited"
            else:
                status = "Not visited"

            print(
                f"{number}. {location.name} - {status}"
            )

        print("===================================")

    # --------------------------------------------------------
    # PLAYER STATUS
    # --------------------------------------------------------

    def show_status(self):
        """Display the player's current status."""

        print("\n========== PLAYER STATUS ==========")

        print(f"Name: {self.player.name}")
        print(f"Age: {self.player.age}")
        print(f"Health: {self.player.health}")
        print(f"Recycling points: {self.player.points}")
        print(f"Eco-coins: {self.player.coins}")

        print(
            f"Locations visited: "
            f"{len(self.player.visited_locations)}"
        )

        print(
            f"Items in inventory: "
            f"{len(self.player.inventory)}"
        )

        print("\nAchievements:")

        if self.player.achievements:

            for achievement in self.player.achievements:
                print(f"✓ {achievement}")

        else:
            print("No achievements yet.")

        print("===================================")

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    def show_help(self):
        """Display the game instructions."""

        print("""
================ HOW TO PLAY ================

OBJECTIVE:
Earn at least 50 recycling points and become
a Helsinki Eco Hero.

HOW TO PLAY:

1. Explore Forest, Lake, Park, or Beach.
2. Collect recyclable litter.
3. Open the recycling menu.
4. Choose the correct recycling station.
5. Earn recycling points and eco-coins.
6. Visit different locations.
7. Reach 50 points to win.

You can choose locations in different orders,
so there are several possible routes through
the game.

The game also includes random travel events,
achievements, and save/load functionality.

==============================================
""")

    # --------------------------------------------------------
    # ACHIEVEMENTS
    # --------------------------------------------------------

    def check_achievements(self):
        """Check whether the player has earned achievements."""

        if self.player.points > 0:
            self.player.add_achievement("First Recycling")

        if len(self.player.visited_locations) >= 2:
            self.player.add_achievement("Explorer")

        if len(self.player.visited_locations) == len(LOCATIONS):
            self.player.add_achievement("Nature Lover")

        if self.player.points >= 30:
            self.player.add_achievement("Master Recycler")

        if self.player.points >= WINNING_SCORE:
            self.player.add_achievement("Eco Hero")

    # --------------------------------------------------------
    # SAVE AND LOAD
    # --------------------------------------------------------

    def save(self):
        """Save the current game."""

        save_game(self.player)

    def load(self):
        """Load a previously saved game."""

        load_game(self.player)

    # --------------------------------------------------------
    # ENDING FUNCTIONS
    # --------------------------------------------------------

    def victory(self):
        """Display the victory message."""

        print("""
==================================================
                 ECO HERO!
==================================================
Congratulations!

You reached 50 recycling points and helped
make the environment cleaner.

You are officially a Helsinki Eco Hero!

Keep recycling and protecting nature!
==================================================
""")

        print(f"Final points: {self.player.points}")
        print(f"Eco-coins: {self.player.coins}")

    def game_over(self):
        """Display the game-over message."""

        print("""
==================================================
                  GAME OVER
==================================================

Your health reached zero.

Thank you for trying to help the environment!
==================================================
""")

    def quit_game(self):
        """End the game."""

        print("\nThanks for playing Helsinki Eco Adventure!")
        print("Keep our environment clean! ♻")

        self.running = False