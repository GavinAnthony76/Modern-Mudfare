# Quest System Documentation

## Overview

The quest system provides a flexible framework for tracking player progress through objectives, managing multiple quests, and automatically integrating with the combat system.

## Features

- **Multiple Quests**: Players can track multiple active quests simultaneously
- **Objectives**: Quests have multiple objectives with progress tracking
- **Rewards**: XP, currency, and item rewards on completion
- **Quest Series**: Chain quests together into story arcs
- **Combat Integration**: Automatically update quest progress when defeating creatures
- **WebSocket Updates**: Real-time updates sent to web client

## Quest System Architecture

### Core Classes

#### Quest
Represents a single quest with objectives and rewards.

```python
quest = Quest(
    "quest_id",
    "Quest Title",
    "Quest description...",
    level=1,
    xp_reward=100,
    currency_reward=50,
    objectives=[
        {
            "id": "obj_1",
            "description": "Defeat the Orc",
            "type": "kill_creature",
            "creature_type": "orc",
            "required": 1
        }
    ]
)
```

#### QuestManager
Manages all quests for a character.

```python
# Initialize
manager = QuestManager(character)

# Start a quest
quest = manager.start_quest("quest_id")

# Update progress
manager.update_quest_progress("quest_id", "obj_id", 1)

# Get quests
active = manager.get_active_quests()
completed = manager.get_completed_quests()
```

### Objective Types

```
KILL_CREATURE     - Defeat N creatures
COLLECT_ITEM      - Gather N items
REACH_LOCATION    - Visit a specific room
TALK_TO_NPC       - Talk to an NPC
USE_ITEM          - Use an item
DISCOVER_LOCATION - Find a hidden location
```

## Quest Commands

### quests / q
View your quest log.

```
> quests
> quests active
> quests completed
```

Shows:
- Active quests with progress
- Completed quests
- Available quests to start

### accept
Start a quest.

```
> accept quest_trial_of_strength
```

### abandon / drop
Abandon an active quest.

```
> abandon quest_trial_of_strength
```

### questinfo / qinfo
Get detailed information about a quest.

```
> questinfo quest_trial_of_strength
```

Shows:
- Full description
- All objectives and progress
- XP and currency rewards
- Item rewards

## Pre-defined Quests

### 1. quest_meet_elder
**Level 1** | Rewards: 100 XP, 50 shekels

Learn about the tests ahead from the Elder.

**Objectives:**
- Speak to the Elder

### 2. quest_trial_of_strength
**Level 2** | Rewards: 250 XP, 150 shekels

Prove your worthiness by defeating three creatures.

**Objectives:**
- Defeat the Orc Guardian (1)
- Defeat the Demon of Shadows (1)
- Defeat the Ancient Serpent (1)

**Integration:** Automatically updates when you defeat these creature types in combat.

### 3. quest_the_descent
**Level 3** | Rewards: 500 XP, 250 shekels

Journey to the lower floors of the palace.

**Objectives:**
- Reach the Second Floor
- Reach the Third Floor

### 4. quest_dark_knight_challenge
**Level 4** | Rewards: 400 XP, 200 shekels

Face a formidable warrior in single combat.

**Objectives:**
- Defeat the Dark Knight

### 5. quest_behemoth_hunt
**Level 5** | Rewards: 600 XP, 350 shekels

Hunt an ancient Behemoth in the depths.

**Objectives:**
- Hunt and defeat the Behemoth

### 6. quest_leviathan_awakened
**Level 6** | Rewards: 1000 XP, 500 shekels

The ultimate test - face the ancient Leviathan.

**Objectives:**
- Defeat the Leviathan

## Combat Integration

Quests automatically update when you defeat creatures. Example flow:

```
1. Player starts "Trial of Strength" quest
   > accept quest_trial_of_strength

2. Player encounters and defeats an Orc
   > fight orc
   > attack
   (Combat sequence...)
   Victory! You defeated Orc!

3. Quest updates automatically
   [Trial of Strength] Defeat the Orc Guardian: 1/1 ✓

4. Continue for other creatures

5. When all objectives complete
   Quest completed: Trial of Strength!
   Rewards: 250 XP, 150 shekels
```

## WebSocket Integration

Quest updates are sent to the web client automatically:

```json
{
  "type": "quest_update",
  "quest": {
    "id": "quest_trial_of_strength",
    "title": "Trial of Strength",
    "status": "active",
    "objectives": [
      {
        "id": "obj_defeat_orc",
        "description": "Defeat the Orc Guardian",
        "type": "kill_creature",
        "required": 1,
        "current": 1,
        "completed": true
      }
    ],
    "rewards": {
      "xp": 250,
      "currency": 150,
      "items": []
    }
  }
}
```

## Implementation Guide

### Adding a New Quest

1. **Define the quest in QUEST_DEFINITIONS** (quests.py):

```python
QUEST_DEFINITIONS = {
    "quest_my_quest": {
        "title": "My Quest Title",
        "description": "Detailed description...",
        "level": 2,
        "xp_reward": 200,
        "currency_reward": 100,
        "giver_id": "npc_id",
        "objectives": [
            {
                "id": "obj_1",
                "description": "Objective description",
                "type": "kill_creature",
                "creature_type": "orc",
                "required": 1
            }
        ]
    }
}
```

2. **Give the quest to players** (in NPC dialogue or startup):

```python
# In an NPC's dialogue handler
quest = create_quest("quest_my_quest")
character.quest_manager.add_quest(quest)
```

3. **Quest automatically updates** when objectives are met:

```python
# When defeating a creature, combat.py handles this:
creature_type = getattr(creature.db, 'creature_type', None)
if creature_type:
    for quest in character.quest_manager.get_active_quests():
        for obj in quest.objectives:
            if (obj.get("type") == "kill_creature" and
                obj.get("creature_type") == creature_type):
                character.quest_manager.update_quest_progress(
                    quest.id,
                    obj["id"],
                    1
                )
```

### Custom Objective Handling

To handle custom objective types, extend the combat victory handler:

```python
# In combat.py end_combat method
# For location objectives
if player.location.key == "target_location":
    character.quest_manager.update_quest_progress(
        quest.id,
        obj["id"],
        1
    )

# For item collection
if item_in_inventory:
    character.quest_manager.update_quest_progress(
        quest.id,
        obj["id"],
        1
    )
```

## Database Storage

Quests are stored in character.db:

```python
character.db.quests       # Available quests (dict of Quest objects)
character.db.quest_log    # Active/completed quests (dict of Quest objects)
```

Serialization happens automatically via Evennia's database system.

## Testing Quest System

### Manual Testing

```bash
# Start server
cd mygame
evennia start

# In game
> quests
# Should show available quests

> accept quest_trial_of_strength
# Quest starts

> quests
# Shows active quest with objectives

> fight orc
> attack
# Victory over orc

> quests
# Should show orc objective as complete (1/1)

> fight demon
> attack
# Victory over demon

> quests
# Shows demon objective as complete

> fight serpent
> attack
# Victory over serpent

> quests
# Should show quest complete!
```

### Expected Output

```
Quest Started: Trial of Strength

Description: Prove your worthiness by defeating the creatures
that dwell in the depths. Three must fall before you.

Objectives:
1. Defeat the Orc Guardian: 0/1
2. Defeat the Demon of Shadows: 0/1
3. Defeat the Ancient Serpent: 0/1

(After defeating orc)

[Trial of Strength] Defeat the Orc Guardian: 1/1 ✓

(After defeating demon)

[Trial of Strength] Defeat the Demon of Shadows: 1/1 ✓

(After defeating serpent)

[Trial of Strength] Defeat the Ancient Serpent: 1/1 ✓

Quest completed: Trial of Strength!
Rewards: 250 XP, 150 shekels
```

## Future Enhancements

- [ ] Quest series tracking (main story quests)
- [ ] Branching quest paths based on choices
- [ ] Timed quests with deadlines
- [ ] Multi-stage quests with checkpoints
- [ ] Quest failure conditions
- [ ] Quest rewards customization
- [ ] NPC quest giver assignments
- [ ] Quest tracker on character screen
- [ ] Quest notifications and alerts
- [ ] Repeatable daily quests
- [ ] Group quest support
- [ ] Quest statistics and tracking

## Architecture Diagram

```
Character
  ├── quest_manager: QuestManager
  │   ├── quests: dict[Quest]  (available)
  │   ├── quest_log: dict[Quest]  (active/completed)
  │   └── Methods:
  │       ├── add_quest()
  │       ├── start_quest()
  │       ├── update_quest_progress()
  │       ├── complete_quest()
  │       └── get_*_quests()
  │
  └── Combat System
      └── On victory:
          ├── Check active quests
          ├── Find matching objectives
          └── Call quest_manager.update_quest_progress()
              ├── Update progress
              ├── Check if complete
              ├── Award rewards
              └── Send WebSocket update
```

## Summary

The quest system provides:
- ✅ Quest tracking and management
- ✅ Objective-based progression
- ✅ Combat integration
- ✅ Automatic progress updates
- ✅ WebSocket client synchronization
- ✅ Rewards on completion
- ✅ Quest series support

Players can now experience full quest chains that integrate seamlessly with combat and progression systems.
