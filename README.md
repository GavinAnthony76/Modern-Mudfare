# Journey Through Scripture - Biblical Fantasy MUD

A graphical Multi-User Dungeon (MUD) game set in a biblical fantasy world, featuring real-time multiplayer, HTML5 graphics, and immersive sound. Embark on a sacred journey through ancient lands, battle mythical creatures from biblical lore, and receive guidance from divine messengers.

## Features

- **Rich Graphics**: HTML5 Canvas-based 2D graphics with animated sprites
- **Immersive Sound**: Background music and sound effects using Web Audio API
- **Biblical Theme**: Explore lands inspired by scripture, encounter creatures from biblical lore
- **Character Progression**: Stats-based system with Faith, Wisdom, Strength, Courage, and Righteousness
- **Divine Messengers**: Angelic NPCs provide quests, wisdom, and guidance
- **Mobile-Responsive**: Touch-friendly controls for phones and tablets
- **Real-Time Multiplayer**: Built on Evennia's proven WebSocket architecture

## Technology Stack

### Backend
- **Evennia 4.0+**: Python-based MUD framework
- **Django**: Web framework and ORM
- **Twisted**: Asynchronous networking
- **WebSockets**: Real-time communication

### Frontend
- **HTML5 Canvas**: 2D graphics rendering
- **Web Audio API**: Sound and music
- **Vanilla JavaScript**: Lightweight, no framework dependencies
- **CSS3**: Responsive design with mobile-first approach

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Automated Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Modern-Mudfare
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run automated setup**
   ```bash
   ./setup_evennia.sh
   ```

   This script will:
   - Initialize Evennia
   - Copy all custom files
   - Configure settings
   - Set up command systems

5. **Complete setup**
   ```bash
   cd mygame
   evennia migrate
   evennia createsuperuser
   evennia start
   ```

6. **Build the world**

   Connect to `http://localhost:4001` and log in.

   In-game, execute:
   ```python
   @py from world import build_world; build_world.build_all()
   ```

   This creates all 30+ rooms, 50+ items, and 20+ NPCs!

7. **Access the game**
   - **Evennia Web Client**: `http://localhost:4001`
   - **Custom Graphical Client**: Open `web/index.html` in browser
   - **Telnet**: `telnet localhost 4000`

See **[docs/EVENNIA_INTEGRATION.md](docs/EVENNIA_INTEGRATION.md)** for detailed setup guide.

## Project Structure

```
Modern-Mudfare/
├── server/                          # Backend game server
│   ├── typeclasses/                 # Custom Evennia typeclasses
│   │   ├── rooms.py                 # Room types (Safe, Boss, Hidden)
│   │   ├── objects.py               # Items (Weapon, Consumable, Key)
│   │   ├── npcs.py                  # NPCs (Priest, Merchant, Boss)
│   │   └── characters.py            # Player character class
│   ├── world/                       # World data and builder
│   │   ├── world_data.py            # All 7 floors, 30+ rooms
│   │   ├── items.py                 # 50+ item definitions
│   │   ├── npcs.py                  # 20+ NPC definitions
│   │   └── build_world.py           # World population script
│   ├── commands/                    # Custom commands
│   │   ├── dialogue.py              # Talk, Ask, Read, Examine
│   │   └── character.py             # Stats, Inventory, Equip, Use
│   └── README.md                    # Backend integration guide
│
├── web/                             # Custom graphical web client
│   ├── index.html                   # Main game page
│   ├── css/
│   │   ├── style.css                # Core styling
│   │   └── mobile.css               # Responsive mobile design
│   └── js/
│       ├── game.js                  # Main game controller
│       ├── renderer.js              # HTML5 Canvas rendering
│       ├── audio.js                 # Sound/music manager
│       ├── websocket.js             # Server communication
│       └── ui.js                    # UI management
│
├── docs/                            # Documentation
│   ├── GAME_DESIGN.md               # Complete game design
│   ├── WORLD_DESIGN.md              # World structure and lore
│   ├── SETUP.md                     # Detailed setup guide
│   ├── EVENNIA_INTEGRATION.md       # Integration walkthrough
│   └── API.md                       # Client-server API (TODO)
│
├── setup_evennia.sh                 # Automated setup script
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Development Roadmap

### Phase 1: Foundation ✓ (COMPLETE)
- [x] Project structure setup
- [x] Complete world data structure (7 floors, 30+ rooms)
- [x] Item database (50+ items)
- [x] NPC database (20+ NPCs with dialogue)
- [x] Evennia typeclasses (rooms, items, NPCs, characters)
- [x] World builder script
- [x] Command systems (dialogue, character, exploration)
- [x] HTML5 web client with graphics and sound

### Phase 2: Integration ✓ (COMPLETE)
- [x] Automated setup script
- [x] Complete integration documentation
- [x] Character class system (Prophet, Warrior, Shepherd, Scribe)
- [x] Stat system (Faith, Wisdom, Strength, Courage, Righteousness)
- [x] Inventory and equipment system
- [x] NPC dialogue trees

### Phase 3: Gameplay (Next)
- [ ] Combat system implementation
- [ ] Boss encounter mechanics
- [ ] Quest tracking and completion
- [ ] Save/load functionality
- [ ] Calling system (spiritual paths)

### Phase 3: Audio
- [ ] Web Audio API integration
- [ ] Background music system
- [ ] Sound effects
- [ ] Audio manager

### Phase 4: Combat & Systems
- [ ] Combat mechanics
- [ ] Monster AI
- [ ] Inventory system
- [ ] Equipment system
- [ ] Quest framework

### Phase 5: Content
- [ ] Biblical world design
- [ ] Mythical creatures
- [ ] Divine messenger NPCs
- [ ] Quests and storylines
- [ ] Items and equipment

### Phase 6: Polish
- [ ] Touch controls
- [ ] Mobile optimization
- [ ] Performance tuning
- [ ] Tutorial system
- [ ] Testing and bug fixes

## Game World

### Regions
- **Desert Wilderness**: Trials and encounters in harsh terrain
- **Ancient Cities**: Jerusalem, Babylon, Nineveh
- **Sacred Mountains**: Sinai, Moriah
- **Rivers and Seas**: Jordan River, Red Sea
- **Temples**: Sacred places and ancient ruins

### Creatures
- **Leviathan**: Massive sea monster
- **Behemoth**: Mighty land beast
- **Nephilim**: Giants from ancient times
- **Demons**: Spiritual adversaries
- **Wild Beasts**: Lions, bears, serpents

### Character Classes
- **Prophet**: High wisdom and faith, divine insight
- **Warrior**: Strong in combat, righteous defender
- **Shepherd**: Balanced stats, natural leader
- **Scribe**: Knowledge-focused, strategic thinker

## Contributing

This is a personal project, but suggestions and feedback are welcome! Please open an issue to discuss major changes.

## VS Code Setup

Recommended extensions:
- Python (Microsoft)
- Pylance
- Live Server (for testing web client)

### Settings
Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

## Resources

- [Evennia Documentation](https://www.evennia.com/docs/)
- [Evennia Discord](https://discord.gg/AJJpcRUhtF)
- [HTML5 Canvas Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Web Audio API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

## License

See LICENSE file for details.

## Credits

Built with:
- [Evennia](https://www.evennia.com/) - MUD creation framework
- Inspired by biblical scripture and ancient lore
- Created as a learning project combining classic MUD gameplay with modern web technologies

---

**Status**: Core Complete - Ready for Integration Testing (Phase 2 Complete)

*"For we walk by faith, not by sight." - 2 Corinthians 5:7*
