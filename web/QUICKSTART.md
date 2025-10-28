# Journey Through Scripture - Quick Start Guide

## How to Run the Game

### Windows Users
1. Double-click **`RUN_GAME.bat`** in this folder
2. A command window will open
3. Open your browser to: **http://localhost:8000**
4. Play the game!
5. Press Ctrl+C in the command window to stop the server

### Mac/Linux Users
1. Open Terminal
2. Navigate to this folder: `cd /path/to/web/`
3. Run: `./run_game.sh`
4. Open your browser to: **http://localhost:8000**
5. Play the game!
6. Press Ctrl+C to stop the server

### Alternative: Manual Server Start
If the scripts don't work:

**Windows (PowerShell):**
```powershell
cd C:\path\to\web
python -m http.server 8000
```

**Mac/Linux (Terminal):**
```bash
cd /path/to/web
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

## Why Do I Need a Server?

Browsers block local file requests (CORS security). When you open `file:///path/to/index.html`, the browser won't let it load `assets.json`. A local server bypasses this limitation so the game can load your sprites and tilesets.

## What If the Scripts Don't Work?

1. Make sure Python is installed: `python --version`
2. Try the manual server start commands above
3. Make sure you're in the correct folder (the one with `index.html`)
4. Make sure port 8000 isn't already in use

## File Structure

```
web/
├── index.html          ← Main game
├── assets.json         ← Asset configuration
├── assets/             ← Sprites, tilesets, audio
├── js/                 ← Game code
├── css/                ← Styling
├── RUN_GAME.bat        ← Windows launcher
├── run_game.sh         ← Mac/Linux launcher
└── QUICKSTART.md       ← This file
```

## Features

✅ Character creation with 4 classes
✅ Beautiful menu system
✅ Real sprite graphics (soldier, orc, knight)
✅ Tileset graphics (stone, grass, walls)
✅ Sound effects and music (when real audio files are added)
✅ Mobile-responsive design
✅ Inventory and quest systems

## Play Controls

- **Arrow Keys / WASD** - Move around
- **Mouse Click** - Interact with NPCs
- **Buttons** - Use action buttons in interface
- **Touch** - Mobile controls work on phones/tablets

## Game Overview

You create a character and explore the Palace of Light. There are NPCs to talk to, quests to complete, and enemies to encounter. The game supports both single-player (offline) and future multiplayer (with Evennia server).

## Keyboard Shortcuts

- **Type command** → Press Enter to send
- **Inventory button** → See your items
- **Quests button** → Check active quests
- **Map button** → View game map (coming soon)
- **Settings button** → Game options (coming soon)

## Need Help?

Check the documentation in `/docs/` for more detailed guides.

---

**Ready to play?** Run `RUN_GAME.bat` or `run_game.sh` now! 🎮
