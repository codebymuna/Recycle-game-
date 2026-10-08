"""
items.py

Contains the RecyclableItem class and the recyclable items
used in the game.
"""


class RecyclableItem:
    """Represent one piece of recyclable litter."""

    def __init__(self, name, material, points):
        """Create a recyclable item."""

        self.name = name
        self.material = material
        self.points = points

    def get_information(self):
        """Return a short description of the item."""

        return f"{self.name} - {self.material} - {self.points} points"


# ------------------------------------------------------------
# RECYCLABLE ITEMS
# ------------------------------------------------------------

water_bottle = RecyclableItem(
    "Water bottle",
    "plastic",
    10
)

newspaper = RecyclableItem(
    "Newspaper",
    "paper",
    8
)

drink_can = RecyclableItem(
    "Drink can",
    "metal",
    12
)

cardboard_box = RecyclableItem(
    "Cardboard box",
    "cardboard",
    10
)

paper_flyer = RecyclableItem(
    "Paper flyer",
    "paper",
    8
)

empty_bottle = RecyclableItem(
    "Empty bottle",
    "plastic",
    10
)

metal_can = RecyclableItem(
    "Metal can",
    "metal",
    12
)

snack_wrapper = RecyclableItem(
    "Snack wrapper",
    "plastic",
    10
)