# Comprehensive Project Reset Prompt for Biblical Fantasy MUD

## Project Overview
I need to build a graphical Multi-User Dungeon (MUD) game with the following specifications:

### Core Requirements
1. **Game Type**: Biblical fantasy MMORPG-style MUD
2. **Technology**: Python-based using Evennia framework
3. **Architecture**: MVC (Model-View-Controller) pattern
4. **Graphics**: 2D graphics using HTML5 Canvas
5. **Audio**: Background music and sound effects using Web Audio API
6. **Platform**: Web-based, fully responsive for mobile and desktop
7. **Multiplayer**: Real-time multiplayer support via WebSockets

### Game Features Required

#### Character System
- Character creation with gender selection (Male/Female)
- Name input (suggest biblical names)
- Starting stats: Faith, Wisdom, Strength, Courage, Righteousness
- Character classes: Prophet, Warrior, Shepherd, Scribe
- Level progression system
- Character attributes that affect gameplay

#### Combat System
- Turn-based or real-time combat (developer decides best approach)
- Fight mythical creatures from biblical lore:
  - Leviathan (sea monster)
  - Behemoth (land beast)
  - Nephilim (giants)
  - Demons and fallen angels
  - Wild beasts (lions, bears, serpents)
- Stats-based damage calculation
- Special abilities based on character stats
- Experience points and leveling

#### Inventory & Equipment System
- Inventory management interface
- Equipment slots: weapon, armor, accessories
- Biblical-themed items:
  - **Weapons**: Staff of Moses, Sword of the Spirit, David's Sling, etc.
  - **Armor**: Armor of God components, Priestly garments
  - **Consumables**: Manna, Water from the Rock, Healing herbs
  - **Quest Items**: Ark fragments, Sacred scrolls, Ancient relics
- Item stats and bonuses
- Drag-and-drop functionality (desktop) and tap-to-equip (mobile)

#### NPC & Divine Messenger System
- Angelic NPCs (divine messengers) who provide:
  - Quest guidance
  - Wisdom teachings (biblical passages/principles)
  - Clues for puzzles and hidden areas
  - Rewards for righteous actions
  - Warnings about dangers
- Interactive dialogue system
- NPC memory of player actions

#### Quest System
- Main storyline quests
- Side quests
- Quest log/journal
- Quest objectives and progress tracking
- Rewards system (items, experience, currency)

#### World Design
- Multiple interconnected regions inspired by biblical lands:
  - Desert Wilderness (trials and encounters)
  - Ancient Cities (Jerusalem, Babylon, Nineveh)
  - Sacred Mountains (Sinai, Moriah)
  - Rivers and Seas (Jordan River, Red Sea)
  - Temples and ancient ruins
  - Underground caves and dungeons
- Room-based navigation with graphical representation
- Interactive objects in rooms
- Day/night cycle (optional)

### User Interface Requirements

#### Welcome Screen
- Title: "Journey Through Scripture" (or similar biblical theme)
- Subtitle explaining the game
- Menu options:
  - New Character
  - Continue Journey (login)
  - Options/Settings
  - About/Credits
- Background art with biblical theme
- Background music on welcome screen

#### Main Game Interface

**Desktop Layout:**
- Center: Main game canvas showing character, environment, NPCs
- Left panel: Character stats, health, inventory
- Right panel: Chat, quest log, map
- Bottom: Action bar with quick commands
- Top: Menu bar with Settings, Help, Logout

**Mobile Layout:**
- Full-screen canvas
- Collapsible panels for inventory, stats, quests
- Touch-friendly action buttons
- Swipe gestures for navigation
- Virtual joystick or directional pad

#### Intro Sequence
Opening narrative when starting new game:
```
"In a time when the world was young and miracles walked the earth,
you are called to embark on a sacred journey. As a traveler seeking
divine wisdom and truth, you must face trials, combat ancient evils,
and discover the mysteries hidden in sacred lands.

Your choices will shape your path. Will you walk in faith, 
or will you fall to darkness? The journey begins now..."
```

### Technical Implementation Structure

#### Project Structure Needed
```
biblical-mud/
├── server/                     # Evennia backend
│   ├── world/                  # Game world definitions
│   │   ├── characters.py       # Character models
│   │   ├── creatures.py        # Monsters and NPCs
│   │   ├── items.py           # Item definitions
│   │   └── rooms.py           # Room/location definitions
│   ├── commands/               # Player commands
│   ├── typeclasses/           # Game systems
│   └── settings.py            # Configuration
│
├── web/                        # Custom web client
│   ├── index.html             # Main page
│   ├── welcome.html           # Welcome/login screen
│   ├── css/
│   │   ├── style.css          # Desktop styles
│   │   └── mobile.css         # Mobile responsive
│   ├── js/
│   │   ├── game.js            # Main game loop
│   │   ├── renderer.js        # Canvas rendering
│   │   ├── audio.js           # Audio manager
│   │   ├── websocket.js       # Server communication
│   │   ├── ui.js              # UI management
│   │   └── controls.js        # Input handling
│   └── assets/
│       ├── sprites/           # Character/monster sprites
│       ├── tiles/             # Environment tiles
│       ├── ui/                # UI elements
│       ├── audio/
│       │   ├── music/         # Background tracks
│       │   └── sfx/           # Sound effects
│       └── fonts/
│
└── docs/
    ├── game_design.md         # Detailed game design
    ├── story.md               # Storylines and lore
    └── setup_guide.md         # Installation instructions
```

#### MVC Architecture Implementation

**Model (Server-side - Python/Evennia):**
- Character data (stats, inventory, position)
- World state (rooms, objects, NPCs)
- Game rules and mechanics
- Database persistence
- Player authentication

**View (Client-side - HTML5 Canvas + JavaScript):**
- Graphics rendering (sprites, animations, effects)
- Audio playback (music, sound effects)
- UI components (inventory, stats, dialogs)
- Visual feedback for actions

**Controller (Both sides):**
- Server: Process commands, update game state, broadcast changes
- Client: Handle input (keyboard, mouse, touch), send commands to server, update local display

#### Graphics System

**Required Visual Elements:**
1. Character sprites (8-direction movement, idle, attack, walk animations)
2. Monster/NPC sprites (varied creatures, animated)
3. Environment tiles (desert, city, temple, water, mountains)
4. UI elements (buttons, health bars, inventory slots, icons)
5. Particle effects (divine interventions, combat effects, magic)
6. Map visualization (mini-map or full map view)

**Canvas Implementation:**
- Tile-based rendering or sprite-based
- Camera system that follows player
- Layered rendering (background, objects, characters, UI)
- Smooth animations (60 FPS target)
- Zoom functionality for mobile

#### Audio System

**Music Tracks Needed:**
1. Welcome screen theme
2. Peaceful exploration/travel music
3. Combat music (intensity varies by enemy)
4. Sacred/temple music
5. Victory fanfare
6. Sad/dramatic music for story moments

**Sound Effects Needed:**
1. Footsteps (varies by terrain)
2. Combat sounds (sword swings, hits, magic)
3. UI sounds (button clicks, inventory actions)
4. Environmental ambience (wind, water, animals)
5. Divine intervention effects
6. Item pickup/use sounds
7. NPC dialogue indicator sounds

**Audio Manager Requirements:**
- Background music with looping
- Crossfade between music tracks
- Sound effect pooling for overlapping sounds
- Volume controls (master, music, sfx)
- Mute functionality
- Mobile-friendly (user-initiated audio)

### Development Phases

#### Phase 1: Environment Setup (Priority: HIGHEST)
**Goal**: Get Evennia running with basic structure

**Tasks:**
1. Install Python 3.11+ on development machine
2. Install Evennia: `pip install evennia`
3. Create new game: `evennia --init biblical_mud`
4. Start server and verify it works
5. Access default web client at localhost:4001
6. Understand Evennia's directory structure
7. Review Evennia beginner tutorial

**Deliverable**: Working Evennia server that can be accessed via browser

#### Phase 2: Basic World Creation
**Goal**: Create initial game world without graphics

**Tasks:**
1. Design first 5-10 rooms (e.g., Starting Village, Wilderness, Temple)
2. Implement basic room navigation (north, south, east, west)
3. Create character creation command/flow
4. Add 2-3 basic NPCs with simple dialogue
5. Implement basic inventory system
6. Add 5-10 basic items
7. Test multiplayer with two browser windows

**Deliverable**: Playable text-based MUD with character creation and basic world

#### Phase 3: Combat System
**Goal**: Implement functional combat mechanics

**Tasks:**
1. Create combat state machine
2. Implement 3-5 mythical creatures
3. Add combat commands (attack, defend, use item)
4. Implement stat-based damage calculation
5. Add experience and leveling
6. Create loot drops from defeated enemies
7. Add health regeneration system

**Deliverable**: Working combat system with enemies and progression

#### Phase 4: Graphics Layer
**Goal**: Add visual representation using HTML5 Canvas

**Tasks:**
1. Create custom HTML page with Canvas element
2. Establish WebSocket connection to Evennia
3. Implement sprite loader
4. Create simple tileset (or use placeholder sprites)
5. Render player character on canvas
6. Display current room graphically
7. Animate character movement
8. Add other players' characters to display
9. Implement camera/viewport system

**Deliverable**: Graphical client showing game world visually

#### Phase 5: Audio Integration
**Goal**: Add music and sound effects

**Tasks:**
1. Create audio manager class
2. Implement music player with looping
3. Add sound effect system
4. Create or source 3-5 music tracks
5. Add 10-15 sound effects
6. Implement volume controls
7. Ensure mobile compatibility (user gesture required)

**Deliverable**: Fully functional audio system

#### Phase 6: Enhanced UI
**Goal**: Create polished user interface

**Tasks:**
1. Design inventory screen
2. Create equipment screen
3. Add quest log/journal
4. Implement character stats display
5. Add chat interface
6. Create mini-map or world map
7. Add settings menu
8. Implement help/tutorial system

**Deliverable**: Complete, polished UI for all game features

#### Phase 7: Mobile Optimization
**Goal**: Make game fully playable on mobile devices

**Tasks:**
1. Implement touch controls (virtual joystick or swipe)
2. Create responsive CSS layouts
3. Optimize canvas for different screen sizes
4. Add touch-friendly UI elements (larger buttons)
5. Test on multiple devices and screen sizes
6. Optimize performance for mobile

**Deliverable**: Fully mobile-responsive game

#### Phase 8: Content & Polish
**Goal**: Fill world with content and polish gameplay

**Tasks:**
1. Expand world to 50+ rooms
2. Add 10+ unique creatures
3. Create 20+ quests
4. Add 50+ items and equipment
5. Write NPC dialogues and lore
6. Balance combat and progression
7. Bug fixes and optimization
8. Playtesting and adjustments

**Deliverable**: Content-rich, polished game ready for players

### Critical Success Factors

**For the Assistant/Developer:**
1. **Start Simple**: Begin with Evennia's default setup, don't overcomplicate
2. **Incremental Progress**: Complete each phase before moving to next
3. **Test Frequently**: Verify each feature works before adding more
4. **Follow Evennia Conventions**: Use Evennia's built-in systems rather than reinventing
5. **Document as You Go**: Keep notes on custom implementations
6. **Beginner-Friendly Code**: Clear comments, simple structure (remember: developer is a beginner)

**What to Avoid:**
- Don't try to build everything at once
- Don't skip the Evennia tutorial
- Don't create custom networking when Evennia handles it
- Don't overcomplicate the MVC architecture
- Don't worry about optimization until Phase 8
- Don't use frameworks unless necessary (keep JavaScript simple initially)

### Expected Challenges & Solutions

**Challenge 1**: Learning Evennia's structure
**Solution**: Follow official beginner tutorial step-by-step, join Discord for help

**Challenge 2**: Integrating graphics with text-based backend
**Solution**: WebSocket communication - server sends room data, client renders visually

**Challenge 3**: Mobile audio restrictions
**Solution**: Require user gesture (button press) before enabling audio

**Challenge 4**: Balancing gameplay
**Solution**: Start with simple math, iterate based on playtesting

**Challenge 5**: Creating art assets
**Solution**: Use placeholder art initially, can be replaced later with commissioned or created art

### Resources Needed

**Documentation:**
- Evennia official docs: https://www.evennia.com/docs/
- MDN Canvas Tutorial: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial
- Web Audio API Guide: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API

**Free Asset Sources (Placeholders):**
- OpenGameArt.org (sprites, tiles, audio)
- Freesound.org (sound effects)
- Kenney.nl (game assets)
- itch.io (free game assets)

**Community Support:**
- Evennia Discord server
- Evennia forums
- Stack Overflow for technical issues

### Current State Assessment

**What we have:**
- Research document identifying Evennia as best solution
- Clear understanding of game requirements
- Technology stack decided (Evennia + HTML5 Canvas + Web Audio)
- MVC architecture plan
- Phase-by-phase implementation roadmap

**What we need NOW:**
1. Clean Evennia installation
2. Basic project structure set up
3. First 2-3 rooms created
4. Character creation working
5. Simple command to move between rooms

**Immediate Next Steps (In Order):**
1. Verify Python 3.11+ is installed
2. Install Evennia via pip
3. Initialize new game project
4. Start server and access default client
5. Create first room using Evennia's building commands
6. Test movement between rooms
7. Review character creation system

### Success Criteria for Phase 1

**You know Phase 1 is complete when:**
- [ ] Evennia server starts without errors
- [ ] Can access web client in browser
- [ ] Can create a character
- [ ] Can enter the game world
- [ ] Can execute basic commands (look, inventory, say)
- [ ] Can move between at least 2 rooms
- [ ] Can see other players in same room (test with 2 browsers)

### Communication Guidelines for Development

**When seeking help, always specify:**
1. What phase are we in?
2. What specific task are we working on?
3. What error or issue occurred?
4. What did we expect to happen?
5. What actually happened?

**Request format example:**
"We're in Phase 2, trying to create our first NPC with dialogue. When we run [specific command], we get [specific error]. We expected the NPC to appear in the room. Can you help us fix the NPC creation code?"

### Final Notes

This is a **3-4 month project** for a beginner developer working part-time. Don't rush. Each phase builds on the previous one. It's better to have a small, working game than a large, broken one.

**Philosophy**: Start with a simple, playable game. Add features incrementally. Test constantly. Polish last.

**Remember**: Evennia handles the hard parts (networking, database, authentication). Your job is to define the game content, rules, and presentation. You're building ON TOP of Evennia, not replacing it.

---

## How to Use This Prompt

**If starting fresh:**
1. Verify Python 3.11+ is installed
2. Install Evennia: `pip install evennia`
3. Create project: `evennia --init biblical_mud`
4. Change to project directory: `cd biblical_mud`
5. Start server: `evennia start`
6. Open browser to: http://localhost:4001
7. Begin Phase 1 tasks

**If continuing existing work:**
1. Assess current state against phase checklist
2. Complete remaining tasks in current phase
3. Test thoroughly before moving to next phase
4. Document what was completed
5. Plan next session's work

**When stuck:**
1. Check Evennia documentation
2. Ask in Evennia Discord
3. Search for similar implementations in Evennia's examples
4. Simplify the problem - break it into smaller pieces
5. Test each piece individually

Good luck on your biblical fantasy MUD journey!
