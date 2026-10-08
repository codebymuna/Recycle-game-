"""
locations.py

Contains the Location class and all locations in the game.
"""

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


class Location:
    """Represent a location that the player can explore."""

    def __init__(self, name, description, items):
        """Create a location."""

        self.name = name
        self.description = description
        self.items = items

    def has_items(self):
        """Return True if there are items left at the location."""

        return len(self.items) > 0


# ------------------------------------------------------------
# GAME LOCATIONS
# ------------------------------------------------------------

forest = Location(
    "Forest",
    "A peaceful forest with trees, plants, and walking paths.",
    [
        water_bottle,
        newspaper
    ]
)

lake = Location(
    "Lake",
    "A beautiful lake where people enjoy walking and relaxing.",
    [
        drink_can,
        cardboard_box
    ]
)

park = Location(
    "Park",
    "A green park where families and children enjoy the outdoors.",
    [
        paper_flyer,
        empty_bottle
    ]
)

beach = Location(
    "Beach",
    "A clean-up area near the water where litter can sometimes be found.",
    [
        metal_can,
        snack_wrapper
    ]
)


# A list containing all available locations.
LOCATIONS = [
    forest,
    lake,
    park,
    beach
]


# Recycling stations.
RECYCLING_STATIONS = {
    "plastic": "Plastic recycling station",
    "paper": "Paper recycling station",
    "metal": "Metal recycling station",
    "cardboard": "Cardboard recycling station"
}