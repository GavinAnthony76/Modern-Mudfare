# Server - Biblical Fantasy MUD Backend

## Directory Structure

```
server/
├── README.md (this file)
├── world/
│   ├── world_data.py       # Complete room definitions (all 7 floors)
│   ├── items.py            # All items with stats and properties
│   ├── npcs.py             # All NPCs with dialogue trees
│   └── build_world.py      # Script to populate the game world (to be created)
├── typeclasses/
│   ├── rooms.py            # Custom room types (to be created)
│   ├── objects.py          # Custom item types (to be created)
│   ├── npcs.py             # Custom NPC types (to be created)
│   └── characters.py       # Player character extensions (to be created)
└── commands/
    ├── default_cmdsets.py  # Custom command sets (to be created)
    ├── dialogue.py         # NPC dialogue commands (to be created)
    └── exploration.py      # Exploration commands (to be created)
```

## Current Implementation Status

### ✓ Complete - World Data

**server/world/world_data.py**
- 7 floors fully structured
- Floor 1: 9 rooms completely detailed
- Floors 2-7: Skeleton rooms ready for expansion
- All room properties: descriptions, exits, items, NPCs, danger levels
- Helper functions for querying rooms

**server/world/items.py**
- 50+ items defined
- Complete Floor 1 item database
- Item types: consumables, weapons, equipment, lore, quest items, keys
- Stat bonuses, healing values, special effects
- Helper functions for item queries

**server/world/npcs.py**
- 20+ NPCs with complete dialogue trees
- NPC types: friendly, merchant, priest, hostile, boss
- Multi-level dialogue system with branching options
- Conditional dialogue based on player progress
- Merchant inventories and boss stats

### 🔄 Next Steps - Integration

1. **Initialize Evennia**
   ```bash
   evennia --init server
   cd server
   evennia migrate
   ```

2. **Create Typeclasses**
   - Custom Room class with support for room_type, danger_level, ambient sounds
   - Custom Item class with stats, effects, and usability
   - Custom NPC class with dialogue system
   - Custom Boss class extending NPC

3. **Build World Script**
   - Import world_data, items, npcs
   - Create all rooms with proper exits
   - Populate rooms with items and NPCs
   - Set up locked doors and boss requirements

4. **Implement Systems**
   - Dialogue command system
   - Combat system
   - Stat tracking and progression
   - Save/load functionality at safe rooms
   - Quest tracking

## World Design Overview

### The Palace of Light

A seven-floor vertical dungeon representing spiritual ascent:

1. **Floor 1: Outer Court** - Tutorial, exploration, first trials
2. **Floor 2: Court of Wisdom** - Knowledge, debate, discernment
3. **Floor 3: Court of Service** - Helping others, craftsmanship, healing
4. **Floor 4: Court of Trial** - Testing faith, spiritual warfare
5. **Floor 5: Court of Sacrifice** - Surrender, difficult choices
6. **Floor 6: Court of Revelation** - Visions, hidden truths
7. **Floor 7: Holy of Holies** - Ultimate trial, completion

### Key Features

- **Safe Rooms**: One per floor with priest NPCs (heal, save, bless)
- **Boss Encounters**: Major enemies blocking progress to next floor
- **Hidden Areas**: Secret rooms rewarding exploration
- **Multiple Paths**: Combat, wisdom, faith, or stealth solutions
- **Rich Lore**: Items, NPCs, and rooms tell interconnected stories
- **Character Callings**: Player choices shape their journey

## Data Access Examples

### Getting Room Data

```python
from world.world_data import get_room, get_floor_rooms, get_safe_rooms

# Get specific room
courtyard = get_room("floor1_courtyard")
print(courtyard['desc'])
print(courtyard['exits'])

# Get all rooms on Floor 1
floor1_rooms = get_floor_rooms(1)

# Get all safe rooms
safe_rooms = get_safe_rooms()
```

### Getting Item Data

```python
from world.items import get_item, get_items_by_type, WEAPONS

# Get specific item
sword = get_item("forgotten_sword")
print(sword['desc'])
print(sword['stats'])

# Get all weapons
weapons = get_items_by_type("weapon")

# Or use pre-filtered dict
all_weapons = WEAPONS
```

### Getting NPC Data

```python
from world.npcs import get_npc, get_npcs_in_room, PRIESTS

# Get specific NPC
ezra = get_npc("priest_ezra")
print(ezra['dialogue']['greeting'])

# Get all NPCs in a room
courtyard_npcs = get_npcs_in_room("floor1_courtyard")

# Get all priests
all_priests = PRIESTS
```

## Character Classes

From the original design:

1. **Prophet**: Faith (5), Wisdom (5), Righteousness (4)
2. **Warrior**: Strength (5), Courage (5), Righteousness (4)
3. **Shepherd**: All stats (4) - balanced
4. **Scribe**: Wisdom (5), Intelligence (5), Faith (4)

## Integration with Web Client

The web client (in `/web`) connects via WebSocket and displays:
- Room descriptions and exits
- Available items and NPCs
- Character stats and inventory
- Combat interface
- Dialogue trees

Server sends JSON messages:
```json
{
  "type": "room_description",
  "room": "Courtyard of Beginnings",
  "description": "A vast open courtyard...",
  "exits": ["north", "south", "east", "west"],
  "items": ["inscribed_stone", "fountain_water"],
  "npcs": ["young_priest", "water_bearer"]
}
```

## Development Workflow

1. **Test Data Integrity**
   ```python
   # Verify all room exits connect to valid rooms
   # Verify all items in rooms exist in items database
   # Verify all NPCs in rooms exist in NPC database
   ```

2. **Build World**
   ```python
   # Run build_world.py to create all rooms, items, NPCs
   # Connect all exits properly
   # Place items and NPCs in starting positions
   ```

3. **Test Gameplay**
   - Connect via web client or telnet
   - Navigate through Floor 1
   - Interact with NPCs
   - Test combat encounters
   - Verify boss defeat unlocks next floor

4. **Expand Content**
   - Flesh out Floors 2-7 with full descriptions
   - Add more items and NPCs
   - Create quest chains
   - Implement crafting system

## Documentation

- **WORLD_DESIGN.md**: Complete world structure and design philosophy
- **GAME_DESIGN.md**: Overall game mechanics and features
- **SETUP.md**: Installation and configuration guide
- **API.md** (to be created): Client-server communication protocol

## Next Implementation Priority

1. Create Evennia typeclasses (rooms, items, NPCs)
2. Build world population script
3. Implement dialogue system
4. Basic combat mechanics
5. Save/load at safe rooms
6. Test complete Floor 1 gameplay loop

---

This server directory contains the complete backend for Journey Through Scripture. The world data is ready—now it needs to be brought to life through Evennia's framework.
