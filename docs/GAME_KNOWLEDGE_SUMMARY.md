# Game Knowledge Summary - Journey Through Scripture

Complete overview of the Biblical Fantasy MUD project.

## Project Overview

**Journey Through Scripture** is a graphical MUD (Multi-User Dungeon) combining:
- **Backend**: Evennia (Python-based MUD framework)
- **Frontend**: HTML5 Canvas web client with graphics and sound
- **Setting**: Biblical fantasy world with spiritual themes
- **Structure**: 7-floor "Palace of Light" dungeon

## Game Concept

Players explore the Palace of Light, a seven-floor vertical dungeon representing spiritual ascent. Each floor has:
- Unique theme and challenges
- Sacred sanctuary (safe room) with a priest
- Boss enemy blocking access to next floor
- NPCs offering quests and guidance
- Loot and divine rewards

## Core Systems

### Character System

**Classes** (4 options):
1. **Prophet** - Divine caster/healer, high Faith & Wisdom
2. **Warrior** - Melee fighter/tank, high Strength & Courage
3. **Shepherd** - Balanced support leader, all stats equal
4. **Scribe** - Knowledge-based strategist, high Wisdom & Intelligence

**Character Stats**:
- Faith - Divine magic power and evil resistance
- Wisdom - Decision-making, perception, spell effectiveness
- Strength - Physical damage and carrying capacity
- Courage - Fear resistance, combat morale
- Righteousness - Alignment stat, affects NPC interactions

**Progression**:
- Levels 1-50 (MVP: 1-20)
- Experience from combat, quests, exploration
- Skill points to improve stats and unlock abilities

### Combat System

- **Turn-based** battles
- **Initiative** based on Wisdom + random roll
- **Damage calculation**: Physical = (Strength × Weapon) - Defense
- **Alternative solutions**: Wisdom/Faith checks, dialogue, stealth
- **Critical hits**: Success = 1.5× base damage

### World Structure - The Seven Floors

#### Floor 1: THE OUTER COURT ✓ (Fully Implemented)
- **Rooms**: 9 rooms including safe room, hidden room, boss room
- **Boss**: The Deceiver (false prophet)
- **NPCs**: Priest Ezra, Gate Keeper Samuel, Garden Keeper Ruth, Young Priest
- **Merchants**: Deborah (honest), Zadok (corrupt)
- **Items**: 20+ items including staff, scrolls, relics
- **Theme**: Introduction, learning, first trials

#### Floor 2: THE COURT OF WISDOM
- **Theme**: Knowledge, learning, scriptural study
- **Rooms**: Library (safe), Debate Hall, Ascending Stairs
- **NPC**: Priest Miriam
- **Enemy**: False Teacher

#### Floor 3: THE COURT OF SERVICE
- **Theme**: Helping others, craftsmanship, healing
- **Rooms**: Workshop, Healing Chambers (safe), Kitchen
- **NPC**: Priest-Healer Tobias
- **Enemy**: Greedy Steward

#### Floor 4: THE COURT OF TRIAL
- **Theme**: Testing faith, spiritual warfare
- **Rooms**: Prayer Sanctuary (safe), Trial Chamber
- **NPC**: Priest-Warrior Caleb
- **Enemies**: Shadow of Doubt, Pride Manifestation

#### Floor 5: THE COURT OF SACRIFICE
- **Theme**: Letting go, surrender
- **Rooms**: Altar Room (safe), Guardian's Gate
- **NPC**: Priest-Elder Sarah
- **Boss**: Guardian Angel Raphael

#### Floor 6: THE COURT OF REVELATION
- **Theme**: Hidden truths, mysteries, spiritual vision
- **Rooms**: Revelation Sanctuary (safe), Vision Chamber
- **NPC**: Priest-Seer Ezekiel
- **Enemy**: False Prophet

#### Floor 7: THE HOLY OF HOLIES
- **Theme**: Ultimate trial, divine presence
- **Rooms**: Preparation Chamber (safe), Veil Chamber, Holy of Holies
- **NPC**: High Priest Aaron
- **Final Boss**: Corrupted Cherub

### Quest System

**Quest Types**:
1. Main Quests - Story-driven, unlock areas
2. Side Quests - Optional NPC tasks
3. Divine Missions - From angelic messengers
4. Exploration Quests - Discover locations
5. Collection Quests - Gather items

**Divine Messengers** (future):
- Gabriel - Main story quests
- Michael - Combat training
- Raphael - Healing quests
- Uriel - Wisdom quests

**Quest Rewards**: XP, gold, equipment, area unlocks, divine favor

### Item System

**Item Types**:
1. **Consumables** - Heal/boost (Manna, Healing Herbs)
2. **Weapons** - Damage dealers (Staff of Moses, Sword of Spirit)
3. **Armor** - Protection (Armor of God set)
4. **Lore Items** - Readable (journals, scrolls)
5. **Quest Items** - Progression (keys, sacred objects)
6. **Materials** - Crafting ingredients (herbs, ash)
7. **Currency** - Trade (temple shekels)
8. **Keys** - Unlock doors/chests

**Notable Biblical Items**:
- Staff of Moses - Transforms into serpent
- Armor of God (Ephesians 6) - Full protection set
- Deceiver's Staff - Cursed weapon (first boss drop)

### NPC System

**NPC Types**:
- Friendly - Helpful, provide info
- Neutral - Conditional help
- Merchant - Buy/sell items
- Priest - Sanctuary services
- Boss - Major encounters
- Ghost/Spirit - Lore providers

**NPC Services**:
- **Healing** - Restore health
- **Saving** - Save game progress
- **Blessing** - Temporary buffs

**Dialogue System**:
- Greeting message
- Main menu with numbered options
- Response text and actions
- Conditional dialogue (requires quest completion)

## Technical Architecture

### Backend (Evennia/Python)

**File Structure**:
```
mygame/
├── world/
│   ├── world_data.py    - Room definitions (9 rooms implemented)
│   ├── items.py         - Item database (20+ items)
│   ├── npcs.py          - NPC data with dialogue
│   └── build_world.py   - World builder script
├── commands/
│   ├── dialogue.py      - Talk, ask, read commands
│   ├── character.py     - Stats, inventory, quests
│   └── default_cmdsets.py - Command set definition
└── typeclasses/
    ├── characters.py    - Character class
    ├── rooms.py         - Room class
    ├── items.py         - Item/object class
    └── npcs.py          - NPC class
```

### Frontend (HTML5 Canvas/JavaScript)

**File Structure**:
```
mygame/web/static/webclient/
├── index.html           - Main game interface
├── js/
│   ├── game.js          - Main game loop & controller
│   ├── renderer.js      - Canvas graphics engine
│   ├── audio.js         - Sound manager
│   └── websocket.js     - Server communication (optional)
├── css/
│   └── style.css        - UI styling
└── assets/
    ├── sprites/         - Character graphics
    ├── tiles/           - Environment graphics
    ├── audio/
    │   ├── music/       - Background tracks
    │   └── sfx/         - Sound effects
    ├── fonts/           - Custom fonts
    └── particles/       - Effect images
```

### Communication

**WebSocket Protocol** (JSON messages):
- Client → Server: Commands, movement, actions
- Server → Client: Room updates, combat data, dialogue
- Real-time for combat, polling for world state

## Current Implementation Status

### ✓ Completed

- [x] **Graphics System**: HTML5 Canvas renderer with sprite support
- [x] **Placeholder Graphics**: SVG sprite generator for all NPCs/items
- [x] **Game Loop**: Real-time 60 FPS game engine
- [x] **Input System**: Keyboard, mouse, and touch controls
- [x] **Audio System**: Web Audio API with sound generation
- [x] **UI Interface**: Character stats, inventory, quests, actions
- [x] **Responsive Design**: Desktop, tablet, and mobile layouts
- [x] **Demo World**: Player, 3 NPCs, 2 items for testing
- [x] **Floor 1 Data**: Complete room, item, and NPC definitions
- [x] **NPCs on Floor 1**: 9 NPCs with full dialogue trees
- [x] **Items on Floor 1**: 20+ items with properties
- [x] **Asset Structure**: Complete directory system with documentation

### 🔄 In Progress

- [ ] Evennia server integration
- [ ] WebSocket client-server communication
- [ ] Dialogue system implementation
- [ ] Combat system mechanics
- [ ] World builder script (creates rooms in Evennia)

### 📋 Planned

- [ ] Floors 2-7 full details
- [ ] Quest progression system
- [ ] Experience and leveling
- [ ] Crafting system
- [ ] Character calling mechanics
- [ ] Save/load functionality
- [ ] Party system (multiplayer)
- [ ] PvP arenas
- [ ] Achievements and leaderboards

## Asset System

### Asset Locations

```
mygame/web/static/webclient/assets/
├── sprites/              (32x32 PNG, transparent)
├── tiles/                (32x32 PNG, seamless)
├── audio/
│   ├── music/            (MP3 + OGG, 2-5 min)
│   └── sfx/              (WAV/MP3, 0.5-3 sec)
├── fonts/                (TTF/WOFF2, <200KB)
└── particles/            (8-32px PNG, transparent)
```

### Asset Guidelines

**Sprites**: 32x32 px (standard), 64x64 px (large), 48x48 px (bosses)
**Music**: MP3 (192 kbps) + OGG (128 kbps), 44.1 kHz, seamless loop
**SFX**: WAV (16-bit) or MP3 (128 kbps), 44.1 kHz, mono
**Total**: Keep under 50 MB for fast loading

### Free Asset Resources

**Graphics**:
- OpenGameArt.org - Game art assets
- itch.io - Asset packs
- Google Fonts - Free fonts

**Audio**:
- Incompetech - Kevin MacLeod music
- Freesound.org - Community SFX
- Zapsplat - Free SFX library
- BBC Sound Library - Professional sounds

**Tools**:
- Aseprite/Piskel - Pixel art creation
- Audacity - Audio editing
- TinyPNG - Image compression
- Krita - Digital painting

## Development Workflow

### Setting Up Locally

1. Clone repository
2. Create Python 3.11+ virtual environment
3. Install Evennia: `pip install evennia`
4. Initialize Evennia: `evennia --init mygame`
5. Run migrations: `evennia migrate`
6. Create superuser: `evennia createsuperuser`
7. Start server: `evennia start`
8. Build world: `@py build_world.build_all()`

### Playing the Game

**Web Client** (Recommended):
- Open `mygame/web/static/webclient/index.html`
- Uses WebSocket to connect to server

**Default Evennia Client**:
- Visit `http://localhost:4001`

**Telnet**:
- `telnet localhost 4000`

### In-Game Commands

**Movement**: `north`, `south`, `east`, `west`, `up`, `down`, `go <dir>`
**Interaction**: `look`, `examine <obj>`, `talk <npc>`, `read <item>`
**Character**: `stats`, `inventory`, `use <item>`, `equip <item>`
**Admin**: `@py <code>`, `@teleport <room>`, `@dig <name>`

## Game Design Philosophy

1. **Multiple Paths** - Combat, wisdom checks, dialogue, stealth
2. **Reward Exploration** - Hidden rooms and secret items
3. **Non-Combat Solutions** - Alternative encounter resolution
4. **Atmospheric Immersion** - Detailed descriptions and ambient sounds
5. **Character Development** - Choices matter, callings shape journey
6. **Balanced Difficulty** - Gradual increase with safe rooms
7. **Rich Narrative** - Every item and NPC tells a story

## Documentation Structure

**docs/** folder contains:
- `GAME_DESIGN.md` - Complete game mechanics and systems
- `WORLD_DESIGN.md` - Room layouts, NPCs, items, progression
- `SETUP.md` - Installation and configuration guide
- `EVENNIA_INTEGRATION.md` - Server setup and building world
- `ASSETS_GUIDE.md` - Asset creation and management (4,500+ words)
- `ASSET_QUICK_START.md` - Quick reference and tutorials
- `ASSET_LOCATIONS_SUMMARY.txt` - ASCII reference card
- `Biblical Fantasy MUD with Graphics Memories.txt` - Original vision

## Quick Reference

### Player Progression Path

```
Start: Floor 1 Entrance
  ↓
Explore 9 rooms, collect items, meet NPCs
  ↓
Talk to Gate Keeper Samuel, Young Priest, Garden Keeper Ruth
  ↓
Find The Deceiver in hidden chamber
  ↓
Defeat The Deceiver boss
  ↓
Unlock Floor 2 stairs
  ↓
Choose "Calling" that affects path
  ↓
Progress through Floors 2-7
  ↓
Face Corrupted Cherub final boss
  ↓
Reach Holy of Holies - Victory!
```

### Core Game Loop

```
Player Input
  ↓
Process Commands (movement, interaction, combat)
  ↓
Update Game State
  ↓
Check Collisions & Triggers
  ↓
Render Graphics
  ↓
Play Audio Effects
  ↓
Update UI
  ↓
Repeat at 60 FPS
```

## Key Statistics

- **Levels**: 1-50 (MVP: 1-20)
- **Rooms**: 30+ (9 on Floor 1, 3-4 per floor)
- **NPCs**: 20+ (9 on Floor 1)
- **Items**: 50+ (20+ on Floor 1)
- **Bosses**: 7 (one per floor)
- **Safe Rooms**: 7 (one per floor)
- **Average Session**: 2-3 hours for full playthrough

## Success Criteria

The game is considered successful when:
- ✓ Graphical client renders properly
- ✓ Combat system is playable
- ✓ At least 3 floors fully implemented
- ✓ NPCs have interactive dialogue
- ✓ Players can save/load progress
- ✓ Asset management system is in place
- ✓ Performance targets met (60 FPS, <100ms latency)

## Next Development Priorities

1. **Integrate Evennia Backend** - Connect web client to server
2. **Implement Combat System** - Turn-based battles
3. **Create Dialogue Engine** - NPC conversation system
4. **Add Saving/Loading** - Persist character progress
5. **Expand Floors 2-7** - Full world development
6. **Create Asset Pipeline** - Integrate custom graphics
7. **Optimize Performance** - Ensure smooth gameplay
8. **Test & Polish** - Bug fixes and balance adjustments

## Resources & Links

- **Evennia Docs**: https://www.evennia.com/docs/
- **Evennia Discord**: https://discord.gg/AJJpcRUhtF
- **HTML5 Canvas**: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- **Web Audio API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- **WebSockets**: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

## Conclusion

**Journey Through Scripture** is a complete biblical fantasy MUD with:
- Unique spiritual theme
- 7-floor palace structure
- Full Floor 1 implementation
- Modern graphical web client
- Comprehensive documentation
- Organized asset system
- Professional code structure

The project is ready for the next phase: integrating the Evennia backend and expanding world content.

---

*"Enter with reverence, seek with humility, find with joy."*

Generated: October 2024
