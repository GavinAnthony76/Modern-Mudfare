"""
Custom Character Typeclasses for Journey Through Scripture
Player characters with biblical fantasy stats and progression
"""

from evennia import DefaultCharacter
from evennia.utils.utils import inherits_from

# Import quest system - delayed import to handle Evennia's module loading
def _import_quests():
    """Lazy import of quests to handle Evennia's module context"""
    import sys
    if 'mygame.quests' in sys.modules:
        quests_module = sys.modules['mygame.quests']
        return quests_module.QuestManager, quests_module.create_quest

    # Try direct import
    try:
        from quests import QuestManager, create_quest as cq
        return QuestManager, cq
    except ImportError:
        # This will be loaded at runtime
        return None, None

# Import at module level but handle ImportError
try:
    from quests import QuestManager, create_quest
except (ImportError, ValueError):
    # Will be imported dynamically at runtime
    QuestManager = None
    create_quest = None


class Character(DefaultCharacter):
    """
    Extended character class for biblical fantasy MUD.

    Attributes:
        Character Classes: Prophet, Warrior, Shepherd, Scribe
        Stats: Faith, Wisdom, Strength, Courage, Righteousness
        Progression: Level, XP, Skills
        Inventory: Items, equipment, currency
    """

    def at_object_creation(self):
        """
        Called when character is first created.
        Set up all character attributes.
        """
        super().at_object_creation()

        # Character class (set during creation)
        self.db.character_class = None  # prophet, warrior, shepherd, scribe

        # Core stats (1-10 scale)
        self.db.faith = 5
        self.db.wisdom = 5
        self.db.strength = 5
        self.db.courage = 5
        self.db.righteousness = 5

        # Combat stats
        self.db.hp = 100
        self.db.max_hp = 100
        self.db.damage = 5

        # Progression
        self.db.level = 1
        self.db.xp = 0
        self.db.xp_to_next_level = 100

        # Inventory
        self.db.currency = 0  # Temple shekels
        self.db.carried_weight = 0.0
        self.db.max_carry_weight = 50.0
        self.db.equipped_weapon = None
        self.db.equipped_armor = None

        # Game state
        self.db.current_floor = 1
        self.db.flags = []  # Quest flags, defeated bosses, etc.
        self.db.calling = None  # wisdom, service, trial, sacrifice, revelation

        # Dialogue state
        self.db.talking_to = None
        self.db.dialogue_state = None

        # Quest system
        self.db.quests = {}  # Available quests
        self.db.quest_log = {}  # Active/completed quests
        if QuestManager:
            self.quest_manager = QuestManager(self)
        else:
            # Lazy load quest manager at runtime
            self.quest_manager = None

    def set_class(self, class_name):
        """
        Set character class and apply stat bonuses.

        Args:
            class_name (str): prophet, warrior, shepherd, or scribe
        """
        class_name = class_name.lower()

        if class_name == "prophet":
            self.db.character_class = "prophet"
            self.db.faith = 8
            self.db.wisdom = 8
            self.db.righteousness = 7
            self.db.strength = 4
            self.db.courage = 5
            self.msg("|yYou are called as a Prophet - speaker of divine truth.|n")

        elif class_name == "warrior":
            self.db.character_class = "warrior"
            self.db.strength = 8
            self.db.courage = 8
            self.db.righteousness = 7
            self.db.faith = 5
            self.db.wisdom = 5
            self.db.max_hp = 120
            self.db.hp = 120
            self.msg("|yYou are called as a Warrior - righteous defender of the faith.|n")

        elif class_name == "shepherd":
            self.db.character_class = "shepherd"
            self.db.faith = 6
            self.db.wisdom = 6
            self.db.strength = 6
            self.db.courage = 6
            self.db.righteousness = 6
            self.msg("|yYou are called as a Shepherd - balanced and versatile guide.|n")

        elif class_name == "scribe":
            self.db.character_class = "scribe"
            self.db.wisdom = 8
            self.db.faith = 7
            self.db.righteousness = 6
            self.db.strength = 4
            self.db.courage = 5
            self.msg("|yYou are called as a Scribe - keeper of sacred knowledge.|n")

        else:
            self.msg("Invalid class. Choose: prophet, warrior, shepherd, or scribe")
            return False

        return True

    def get_total_stat(self, stat_name):
        """
        Get total value of a stat including equipment bonuses.

        Args:
            stat_name (str): Name of stat (faith, wisdom, etc.)

        Returns:
            int: Total stat value
        """
        base_stat = getattr(self.db, stat_name, 0)
        bonus = 0

        # Add weapon bonuses
        if self.db.equipped_weapon and hasattr(self.db.equipped_weapon.db, 'stats'):
            bonus += self.db.equipped_weapon.db.stats.get(f"{stat_name}_bonus", 0)

        # Add armor bonuses
        if self.db.equipped_armor and hasattr(self.db.equipped_armor.db, 'stats'):
            bonus += self.db.equipped_armor.db.stats.get(f"{stat_name}_bonus", 0)

        return base_stat + bonus

    def get_total_damage(self):
        """Calculate total damage output"""
        base_damage = self.db.damage
        weapon_damage = 0

        if self.db.equipped_weapon and hasattr(self.db.equipped_weapon.db, 'stats'):
            weapon_damage = self.db.equipped_weapon.db.stats.get('damage', 0)

        strength_bonus = self.get_total_stat('strength') - 5  # 5 is average

        return base_damage + weapon_damage + strength_bonus

    def take_damage(self, amount, attacker=None):
        """
        Take damage and check for death.

        Args:
            amount (int): Damage amount
            attacker: Who attacked (optional)

        Returns:
            bool: True if still alive, False if died
        """
        self.db.hp -= amount
        self.msg(f"|rYou take {amount} damage! ({self.db.hp}/{self.db.max_hp} HP)|n")

        if self.db.hp <= 0:
            self.db.hp = 0
            self.die(attacker)
            return False

        return True

    def heal(self, amount):
        """Heal character"""
        old_hp = self.db.hp
        self.db.hp = min(self.db.max_hp, self.db.hp + amount)
        actual_healing = self.db.hp - old_hp

        if actual_healing > 0:
            self.msg(f"|gYou are healed for {actual_healing} HP! ({self.db.hp}/{self.db.max_hp})|n")
            return actual_healing
        else:
            self.msg("You are already at full health.")
            return 0

    def die(self, killer=None):
        """Handle character death"""
        self.msg("|rYou have fallen!|n")
        self.location.msg_contents(
            f"{self.name} has fallen!",
            exclude=[self]
        )

        # Respawn at last safe room (simplified)
        self.msg("|yYou awaken in the last sanctuary you visited...|n")
        self.db.hp = self.db.max_hp

        # Could implement more complex death penalties

    def gain_xp(self, amount):
        """Gain experience points"""
        self.db.xp += amount
        self.msg(f"|y+{amount} XP|n")

        # Check for level up
        while self.db.xp >= self.db.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Level up the character"""
        self.db.level += 1
        self.db.xp -= self.db.xp_to_next_level
        self.db.xp_to_next_level = int(self.db.xp_to_next_level * 1.5)

        # Increase stats
        self.db.max_hp += 10
        self.db.hp = self.db.max_hp

        self.msg("|y" + "=" * 50 + "|n")
        self.msg("|yLEVEL UP! You are now level {}!|n".format(self.db.level))
        self.msg("|y+10 Max HP|n")
        self.msg("|y" + "=" * 50 + "|n")

        self.location.msg_contents(
            f"|y{self.name} has reached level {self.db.level}!|n",
            exclude=[self]
        )

    def return_appearance(self, looker, **kwargs):
        """How character appears when looked at"""
        # Use the base appearance
        string = super().return_appearance(looker, **kwargs)

        # If looking at self, show detailed stats
        if looker == self:
            string += f"\n\n|w=== CHARACTER STATS ===|n"
            string += f"\n|wClass:|n {self.db.character_class or 'None'}"
            string += f"\n|wLevel:|n {self.db.level}  |wXP:|n {self.db.xp}/{self.db.xp_to_next_level}"
            string += f"\n\n|wHealth:|n {self.db.hp}/{self.db.max_hp}"
            string += f"\n\n|wStats:|n"
            string += f"\n  Faith: {self.db.faith}"
            string += f"\n  Wisdom: {self.db.wisdom}"
            string += f"\n  Strength: {self.db.strength}"
            string += f"\n  Courage: {self.db.courage}"
            string += f"\n  Righteousness: {self.db.righteousness}"

            if self.db.equipped_weapon:
                string += f"\n\n|wWeapon:|n {self.db.equipped_weapon.name}"
            else:
                string += f"\n\n|wWeapon:|n Unarmed"

            if self.db.equipped_armor:
                string += f"\n|wArmor:|n {self.db.equipped_armor.name}"

            string += f"\n\n|wCurrency:|n {self.db.currency} shekels"
            string += f"\n|wWeight:|n {self.db.carried_weight:.1f}/{self.db.max_carry_weight} lbs"

            if self.db.calling:
                string += f"\n\n|yYour calling:|n {self.db.calling.capitalize()}"

        return string

    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Called when receiving an object"""
        super().at_object_receive(moved_obj, source_location, **kwargs)

        # Check if over-encumbered
        if self.db.carried_weight > self.db.max_carry_weight:
            self.msg("|yYou are over-encumbered!|n")

    def send_to_web_client(self, message_dict):
        """
        Send a message to the web client via WebSocket.

        Args:
            message_dict: Dictionary with message data
        """
        try:
            sessions = self.sessions.all()
            for session in sessions:
                # Check if this session has WebSocket support
                if hasattr(session, 'msg') and callable(session.msg):
                    try:
                        session.msg(message_dict)
                    except Exception as e:
                        # Session may not support JSON/WebSocket
                        pass
        except Exception as e:
            # Character may not have sessions attribute in all contexts
            pass

    def send_character_update(self):
        """Send character state update to web client"""
        char_state = {
            "id": self.key,
            "name": self.get_display_name(self),
            "class": self.db.character_class or "shepherd",
            "level": self.db.level or 1,
            "stats": {
                "faith": self.db.faith or 5,
                "wisdom": self.db.wisdom or 5,
                "strength": self.db.strength or 5,
                "courage": self.db.courage or 5,
                "righteousness": self.db.righteousness or 5
            },
            "health": {
                "current": self.db.hp or 100,
                "max": self.db.max_hp or 100
            },
            "xp": {
                "current": self.db.xp or 0,
                "next_level": self.db.xp_to_next_level or 100
            },
            "currency": self.db.currency or 0
        }

        # Build inventory
        inventory = []
        for item in self.contents:
            if not inherits_from(item, "typeclasses.objects.Item"):
                continue

            is_equipped = (
                item == self.db.equipped_weapon or
                item == self.db.equipped_armor
            )

            inventory.append({
                "id": item.key,
                "name": item.get_display_name(self),
                "type": getattr(item.db, "item_type", "misc"),
                "equipped": is_equipped
            })

        char_state["inventory"] = inventory

        self.send_to_web_client({
            "type": "character_update",
            "character": char_state
        })

    def send_room_update(self):
        """Send current room state to web client"""
        room = self.location
        if not room:
            return

        # Get characters in room
        characters = []
        for obj in room.contents:
            if inherits_from(obj, "typeclasses.characters.Character"):
                characters.append({
                    "id": obj.key,
                    "name": obj.get_display_name(self),
                    "class": obj.db.character_class or "shepherd",
                    "sprite": f"{obj.db.character_class or 'shepherd'}_idle"
                })

        # Get items in room
        objects = []
        for obj in room.contents:
            if inherits_from(obj, "typeclasses.objects.Item"):
                objects.append({
                    "id": obj.key,
                    "name": obj.get_display_name(self),
                    "type": getattr(obj.db, "item_type", "misc"),
                    "sprite": getattr(obj.db, "sprite", "item_default")
                })

        # Get exits
        exits = []
        for exit_obj in room.exits:
            if exit_obj:
                direction = getattr(exit_obj.db, "direction", None)
                if direction:
                    exits.append(direction)

        room_state = {
            "id": room.key,
            "name": room.get_display_name(self),
            "description": room.db.description or getattr(room.db, 'desc', 'A place of mystery.'),
            "floor": getattr(room.db, 'floor', 1),
            "characters": characters,
            "objects": objects,
            "exits": exits
        }

        self.send_to_web_client({
            "type": "room_update",
            "room": room_state
        })

    def send_text_output(self, text, text_class="narrative"):
        """
        Send text output to web client.

        Args:
            text: The text to display
            text_class: CSS class for styling (narrative, system, success, warning, error, combat)
        """
        self.send_to_web_client({
            "type": "text",
            "text": text,
            "class": text_class
        })
