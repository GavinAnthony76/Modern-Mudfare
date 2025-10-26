# World Design - Journey Through Scripture

## Overview

The Palace of Light is a seven-floor vertical dungeon representing spiritual ascent. Each floor has a theme, challenges, NPCs, items, and a safe room with a priest. Floor 1 is fully detailed with 9 rooms. Floors 2-7 are sketched and ready for expansion.

## The Seven Floors

### Floor 1: THE OUTER COURT ✓ (Fully Implemented)
- **Theme**: Introduction, exploration, first trials
- **Rooms**: 9 (including 1 safe room, 1 hidden room, 1 boss room)
- **Key NPCs**: Priest Ezra, Gate Keeper Samuel, Garden Keeper Ruth, The Deceiver (Boss)
- **Boss**: The Deceiver (False Prophet blocking ascent to Floor 2)
- **Reward**: Access to Floor 2, Deceiver's Staff, Experience
- **Lore Focus**: Learning the basics, understanding the palace structure

### Floor 2: THE COURT OF WISDOM
- **Theme**: Knowledge, learning, scriptural study, debate
- **Rooms**: 3 (Ascending Stairs, Library [SAFE], Debate Hall)
- **Key NPC**: Priest Miriam
- **Enemy**: False Teacher (debate-based encounter)
- **Lore Focus**: Discernment between truth and clever lies

### Floor 3: THE COURT OF SERVICE
- **Theme**: Helping others, craftsmanship, healing, humility
- **Rooms**: 4 (Stairs, Workshop, Healing Chambers [SAFE], Kitchen)
- **Key NPC**: Priest-Healer Tobias
- **Enemy**: Greedy Steward
- **Lore Focus**: Service over self, practical skills

### Floor 4: THE COURT OF TRIAL
- **Theme**: Testing faith, spiritual warfare, darker challenges
- **Rooms**: 3 (Darkening Stairway, Prayer Sanctuary [SAFE], Trial Chamber)
- **Key NPC**: Priest-Warrior Caleb
- **Enemies**: Shadow of Doubt, Manifestation of Pride
- **Lore Focus**: Inner struggles, spiritual combat

### Floor 5: THE COURT OF SACRIFICE
- **Theme**: Letting go, surrender, difficult choices
- **Rooms**: 3 (Stairs of Relinquishment, Altar Room [SAFE], Guardian's Gate)
- **Key NPC**: Priest-Elder Sarah
- **Boss**: Guardian Angel Raphael (test of worthiness)
- **Lore Focus**: What must be surrendered to ascend?

### Floor 6: THE COURT OF REVELATION
- **Theme**: Hidden truths, mysteries, spiritual vision
- **Rooms**: 3 (Stairway of Visions, Revelation Sanctuary [SAFE], Vision Chamber)
- **Key NPC**: Priest-Seer Ezekiel
- **Enemy**: False Prophet of Visions
- **Lore Focus**: Discerning true revelation from deception

### Floor 7: THE HOLY OF HOLIES
- **Theme**: Ultimate trial, divine presence, completion
- **Rooms**: 4 (Final Ascent, Preparation Chamber [SAFE], Veil Chamber [BOSS], Holy of Holies [COMPLETION])
- **Key NPC**: High Priest Aaron
- **Final Boss**: Corrupted Cherub
- **Lore Focus**: The culmination of the spiritual journey

## Room Types

### Normal Rooms
- Standard exploration and encounters
- May contain items, NPCs, enemies
- Connected to other rooms via exits

### Safe Rooms (Sanctuaries)
- One per floor
- Tended by a Priest NPC
- Services: Healing, Saving, Blessings
- NO combat allowed
- Marked with `"room_type": "safe"` and `"is_save_point": True`

### Hidden Rooms
- Require exploration or special items to discover
- Often contain valuable lore or items
- Examples: Floor 1's Hidden Alcove

### Boss Rooms
- Contain major enemies blocking progress
- Often lock access to next floor
- May have alternative solutions (wisdom/faith checks vs combat)
- `"room_type": "boss"`

### Completion Rooms
- End-game areas
- No further progression
- Victory/completion scenes

## Navigation System

### Exit Types

1. **Cardinal Directions**: `north`, `south`, `east`, `west`, `up`, `down`
2. **Descriptive**: `through gate`, `narrow path`, `hidden door`
3. **Locked Exits**: Require defeating bosses or obtaining keys
   ```python
   "locked_exit": {
       "direction": "stairs up",
       "unlocks_to": "floor2_ascending_stairs",
       "requires": "defeated_the_deceiver"
   }
   ```

### Example Room Structure

```python
"floor1_courtyard": {
    "key": "Courtyard of Beginnings",
    "desc": "A vast open courtyard...",
    "floor": 1,
    "room_type": "normal",
    "exits": {
        "south": "floor1_entrance",
        "north": "floor1_pilgrim_rest",
        "east": "floor1_hall_testing",
        "west": "floor1_garden"
    },
    "items": ["inscribed_stone", "fountain_water"],
    "npcs": ["young_priest", "water_bearer"],
    "danger_level": 1,
    "hint": "The heart of the outer court...",
    "lore": "Every pilgrim who enters...",
    "ambient_sounds": ["splashing fountain", "murmured prayers"]
}
```

## Item System

### Item Types

1. **Consumables**: Heal, boost stats, single or multiple uses
   - `healing_bread`, `anointing_oil`, `fountain_water`

2. **Weapons**: Increase damage, may have stat requirements
   - `worn_walking_staff`, `bronze_short_sword`, `forgotten_sword`, `deceiver_staff`

3. **Equipment**: Armor, clothing, accessories with stat bonuses
   - `prayer_shawl`, `meditation_stone`

4. **Lore Items**: Readable, provide backstory and hints
   - `pilgrim_journal`, `ancient_scroll`, `false_scripture`

5. **Quest Items**: Required for progression
   - `mysterious_key`, `silver_key`, `sacred_lamp`

6. **Materials**: Crafting ingredients
   - `hyssop_branch`, `brazier_ash`, `olive_branch`

7. **Currency**: Trade items
   - `temple_shekel`, `forgotten_coin`

8. **Keys**: Unlock doors and chests
   - `mysterious_key` (Floor 1 hidden door), `silver_key` (Floor 2+)

### Item Properties

```python
"forgotten_sword": {
    "key": "Sword of the Faithful",
    "desc": "An exceptional weapon abandoned by a pilgrim long ago.",
    "item_type": "weapon",
    "stats": {
        "damage": 8,
        "strength_bonus": 3,
        "faith_bonus": 2
    },
    "value": 100,
    "weight": 4,
    "usable_by": ["warrior", "shepherd", "prophet"]
}
```

### Special Item Features

- **Readable Items**: Have `"readable": True` and `"text"` field
- **Cursed Items**: Like `deceiver_staff`, have penalties
- **Blessed Items**: Grant bonuses without penalties
- **Quest-Critical**: Cannot be dropped/sold

## NPC System

### NPC Types

1. **Friendly**: Helpful, provide information and quests
2. **Neutral**: May help or hinder based on player actions
3. **Merchant**: Buy/sell items
4. **Priest**: Provide sanctuary services (heal, save, bless)
5. **Hostile**: Enemies to fight or avoid
6. **Boss**: Major encounters blocking progression

### Dialogue Structure

```python
"dialogue": {
    "greeting": "Welcome message",
    "main_menu": {
        1: {"text": "Option 1", "response": "response_key"},
        2: {"text": "Option 2", "response": "response_key"},
        3: {"text": "Farewell", "response": "farewell"}
    },
    "responses": {
        "response_key": "The NPC's response text or action",
        "farewell": "Goodbye message"
    }
}
```

### Special NPC Features

- **Conditional Dialogue**: Some options require quest completion
  ```python
  4: {"text": "What is my calling?", "response": "calling", "requires": "defeated_deceiver"}
  ```

- **Merchant NPCs**: Have `"shop_inventory"` and `"shop_prices"`
- **Priest NPCs**: Provide `"services": ["heal", "save", "bless"]`
- **Boss NPCs**: Have `"boss_stats"`, `"defeat_unlocks"`, `"defeat_reward"`

### NPC Example

```python
"priest_ezra": {
    "key": "Priest Ezra",
    "desc": "An elderly priest with kind eyes...",
    "room": "floor1_pilgrim_rest",
    "npc_type": "priest",
    "dialogue": { ... },
    "services": ["heal", "save", "bless"]
}
```

## Combat System (To Be Implemented)

### Basic Combat Flow

1. **Initiative**: Determined by Wisdom + random roll
2. **Actions**: Move, Attack, Use Item, Cast Spell (if applicable)
3. **Damage Calculation**:
   - Physical: `(Strength × Weapon Multiplier) - Enemy Defense`
   - Magical: `(Faith × Spell Power) - Enemy Resistance`
4. **Victory**: Gain XP, loot, and unlock progress

### Alternative Solutions

Many encounters can be resolved without combat:
- **Wisdom Checks**: Outsmart or expose enemies
- **Faith Checks**: Resist spiritual attacks
- **Dialogue**: Convince, convert, or calm hostiles
- **Stealth**: Avoid encounters entirely

### Boss Encounters

Floor 1 Boss Example:
```python
"the_deceiver": {
    "boss_stats": {
        "hp": 50,
        "damage": 8,
        "defense": 3,
        "special_ability": "confusion_attack",
        "weakness": "truth_exposure"
    },
    "defeat_unlocks": "floor2_ascending_stairs",
    "defeat_reward": ["deceiver_staff", "experience_100", "access_floor_2"]
}
```

## Progression System

### Vertical Progression

- Start on Floor 1 (Outer Court)
- Defeat floor boss to unlock next floor
- Each floor increases in difficulty (danger_level)
- Safe rooms on each floor provide respite

### Character Callings

After defeating The Deceiver (Floor 1 Boss), players can choose a "calling" that influences their path:

1. **Calling of Wisdom**: Bonuses in Floor 2 (Court of Wisdom)
2. **Calling of Service**: Bonuses in Floor 3 (Court of Service)
3. **Calling of Trial**: Bonuses in Floor 4 (Court of Trial)
4. **Calling of Sacrifice**: Bonuses in Floor 5 (Court of Sacrifice)
5. **Calling of Revelation**: Bonuses in Floor 6 (Court of Revelation)

### Experience and Levels

- Gain XP from combat, quests, exploration
- Level up improves stats
- Higher floors require higher levels (recommended)

## Exploration Rewards

### Hidden Secrets

- **Floor 1**: Hidden Alcove (accessible from Garden or Merchant Corner)
- Contains valuable lore, rare items, and hints about upper floors
- Rewards thorough exploration

### Environmental Storytelling

- Ambient sounds enhance immersion
- Room descriptions reveal lore
- Items tell stories of past pilgrims
- NPC dialogue provides context

### Lore Collection

Players can collect:
- Pilgrim journals
- Ancient scrolls
- Inscriptions and plaques
- NPC stories
- Boss backstories

This builds a complete narrative of the Palace's history and purpose.

## Implementation Status

### ✓ Completed

- [x] Floor 1 complete room data (9 rooms)
- [x] Floor 1 complete item database
- [x] Floor 1 complete NPC database with dialogue
- [x] Floors 2-7 skeleton structure
- [x] World data Python module
- [x] Item data Python module
- [x] NPC data Python module

### 🔄 In Progress

- [ ] Evennia typeclasses for rooms, items, NPCs
- [ ] World builder script
- [ ] Dialogue system implementation
- [ ] Combat system

### 📋 Planned

- [ ] Floors 2-7 full detail
- [ ] Quest system
- [ ] Crafting system
- [ ] Character calling mechanics
- [ ] Achievement system
- [ ] Multiple endings based on choices

## Extending the World

### Adding New Rooms

1. Add room data to appropriate `FLOOR_X_ROOMS` dict in `world_data.py`
2. Include all required fields: `key`, `desc`, `floor`, `room_type`, `exits`
3. Update `ALL_ROOMS` dict
4. Add any new items to `items.py`
5. Add any new NPCs to `npcs.py`

### Adding New Items

1. Add item to `ITEMS` dict in `items.py`
2. Include: `key`, `desc`, `item_type`, `value`, `weight`
3. Add any special properties: `stats`, `healing`, `usable_by`, etc.
4. Place item in room's `items` list

### Adding New NPCs

1. Add NPC to `NPCS` dict in `npcs.py`
2. Include: `key`, `desc`, `room`, `npc_type`, `dialogue`
3. Define dialogue tree with `greeting`, `main_menu`, `responses`
4. Add NPC to room's `npcs` list

## Design Philosophy

1. **Multiple Paths**: Players can approach challenges differently
2. **Reward Exploration**: Hidden rooms, secret items, lore for the curious
3. **Non-Combat Solutions**: Wisdom and faith checks offer alternatives
4. **Atmospheric Immersion**: Detailed descriptions, ambient sounds, lore
5. **Character Development**: Choices matter, callings shape the journey
6. **Balanced Difficulty**: Gradual increase, safe rooms for respite
7. **Rich Narrative**: Every item, NPC, and room tells part of the story

---

*"Enter with reverence, seek with humility, find with joy."*
