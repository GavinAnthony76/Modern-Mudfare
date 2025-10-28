# Game Structure Fixes & Organization Guide

## Issues Identified

### 1. Import Path Inconsistencies
**Problem:** Mixed use of absolute and relative imports
- Some files use `from evennia import ...` (correct)
- Some use `from typeclasses.rooms import ...` (relative)
- Some use `from mygame.quests import ...` (absolute)

**Impact:** Can cause import errors in production, inconsistent behavior

### 2. Missing __init__.py Files
**Location:** `mygame/web/` directory
**Issue:** New websocket_plugin.py added but no __init__.py in web package

### 3. Circular Import Potential
**Path:** characters.py imports quests.py, quests.py may need character references
**Current Status:** OK (no circular deps yet) but at risk

### 4. WebSocket Plugin Not Registered
**File:** `mygame/web/websocket_plugin.py`
**Issue:** Plugin created but not registered in web_plugins.py configuration

### 5. Lazy QuestManager Initialization
**File:** characters.py
**Issue:** QuestManager initialized in at_object_creation but might not persist properly

## Fixes Applied

### Fix 1: Standardize Import Paths
All internal module imports now use absolute paths from mygame root:

```python
# WRONG (relative)
from typeclasses.characters import Character

# RIGHT (absolute from mygame)
from mygame.typeclasses.characters import Character
```

### Fix 2: Add Missing __init__.py
Create `mygame/web/__init__.py` to make web a proper package:

```python
"""
WebSocket and web integration for Journey Through Scripture
"""
```

### Fix 3: Register WebSocket Plugin
Update `mygame/server/conf/web_plugins.py` to include websocket handler registration.

### Fix 4: Fix QuestManager Initialization
Ensure quest_manager is properly initialized and accessible:

```python
# In Character.at_object_creation()
self.quest_manager = QuestManager(self)

# Add property for safe access
@property
def quest_mgr(self):
    if not hasattr(self, '_quest_manager'):
        self._quest_manager = QuestManager(self)
    return self._quest_manager
```

## File Structure (Corrected)

```
mygame/
├── __init__.py                      # ✅ Exists
├── manage.py
├── combat.py                        # New - Combat system
├── quests.py                        # New - Quest system
├── encounters.py                    # New - Encounter system
│
├── commands/
│   ├── __init__.py                  # ✅ Exists
│   ├── command.py
│   ├── default_cmdsets.py           # ✅ Updated with imports
│   ├── character.py
│   ├── dialogue.py
│   ├── combat.py                    # New
│   └── quests.py                    # New
│
├── typeclasses/
│   ├── __init__.py                  # ✅ Exists
│   ├── accounts.py
│   ├── characters.py                # ✅ Updated
│   ├── npcs.py
│   ├── objects.py
│   ├── rooms.py
│   ├── exits.py
│   ├── channels.py
│   └── scripts.py
│
├── world/
│   ├── __init__.py                  # ✅ Exists
│   ├── world_data.py
│   ├── items.py
│   ├── npcs.py
│   ├── build_world.py
│   ├── prototypes.py
│   └── help_entries.py
│
├── web/
│   ├── __init__.py                  # ⚠️ NEEDS CREATION
│   ├── websocket_plugin.py          # New
│   ├── admin/
│   ├── api/
│   ├── webclient/
│   ├── website/
│   └── static/
│
└── server/
    ├── __init__.py
    ├── conf/
    │   ├── __init__.py
    │   ├── settings.py              # ✅ Has WebSocket config
    │   ├── web_plugins.py           # ⚠️ NEEDS UPDATE
    │   ├── at_initial_setup.py
    │   └── ...
    └── logs/
```

## Implementation Steps

### Step 1: Create mygame/web/__init__.py

```python
"""
WebSocket and web integration for Journey Through Scripture
"""
```

### Step 2: Fix Import Statements

Change all relative imports to absolute:

```python
# File: mygame/typeclasses/characters.py
from mygame.quests import QuestManager, create_quest

# File: mygame/commands/default_cmdsets.py
from mygame.commands.dialogue import CmdTalk, CmdSay, CmdAsk, ...
from mygame.commands.character import CmdStats, CmdInventory, ...
from mygame.commands.combat import CmdAttack, CmdDefend, ...
from mygame.commands.quests import CmdQuests, CmdAccept, ...
```

### Step 3: Register WebSocket Plugin

Add to `mygame/server/conf/web_plugins.py`:

```python
def at_webproxy_root_creation(web_root):
    """
    Modify the portal proxy service for WebSocket support.
    """
    # WebSocket is already enabled in settings.py
    # Port 4001 handles WebSocket connections
    return web_root
```

### Step 4: Initialize Quests on Character Login

Add to Character class:

```python
def at_post_unpuppet(self, **kwargs):
    """Called after player disconnects"""
    super().at_post_unpuppet(**kwargs)
    # Save quest state if needed

def at_post_puppet(self, **kwargs):
    """Called after player connects"""
    super().at_post_puppet(**kwargs)
    # Ensure quest manager initialized
    if not hasattr(self, 'quest_manager'):
        from mygame.quests import QuestManager
        self.quest_manager = QuestManager(self)
```

### Step 5: Update Settings Configuration

Verify `mygame/server/conf/settings.py`:

```python
# WebSocket Configuration
WEBCLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4001

# Command sets
CMDSET_CHARACTER = "mygame.commands.default_cmdsets.CharacterCmdSet"

# Typeclasses
BASE_CHARACTER_TYPECLASS = "mygame.typeclasses.characters.Character"
BASE_ROOM_TYPECLASS = "mygame.typeclasses.rooms.Room"
BASE_OBJECT_TYPECLASS = "mygame.typeclasses.objects.Item"
```

## Testing Checklist

### Import Testing
- [ ] Python can import all mygame modules
- [ ] No circular dependency warnings
- [ ] All commands load in command set

### Initialization Testing
- [ ] Game starts without errors
- [ ] Character creation works
- [ ] QuestManager initializes with character
- [ ] WebSocket plugin loads

### Functional Testing
- [ ] Combat system works
- [ ] Quest system works
- [ ] Encounters trigger
- [ ] WebSocket messages sent/received

## Common Errors & Solutions

### Error: ModuleNotFoundError: No module named 'quests'
**Solution:** Use absolute import: `from mygame.quests import ...`

### Error: ImportError circular import
**Solution:** Use lazy imports inside methods instead of module top-level

### Error: WebSocket plugin not loading
**Solution:** Ensure web_plugins.py is properly configured in settings.py

### Error: QuestManager not found on character
**Solution:** Ensure QuestManager initialized in at_post_puppet

## Code Organization Best Practices

### 1. Always Use Absolute Imports in mygame

```python
# DON'T
from commands.combat import CmdAttack

# DO
from mygame.commands.combat import CmdAttack
```

### 2. Group Related Classes in Modules

```
mygame/
├── combat.py          # CombatHandler, Creature, related classes
├── quests.py          # Quest, QuestManager, ObjectiveType
└── encounters.py      # Encounter, EncounterManager
```

### 3. Avoid Circular Dependencies

```python
# In characters.py - OK to import
from mygame.quests import QuestManager

# In quests.py - Avoid direct import of Character
# Use TYPE_CHECKING for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mygame.typeclasses.characters import Character
```

### 4. Use __init__.py for Package Exports

```python
# mygame/__init__.py
from mygame.combat import CombatHandler, Creature
from mygame.quests import Quest, QuestManager
from mygame.encounters import Encounter, EncounterManager

__all__ = [
    'CombatHandler',
    'Creature',
    'Quest',
    'QuestManager',
    'Encounter',
    'EncounterManager',
]
```

## Verification Commands

### Check Imports
```python
# In game shell (@py)
from mygame.combat import CombatHandler
from mygame.quests import QuestManager
from mygame.encounters import EncounterManager
print("All imports successful!")
```

### Test Character Creation
```
> create_character
> stats
> quests
```

### Test Combat System
```
> fight orc
> attack
> status
```

### Test Quest System
```
> quests
> accept quest_trial_of_strength
> quests
```

## File Dependency Map

```
settings.py (master config)
    ↓
at_initial_setup.py (world build)
    ↓
typeclasses/characters.py
    ├─→ quests.py
    ├─→ combat.py (for methods)
    └─→ encounters.py (for methods)

commands/default_cmdsets.py
    ├─→ commands/combat.py
    ├─→ commands/quests.py
    ├─→ commands/character.py
    └─→ commands/dialogue.py

world/build_world.py
    ├─→ typeclasses/*
    ├─→ world/world_data.py
    ├─→ world/items.py
    └─→ world/npcs.py

web/websocket_plugin.py
    └─→ typeclasses/characters.py
```

## Summary of Required Changes

| File | Change | Priority | Status |
|------|--------|----------|--------|
| mygame/web/__init__.py | Create | HIGH | ⏳ Pending |
| mygame/typeclasses/characters.py | Update imports | MEDIUM | ✅ Done |
| mygame/commands/default_cmdsets.py | Update imports | MEDIUM | ✅ Done |
| mygame/server/conf/web_plugins.py | Register handler | LOW | ⏳ Pending |
| mygame/server/conf/settings.py | Verify config | LOW | ✅ OK |

## Next Steps

1. **Create missing __init__.py** in mygame/web/
2. **Test imports** - Run Python import checks
3. **Start server** - Verify no startup errors
4. **Test functionality** - Combat, quests, encounters
5. **Monitor logs** - Watch for runtime warnings

## Reference Documentation

- Evennia Import Best Practices: https://www.evennia.com/docs/
- Python Module System: https://docs.python.org/3/tutorial/modules.html
- Package Structure: PEP 420 (Implicit Namespace Packages)
