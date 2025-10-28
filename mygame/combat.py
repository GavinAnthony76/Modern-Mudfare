"""
Combat System for Journey Through Scripture

Handles turn-based combat mechanics, damage calculation, and combat events.
"""

import random
import logging
from evennia.utils.utils import inherits_from

logger = logging.getLogger(__name__)


class CombatHandler:
    """
    Manages combat between two combatants.
    Handles turn order, damage calculation, and combat flow.
    """

    def __init__(self, attacker, defender):
        """
        Initialize combat.

        Args:
            attacker: The character initiating combat
            defender: The enemy being fought
        """
        self.attacker = attacker
        self.defender = defender
        self.active = True
        self.turn_count = 0

        # Store original HP for reference
        self.attacker_start_hp = attacker.db.hp or 100
        self.defender_start_hp = defender.db.hp or 100

        # Combat state
        self.attacker.db.in_combat = True
        self.defender.db.in_combat = True
        self.attacker.db.combat_target = defender
        self.defender.db.combat_target = attacker

    def get_damage(self, attacker):
        """
        Calculate damage output for an attacker.

        Args:
            attacker: The character attacking

        Returns:
            int: Damage amount
        """
        # Base damage from stats
        base_damage = attacker.db.damage or 5
        strength = attacker.db.strength or 5
        strength_bonus = max(0, strength - 5) * 0.5  # Half strength bonus

        # Weapon damage
        weapon_damage = 0
        if attacker.db.equipped_weapon:
            weapon_damage = getattr(attacker.db.equipped_weapon.db, 'damage', 0)

        # Randomize damage (±20%)
        total_damage = base_damage + strength_bonus + weapon_damage
        variance = total_damage * 0.2
        final_damage = int(total_damage + random.uniform(-variance, variance))

        return max(1, final_damage)

    def calculate_accuracy(self, attacker, defender):
        """
        Calculate chance to hit.

        Args:
            attacker: The attacking character
            defender: The defending character

        Returns:
            float: Accuracy percentage (0.0 to 1.0)
        """
        # Attacker's accuracy based on courage
        attacker_accuracy = (attacker.db.courage or 5) * 0.1  # 10% per courage point

        # Defender's evasion based on courage
        defender_evasion = (defender.db.courage or 5) * 0.05  # 5% per point

        base_accuracy = 0.75  # 75% base hit chance
        final_accuracy = base_accuracy + attacker_accuracy - defender_evasion

        return max(0.1, min(1.0, final_accuracy))  # Clamp between 10% and 100%

    def attacker_turn(self):
        """
        Execute attacker's turn.

        Returns:
            dict: Combat action results
        """
        if not self.active:
            return None

        accuracy = self.calculate_accuracy(self.attacker, self.defender)
        hit = random.random() < accuracy

        result = {
            "attacker_name": self.attacker.get_display_name(self.attacker),
            "defender_name": self.defender.get_display_name(self.attacker),
            "hit": hit
        }

        if hit:
            damage = self.get_damage(self.attacker)
            self.defender.take_damage(damage, self.attacker)

            result["damage"] = damage
            result["message"] = f"{self.attacker.name} strikes {self.defender.name} for {damage} damage!"

            # Check if defender is defeated
            if self.defender.db.hp <= 0:
                self.end_combat(victory=True)
                result["combat_ended"] = True
                result["victory"] = True
        else:
            result["message"] = f"{self.attacker.name} swings at {self.defender.name} but misses!"

        result["defender_hp"] = self.defender.db.hp
        result["defender_max_hp"] = self.defender.db.max_hp

        return result

    def end_combat(self, victory=False):
        """
        End combat.

        Args:
            victory: Whether the attacker won
        """
        self.active = False

        self.attacker.db.in_combat = False
        self.defender.db.in_combat = False
        self.attacker.db.combat_target = None
        self.defender.db.combat_target = None

        if victory:
            # Award experience
            xp_reward = self.defender.db.xp_reward or 50
            self.attacker.gain_xp(xp_reward)

            # Award currency
            currency_reward = self.defender.db.currency_reward or 25
            self.attacker.db.currency = (self.attacker.db.currency or 0) + currency_reward

            self.attacker.send_text_output(f"Victory! You defeated {self.defender.name}!", 'success')
            self.attacker.send_text_output(f"You gained {xp_reward} XP and {currency_reward} shekels!", 'success')

            # Update quests that require defeating this creature
            creature_type = getattr(self.defender.db, 'creature_type', None)
            if creature_type and hasattr(self.attacker, 'quest_manager'):
                for quest in self.attacker.quest_manager.get_active_quests():
                    for obj in quest.objectives:
                        if (obj.get("type") == "kill_creature" and
                            obj.get("creature_type") == creature_type):
                            self.attacker.quest_manager.update_quest_progress(
                                quest.id,
                                obj["id"],
                                1
                            )

            # Send combat end event
            self.attacker.send_to_web_client({
                "type": "combat_event",
                "event": "combat_ended",
                "victory": True,
                "xp_gained": xp_reward,
                "currency_gained": currency_reward,
                "enemy_name": self.defender.get_display_name(self.attacker)
            })
        else:
            self.attacker.send_text_output(f"You have been defeated by {self.defender.name}!", 'error')
            self.attacker.send_to_web_client({
                "type": "combat_event",
                "event": "combat_ended",
                "victory": False,
                "enemy_name": self.defender.get_display_name(self.attacker)
            })


class Creature:
    """
    Base class for creatures/enemies in combat.
    Stored on character objects as combatants.
    """

    creature_types = {
        'orc': {
            'name': 'Orc',
            'hp': 30,
            'damage': 8,
            'strength': 7,
            'courage': 6,
            'xp_reward': 100,
            'currency_reward': 50,
            'sprite': 'orc_idle'
        },
        'demon': {
            'name': 'Demon',
            'hp': 45,
            'damage': 12,
            'strength': 8,
            'courage': 7,
            'xp_reward': 150,
            'currency_reward': 75,
            'sprite': 'demon_idle'
        },
        'leviathan': {
            'name': 'Leviathan',
            'hp': 100,
            'damage': 18,
            'strength': 10,
            'courage': 9,
            'xp_reward': 300,
            'currency_reward': 200,
            'sprite': 'leviathan_idle'
        },
        'behemoth': {
            'name': 'Behemoth',
            'hp': 80,
            'damage': 15,
            'strength': 9,
            'courage': 8,
            'xp_reward': 250,
            'currency_reward': 150,
            'sprite': 'behemoth_idle'
        },
        'nephilim': {
            'name': 'Nephilim',
            'hp': 60,
            'damage': 14,
            'strength': 9,
            'courage': 8,
            'xp_reward': 200,
            'currency_reward': 100,
            'sprite': 'nephilim_idle'
        },
        'dark_knight': {
            'name': 'Dark Knight',
            'hp': 55,
            'damage': 13,
            'strength': 8,
            'courage': 8,
            'xp_reward': 180,
            'currency_reward': 90,
            'sprite': 'dark_knight_idle'
        },
        'serpent': {
            'name': 'Ancient Serpent',
            'hp': 40,
            'damage': 10,
            'strength': 7,
            'courage': 7,
            'xp_reward': 120,
            'currency_reward': 60,
            'sprite': 'serpent_idle'
        }
    }

    @staticmethod
    def create_creature(creature_type, level=1):
        """
        Create a creature for combat.

        Args:
            creature_type: Type of creature ('orc', 'demon', etc.)
            level: Creature level (affects stats)

        Returns:
            dict: Creature stats object
        """
        if creature_type not in Creature.creature_types:
            creature_type = 'orc'

        base_stats = Creature.creature_types[creature_type].copy()

        # Scale stats by level
        level_multiplier = 1.0 + (level - 1) * 0.25
        base_stats['hp'] = int(base_stats['hp'] * level_multiplier)
        base_stats['damage'] = int(base_stats['damage'] * level_multiplier)
        base_stats['xp_reward'] = int(base_stats['xp_reward'] * level_multiplier)
        base_stats['currency_reward'] = int(base_stats['currency_reward'] * level_multiplier)
        base_stats['level'] = level
        base_stats['creature_type'] = creature_type  # Store the type

        return base_stats


def start_combat(character, creature_type, creature_level=1):
    """
    Start combat between a character and a creature.

    Args:
        character: The character
        creature_type: Type of creature to fight
        creature_level: Level of the creature

    Returns:
        CombatHandler: The combat handler
    """
    # Check if already in combat
    if character.db.in_combat:
        character.send_text_output("You are already in combat!", 'error')
        return None

    # Create creature stats
    creature_stats = Creature.create_creature(creature_type, creature_level)

    # Create a simple object to hold creature stats
    class CreatureObject:
        def __init__(self, stats):
            self.key = f"creature_{creature_type}_{random.randint(1000, 9999)}"
            self.name = stats['name']
            self.db = type('obj', (object,), {})()

            for key, value in stats.items():
                setattr(self.db, key, value)

            self.db.in_combat = False
            self.db.combat_target = None

        def get_display_name(self, viewer):
            return self.name

        def take_damage(self, amount, attacker=None):
            self.db.hp -= amount
            return self.db.hp > 0

        def send_text_output(self, text, text_class):
            pass  # Creatures don't send output

        def send_to_web_client(self, message_dict):
            pass  # Creatures don't send WebSocket messages

    creature = CreatureObject(creature_stats)

    # Create combat handler
    combat = CombatHandler(character, creature)

    # Send combat started event
    character.send_to_web_client({
        "type": "combat_event",
        "event": "combat_started",
        "enemy": {
            "id": creature.key,
            "name": creature.name,
            "creature_type": creature_type,
            "health": creature.db.hp,
            "max_health": creature.db.hp,
            "level": creature.db.level,
            "sprite": creature.db.sprite
        }
    })

    character.send_text_output(f"You encounter a {creature.name}!", 'combat')
    character.send_text_output(f"{creature.name} attacks you!", 'combat')

    return combat


def continue_combat(character, action="attack"):
    """
    Continue combat with a specific action.

    Args:
        character: The character in combat
        action: The action to take ('attack', 'defend', 'heal', 'flee')

    Returns:
        dict: Combat result
    """
    if not character.db.in_combat or not character.db.combat_target:
        character.send_text_output("You are not in combat!", 'error')
        return None

    creature = character.db.combat_target
    result = {}

    if action == "attack":
        # Character attacks
        attacker_result = character.db.combat.attacker_turn() if hasattr(character.db, 'combat') else None

        if attacker_result:
            character.send_text_output(attacker_result['message'], 'combat')

            if attacker_result.get('combat_ended'):
                return attacker_result

            # Creature counter-attacks
            # Create temporary reverse combat for creature
            damage = random.randint(1, 10)
            character.take_damage(damage)
            character.send_text_output(f"{creature.name} attacks you for {damage} damage!", 'combat')

            # Send combat health update
            character.send_to_web_client({
                "type": "combat_event",
                "event": "health_updated",
                "attacker_health": creature.db.hp,
                "target_health": character.db.hp,
                "message": f"{creature.name} retaliates!"
            })

            result = attacker_result

    elif action == "defend":
        character.send_text_output("You brace for impact, reducing damage.", 'combat')
        # Defender gets 50% damage reduction next turn
        character.db.defending = True
        result["defending"] = True

    elif action == "heal":
        # Attempt to heal
        healing_amount = 15
        character.heal(healing_amount)
        character.send_text_output(f"You heal yourself for {healing_amount} HP.", 'success')

    elif action == "flee":
        # Attempt to flee
        flee_chance = character.db.courage or 5
        if random.random() < (flee_chance / 10.0):
            character.send_text_output(f"You successfully flee from {creature.name}!", 'success')
            character.db.in_combat = False
            character.db.combat_target = None
            result["fled"] = True
        else:
            character.send_text_output(f"You failed to flee from {creature.name}!", 'error')
            # Creature attacks
            damage = random.randint(1, 8)
            character.take_damage(damage)
            character.send_text_output(f"{creature.name} attacks you for {damage} damage!", 'combat')

    return result
