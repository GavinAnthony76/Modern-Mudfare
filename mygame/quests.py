"""
Quest System for Journey Through Scripture

Manages quests, objectives, rewards, and player progress.
Integrated with combat system for quest-based encounters.
"""

from enum import Enum
from datetime import datetime
import json


class QuestStatus(Enum):
    """Quest status enumeration"""
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class ObjectiveType(Enum):
    """Types of quest objectives"""
    KILL_CREATURE = "kill_creature"
    COLLECT_ITEM = "collect_item"
    REACH_LOCATION = "reach_location"
    TALK_TO_NPC = "talk_to_npc"
    USE_ITEM = "use_item"
    DISCOVER_LOCATION = "discover_location"


class Quest:
    """Represents a single quest"""

    def __init__(self, quest_id, title, description, level=1, **kwargs):
        """
        Initialize a quest.

        Args:
            quest_id: Unique quest identifier
            title: Quest title
            description: Long description
            level: Recommended level
            **kwargs: Additional attributes
        """
        self.id = quest_id
        self.title = title
        self.description = description
        self.level = level

        # Objectives
        self.objectives = kwargs.get("objectives", [])

        # Rewards
        self.xp_reward = kwargs.get("xp_reward", 100)
        self.currency_reward = kwargs.get("currency_reward", 50)
        self.item_rewards = kwargs.get("item_rewards", [])

        # Quest properties
        self.status = QuestStatus.AVAILABLE
        self.started_at = None
        self.completed_at = None
        self.giver_id = kwargs.get("giver_id", None)
        self.repeatable = kwargs.get("repeatable", False)
        self.series = kwargs.get("series", None)  # Quest series ID

        # Progress tracking
        self.progress = {}
        for obj in self.objectives:
            self.progress[obj["id"]] = 0

    def start(self):
        """Start the quest"""
        self.status = QuestStatus.ACTIVE
        self.started_at = datetime.now()

    def complete(self):
        """Complete the quest"""
        self.status = QuestStatus.COMPLETED
        self.completed_at = datetime.now()

    def abandon(self):
        """Abandon the quest"""
        self.status = QuestStatus.ABANDONED

    def fail(self):
        """Fail the quest"""
        self.status = QuestStatus.FAILED

    def update_objective(self, objective_id, progress_value):
        """
        Update progress on an objective.

        Args:
            objective_id: ID of objective
            progress_value: New progress value

        Returns:
            bool: True if objective completed
        """
        if objective_id not in self.progress:
            return False

        self.progress[objective_id] = progress_value

        # Get objective requirement
        obj = next((o for o in self.objectives if o["id"] == objective_id), None)
        if obj:
            required = obj.get("required", 1)
            return progress_value >= required

        return False

    def is_complete(self):
        """Check if all objectives are complete"""
        for obj in self.objectives:
            required = obj.get("required", 1)
            current = self.progress.get(obj["id"], 0)
            if current < required:
                return False
        return True

    def get_status_dict(self):
        """Get quest status as dict for sending to client"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "level": self.level,
            "objectives": [
                {
                    "id": obj["id"],
                    "description": obj["description"],
                    "type": obj["type"],
                    "required": obj.get("required", 1),
                    "current": self.progress.get(obj["id"], 0),
                    "completed": self.progress.get(obj["id"], 0) >= obj.get("required", 1)
                }
                for obj in self.objectives
            ],
            "rewards": {
                "xp": self.xp_reward,
                "currency": self.currency_reward,
                "items": self.item_rewards
            }
        }


class QuestManager:
    """Manages quests for a character"""

    def __init__(self, character):
        """
        Initialize quest manager.

        Args:
            character: The character object
        """
        self.character = character
        self.quests = {}
        self.quest_log = {}

        # Load from character db if exists
        if hasattr(character.db, 'quests'):
            self.quests = character.db.quests or {}
        if hasattr(character.db, 'quest_log'):
            self.quest_log = character.db.quest_log or {}

    def add_quest(self, quest):
        """
        Add a quest to character's available quests.

        Args:
            quest: Quest object
        """
        self.quests[quest.id] = quest
        self.character.db.quests = self.quests

        self.character.send_text_output(
            f"Quest available: {quest.title}",
            "system"
        )

    def start_quest(self, quest_id):
        """
        Start a quest.

        Args:
            quest_id: ID of quest to start

        Returns:
            Quest: The started quest or None
        """
        if quest_id not in self.quests:
            self.character.send_text_output(f"Quest not found: {quest_id}", "error")
            return None

        quest = self.quests[quest_id]

        if quest.status != QuestStatus.AVAILABLE:
            self.character.send_text_output(
                f"Quest {quest.title} is already active or completed",
                "warning"
            )
            return None

        quest.start()
        self.quest_log[quest_id] = quest
        self.character.db.quest_log = self.quest_log

        self.character.send_text_output(f"Started quest: {quest.title}", "success")
        self.character.send_text_output(quest.description, "narrative")

        # Send to web client
        self.character.send_to_web_client({
            "type": "quest_update",
            "quest": quest.get_status_dict()
        })

        return quest

    def update_quest_progress(self, quest_id, objective_id, value=1):
        """
        Update progress on a quest objective.

        Args:
            quest_id: ID of quest
            objective_id: ID of objective
            value: Progress amount (adds to current)

        Returns:
            bool: True if objective was just completed
        """
        if quest_id not in self.quest_log:
            return False

        quest = self.quest_log[quest_id]

        # Get current value
        current = quest.progress.get(objective_id, 0)
        new_value = current + value

        # Update objective
        objective_completed = quest.update_objective(objective_id, new_value)

        # Get objective info
        obj = next((o for o in quest.objectives if o["id"] == objective_id), None)
        if obj:
            self.character.send_text_output(
                f"[{quest.title}] {obj['description']}: {new_value}/{obj.get('required', 1)}",
                "system"
            )

        # Check if quest is complete
        if quest.is_complete():
            self.complete_quest(quest_id)
            return True

        # Send update to client
        self.character.send_to_web_client({
            "type": "quest_update",
            "quest": quest.get_status_dict()
        })

        return objective_completed

    def complete_quest(self, quest_id):
        """
        Complete a quest and give rewards.

        Args:
            quest_id: ID of quest to complete
        """
        if quest_id not in self.quest_log:
            return

        quest = self.quest_log[quest_id]
        quest.complete()

        # Award XP
        self.character.gain_xp(quest.xp_reward)

        # Award currency
        self.character.db.currency = (self.character.db.currency or 0) + quest.currency_reward

        # Award items
        for item_key in quest.item_rewards:
            # Create item from database (simplified)
            self.character.send_text_output(
                f"Received: {item_key}",
                "success"
            )

        # Send completion message
        self.character.send_text_output(
            f"Quest completed: {quest.title}!",
            "success"
        )
        self.character.send_text_output(
            f"Rewards: {quest.xp_reward} XP, {quest.currency_reward} shekels",
            "success"
        )

        # Send to client
        self.character.send_to_web_client({
            "type": "quest_update",
            "quest": quest.get_status_dict()
        })

        # Mark as completed
        self.character.db.quest_log = self.quest_log

    def get_quest(self, quest_id):
        """Get a quest by ID"""
        if quest_id in self.quest_log:
            return self.quest_log[quest_id]
        return self.quests.get(quest_id)

    def get_active_quests(self):
        """Get all active quests"""
        return [q for q in self.quest_log.values() if q.status == QuestStatus.ACTIVE]

    def get_completed_quests(self):
        """Get all completed quests"""
        return [q for q in self.quest_log.values() if q.status == QuestStatus.COMPLETED]


# Pre-defined quests
QUEST_DEFINITIONS = {
    "quest_meet_elder": {
        "title": "Meet the Elder",
        "description": "Seek out the Elder of the Courtyard and learn about the tests ahead.",
        "level": 1,
        "xp_reward": 100,
        "currency_reward": 50,
        "giver_id": "gate_keeper_samuel",
        "objectives": [
            {
                "id": "obj_talk_elder",
                "description": "Speak to the Elder",
                "type": ObjectiveType.TALK_TO_NPC.value,
                "required": 1
            }
        ]
    },

    "quest_trial_of_strength": {
        "title": "Trial of Strength",
        "description": "Prove your worthiness by defeating the creatures that dwell in the depths. Three must fall before you.",
        "level": 2,
        "xp_reward": 250,
        "currency_reward": 150,
        "giver_id": "priest_ezra",
        "objectives": [
            {
                "id": "obj_defeat_orc",
                "description": "Defeat the Orc Guardian",
                "type": ObjectiveType.KILL_CREATURE.value,
                "creature_type": "orc",
                "required": 1
            },
            {
                "id": "obj_defeat_demon",
                "description": "Defeat the Demon of Shadows",
                "type": ObjectiveType.KILL_CREATURE.value,
                "creature_type": "demon",
                "required": 1
            },
            {
                "id": "obj_defeat_serpent",
                "description": "Defeat the Ancient Serpent",
                "type": ObjectiveType.KILL_CREATURE.value,
                "creature_type": "serpent",
                "required": 1
            }
        ]
    },

    "quest_the_descent": {
        "title": "The Descent",
        "description": "Journey to the lower floors and face the trials that await. Return with proof of your journey.",
        "level": 3,
        "xp_reward": 500,
        "currency_reward": 250,
        "series": "main_story",
        "objectives": [
            {
                "id": "obj_reach_floor2",
                "description": "Reach the Second Floor",
                "type": ObjectiveType.REACH_LOCATION.value,
                "location": "floor2_entrance",
                "required": 1
            },
            {
                "id": "obj_reach_floor3",
                "description": "Reach the Third Floor",
                "type": ObjectiveType.REACH_LOCATION.value,
                "location": "floor3_entrance",
                "required": 1
            }
        ]
    },

    "quest_dark_knight_challenge": {
        "title": "The Dark Knight's Challenge",
        "description": "A formidable warrior challenges you to single combat. Defeat the Dark Knight to prove your mastery.",
        "level": 4,
        "xp_reward": 400,
        "currency_reward": 200,
        "objectives": [
            {
                "id": "obj_defeat_dark_knight",
                "description": "Defeat the Dark Knight",
                "type": ObjectiveType.KILL_CREATURE.value,
                "creature_type": "dark_knight",
                "required": 1
            }
        ]
    },

    "quest_behemoth_hunt": {
        "title": "The Behemoth Hunt",
        "description": "An ancient Behemoth has been awakened in the depths. Only the bravest should attempt this hunt.",
        "level": 5,
        "xp_reward": 600,
        "currency_reward": 350,
        "objectives": [
            {
                "id": "obj_defeat_behemoth",
                "description": "Hunt and defeat the Behemoth",
                "type": ObjectiveType.KILL_CREATURE.value,
                "creature_type": "behemoth",
                "required": 1
            }
        ]
    },

    "quest_leviathan_awakened": {
        "title": "Leviathan Awakened",
        "description": "The ancient Leviathan has stirred from its slumber. This is the ultimate test of your abilities.",
        "level": 6,
        "xp_reward": 1000,
        "currency_reward": 500,
        "series": "main_story",
        "objectives": [
            {
                "id": "obj_defeat_leviathan",
                "description": "Defeat the Leviathan",
                "type": ObjectiveType.KILL_CREATURE.value,
                "creature_type": "leviathan",
                "required": 1
            }
        ]
    }
}


def create_quest(quest_id):
    """
    Create a quest object from definition.

    Args:
        quest_id: ID of quest to create

    Returns:
        Quest: The created quest or None
    """
    if quest_id not in QUEST_DEFINITIONS:
        return None

    quest_def = QUEST_DEFINITIONS[quest_id]
    return Quest(
        quest_id,
        quest_def["title"],
        quest_def["description"],
        quest_def.get("level", 1),
        **quest_def
    )
