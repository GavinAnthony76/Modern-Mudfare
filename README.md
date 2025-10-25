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

### Installation

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

4. **Initialize Evennia**
   ```bash
   cd server
   evennia migrate
   ```

5. **Create superuser account**
   ```bash
   evennia createsuperuser
   ```

6. **Start the server**
   ```bash
   evennia start
   ```

7. **Access the game**
   - Web Client: Open `web/index.html` in your browser
   - Or visit: `http://localhost:4001` for Evennia's default web client
   - Admin Panel: `http://localhost:4001/admin`

## Project Structure

```
biblical-mud/
├── server/                    # Evennia server (created after init)
│   ├── world/                 # World building modules
│   ├── commands/              # Custom game commands
│   └── typeclasses/          # Game systems and mechanics
│
├── web/                       # Custom graphical web client
│   ├── index.html            # Main game page
│   ├── css/                  # Stylesheets
│   ├── js/                   # Game client code
│   │   ├── game.js           # Main game loop
│   │   ├── renderer.js       # Canvas rendering
│   │   ├── audio.js          # Sound management
│   │   ├── websocket.js      # Server communication
│   │   └── ui.js             # User interface
│   └── assets/               # Game assets
│       ├── sprites/          # Character & creature sprites
│       ├── tiles/            # Environment tiles
│       └── audio/            # Music and sound effects
│
├── docs/                      # Documentation
│   ├── GAME_DESIGN.md        # Game design document
│   ├── SETUP.md              # Detailed setup guide
│   └── API.md                # Client-server API reference
│
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Development Roadmap

### Phase 1: Foundation ✓ (In Progress)
- [x] Project structure setup
- [x] Evennia installation
- [ ] Basic world creation
- [ ] Character creation system
- [ ] Basic movement commands

### Phase 2: Graphics (Next)
- [ ] HTML5 Canvas client
- [ ] Sprite rendering system
- [ ] Basic tileset
- [ ] Character animations
- [ ] Camera/viewport system

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

**Status**: Early Development (Phase 1)

*"For we walk by faith, not by sight." - 2 Corinthians 5:7*
