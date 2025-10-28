"""
Journey Through Scripture - A Biblical Fantasy MUD

Main package initialization for the game.

Features:
    - Turn-based combat system
    - Quest tracking and progression
    - Encounter management
    - Real-time WebSocket communication
    - HTML5 Canvas graphics client
    - Character progression system

Modules:
    combat - Turn-based combat engine
    quests - Quest management and tracking
    encounters - Room-based encounter system
    commands - Player commands (dialogue, combat, quests, character)
    typeclasses - Game object types (rooms, characters, items, NPCs)
    world - World data and builder
    web - WebSocket integration
"""

__version__ = "1.0.0"
__author__ = "Journey Through Scripture Team"
__license__ = "MIT"

# Import core systems for easy access
try:
    from . import combat
    from . import quests
    from . import encounters
except ImportError as e:
    # These will be imported properly when the game starts
    # Module dependencies are resolved at runtime by Evennia
    pass

__all__ = [
    'combat',
    'quests',
    'encounters',
    'commands',
    'typeclasses',
    'world',
    'web',
]
