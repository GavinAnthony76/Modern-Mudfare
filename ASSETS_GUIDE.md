# Asset Management Guide - Biblical Fantasy MUD

Complete guide for organizing, creating, and integrating game assets.

## Quick Directory Reference

```
mygame/web/static/webclient/assets/
├── sprites/              ← Character & NPC art (32x32, 64x64)
├── tiles/                ← Environment tiles (32x32)
├── audio/                ← All audio files
│   ├── music/            ← Background tracks (MP3, OGG)
│   └── sfx/              ← Sound effects (WAV, MP3)
├── fonts/                ← Custom fonts (TTF, WOFF2)
└── particles/            ← Particle effect images (PNG)
```

## Asset Types & Specifications

### 1. SPRITES (Character Graphics)

**Location**: `mygame/web/static/webclient/assets/sprites/`

**Specifications**:
- Format: PNG with transparency (RGBA)
- Size: 32x32 px (standard), 64x64 px (large), 48x48 px (bosses)
- Color Depth: RGBA (32-bit)
- Compression: PNG lossless

**Files to Create**:

```
sprites/
├── player/
│   ├── player_idle.png           (32x32)
│   ├── player_walk.png           (128x32) - 4 frames
│   ├── player_attack.png         (32x32)
│   └── player_hurt.png           (32x32)
├── npcs/
│   ├── npc_elder.png             (32x32)
│   ├── npc_priest.png            (32x32)
│   ├── npc_merchant.png          (32x32)
│   └── npc_ghost.png             (32x32, alpha 0.5)
└── enemies/
    ├── enemy_demon.png           (40x40)
    └── enemy_deceiver.png        (48x48)
```

**Code Usage**:
```javascript
// In game.js or renderer.js
renderer.loadSprite('player_idle', {
  type: 'image',
  path: '/static/webclient/assets/sprites/player_idle.png',
  width: 32,
  height: 32
});

// For animated spritesheets
renderer.loadSprite('player_walk', {
  type: 'spritesheet',
  path: '/static/webclient/assets/sprites/player_walk.png',
  frameWidth: 32,
  frameHeight: 32,
  columns: 4,    // 4 frames horizontal
  frames: 4      // 4 total frames
});
```

---

### 2. TILES (Environment Graphics)

**Location**: `mygame/web/static/webclient/assets/tiles/`

**Specifications**:
- Format: PNG with transparency
- Size: 32x32 px (standard tile size)
- Color Depth: RGBA (32-bit)
- Seamless: Edges should blend smoothly

**Files to Create**:

```
tiles/
├── floor_stone.png       (32x32) - Stone floor
├── floor_grass.png       (32x32) - Grass/garden
├── floor_sand.png        (32x32) - Desert sand
├── floor_water.png       (32x32) - Water/river
├── floor_marble.png      (32x32) - Holy temple marble
├── wall_stone.png        (32x32) - Stone wall
├── wall_wood.png         (32x32) - Wooden wall
├── door_closed.png       (32x32) - Closed door
└── door_open.png         (32x32) - Open doorway
```

---

### 3. AUDIO (Music & Sound Effects)

**Location**: `mygame/web/static/webclient/assets/audio/`

#### Background Music
**Location**: `audio/music/`

**Specifications**:
- Format: MP3 (primary) + OGG (fallback)
- Sample Rate: 44.1 kHz or 48 kHz
- Bitrate: 192-256 kbps (MP3), 128 kbps (OGG)
- Channels: Stereo
- Length: 2-5 minutes with seamless loop
- Loop Point: No clicks/pops at end

**Files to Create**:

```
audio/music/
├── exploration_peaceful.mp3      - General exploration
├── exploration_peaceful.ogg      - (fallback)
├── combat_intense.mp3            - Combat encounters
├── sacred_temple.mp3             - Temple/holy areas
├── boss_battle.mp3               - Boss fights
├── ambient.mp3                   - Peaceful ambience
├── puzzle_thinking.mp3           - Puzzle solving
├── victory_fanfare.mp3           - Victory/quest complete
└── defeat_theme.mp3              - Defeat/death
```

**Code Usage**:
```javascript
// In game.js
audioManager.playMusic('exploration_peaceful');

// Change based on game state
audioManager.playStateMusic('combat');  // Plays combat_intense
audioManager.playStateMusic('temple');  // Plays sacred_temple
audioManager.playStateMusic('boss');    // Plays boss_battle
```

#### Sound Effects
**Location**: `audio/sfx/`

**Specifications**:
- Format: WAV (lossless) or MP3
- Sample Rate: 44.1 kHz
- Bitrate: 128 kbps (MP3), 16-bit PCM (WAV)
- Channels: Mono (recommended)
- Length: 0.5 - 3 seconds
- Peak Volume: -3dB to -6dB

**Files to Create**:

```
audio/sfx/
├── combat/
│   ├── sword_slash.wav
│   ├── magic_cast.wav
│   ├── hit_impact.wav
│   ├── enemy_death.wav
│   └── player_hurt.wav
├── movement/
│   ├── footstep_stone.wav
│   ├── footstep_grass.wav
│   └── jump.wav
├── ui/
│   ├── button_click.wav
│   ├── ui_select.wav
│   └── ui_error.wav
├── dialogue/
│   ├── npc_talk.wav
│   └── dialogue_open.wav
└── special/
    ├── divine_light.wav
    ├── healing.wav
    ├── level_up.wav
    └── teleport.wav
```

**Code Usage**:
```javascript
// In game.js
audioManager.playSFX('sword_slash');
audioManager.playSFX('footstep_stone');
audioManager.playSFX('button_click');

// Multiple sounds in sequence
audioManager.playMultipleSFX(['sword_slash', 'hit_impact']);
```

---

### 4. FONTS (Custom Text)

**Location**: `mygame/web/static/webclient/assets/fonts/`

**Specifications**:
- Formats: TTF, WOFF2 (preferred), OTF
- File Size: Keep under 200 KB per font
- Character Set: At least Latin-1 supplement

**Files to Create**:

```
fonts/
├── biblical_serif.ttf      - For story/lore text
├── ui_sans.ttf             - For UI elements
└── monospace_code.ttf      - For status displays
```

**Code Usage** (in index.html or CSS):
```css
@font-face {
  font-family: 'Biblical';
  src: url('/static/webclient/assets/fonts/biblical_serif.ttf') format('truetype');
}

.story-text {
  font-family: 'Biblical', serif;
}
```

---

### 5. PARTICLES (Effect Graphics)

**Location**: `mygame/web/static/webclient/assets/particles/`

**Specifications**:
- Format: PNG with transparency (RGBA)
- Size: 8x8 to 32x32 pixels
- Style: Match game's art direction

**Files to Create**:

```
particles/
├── spark_yellow.png      - Yellow magical spark
├── spark_blue.png        - Blue magical spark
├── spark_red.png         - Red/fire spark
├── healing_light.png     - Healing effect
├── damage_red.png        - Damage splash
└── curse_dark.png        - Curse effect
```

**Code Usage**:
```javascript
// In game.js
renderer.addParticle(x, y, '#FFD700', 1000);  // Yellow, 1 sec
renderer.addParticle(x, y, '#FF0000');         // Red (damage)
renderer.addParticle(x, y, '#00FF00');         // Green (healing)
```

---

## File Organization Strategy

### By Asset Type (Recommended)
```
assets/
├── sprites/
├── tiles/
├── audio/music/
├── audio/sfx/
├── fonts/
└── particles/
```

### By Game Location (Alternative)
```
assets/
├── floor_01_outer_court/
│   ├── sprites/
│   ├── tiles/
│   └── audio/
├── floor_02_court_of_wisdom/
│   └── ...
└── shared/
    ├── fonts/
    ├── ui_sprites/
    └── ambient_audio/
```

**Recommendation**: Use "By Asset Type" for easier organization and reuse.

---

## Asset Pipeline

### 1. Creation Phase
- Design/create assets in your tool (Aseprite, Audacity, etc.)
- Ensure specs match above requirements
- Test for quality and consistency

### 2. Optimization Phase
- Compress images (use TinyPNG, ImageOptim)
- Reduce audio bitrate where appropriate
- Ensure web compatibility

### 3. File Organization
- Name files clearly (player_idle.png, not sprite1.png)
- Place in correct directories
- Create fallback formats (OGG for MP3, etc.)

### 4. Code Integration
- Update renderer.js or game.js to load new assets
- Test in browser (check console for errors)
- Verify proper playback/display

### 5. Version Control
- Commit asset files to git
- Document source/license in ASSETS_CREDITS.md
- Tag major asset updates

---

## Recommended Asset Tools

### Image Editing
- **Aseprite** ($20) - Professional pixel art
- **Piskel** (free) - Simple online sprite editor
- **Krita** (free) - Full-featured digital painting
- **LibreSprite** (free) - Free Aseprite fork

### Audio Editing
- **Audacity** (free) - Multi-track audio editor
- **Adobe Audition** ($20/month) - Professional
- **Reaper** ($60) - DAW for music

### Optimization
- **TinyPNG.com** - Image compression (online)
- **ImageOptim** (Mac) - Batch image optimization
- **FileSize.com** - Video/audio compression (online)

### Asset Resources
- **Incompetech** - Royalty-free music by Kevin MacLeod
- **Freesound.org** - Community sound effects
- **OpenGameArt.org** - Game art assets
- **itch.io** - Game asset packs

---

## Quick Start: Adding New Assets

### Adding a Character Sprite
1. Create sprite image (32x32 PNG with transparency)
2. Place in `assets/sprites/` folder
3. Name clearly: `npc_sage.png`
4. Update `game.js` to register:
   ```javascript
   renderer.loadSprite('npc_sage', {
     type: 'image',
     path: '/static/webclient/assets/sprites/npc_sage.png',
     width: 32,
     height: 32
   });
   ```
5. Use in game objects:
   ```javascript
   const sage = {
     sprite: 'npc_sage',
     label: 'Sage'
   };
   ```

### Adding Background Music
1. Create or source music track (2-5 min loop)
2. Export as MP3 (192 kbps, 44.1 kHz)
3. Place in `assets/audio/music/`
4. Create OGG fallback (128 kbps)
5. Update `game.js`:
   ```javascript
   // In playStateMusic()
   case 'library':
     this.playMusic('library_quiet');
     break;
   ```

### Adding Sound Effect
1. Create or source SFX (0.5-3 seconds)
2. Export as WAV (44.1 kHz, 16-bit, mono)
3. Place in `assets/audio/sfx/`
4. Test playback in browser
5. Use in code: `audioManager.playSFX('new_effect');`

---

## Troubleshooting

### Images Not Loading
- Check path: `/static/webclient/assets/...`
- Verify file exists and filename matches exactly
- Check browser console for CORS errors
- Ensure PNG has transparency support

### Audio Not Playing
- Check browser console for errors
- Verify audio format is supported (MP3, OGG, WAV)
- Check volume levels (should be -3dB to -6dB peak)
- Test in multiple browsers (Safari has audio restrictions)

### Performance Issues
- Check file sizes (sprites < 50KB, music < 3MB)
- Reduce image colors if possible
- Compress audio bitrate
- Limit concurrent sounds (8-16 max)

### File Size Too Large
- Use image compression (TinyPNG)
- Reduce audio bitrate (128 kbps for UI sounds)
- Use MP3 instead of WAV for storage
- Remove metadata from files

---

## Asset Checklist

Before deploying, ensure you have:

- [ ] All sprite files (32x32, PNG, transparent)
- [ ] All tile files (32x32, PNG, seamless)
- [ ] Background music (2-5 min loops, MP3 + OGG)
- [ ] Sound effects (WAV or MP3, < 200KB each)
- [ ] Custom fonts (TTF or WOFF2)
- [ ] Particle effect images (8x32px PNG)
- [ ] File size < 50MB total
- [ ] All files named clearly
- [ ] ASSETS_CREDITS.md created
- [ ] Code updated to reference new assets
- [ ] Assets tested in browser

---

## License & Attribution

Create `ASSETS_CREDITS.md` with all sources:

```markdown
# Asset Credits

## Music
- exploration_peaceful.mp3
  Source: Incompetech
  Artist: Kevin MacLeod
  License: CC BY 3.0

## Sound Effects
- sword_slash.wav
  Source: Freesound.org
  Artist: [Artist Name]
  License: CC0 Public Domain

## Graphics
- player_idle.png
  Created by: [Your Name]
  License: Original Work
```

---

## Summary

**Asset Directory**: `mygame/web/static/webclient/assets/`

**Main Subdirectories**:
1. `sprites/` - Character graphics (PNG, 32x32)
2. `tiles/` - Environment (PNG, 32x32)
3. `audio/music/` - Background tracks (MP3/OGG)
4. `audio/sfx/` - Sound effects (WAV/MP3)
5. `fonts/` - Custom fonts (TTF/WOFF2)
6. `particles/` - Effects (PNG, transparent)

Each subdirectory has a README with specifications and usage examples. Start there!
