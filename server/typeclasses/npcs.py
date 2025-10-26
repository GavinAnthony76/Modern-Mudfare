"""
Custom NPC Typeclasses for Journey Through Scripture
NPCs, merchants, priests, and bosses
"""

from evennia import DefaultCharacter
from evennia.utils.evmenu import EvMenu


class NPC(DefaultCharacter):
    """
    Base NPC class with dialogue system.

    Attributes:
        npc_type (str): friendly, neutral, merchant, priest, hostile, boss
        dialogue (dict): Dialogue tree structure
        quest (str): Quest ID if NPC gives quests
        merchant (bool): Whether NPC is a merchant
        shop_inventory (list): Items for sale
        shop_prices (str): 'fair' or 'inflated'
        services (list): Services provided (heal, save, bless)
        boss_stats (dict): Combat stats if boss
        can_become_hostile (bool): Whether NPC can turn hostile
    """

    def at_object_creation(self):
        """Called when NPC is first created"""
        super().at_object_creation()

        # NPC properties
        self.db.npc_type = "friendly"
        self.db.dialogue = {
            "greeting": "Hello, traveler.",
            "main_menu": {},
            "responses": {}
        }
        self.db.quest = None
        self.db.merchant = False
        self.db.shop_inventory = []
        self.db.shop_prices = "fair"
        self.db.services = []
        self.db.boss_stats = None
        self.db.can_become_hostile = False
        self.db.defeated = False

        # Combat stats
        self.db.hp = 50
        self.db.max_hp = 50
        self.db.damage = 5
        self.db.defense = 2

        # Make NPCs not controllable
        self.locks.add("puppet:false()")
        self.locks.add("get:false()")

    def at_char_entered(self, character):
        """Called when a character enters the room"""
        # Greet characters who enter
        if character.has_account and self.db.npc_type != "hostile":
            greeting = self.db.dialogue.get("greeting", "...")
            character.msg(f"{self.name} says, \"{greeting}\"")

    def talk_to(self, character):
        """Initiate dialogue with a character"""
        if not character.has_account:
            return

        # Check if hostile
        if self.db.npc_type == "hostile":
            character.msg(f"{self.name} glares at you menacingly!")
            return

        # Check if defeated boss
        if self.db.npc_type == "boss" and self.db.defeated:
            character.msg(f"{self.name} lies defeated and cannot speak.")
            return

        # Start dialogue menu
        self.start_dialogue(character)

    def start_dialogue(self, character):
        """Start a dialogue tree with the character"""
        dialogue = self.db.dialogue

        # Show greeting
        character.msg(f"\n{self.name} says, \"{dialogue.get('greeting', 'Hello.')}\"")

        # Show main menu options
        main_menu = dialogue.get('main_menu', {})
        if not main_menu:
            character.msg("(They have nothing more to say)")
            return

        character.msg("\n|wWhat do you say?|n")
        for num, option in main_menu.items():
            character.msg(f"  {num}. {option['text']}")

        # Store dialogue state on character
        character.db.talking_to = self
        character.db.dialogue_state = "main_menu"

    def respond(self, character, choice):
        """Handle character's dialogue choice"""
        dialogue = self.db.dialogue
        main_menu = dialogue.get('main_menu', {})
        responses = dialogue.get('responses', {})

        # Get the chosen option
        option = main_menu.get(int(choice))
        if not option:
            character.msg("Invalid choice.")
            return

        # Check if option requires something
        if 'requires' in option:
            required = option['requires']
            if not character.db.flags or required not in character.db.flags:
                character.msg("(That option is not available yet)")
                return

        # Get the response
        response_key = option['response']

        if response_key == "farewell":
            character.msg(f"\n{self.name} says, \"{responses.get('farewell', 'Farewell.')}\"")
            character.db.talking_to = None
            character.db.dialogue_state = None
            return

        response_text = responses.get(response_key, "...")

        # Handle special responses
        if response_text.startswith("[GAME ACTION:"):
            self.handle_game_action(character, response_text)
        else:
            character.msg(f"\n{self.name} says, \"{response_text}\"")

        # Show menu again
        character.msg("\n|wWhat else do you want to ask?|n")
        for num, opt in main_menu.items():
            character.msg(f"  {num}. {opt['text']}")

    def handle_game_action(self, character, action_text):
        """Handle special game actions in dialogue"""
        if "Heal" in action_text or "heal" in action_text:
            self.heal_character(character)
        elif "Save" in action_text or "save" in action_text:
            self.save_game(character)
        elif "shop" in action_text or "Shop" in action_text:
            self.open_shop(character)
        elif "COMBAT" in action_text:
            self.initiate_combat(character)
        else:
            character.msg(action_text)

    def heal_character(self, character):
        """Heal a character to full HP"""
        if hasattr(character.db, 'hp'):
            old_hp = character.db.hp
            character.db.hp = character.db.max_hp
            healed = character.db.hp - old_hp
            character.msg(f"|g{self.name} places a hand on your shoulder.|n")
            character.msg(f"|gDivine light flows through you, restoring {healed} health!|n")
            character.msg(f"|gYou are now at {character.db.hp}/{character.db.max_hp} HP.|n")
        else:
            character.msg(f"{self.name} blesses you with healing energy.")

    def save_game(self, character):
        """Save character's progress"""
        character.msg(f"|y{self.name} records your journey in the sacred book.|n")
        character.msg("|yYour progress has been saved.|n")
        # In a full implementation, this would save to database

    def open_shop(self, character):
        """Open merchant shop interface"""
        if not self.db.merchant:
            character.msg(f"{self.name} is not a merchant.")
            return

        character.msg(f"\n|w--- {self.name}'s Shop ---|n")
        character.msg(f"\nInventory:")

        # Show items for sale
        for item_key in self.db.shop_inventory:
            # Would look up item data from items.py
            character.msg(f"  - {item_key} (price varies)")

        character.msg("\n(Shop system coming soon!)")

    def initiate_combat(self, character):
        """Start combat with this NPC"""
        character.msg(f"|r{self.name} prepares to fight!|n")
        character.msg("(Combat system coming soon!)")


class Priest(NPC):
    """
    Priest NPCs that tend safe rooms.
    Provide healing, saving, and blessings.
    """

    def at_object_creation(self):
        """Set up priest properties"""
        super().at_object_creation()
        self.db.npc_type = "priest"
        self.db.services = ["heal", "save", "bless"]

    def bless_character(self, character):
        """Grant a temporary blessing"""
        character.msg(f"|y{self.name} raises hands in blessing.|n")
        character.msg("|yYou feel spiritually strengthened!|n")
        character.msg("|y(+1 to all stats for 30 minutes)|n")
        # Would implement actual buff system

class Merchant(NPC):
    """
    Merchant NPCs that buy and sell items.
    """

    def at_object_creation(self):
        """Set up merchant properties"""
        super().at_object_creation()
        self.db.npc_type = "merchant"
        self.db.merchant = True
        self.db.shop_inventory = []
        self.db.shop_prices = "fair"


class Boss(NPC):
    """
    Boss NPCs that block progression.
    Must be defeated to unlock new areas.
    """

    def at_object_creation(self):
        """Set up boss properties"""
        super().at_object_creation()
        self.db.npc_type = "boss"
        self.db.hp = 100
        self.db.max_hp = 100
        self.db.damage = 15
        self.db.defense = 5
        self.db.defeated = False
        self.db.defeat_unlocks = ""  # Room to unlock
        self.db.defeat_reward = []  # Items to give

    def die(self, killer):
        """Called when boss is defeated"""
        self.db.defeated = True
        self.db.hp = 0

        # Announce to room
        self.location.msg_contents(
            f"|y✧ {self.name} has been defeated! ✧|n"
        )

        # Give rewards
        if self.db.defeat_reward:
            killer.msg("|gYou have gained:|n")
            for reward in self.db.defeat_reward:
                killer.msg(f"  - {reward}")

        # Unlock next area
        if self.db.defeat_unlocks and hasattr(self.location, 'defeat_boss'):
            self.location.defeat_boss()

        killer.msg(f"|yYou gain 100 experience!|n")

        # Add defeat flag
        if not killer.db.flags:
            killer.db.flags = []
        killer.db.flags.append(f"defeated_{self.key}")


class HostileNPC(NPC):
    """
    Hostile NPCs that attack on sight or when provoked.
    """

    def at_object_creation(self):
        """Set up hostile NPC properties"""
        super().at_object_creation()
        self.db.npc_type = "hostile"
        self.db.hp = 30
        self.db.max_hp = 30
        self.db.damage = 8
        self.db.defense = 3

    def at_char_entered(self, character):
        """Attack characters who enter"""
        if character.has_account:
            character.msg(f"|r{self.name} attacks!|n")
            # Would initiate combat
