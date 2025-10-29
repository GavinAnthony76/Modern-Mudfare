"""
Quest Commands for Journey Through Scripture

Commands for managing quests: quests, accept, abandon, complete
"""

from evennia import Command

# Handle imports in both direct and Evennia contexts
try:
    from ..quests import create_quest, QuestStatus
except (ImportError, ValueError):
    # Fallback for Evennia's module loading context
    import os
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from quests import create_quest, QuestStatus


class CmdQuests(Command):
    """
    View active quests.

    Usage:
        quests
        quests active
        quests completed

    Shows your active quests or other quest lists.
    """

    key = "quests"
    aliases = ["q", "journal", "log"]
    locks = "cmd:all()"
    help_category = "quest"

    def func(self):
        """Execute quests command"""
        if not hasattr(self.caller, 'quest_manager'):
            self.caller.send_text_output("Quest system not initialized.", "error")
            return

        if self.args:
            quest_type = self.args.strip().lower()
        else:
            quest_type = "active"

        output = "\n|w=== QUEST LOG ===|n\n"

        if quest_type in ["active", "all"]:
            active_quests = self.caller.quest_manager.get_active_quests()
            if active_quests:
                output += "|yActive Quests:|n\n"
                for quest in active_quests:
                    output += f"  • {quest.title} (Level {quest.level})\n"
                    for obj in quest.objectives:
                        current = quest.progress.get(obj["id"], 0)
                        required = obj.get("required", 1)
                        status = "✓" if current >= required else "○"
                        output += f"    {status} {obj['description']}: {current}/{required}\n"
                    output += "\n"
            else:
                output += "|yNo active quests.|n\n"

        if quest_type in ["completed", "all"]:
            completed_quests = self.caller.quest_manager.get_completed_quests()
            if completed_quests:
                output += "|gCompleted Quests:|n\n"
                for quest in completed_quests:
                    output += f"  ✓ {quest.title}\n"
                output += "\n"
            elif quest_type == "completed":
                output += "|gNo completed quests yet.|n\n"

        output += "|wAvailable Quests:|n\n"
        available = [q for q in self.caller.quest_manager.quests.values()
                     if q.status == QuestStatus.AVAILABLE]
        if available:
            for quest in available:
                output += f"  • {quest.title} (Level {quest.level})\n"
                output += f"    Type 'accept {quest.id}' to start\n"
        else:
            output += "  No new quests available.\n"

        self.caller.send_text_output(output, "system")


class CmdAccept(Command):
    """
    Accept a quest.

    Usage:
        accept <quest_id>
        accept quest_meet_elder

    Starts a new quest. Use 'quests' to see available quests.
    """

    key = "accept"
    aliases = ["start"]
    locks = "cmd:all()"
    help_category = "quest"

    def func(self):
        """Execute accept command"""
        if not self.args:
            self.caller.send_text_output("Accept which quest? Use 'quests' to see available.", "error")
            return

        quest_id = self.args.strip()

        if not hasattr(self.caller, 'quest_manager'):
            self.caller.send_text_output("Quest system not initialized.", "error")
            return

        # Check if quest exists in available quests
        if quest_id not in self.caller.quest_manager.quests:
            self.caller.send_text_output(f"Quest not found: {quest_id}", "error")
            return

        # Start the quest
        self.caller.quest_manager.start_quest(quest_id)


class CmdAbandon(Command):
    """
    Abandon a quest.

    Usage:
        abandon <quest_id>
        abandon quest_meet_elder

    Removes a quest from your active quest log.
    """

    key = "abandon"
    aliases = ["drop", "cancel"]
    locks = "cmd:all()"
    help_category = "quest"

    def func(self):
        """Execute abandon command"""
        if not self.args:
            self.caller.send_text_output("Abandon which quest?", "error")
            return

        quest_id = self.args.strip()

        if not hasattr(self.caller, 'quest_manager'):
            self.caller.send_text_output("Quest system not initialized.", "error")
            return

        quest = self.caller.quest_manager.get_quest(quest_id)
        if not quest:
            self.caller.send_text_output(f"Quest not found: {quest_id}", "error")
            return

        if quest.status != QuestStatus.ACTIVE:
            self.caller.send_text_output("That quest is not active.", "warning")
            return

        quest.abandon()
        self.caller.send_text_output(f"Abandoned quest: {quest.title}", "warning")

        # Send update to client
        self.caller.send_to_web_client({
            "type": "quest_update",
            "quest": quest.get_status_dict()
        })


class CmdQuestInfo(Command):
    """
    Get detailed information about a quest.

    Usage:
        questinfo <quest_id>
        questinfo quest_trial_of_strength

    Shows full details about a quest including objectives and rewards.
    """

    key = "questinfo"
    aliases = ["qinfo", "questdetails"]
    locks = "cmd:all()"
    help_category = "quest"

    def func(self):
        """Execute questinfo command"""
        if not self.args:
            self.caller.send_text_output("Get info on which quest?", "error")
            return

        quest_id = self.args.strip()

        if not hasattr(self.caller, 'quest_manager'):
            self.caller.send_text_output("Quest system not initialized.", "error")
            return

        quest = self.caller.quest_manager.get_quest(quest_id)
        if not quest:
            self.caller.send_text_output(f"Quest not found: {quest_id}", "error")
            return

        output = f"\n|w=== {quest.title} ===|n\n"
        output += f"|wLevel: |n{quest.level}\n"
        output += f"|wStatus: |n{quest.status.value.upper()}\n\n"

        output += f"|wDescription:|n\n{quest.description}\n\n"

        output += f"|wObjectives:|n\n"
        for obj in quest.objectives:
            current = quest.progress.get(obj["id"], 0)
            required = obj.get("required", 1)
            status = "✓" if current >= required else "○"
            output += f"  {status} {obj['description']}: {current}/{required}\n"

        output += f"\n|wRewards:|n\n"
        output += f"  Experience: {quest.xp_reward}\n"
        output += f"  Currency: {quest.currency_reward} shekels\n"
        if quest.item_rewards:
            output += f"  Items: {', '.join(quest.item_rewards)}\n"

        self.caller.send_text_output(output, "system")
