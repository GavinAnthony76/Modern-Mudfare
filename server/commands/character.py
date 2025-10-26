"""
Character management commands for Journey Through Scripture
"""

from evennia import Command


class CmdStats(Command):
    """
    View your character statistics.

    Usage:
        stats
        score

    Displays your complete character sheet including class, level, stats, and equipment.
    """

    key = "stats"
    aliases = ["score", "sheet", "character"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the stats command"""
        char = self.caller

        # Display character sheet
        output = "\n|w" + "=" * 60 + "|n"
        output += f"\n|w{char.name.upper()} - LEVEL {char.db.level} {(char.db.character_class or 'Pilgrim').upper()}|n"
        output += "\n|w" + "=" * 60 + "|n"

        # Health and XP
        hp_bar = self.make_bar(char.db.hp, char.db.max_hp, 20, "|r", "|x")
        xp_bar = self.make_bar(char.db.xp, char.db.xp_to_next_level, 20, "|y", "|x")

        output += f"\n|wHealth:|n {hp_bar} {char.db.hp}/{char.db.max_hp}"
        output += f"\n|wXP:|n     {xp_bar} {char.db.xp}/{char.db.xp_to_next_level}"

        # Stats
        output += "\n\n|w=== STATS ===|n"
        output += f"\n  |wFaith:|n         {char.db.faith}"
        output += f"\n  |wWisdom:|n        {char.db.wisdom}"
        output += f"\n  |wStrength:|n      {char.db.strength}"
        output += f"\n  |wCourage:|n       {char.db.courage}"
        output += f"\n  |wRighteousness:|n {char.db.righteousness}"

        # Equipment
        output += "\n\n|w=== EQUIPMENT ===|n"
        if char.db.equipped_weapon:
            output += f"\n  |wWeapon:|n {char.db.equipped_weapon.name}"
        else:
            output += f"\n  |wWeapon:|n Unarmed"

        if char.db.equipped_armor:
            output += f"\n  |wArmor:|n {char.db.equipped_armor.name}"
        else:
            output += f"\n  |wArmor:|n None"

        # Inventory info
        output += f"\n\n|w=== INVENTORY ===|n"
        output += f"\n  |wCurrency:|n {char.db.currency} temple shekels"
        output += f"\n  |wWeight:|n   {char.db.carried_weight:.1f}/{char.db.max_carry_weight} lbs"

        # Progress
        output += f"\n\n|w=== JOURNEY ===|n"
        output += f"\n  |wCurrent Floor:|n {char.db.current_floor}"
        if char.db.calling:
            output += f"\n  |wCalling:|n       {char.db.calling.capitalize()}"

        output += "\n|w" + "=" * 60 + "|n\n"

        self.caller.msg(output)

    def make_bar(self, current, maximum, width, fill_color, empty_color):
        """Create a progress bar"""
        if maximum == 0:
            filled = 0
        else:
            filled = int((current / maximum) * width)

        empty = width - filled
        bar = f"{fill_color}{'█' * filled}{empty_color}{'░' * empty}|n"
        return bar


class CmdInventory(Command):
    """
    View your inventory.

    Usage:
        inventory
        inv

    Shows all items you are carrying.
    """

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the inventory command"""
        items = [obj for obj in self.caller.contents if obj.typename == "Item"]

        if not items:
            self.caller.msg("You are not carrying anything.")
            return

        output = "\n|w=== INVENTORY ===|n\n"

        for item in items:
            # Show equipped status
            equipped = ""
            if hasattr(item.db, 'equipped') and item.db.equipped:
                equipped = " |y(equipped)|n"

            output += f"  - {item.name}{equipped} ({item.db.weight} lbs)"

            # Show item value
            if hasattr(item.db, 'value'):
                output += f" - {item.db.value} shekels"

            output += "\n"

        output += f"\n|wTotal weight:|n {self.caller.db.carried_weight:.1f}/{self.caller.db.max_carry_weight} lbs"
        output += f"\n|wCurrency:|n {self.caller.db.currency} shekels\n"

        self.caller.msg(output)


class CmdUse(Command):
    """
    Use an item from your inventory.

    Usage:
        use <item>

    Use a consumable item like food, potions, or scrolls.
    """

    key = "use"
    aliases = ["consume", "drink", "eat"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the use command"""
        if not self.args:
            self.caller.msg("Use what?")
            return

        # Find item in inventory
        item = self.caller.search(
            self.args,
            location=self.caller,
            nofound_string=f"You don't have '{self.args}'."
        )

        if not item:
            return

        # Try to use it
        if hasattr(item, 'use'):
            item.use(self.caller)
        else:
            self.caller.msg(f"You cannot use {item.name}.")


class CmdEquip(Command):
    """
    Equip a weapon or armor.

    Usage:
        equip <item>
        wield <weapon>
        wear <armor>

    Equips an item from your inventory to gain its bonuses.
    """

    key = "equip"
    aliases = ["wield", "wear"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the equip command"""
        if not self.args:
            self.caller.msg("Equip what?")
            return

        # Find item in inventory
        item = self.caller.search(
            self.args,
            location=self.caller,
            nofound_string=f"You don't have '{self.args}'."
        )

        if not item:
            return

        # Try to equip it
        if hasattr(item, 'equip'):
            item.equip(self.caller)
        else:
            self.caller.msg(f"You cannot equip {item.name}.")


class CmdUnequip(Command):
    """
    Unequip a weapon or armor.

    Usage:
        unequip <item>
        remove <item>

    Removes an equipped item.
    """

    key = "unequip"
    aliases = ["remove", "unwield"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the unequip command"""
        if not self.args:
            self.caller.msg("Unequip what?")
            return

        # Find equipped item
        item = None
        if self.caller.db.equipped_weapon and \
           self.args.lower() in self.caller.db.equipped_weapon.name.lower():
            item = self.caller.db.equipped_weapon
            self.caller.db.equipped_weapon = None

        elif self.caller.db.equipped_armor and \
             self.args.lower() in self.caller.db.equipped_armor.name.lower():
            item = self.caller.db.equipped_armor
            self.caller.db.equipped_armor = None

        if item:
            item.db.equipped = False
            self.caller.msg(f"You unequip {item.name}.")
        else:
            self.caller.msg(f"You don't have '{self.args}' equipped.")


class CmdQuests(Command):
    """
    View your active quests and progress.

    Usage:
        quests

    Shows all quests you have accepted and their current status.
    """

    key = "quests"
    aliases = ["quest", "journal"]
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the quests command"""
        if not hasattr(self.caller.db, 'quests') or not self.caller.db.quests:
            self.caller.msg("You have no active quests.")
            self.caller.msg("\n|ySeek out NPCs to receive divine missions!|n")
            return

        output = "\n|w=== ACTIVE QUESTS ===|n\n"

        for quest_id, quest_data in self.caller.db.quests.items():
            output += f"\n|y{quest_data['name']}|n"
            output += f"\n{quest_data['description']}"
            if 'progress' in quest_data:
                output += f"\n|wProgress:|n {quest_data['progress']}/{quest_data['total']}"
            output += "\n"

        self.caller.msg(output)


class CmdCalling(Command):
    """
    View or set your spiritual calling.

    Usage:
        calling

    After defeating the first boss, you can choose a calling that shapes your journey:
    - Wisdom: Bonuses in the Court of Wisdom
    - Service: Bonuses in the Court of Service
    - Trial: Bonuses in the Court of Trial
    - Sacrifice: Bonuses in the Court of Sacrifice
    - Revelation: Bonuses in the Court of Revelation
    """

    key = "calling"
    locks = "cmd:all()"
    help_category = "Character"

    def func(self):
        """Execute the calling command"""
        if self.caller.db.calling:
            self.caller.msg(f"\n|yYour calling is:|n {self.caller.db.calling.capitalize()}")
            self.caller.msg(f"This calling guides your path through the Palace of Light.")
        else:
            self.caller.msg("\n|yYou have not yet received your calling.|n")
            self.caller.msg("Complete the first trial and speak to a priest to discover your path.")
