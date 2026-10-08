"""
player.py

Contains the Player class.

The Player object stores the player's name, age, health,
points, eco-coins, inventory, visited locations, and achievements.
"""


class Player:
    """Represent the player and their progress in the game."""

    def __init__(self, name, age):
        """Create a new player."""

        self.name = name
        self.age = age

        # Starting statistics.
        self.health = 100
        self.points = 0
        self.coins = 0

        # Lists storing the player's game information.
        self.inventory = []
        self.visited_locations = []
        self.achievements = []

    def add_item(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)

    def add_points(self, points):
        """Add recycling points."""
        self.points += points

    def add_coins(self, amount):
        """Add eco-coins."""
        self.coins += amount

    def visit_location(self, location_name):
        """Remember a location that the player has visited."""

        if location_name not in self.visited_locations:
            self.visited_locations.append(location_name)

    def add_achievement(self, achievement):
        """Add an achievement if it has not already been earned."""

        if achievement not in self.achievements:
            self.achievements.append(achievement)

    def is_alive(self):
        """Return True if the player's health is above zero."""

        return self.health > 0
    

    def lose_health(self, amount):
        """Reduce the player's health without going below zero."""
        self.health = max(0, self.health - amount)

    def has_won(self, winning_score):
        """Return True if the player has reached the winning score."""

        return self.points >= winning_score