"""
Encounter System for Journey Through Scripture

Manages creature encounters in specific rooms and locations.
Defines where creatures spawn and how often.
"""

import random

# Import combat system - handle Evennia's module loading
try:
    from .combat import Creature
except (ImportError, ValueError):
    try:
        from combat import Creature
    except ImportError:
        Creature = None


class Encounter:
    """Defines an encounter in a specific room"""

    def __init__(self, encounter_id, room_key, creatures, frequency=1.0, **kwargs):
        """
        Initialize an encounter.

        Args:
            encounter_id: Unique ID for this encounter
            room_key: Room key where encounter occurs
            creatures: List of creature types that can appear
            frequency: Chance (0.0-1.0) of encountering per action
            **kwargs: Additional options (min_level, max_level, etc.)
        """
        self.id = encounter_id
        self.room_key = room_key
        self.creatures = creatures  # List of creature types
        self.frequency = frequency  # Encounter chance
        self.min_level = kwargs.get("min_level", 1)
        self.max_level = kwargs.get("max_level", 1)
        self.description = kwargs.get("description", "")
        self.active = True

    def get_creature(self):
        """
        Get a random creature from this encounter.

        Returns:
            str: Creature type
        """
        return random.choice(self.creatures)

    def get_level(self):
        """
        Get creature level for this encounter.

        Returns:
            int: Creature level
        """
        return random.randint(self.min_level, self.max_level)

    def should_trigger(self):
        """
        Check if encounter should trigger.

        Returns:
            bool: True if encounter triggers
        """
        if not self.active:
            return False
        return random.random() < self.frequency


# Encounter Definitions for Each Floor

# FLOOR 1: THE OUTER COURT
FLOOR_1_ENCOUNTERS = {
    "enc_courtyard_bandits": Encounter(
        "enc_courtyard_bandits",
        "floor1_courtyard",
        ["orc", "demon"],
        frequency=0.3,
        min_level=1,
        max_level=2,
        description="Bandits have infiltrated the courtyard!"
    ),

    "enc_garden_serpent": Encounter(
        "enc_garden_serpent",
        "floor1_garden",
        ["serpent"],
        frequency=0.25,
        min_level=1,
        max_level=1,
        description="A serpent coils among the garden plants."
    ),

    "enc_hall_testing_trial": Encounter(
        "enc_hall_testing_trial",
        "floor1_hall_testing",
        ["orc", "demon"],
        frequency=0.4,
        min_level=2,
        max_level=2,
        description="The Hall of Testing lives up to its name."
    ),

    "enc_library_scholar": Encounter(
        "enc_library_scholar",
        "floor1_library_sacred",
        ["demon"],
        frequency=0.2,
        min_level=2,
        max_level=3,
        description="A demon has corrupted the sacred texts!"
    ),

    "enc_false_prophet_boss": Encounter(
        "enc_false_prophet_boss",
        "floor1_sanctuary_deception",
        ["dark_knight"],
        frequency=1.0,  # Boss always appears
        min_level=3,
        max_level=3,
        description="The False Prophet stands before you, blocking your ascent."
    )
}

# FLOOR 2: THE COURT OF WISDOM
FLOOR_2_ENCOUNTERS = {
    "enc_wisdom_stairs": Encounter(
        "enc_wisdom_stairs",
        "floor2_ascending_stairs",
        ["orc", "serpent"],
        frequency=0.3,
        min_level=2,
        max_level=3,
        description="Guardians of the ascending path challenge you."
    ),

    "enc_wisdom_library": Encounter(
        "enc_wisdom_library",
        "floor2_library_wisdom",
        ["demon", "nephilim"],
        frequency=0.35,
        min_level=3,
        max_level=3,
        description="Creatures of deception dwell in the library."
    ),

    "enc_wisdom_debate": Encounter(
        "enc_wisdom_debate",
        "floor2_debate_hall",
        ["dark_knight"],
        frequency=1.0,
        min_level=3,
        max_level=4,
        description="The False Teacher materializes before you!"
    )
}

# FLOOR 3: THE COURT OF SERVICE
FLOOR_3_ENCOUNTERS = {
    "enc_service_stairs": Encounter(
        "enc_service_stairs",
        "floor3_ascending_stairs",
        ["orc", "demon"],
        frequency=0.3,
        min_level=3,
        max_level=3,
        description="Servants of darkness block the path."
    ),

    "enc_service_workshop": Encounter(
        "enc_service_workshop",
        "floor3_workshop",
        ["nephilim"],
        frequency=0.25,
        min_level=3,
        max_level=4,
        description="A Nephilim guards the workshop."
    ),

    "enc_service_kitchen": Encounter(
        "enc_service_kitchen",
        "floor3_kitchen",
        ["orc", "serpent"],
        frequency=0.2,
        min_level=2,
        max_level=3,
        description="Hungry creatures raid the kitchen."
    )
}

# FLOOR 4: THE COURT OF TRIAL
FLOOR_4_ENCOUNTERS = {
    "enc_trial_darkening": Encounter(
        "enc_trial_darkening",
        "floor4_darkening_stairway",
        ["demon", "nephilim"],
        frequency=0.4,
        min_level=4,
        max_level=4,
        description="Shadows gather as you descend."
    ),

    "enc_trial_chamber": Encounter(
        "enc_trial_chamber",
        "floor4_trial_chamber",
        ["behemoth"],
        frequency=0.8,
        min_level=4,
        max_level=5,
        description="A Behemoth emerges from the darkness of your inner trial!"
    )
}

# FLOOR 5: THE COURT OF SACRIFICE
FLOOR_5_ENCOUNTERS = {
    "enc_sacrifice_stairs": Encounter(
        "enc_sacrifice_stairs",
        "floor5_relinquishment_stairs",
        ["dark_knight", "nephilim"],
        frequency=0.35,
        min_level=4,
        max_level=5,
        description="Guardians test your commitment to sacrifice."
    ),

    "enc_sacrifice_altar": Encounter(
        "enc_sacrifice_altar",
        "floor5_altar_room",
        ["demon"],
        frequency=0.2,
        min_level=4,
        max_level=4,
        description="A demon attempts to corrupt your sacrifice."
    ),

    "enc_sacrifice_guardian": Encounter(
        "enc_sacrifice_guardian",
        "floor5_guardian_gate",
        ["behemoth"],
        frequency=1.0,
        min_level=5,
        max_level=5,
        description="The Guardian blocks your path - a final test."
    )
}

# FLOOR 6: THE COURT OF REVELATION
FLOOR_6_ENCOUNTERS = {
    "enc_revelation_stairs": Encounter(
        "enc_revelation_stairs",
        "floor6_stairway_visions",
        ["nephilim", "demon"],
        frequency=0.4,
        min_level=5,
        max_level=5,
        description="Manifestations of false visions attack you."
    ),

    "enc_revelation_vision": Encounter(
        "enc_revelation_vision",
        "floor6_vision_chamber",
        ["leviathan"],
        frequency=0.5,
        min_level=5,
        max_level=6,
        description="A false revelation takes terrible form!"
    )
}

# FLOOR 7: THE HOLY OF HOLIES
FLOOR_7_ENCOUNTERS = {
    "enc_holiest_ascent": Encounter(
        "enc_holiest_ascent",
        "floor7_final_ascent",
        ["dark_knight", "nephilim"],
        frequency=0.3,
        min_level=5,
        max_level=6,
        description="Final guardians stand before the most holy."
    ),

    "enc_holiest_veil": Encounter(
        "enc_holiest_veil",
        "floor7_veil_chamber",
        ["leviathan"],
        frequency=1.0,
        min_level=6,
        max_level=6,
        description="The Corrupted Cherub manifests in terrible majesty!"
    )
}

# Consolidated encounter map
ENCOUNTERS_BY_FLOOR = {
    1: FLOOR_1_ENCOUNTERS,
    2: FLOOR_2_ENCOUNTERS,
    3: FLOOR_3_ENCOUNTERS,
    4: FLOOR_4_ENCOUNTERS,
    5: FLOOR_5_ENCOUNTERS,
    6: FLOOR_6_ENCOUNTERS,
    7: FLOOR_7_ENCOUNTERS,
}

# Map room keys to encounters
ENCOUNTERS_BY_ROOM = {}
for floor, encounters in ENCOUNTERS_BY_FLOOR.items():
    for enc_id, encounter in encounters.items():
        room_key = encounter.room_key
        if room_key not in ENCOUNTERS_BY_ROOM:
            ENCOUNTERS_BY_ROOM[room_key] = []
        ENCOUNTERS_BY_ROOM[room_key].append(encounter)


class EncounterManager:
    """Manages encounters for a room or location"""

    def __init__(self):
        """Initialize encounter manager"""
        self.active_encounters = {}

    def get_encounter_for_room(self, room_key):
        """
        Get an encounter for a specific room.

        Args:
            room_key: The room's key

        Returns:
            Encounter: A random active encounter for the room or None
        """
        if room_key not in ENCOUNTERS_BY_ROOM:
            return None

        possible_encounters = [
            enc for enc in ENCOUNTERS_BY_ROOM[room_key]
            if enc.should_trigger()
        ]

        if possible_encounters:
            return random.choice(possible_encounters)

        return None

    def trigger_encounter(self, character, room_key):
        """
        Check if an encounter triggers in a room.

        Args:
            character: The character
            room_key: The room key

        Returns:
            tuple: (creature_type, creature_level) or None
        """
        encounter = self.get_encounter_for_room(room_key)

        if not encounter:
            return None

        creature_type = encounter.get_creature()
        creature_level = encounter.get_level()

        # Send message about encounter
        if encounter.description:
            character.send_text_output(
                encounter.description,
                "combat"
            )
            character.send_text_output(
                f"A {creature_type} appears!",
                "combat"
            )

        return (creature_type, creature_level)

    @staticmethod
    def disable_encounter(encounter_id):
        """
        Disable an encounter (after boss defeated, etc.)

        Args:
            encounter_id: ID of encounter to disable
        """
        # Search through all encounters
        for floor, encounters in ENCOUNTERS_BY_FLOOR.items():
            if encounter_id in encounters:
                encounters[encounter_id].active = False
                break


# Singleton instance
_encounter_manager = None


def get_encounter_manager():
    """Get the global encounter manager"""
    global _encounter_manager
    if _encounter_manager is None:
        _encounter_manager = EncounterManager()
    return _encounter_manager


def check_room_encounter(character, room_key):
    """
    Check if an encounter triggers when entering a room.

    Args:
        character: The character
        room_key: The room's key

    Returns:
        tuple: (creature_type, creature_level) or None
    """
    manager = get_encounter_manager()
    return manager.trigger_encounter(character, room_key)
