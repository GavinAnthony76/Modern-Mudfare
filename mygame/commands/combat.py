"""
Combat Commands for Journey Through Scripture

Commands for combat actions: attack, defend, heal, flee, etc.
"""

from evennia import Command
from evennia.utils.utils import inherits_from
from mygame.combat import start_combat, continue_combat


class CombatCommand(Command):
    """
    Base class for combat commands.
    Ensures character is in combat.
    """

    def check_combat(self):
        """Check if character is in combat"""
        if not self.caller.db.in_combat:
            self.caller.send_text_output("You are not in combat!", 'error')
            return False
        if not self.caller.db.combat_target:
            self.caller.send_text_output("Combat target lost!", 'error')
            return False
        return True


class CmdAttack(CombatCommand):
    """
    Attack your combat target.

    Usage:
        attack
        attack [target]

    If in combat, attacks your current target.
    Otherwise, initiates combat with the target.
    """

    key = "attack"
    aliases = ["a", "hit", "strike"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        """Execute attack command"""
        # If already in combat, continue fighting
        if self.caller.db.in_combat:
            continue_combat(self.caller, "attack")
            return

        # If argument given, try to attack that target
        if self.args:
            target_name = self.args.strip().lower()

            # Look for target in room
            if not self.caller.location:
                self.caller.send_text_output("You are nowhere!", 'error')
                return

            for obj in self.caller.location.contents:
                if (inherits_from(obj, "typeclasses.npcs.NPC") or
                    (hasattr(obj, 'key') and target_name in obj.key.lower()) or
                    (hasattr(obj, 'name') and target_name in obj.name.lower())):

                    # Check if it's a combatant
                    if hasattr(obj, 'db') and hasattr(obj.db, 'health'):
                        # Start combat
                        start_combat(self.caller, obj)
                        continue_combat(self.caller, "attack")
                        return

            self.caller.send_text_output(f"You don't see '{self.args}' here.", 'error')
            return

        self.caller.send_text_output("Attack what?", 'error')


class CmdDefend(CombatCommand):
    """
    Take a defensive stance.

    Usage:
        defend

    In combat, this reduces damage taken and prepares for the next attack.
    """

    key = "defend"
    aliases = ["d", "block", "guard"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        """Execute defend command"""
        if not self.check_combat():
            self.caller.send_text_output("You are not in combat!", 'error')
            return

        continue_combat(self.caller, "defend")


class CmdHeal(CombatCommand):
    """
    Use a healing item or spell.

    Usage:
        heal

    Restores your health during combat.
    """

    key = "heal"
    aliases = ["h", "restore"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        """Execute heal command"""
        if not self.check_combat():
            self.caller.send_text_output("You are not in combat!", 'error')
            return

        continue_combat(self.caller, "heal")


class CmdFlee(CombatCommand):
    """
    Attempt to flee from combat.

    Usage:
        flee

    Attempts to escape from your current enemy.
    Success depends on your Courage stat.
    """

    key = "flee"
    aliases = ["f", "run", "escape"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        """Execute flee command"""
        if not self.check_combat():
            self.caller.send_text_output("You are not in combat!", 'error')
            return

        continue_combat(self.caller, "flee")


class CmdCombatStatus(CombatCommand):
    """
    Check your combat status.

    Usage:
        status
        combat

    Displays current health and enemy status.
    """

    key = "status"
    aliases = ["st", "combat"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        """Execute status command"""
        if not self.caller.db.in_combat:
            self.caller.send_text_output("You are not in combat!", 'error')
            return

        target = self.caller.db.combat_target
        if not target:
            self.caller.send_text_output("Combat target lost!", 'error')
            return

        # Send combat status
        self.caller.send_text_output(f"\n|w=== Combat Status ===|n", 'system')
        self.caller.send_text_output(
            f"|wYour Health:|n {self.caller.db.hp}/{self.caller.db.max_hp}",
            'system'
        )
        self.caller.send_text_output(
            f"|w{target.name} Health:|n {target.db.hp}/{target.db.hp}",
            'system'
        )
        self.caller.send_text_output(
            f"|wAvailable actions:|n attack, defend, heal, flee",
            'system'
        )

        # Send updated combat event
        self.caller.send_to_web_client({
            "type": "combat_event",
            "event": "health_updated",
            "player_health": {
                "current": self.caller.db.hp,
                "max": self.caller.db.max_hp
            },
            "enemy_health": {
                "current": target.db.hp,
                "max": target.db.hp
            }
        })


class CmdFight(Command):
    """
    Initiate combat with an enemy.

    Usage:
        fight <enemy>
        fight orc
        fight demon

    Starts combat with a creature type.
    """

    key = "fight"
    aliases = ["encounter", "battle"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        """Execute fight command"""
        if not self.args:
            self.caller.send_text_output("Fight what? (orc, demon, etc.)", 'error')
            return

        creature_type = self.args.strip().lower()

        # Valid creature types
        valid_creatures = ['orc', 'demon', 'leviathan', 'behemoth', 'nephilim', 'dark_knight', 'serpent']

        if creature_type not in valid_creatures:
            self.caller.send_text_output(
                f"Unknown creature. Valid types: {', '.join(valid_creatures)}",
                'error'
            )
            return

        # Start combat
        level = 1  # Could be adjusted based on room or difficulty
        start_combat(self.caller, creature_type, level)

