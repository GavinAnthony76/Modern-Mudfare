"""
Custom Room Typeclasses for Journey Through Scripture
Extends Evennia's base Room with biblical MUD features
"""

from evennia import DefaultRoom
from evennia.utils.evtable import EvTable


class Room(DefaultRoom):
    """
    Base room typeclass with enhanced features for the Palace of Light.

    Attributes:
        floor (int): Which floor of the palace (1-7)
        room_type (str): Type of room (normal, safe, hidden, boss, completion)
        danger_level (int): Difficulty rating (0-10)
        hint (str): Subtle hint about the room
        lore (str): Background story/lore text
        ambient_sounds (list): Environmental sounds for atmosphere
        is_save_point (bool): Whether this is a save location
    """

    def at_object_creation(self):
        """Called when room is first created"""
        super().at_object_creation()

        # Set default attributes
        self.db.floor = 1
        self.db.room_type = "normal"
        self.db.danger_level = 0
        self.db.hint = ""
        self.db.lore = ""
        self.db.ambient_sounds = []
        self.db.is_save_point = False
        self.db.locked_exits = {}  # Exits that require conditions to unlock

    def return_appearance(self, looker, **kwargs):
        """
        Called when someone looks at the room.
        Returns a formatted description with all room information.
        """
        if not looker:
            return ""

        # Get the base description
        string = super().return_appearance(looker, **kwargs)

        # Add floor information
        if self.db.floor:
            string += f"\n|w[Floor {self.db.floor}]|n"

        # Add room type indicator
        if self.db.room_type == "safe":
            string += "\n|g✦ This is a sanctuary. You are safe here. ✦|n"
        elif self.db.room_type == "boss":
            string += "\n|r⚠ A powerful presence emanates from this chamber. ⚠|n"
        elif self.db.room_type == "hidden":
            string += "\n|c✧ A secret place, hidden from casual observation. ✧|n"

        # Add hint if present
        if self.db.hint:
            string += f"\n|y[Hint: {self.db.hint}]|n"

        # Add ambient sounds
        if self.db.ambient_sounds:
            sounds = ", ".join(self.db.ambient_sounds)
            string += f"\n|c(You hear: {sounds})|n"

        # Show items in room
        items = [obj for obj in self.contents if obj.typename == "Item" and obj != looker]
        if items:
            string += "\n\n|wItems here:|n"
            for item in items:
                string += f"\n  - {item.name}"

        # Show NPCs in room
        npcs = [obj for obj in self.contents if obj.typename == "NPC"]
        if npcs:
            string += "\n\n|wPeople here:|n"
            for npc in npcs:
                string += f"\n  - {npc.name}"

        # Show other characters
        characters = [obj for obj in self.contents
                     if obj.has_account and obj != looker]
        if characters:
            string += "\n\n|wOther pilgrims:|n"
            for char in characters:
                string += f"\n  - {char.name}"

        return string

    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """
        Called when an object enters this room.
        """
        super().at_object_receive(moved_obj, source_location, **kwargs)

        # If it's a character entering, show ambient message
        if moved_obj.has_account:
            if self.db.room_type == "safe":
                moved_obj.msg("|gA feeling of peace washes over you as you enter the sanctuary.|n")
            elif self.db.danger_level >= 7:
                moved_obj.msg("|rYou sense great danger ahead. Prepare yourself.|n")

    def get_lore(self):
        """Return the lore text for this room"""
        return self.db.lore or "No additional lore available."


class SafeRoom(Room):
    """
    Special room type where combat is disabled and healing is available.
    Each floor has one safe room with a priest NPC.
    """

    def at_object_creation(self):
        """Set up safe room properties"""
        super().at_object_creation()
        self.db.room_type = "safe"
        self.db.is_save_point = True
        self.db.danger_level = 0
        self.locks.add("combat:false()")  # No combat allowed

    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Heal characters who enter"""
        super().at_object_receive(moved_obj, source_location, **kwargs)

        if moved_obj.has_account and hasattr(moved_obj.db, 'hp'):
            # Restore some health when entering
            if moved_obj.db.hp < moved_obj.db.max_hp:
                heal_amount = min(10, moved_obj.db.max_hp - moved_obj.db.hp)
                moved_obj.db.hp += heal_amount
                moved_obj.msg(f"|gThe sanctuary's divine presence restores {heal_amount} health.|n")


class BossRoom(Room):
    """
    Room containing a boss enemy that must be defeated to progress.
    """

    def at_object_creation(self):
        """Set up boss room properties"""
        super().at_object_creation()
        self.db.room_type = "boss"
        self.db.boss_defeated = False
        self.db.locked_exit_direction = None  # Which exit unlocks when boss dies
        self.db.locked_exit_destination = None

    def defeat_boss(self):
        """Called when the boss in this room is defeated"""
        self.db.boss_defeated = True

        # Unlock the progression exit
        if self.db.locked_exit_direction and self.db.locked_exit_destination:
            # Announce to everyone in room
            self.msg_contents(
                "|y✧ The path forward is now open! ✧|n"
            )

    def return_appearance(self, looker, **kwargs):
        """Add boss status to room description"""
        string = super().return_appearance(looker, **kwargs)

        if not self.db.boss_defeated:
            string += "\n|rThe boss of this chamber bars your way forward.|n"
        else:
            string += "\n|gThe boss has been vanquished. The way is clear.|n"

        return string


class HiddenRoom(Room):
    """
    Secret room that's not immediately visible from normal exploration.
    """

    def at_object_creation(self):
        """Set up hidden room properties"""
        super().at_object_creation()
        self.db.room_type = "hidden"
        self.db.discovered = False

    def discover(self, character):
        """Mark this room as discovered by a character"""
        if not self.db.discovered:
            self.db.discovered = True
            character.msg(
                "|y✧ You have discovered a secret location! ✧|n"
            )
