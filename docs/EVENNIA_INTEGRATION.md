

# Evennia Integration Guide - Journey Through Scripture

## Complete Setup Instructions

This guide walks you through integrating the Biblical Fantasy MUD with Evennia.

## Prerequisites

- Python 3.11 or higher
- Virtual environment activated
- Evennia installed (`pip install evennia`)

## Step-by-Step Integration

### 1. Initialize Evennia

From the repository root:

```bash
cd Modern-Mudfare
evennia --init mygame
```

This creates a new Evennia game directory called `mygame/`.

### 2. Copy Custom Files

Copy our custom files into the Evennia structure:

```bash
# Copy typeclasses
cp -r server/typeclasses/* mygame/typeclasses/

# Copy world data and builder
cp -r server/world/* mygame/world/

# Copy commands
cp -r server/commands/* mygame/commands/
```

### 3. Update Evennia Settings

Edit `mygame/server/conf/settings.py` and add:

```python
# Journey Through Scripture Custom Settings

# Set default typeclasses
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"
BASE_OBJECT_TYPECLASS = "typeclasses.objects.Item"

# Starting location
START_LOCATION = "floor1_approach"

# Game name
SERVERNAME = "Journey Through Scripture"
GAME_SLOGAN = "A Biblical Fantasy MUD"

# Default commands
from commands import dialogue, character

CMDSET_CHARACTER = "commands.default_cmdsets.CharacterCmdSet"

# Web client settings
WEBCLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4001
```

### 4. Create Command Set

Create `mygame/commands/default_cmdsets.py`:

```python
"""
Command sets for Journey Through Scripture
"""

from evennia import default_cmds
from commands.dialogue import CmdTalk, CmdSay, CmdAsk, CmdRead, CmdExamine, CmdLore
from commands.character import (CmdStats, CmdInventory, CmdUse, CmdEquip,
                                CmdUnequip, CmdQuests, CmdCalling)


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    Extended command set for player characters
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()

        # Add dialogue commands
        self.add(CmdTalk())
        self.add(CmdSay())
        self.add(CmdAsk())
        self.add(CmdRead())
        self.add(CmdExamine())
        self.add(CmdLore())

        # Add character commands
        self.add(CmdStats())
        self.add(CmdInventory())
        self.add(CmdUse())
        self.add(CmdEquip())
        self.add(CmdUnequip())
        self.add(CmdQuests())
        self.add(CmdCalling())
```

### 5. Initialize Database

```bash
cd mygame
evennia migrate
```

### 6. Create Superuser

```bash
evennia createsuperuser
```

Follow the prompts to create your admin account.

### 7. Start Evennia

```bash
evennia start
```

You should see:
```
Evennia Server started!
Portal started!
```

### 8. Connect and Build the World

Connect via telnet or web client:
```bash
telnet localhost 4000
```

Or visit: `http://localhost:4001`

Log in with your superuser credentials.

### 9. Build the Palace of Light

In-game, execute:

```python
@py from world import build_world; build_world.build_all()
```

This creates all 30+ rooms, 50+ items, and 20+ NPCs from the data files.

You should see:
```
=== BUILDING PALACE OF LIGHT ===
Created 30 rooms
Connected all exits
Created 50+ items
Created 20+ NPCs
=== WORLD BUILD COMPLETE ===
```

### 10. Set Starting Location

```python
@py from evennia import search_object;
     start = search_object("floor1_approach")[0];
     start.db.desc
```

### 11. Create Your Character

```python
@typeclass Character
@name Pilgrim
```

Then set your class:
```python
@py self.set_class("prophet")
```

Options: prophet, warrior, shepherd, scribe

### 12. Begin Your Journey!

```
look
north
talk to elderly pilgrim
stats
inventory
```

## Available Commands

### Movement
- `north`, `south`, `east`, `west`, `up`, `down`
- `go <direction>`
- Room-specific exits like `through gate`, `narrow path`

### Interaction
- `look` - Examine your surroundings
- `examine <object>` - Look closely at something
- `talk <npc>` - Start dialogue with an NPC
- `<number>` - Choose dialogue option while talking
- `ask <npc> about <topic>` - Ask about specific topics
- `read <item>` - Read books, scrolls, journals
- `lore` - Read the room's history

### Character
- `stats` / `score` - View character sheet
- `inventory` / `inv` - View your items
- `use <item>` - Use consumable items
- `equip <item>` - Equip weapons/armor
- `unequip <item>` - Remove equipment
- `quests` - View active quests
- `calling` - View your spiritual calling

### Items
- `get <item>` - Pick up an item
- `drop <item>` - Drop an item
- `give <item> to <npc>` - Give items to NPCs

### Admin/Builder
- `@py <python code>` - Execute Python
- `@teleport <location>` - Teleport to a room
- `@dig <name>` - Create new room
- `@create <name>` - Create object

## World Structure

### Starting Path

```
Approach Path (Starting Room)
    ↓
Entrance Gate (Gate Keeper Samuel)
    ↓
Courtyard of Beginnings (Central Hub)
    ├─ North: Pilgrim's Rest (SAFE - Priest Ezra)
    ├─ East: Hall of Testing
    │      └─ East: Merchant's Corner
    │             └─ Hidden: Hidden Alcove
    │                     └─ Down: Boss Chamber (The Deceiver)
    └─ West: Garden of Reflection
           └─ Hidden: Hidden Alcove (alternate route)
```

### Floor Progression

1. **Floor 1**: The Outer Court (9 rooms) ✓
2. **Floor 2**: Court of Wisdom (3 rooms)
3. **Floor 3**: Court of Service (4 rooms)
4. **Floor 4**: Court of Trial (3 rooms)
5. **Floor 5**: Court of Sacrifice (3 rooms)
6. **Floor 6**: Court of Revelation (3 rooms)
7. **Floor 7**: Holy of Holies (4 rooms)

## Testing the Integration

### 1. Test Room Navigation

```
look
north
look
exits
```

### 2. Test Item Interaction

```
look
get pilgrim journal
inventory
read pilgrim journal
```

### 3. Test NPC Dialogue

```
talk gate keeper samuel
1
2
3
4
```

### 4. Test Character Stats

```
stats
@py self.db.faith
@py self.db.hp
```

### 5. Test Safe Room

```
@teleport floor1_pilgrim_rest
talk priest ezra
1
```

## Troubleshooting

### World doesn't build

```python
# Check for errors
@py from world import build_world
@py build_world.build_all()
```

Look for error messages about missing modules.

### Can't find rooms

```python
# Search for a room
@py from evennia import search_object
@py rooms = search_object("Courtyard")
@py for r in rooms: print(r.name, r.dbref)
```

### Reset and Rebuild

If something goes wrong:

```python
# Reset entire world (CAUTION!)
@py from world.build_world import reset_world, build_all
@py reset_world()
@py build_all()
```

### Check NPC Placement

```python
@py from typeclasses.npcs import NPC
@py from evennia import search_object
@py npcs = search_object(typeclass=NPC)
@py for npc in npcs: print(f"{npc.name} in {npc.location}")
```

## Connecting the Web Client

The custom web client in `/web` can connect to Evennia:

1. Evennia server must be running on port 4001
2. Open `web/index.html` in browser
3. Click "New Character"
4. Enter name and select class
5. Client connects via WebSocket to `ws://localhost:4001/ws`

The client will send commands and receive room descriptions, updates, and combat information.

## Extending the World

### Add a New Room

1. Add to `server/world/world_data.py`
2. Rebuild: `@py build_world.rebuild()`

### Add a New Item

1. Add to `server/world/items.py`
2. Add to room's `items` list in world_data.py
3. Rebuild items: `@py build_world.build_items(rooms)`

### Add a New NPC

1. Add to `server/world/npcs.py`
2. Rebuild NPCs: `@py build_world.build_npcs(rooms)`

### Modify Dialogue

Edit the NPC's dialogue in `server/world/npcs.py` and rebuild.

## Next Steps

1. **Implement Combat System**: Create turn-based combat encounters
2. **Quest System**: Track quest progress and rewards
3. **Crafting**: Allow combining materials into items
4. **Save/Load**: Persist character progress
5. **Expand Floors 2-7**: Flesh out upper floors with full details
6. **Multiplayer**: Enable party system and PvP arenas
7. **Events**: Create timed world events and boss respawns

## Resources

- **Evennia Docs**: https://www.evennia.com/docs/
- **Evennia Discord**: https://discord.gg/AJJpcRUhtF
- **Project Docs**: See `docs/` folder for world design and game mechanics

## Quick Reference Card

```
=== JOURNEY THROUGH SCRIPTURE - QUICK REFERENCE ===

MOVEMENT:  north, south, east, west, up, down
LOOK:      look, examine <object>, lore
TALK:      talk <npc>, <number>, ask <npc> about <topic>
ITEMS:     get <item>, drop <item>, use <item>, read <item>
EQUIP:     equip <item>, unequip <item>
STATUS:    stats, inventory, quests, calling

SPECIAL:   Pilgrims Rest on each floor = SAFE ROOM
           Talk to Priests for healing and saving
           Defeat bosses to unlock next floor

May your journey be blessed!
```

---

*"Enter with reverence, seek with humility, find with joy."*
