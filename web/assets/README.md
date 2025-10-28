# Game Assets Directory

This directory contains all game assets (graphics, audio, fonts) for the Biblical Fantasy MUD.

## Directory Structure

```
assets/
├── sprites/          # Character and NPC sprite sheets
├── tiles/            # Environment tile sets
├── audio/            # Sound effects and music
│   ├── music/        # Background music tracks
│   └── sfx/          # Sound effects
├── fonts/            # Custom fonts for UI
└── particles/        # Particle effect images
```

## Asset Guidelines

### File Naming Convention
- Use **lowercase** with **underscores**: `player_idle.png`, `sword_slash.wav`
- Include descriptive names: `npc_priest_talking.png` not `sprite1.png`
- Version names if needed: `background_v1.png`, `background_v2.png`

### Sprites
- **Format**: PNG with transparency (RGBA)
- **Size**: 32x32px for basic tiles, 64x64px for characters
- **Frame Rate**: 8-12 FPS for animations
- **Examples**:
  - `player_idle.png`, `player_walk.png`, `player_attack.png`
  - `npc_elder.png`, `npc_priest.png`, `npc_merchant.png`
  - `enemy_demon.png`, `enemy_deceiver.png`

### Tiles
- **Format**: PNG with transparency
- **Size**: 32x32px per tile (standard tile size)
- **Examples**:
  - `floor_stone.png`, `floor_grass.png`, `floor_sand.png`
  - `wall_brick.png`, `wall_temple.png`
  - `object_fountain.png`, `object_statue.png`

### Audio - Background Music
Location: `audio/music/`
- **Format**: MP3 (for web compatibility) or OGG (fallback)
- **Sample Rate**: 44.1 kHz or 48 kHz
- **Bitrate**: 128 kbps (MP3) or 128 kbps (OGG)
- **Length**: 2-5 minutes (loops)
- **Examples**:
  - `exploration_peaceful.mp3` - General exploration
  - `combat_intense.mp3` - Combat encounters
  - `sacred_temple.mp3` - Temple/holy areas
  - `boss_battle.mp3` - Boss fights
  - `ambient.mp3` - Peaceful ambience

### Audio - Sound Effects
Location: `audio/sfx/`
- **Format**: WAV (best quality) or MP3
- **Sample Rate**: 44.1 kHz or 48 kHz
- **Length**: 0.5-3 seconds
- **Examples**:
  - `footstep_stone.wav`, `footstep_grass.wav`
  - `sword_slash.wav`, `magic_cast.wav`
  - `hit_impact.wav`, `enemy_death.wav`
  - `item_pickup.wav`, `level_up.wav`
  - `npc_talk.wav`, `dialogue_open.wav`
  - `divine_light.wav`, `healing.wav`
  - `button_click.wav`, `ui_select.wav`

### Fonts
Location: `fonts/`
- **Format**: TTF or WOFF2 (web optimized)
- **Examples**:
  - `biblical_serif.ttf` - For story/lore text
  - `modern_sans.ttf` - For UI elements
  - `monospace_code.ttf` - For status displays

### Particles
Location: `particles/`
- **Format**: PNG with transparency
- **Size**: 8x8px to 32x32px
- **Examples**:
  - `spark_yellow.png`, `spark_blue.png`
  - `healing_light.png`, `damage_red.png`
  - `divine_glow.png`, `evil_dark.png`

## How to Use Assets in Code

### Loading Sprites in renderer.js

```javascript
// Load image sprite
renderer.loadSprite('player_idle', {
  type: 'image',
  path: '/static/webclient/assets/sprites/player_idle.png',
  width: 32,
  height: 32
});

// Load spritesheet with multiple frames
renderer.loadSprite('player_walk', {
  type: 'spritesheet',
  path: '/static/webclient/assets/sprites/player_walk.png',
  frameWidth: 32,
  frameHeight: 32,
  columns: 4,      // 4 frames per row
  frames: 8        // 8 total frames
});
```

### Playing Audio in game.js

```javascript
// Play music
audioManager.playMusic('exploration_peaceful');

// Play sound effect
audioManager.playSFX('footstep_stone');

// Play multiple SFX
audioManager.playMultipleSFX(['sword_slash', 'hit_impact']);

// Change game state music
audioManager.playStateMusic('combat');  // Plays combat_intense
```

### CSS Custom Fonts

```css
@font-face {
  font-family: 'Biblical';
  src: url('/static/webclient/assets/fonts/biblical_serif.ttf') format('truetype');
}

body {
  font-family: 'Biblical', serif;
}
```

## Asset File Size Recommendations

### For Web Performance
- **Sprites**: 20-50 KB per file
- **Music**: 500 KB - 2 MB per track
- **SFX**: 10-100 KB per file
- **Fonts**: 50-200 KB per font
- **Total Assets**: Keep under 50 MB for fast loading

## Audio Recording Tips

### For Background Music
1. Record or compose 2-5 minute loops
2. Ensure smooth looping (no clicks or pops at loop point)
3. Use moderate BPM (100-140 for adventure music)
4. Consider mixing multiple instruments/layers

### For Sound Effects
1. Keep consistent volume levels (-6dB to -3dB peak)
2. Use high-quality recordings (16-bit or 24-bit)
3. Remove background noise and clicks
4. Add subtle reverb for spatial awareness
5. Normalize audio before export

## Organizing Assets by Game Content

### Character Assets
```
sprites/
  characters/
    player/
    npc_elder/
    npc_priest/
    npc_merchant/
  enemies/
    demon/
    deceiver/
```

### Environment Assets
```
tiles/
  floor_01_stone/
  floor_02_grass/
  floor_03_sand/
  floor_04_holy/
  wall_types/
  object_decorative/
```

### Audio Organization
```
audio/
  music/
    floor_01/
    floor_02/
    boss_battles/
  sfx/
    combat/
    ambient/
    ui/
    dialogue/
```

## Compression & Optimization

### Image Optimization
Use tools like ImageOptim, TinyPNG, or FileSize.com to reduce file size without quality loss.

### Audio Optimization
- Use lower bitrate for UI sounds (64-128 kbps)
- Use higher bitrate for music (192-320 kbps)
- Consider lossy compression for real-time games

## Copyright & Licensing

Document the source of all assets:
- Create an `ASSETS_CREDITS.md` file
- List source, artist, and license for each asset
- Ensure all assets are licensed for use in your project

Example:
```
## Music Credits
- exploration_peaceful.mp3
  Source: Incompetech
  Artist: Kevin MacLeod
  License: CC BY 3.0

## Sound Effects Credits
- footstep_stone.wav
  Source: Freesound.org
  Artist: Mike Koenig
  License: CC0 (Public Domain)
```

## Next Steps

1. **Create sprite sheets** for characters and NPCs (use Aseprite, Piskel, or similar)
2. **Record or source music** from royalty-free libraries
3. **Find or create SFX** from platforms like Freesound.org or Zapsplat
4. **Organize** assets into proper subdirectories
5. **Update code** to reference actual asset paths instead of placeholders
6. **Test** in browser to ensure proper loading and playback

## Resources

- **Sprite Art**: Aseprite, Piskel, Krita
- **Music**: Incompetech, Freepd.com, OpenGameArt.org
- **Sound Effects**: Freesound.org, Zapsplat, BBC Sound Library
- **Image Optimization**: ImageOptim, TinyPNG, PNGQuant
- **Audio Editing**: Audacity (free), Adobe Audition
