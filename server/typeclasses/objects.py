"""
Custom Object Typeclasses for Journey Through Scripture
Items, equipment, consumables, and quest objects
"""

from evennia import DefaultObject
from evennia.utils.utils import inherits_from


class Item(DefaultObject):
    """
    Base item class for all objects in the game.

    Attributes:
        item_type (str): consumable, weapon, equipment, lore, quest, material, currency, key
        value (int): Base value in temple shekels
        weight (float): Weight for encumbrance
        stats (dict): Stat bonuses (damage, strength_bonus, faith_bonus, etc.)
        healing (int): HP restored if consumable
        uses (int): Number of uses for consumables
        usable_by (list): Which classes can use this item
        readable (bool): Whether item has text to read
        text (str): Text content for readable items
        cursed (bool): Whether item has negative effects
        effect (str): Special effect identifier
    """

    def at_object_creation(self):
        """Called when item is first created"""
        super().at_object_creation()

        # Item properties
        self.db.item_type = "material"
        self.db.value = 0
        self.db.weight = 1.0
        self.db.stats = {}
        self.db.healing = 0
        self.db.uses = 1
        self.db.usable_by = ["all"]
        self.db.readable = False
        self.db.text = ""
        self.db.cursed = False
        self.db.effect = None
        self.db.equipped = False

        # Make items gettable
        self.locks.add("get:all()")

    def at_get(self, getter, **kwargs):
        """Called when item is picked up"""
        super().at_get(getter, **kwargs)

        # Add to character's inventory weight
        if hasattr(getter.db, 'carried_weight'):
            getter.db.carried_weight += self.db.weight

    def at_drop(self, dropper, **kwargs):
        """Called when item is dropped"""
        super().at_drop(dropper, **kwargs)

        # Remove from character's inventory weight
        if hasattr(dropper.db, 'carried_weight'):
            dropper.db.carried_weight -= self.db.weight

    def use(self, user):
        """Use this item (consumables, etc.)"""
        if self.db.item_type != "consumable":
            user.msg(f"You cannot use {self.name} that way.")
            return False

        if self.db.uses <= 0:
            user.msg(f"{self.name} has been used up.")
            return False

        # Check if user can use this item
        if "all" not in self.db.usable_by and \
           user.db.character_class not in self.db.usable_by:
            user.msg(f"Your class cannot use {self.name}.")
            return False

        # Apply healing
        if self.db.healing > 0:
            if hasattr(user.db, 'hp'):
                old_hp = user.db.hp
                user.db.hp = min(user.db.max_hp, user.db.hp + self.db.healing)
                actual_healing = user.db.hp - old_hp
                user.msg(f"|gYou use {self.name} and restore {actual_healing} health.|n")
                user.location.msg_contents(
                    f"{user.name} uses {self.name}.",
                    exclude=[user]
                )

        # Apply special effects
        if self.db.effect:
            self.apply_effect(user)

        # Decrease uses
        self.db.uses -= 1
        if self.db.uses <= 0:
            user.msg(f"{self.name} crumbles to dust, its power spent.")
            self.delete()
        else:
            user.msg(f"({self.db.uses} use(s) remaining)")

        return True

    def apply_effect(self, user):
        """Apply special effects from items"""
        effect = self.db.effect

        if effect == "faith_permanent_+1":
            user.db.faith += 1
            user.msg("|yYour faith has permanently increased by 1!|n")

        elif effect == "wisdom_permanent_+1":
            user.db.wisdom += 1
            user.msg("|yYour wisdom has permanently increased by 1!|n")

        elif effect.startswith("all_stats_+"):
            # Parse effect like "all_stats_+2_10turns"
            parts = effect.split("_")
            bonus = int(parts[2].replace("+", ""))
            duration = int(parts[3].replace("turns", ""))

            # Apply temporary buff (would need a buff system to fully implement)
            user.msg(f"|yAll your stats increase by {bonus} for {duration} turns!|n")
            # TODO: Implement temporary buff system

    def read(self, reader):
        """Read this item if it's readable"""
        if not self.db.readable:
            reader.msg(f"There is nothing to read on {self.name}.")
            return False

        if not self.db.text:
            reader.msg(f"{self.name} appears to be blank.")
            return False

        # Display the text in a nice format
        reader.msg(f"\n|w--- {self.name.upper()} ---|n")
        reader.msg(self.db.text)
        reader.msg("|w" + "-" * (len(self.name) + 10) + "|n\n")
        return True

    def equip(self, user):
        """Equip this item (weapons, armor, etc.)"""
        if self.db.item_type not in ["weapon", "equipment", "clothing"]:
            user.msg(f"You cannot equip {self.name}.")
            return False

        # Check class restriction
        if "all" not in self.db.usable_by and \
           user.db.character_class not in self.db.usable_by:
            user.msg(f"Your class cannot equip {self.name}.")
            return False

        # Unequip current item in slot (simple version - one weapon slot)
        if self.db.item_type == "weapon":
            if user.db.equipped_weapon:
                user.db.equipped_weapon.db.equipped = False
                user.msg(f"You unequip {user.db.equipped_weapon.name}.")
            user.db.equipped_weapon = self

        self.db.equipped = True
        user.msg(f"|gYou equip {self.name}.|n")

        # Show stat bonuses
        if self.db.stats:
            user.msg(f"Bonuses: {', '.join([f'{k}: +{v}' for k, v in self.db.stats.items()])}")

        if self.db.cursed:
            user.msg("|rYou feel a dark energy emanating from the item...|n")

        return True

    def return_appearance(self, looker, **kwargs):
        """How item appears when examined"""
        string = super().return_appearance(looker, **kwargs)

        # Add item type
        string += f"\n|wType:|n {self.db.item_type.capitalize()}"

        # Add value and weight
        string += f"\n|wValue:|n {self.db.value} shekels  |wWeight:|n {self.db.weight} lbs"

        # Add stats if present
        if self.db.stats:
            string += "\n|wBonuses:|n"
            for stat, value in self.db.stats.items():
                string += f"\n  {stat}: +{value}"

        # Add healing if consumable
        if self.db.healing > 0:
            string += f"\n|gRestores:|n {self.db.healing} HP"

        # Add uses if consumable
        if self.db.item_type == "consumable" and self.db.uses:
            string += f"\n|yUses remaining:|n {self.db.uses}"

        # Warn if cursed
        if self.db.cursed:
            string += "\n|r⚠ This item is cursed! ⚠|n"

        # Show if readable
        if self.db.readable:
            string += "\n|c(Use 'read <item>' to read this)|n"

        # Show who can use it
        if self.db.usable_by and "all" not in self.db.usable_by:
            string += f"\n|yUsable by:|n {', '.join(self.db.usable_by)}"

        return string


class Weapon(Item):
    """Weapon items with combat bonuses"""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "weapon"
        self.db.stats = {"damage": 5, "strength_bonus": 1}


class Consumable(Item):
    """Consumable items that restore health or provide buffs"""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "consumable"
        self.db.healing = 10
        self.db.uses = 1


class QuestItem(Item):
    """Important quest items that cannot be dropped or sold"""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "quest"
        self.locks.add("drop:false()")  # Cannot drop quest items

    def at_drop(self, dropper, **kwargs):
        """Prevent dropping quest items"""
        dropper.msg(f"{self.name} is too important to discard.")
        return False


class Key(Item):
    """Keys that unlock doors and containers"""

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "key"
        self.db.unlocks = ""  # What this key unlocks

    def unlock_door(self, door, user):
        """Use key to unlock a door"""
        if door.key == self.db.unlocks:
            user.msg(f"|gYou use {self.name} to unlock the door!|n")
            # Unlock the door
            return True
        else:
            user.msg(f"{self.name} doesn't fit this lock.")
            return False
