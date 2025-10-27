# Asset Quick Start Guide

Quick reference for adding assets to the Biblical Fantasy MUD.

## Asset Directory Structure

```
mygame/web/static/webclient/assets/
├── sprites/              ← Character & NPC art
├── tiles/                ← Environment tiles
├── audio/
│   ├── music/            ← Background music (MP3/OGG)
│   └── sfx/              ← Sound effects (WAV/MP3)
├── fonts/                ← Custom fonts
└── particles/            ← Particle effect images
```

## Where to Put Different Asset Types

| Asset Type | Directory | Format | Size | Example |
|-----------|-----------|--------|------|---------|
| **Characters/NPCs** | `sprites/` | PNG | 32x32 | player_idle.png |
| **Enemies** | `sprites/` | PNG | 32-48x32-48 | enemy_demon.png |
| **Tiles/Floors** | `tiles/` | PNG | 32x32 | floor_stone.png |
| **Walls** | `tiles/` | PNG | 32x32 | wall_brick.png |
| **Background Music** | `audio/music/` | MP3/OGG | 2-5 min | exploration_peaceful.mp3 |
| **Sound Effects** | `audio/sfx/` | WAV/MP3 | 0.5-3 sec | sword_slash.wav |
| **Custom Fonts** | `fonts/` | TTF/WOFF2 | < 200 KB | biblical_serif.ttf |
| **Particles** | `particles/` | PNG | 8x32 | spark_yellow.png |

## Adding a Sprite (Step by Step)

### 1. Create the Image
- Use Aseprite, Krita, or Piskel
- Size: 32x32 pixels (for most sprites)
- Format: PNG with transparent background
- Example: Draw a character sprite

### 2. Export as PNG
- Ensure transparency is preserved (RGBA)
- Name it clearly: `my_character.png`
- Save to: `mygame/web/static/webclient/assets/sprites/`

### 3. Use in Code (game.js)
```javascript
// Add to createDemoWorld() function
const mySprite = {
  id: 'my_sprite',
  type: 'npc',
  x: 300,
  y: 300,
  sprite: 'my_character',  ← Reference sprite name
  label: 'My Character',
  visible: true
};
gameObjects.push(mySprite);
```

### 4. Register Sprite in Renderer
```javascript
// In renderer.js registerPlaceholderAssets()
this.loadSprite('my_character', {
  type: 'placeholder',
  width: 32,
  height: 32,
  color: '#FF6B6B',
  shape: 'character'
});
```

## Adding Background Music (Step by Step)

### 1. Create or Find Music
- Create/compose a 2-5 minute loop
- OR download from Incompetech, Freepd.com, etc.
- Ensure it loops seamlessly (no clicks at end)

### 2. Export Formats
- Primary: MP3 at 192 kbps, 44.1 kHz
- Fallback: OGG at 128 kbps, 44.1 kHz

### 3. Save Files
- **exploration_peaceful.mp3** → `audio/music/`
- **exploration_peaceful.ogg** → `audio/music/`

### 4. Use in Code (game.js)
```javascript
// In setupWebSocket() or initialization
audioManager.playMusic('exploration_peaceful');

// Or based on game state
audioManager.playStateMusic('combat');  // Plays combat_intense
```

## Adding Sound Effects (Step by Step)

### 1. Create or Find SFX
- Record/find a 0.5-3 second sound
- Use Freesound.org, Zapsplat, BBC Sound Library
- Edit in Audacity to trim and normalize

### 2. Export as WAV
- Format: WAV, 44.1 kHz, 16-bit, Mono
- Peak volume: -3dB to -6dB
- No silence at start/end

### 3. Save File
- **button_click.wav** → `audio/sfx/`
- (Creates both WAV and optional MP3)

### 4. Use in Code (game.js)
```javascript
// Play single effect
audioManager.playSFX('button_click');

// Multiple effects
audioManager.playMultipleSFX(['sword_slash', 'hit_impact']);

// In event listeners
document.getElementById('btnAttack').addEventListener('click', () => {
  audioManager.playSFX('sword_slash');
});
```

## Adding Tiles (Step by Step)

### 1. Create Tile Image
- Size: 32x32 pixels
- Format: PNG with transparency
- Ensure seamless tiling (edges blend)
- Create multiple tiles (stone, grass, sand, walls, etc.)

### 2. Save Tiles
- **floor_stone.png** → `assets/tiles/`
- **wall_brick.png** → `assets/tiles/`

### 3. Use in World Building
```javascript
// In world/build_world.py (Evennia backend)
room_layout = [
  ['floor_stone', 'floor_stone', 'wall_brick'],
  ['floor_stone', 'fountain', 'wall_brick'],
  ['floor_grass', 'floor_grass', 'tree']
]
```

## Asset File Size Recommendations

**Keep total assets under 50 MB for fast loading:**

- Sprites: 20-50 KB each
- Tiles: 15-40 KB each
- Music: 1-2 MB per track
- SFX: 10-100 KB each
- Fonts: 50-200 KB each

**Compression Tools:**
- TinyPNG.com (images)
- ImageOptim (Mac)
- Audacity (audio normalization)

## Testing Your Assets

### In Browser
1. Open: `mygame/web/static/webclient/index.html`
2. Open Browser Console: **F12 → Console**
3. Watch for errors loading assets
4. Check Network tab for file sizes

### Common Issues

| Issue | Solution |
|-------|----------|
| Sprites not showing | Check file path, ensure PNG transparency |
| Music not playing | Check format (MP3), volume levels, browser restrictions |
| Audio overlapping | Limit concurrent sounds (max 8-16) |
| Game stuttering | Reduce sprite sizes, compress music |

## Common Asset File Names

### Sprites
```
player_idle.png
player_walk.png
npc_elder.png
npc_priest.png
enemy_demon.png
```

### Tiles
```
floor_stone.png
floor_grass.png
wall_brick.png
door_open.png
```

### Music
```
exploration_peaceful.mp3
combat_intense.mp3
sacred_temple.mp3
boss_battle.mp3
```

### Sound Effects
```
sword_slash.wav
footstep_stone.wav
button_click.wav
healing.wav
level_up.wav
```

## Quick Commands

### Create Asset Directories
```bash
mkdir -p mygame/web/static/webclient/assets/{sprites,tiles,audio/{music,sfx},fonts,particles}
```

### Check Asset Sizes
```bash
du -sh mygame/web/static/webclient/assets/
```

### Find All Assets
```bash
find mygame/web/static/webclient/assets -type f -name "*"
```

## Free Asset Resources

### Sprites & Graphics
- **OpenGameArt.org** - Game art assets
- **itch.io** - Game asset packs
- **Aseprite** - Professional pixel art editor ($20)
- **Krita** - Free digital painting

### Music
- **Incompetech** - Kevin MacLeod compositions (CC BY)
- **Freepd.com** - Curated royalty-free music
- **OpenGameArt.org** - Game music assets
- **YouTube Audio Library** - Premium music

### Sound Effects
- **Freesound.org** - Community SFX (register free)
- **Zapsplat** - Free SFX library
- **BBC Sound Library** - Professional sounds
- **OpenGameArt.org** - Game audio

### Fonts
- **Google Fonts** - Free, open-source fonts
- **DaFont.com** - Creative fonts
- **1001Fonts.com** - Curated collection

## Next Steps

1. ✓ Read full **ASSETS_GUIDE.md** for details
2. ✓ Create/gather your game assets
3. ✓ Organize by type in appropriate directories
4. ✓ Update code references if needed
5. ✓ Test in browser (F12 console)
6. ✓ Create **ASSETS_CREDITS.md** for attribution
7. ✓ Commit and push to GitHub

## Additional Help

- Full guide: **ASSETS_GUIDE.md**
- Sprites: **assets/sprites/README.md**
- Tiles: **assets/tiles/README.md**
- Audio: **assets/audio/README.md**
- Fonts: **assets/fonts/README.md**

---

**Summary**:
- Sprites → `assets/sprites/` (PNG, 32x32)
- Tiles → `assets/tiles/` (PNG, 32x32)
- Music → `assets/audio/music/` (MP3/OGG, 2-5 min)
- SFX → `assets/audio/sfx/` (WAV/MP3, 0.5-3 sec)
- Fonts → `assets/fonts/` (TTF/WOFF2)
- Particles → `assets/particles/` (PNG, 8-32px)
