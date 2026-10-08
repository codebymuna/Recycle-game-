"""
events.py

Contains random travel events that can happen while
the player moves to a location.
"""

import random


# Each event is stored as a dictionary.
TRAVEL_EVENTS = [
    {
        "message": "A friendly passer-by thanks you for helping the environment!",
        "health_change": 0
    },
    {
        "message": "You see a recycling sign and feel motivated!",
        "health_change": 0
    },
    {
        "message": "A strong wind makes your journey harder. You lose 2 health.",
        "health_change": -2
    },
    {
        "message": "The walk is peaceful. Nothing unusual happens.",
        "health_change": 0
    }
]


def travel_event(player):
    """
    Choose a random travel event and apply its effect.

    Parameters:
        player: The current Player object.

    Returns:
        The selected event message.
    """

    event = random.choice(TRAVEL_EVENTS)

    print("\nTravel event:")
    print(event["message"])

   # Apply the health change from the event.
    if event["health_change"] < 0:
        player.lose_health(abs(event["health_change"]))
    else:
        player.health += event["health_change"]

    return event["message"]