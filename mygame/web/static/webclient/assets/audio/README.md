# Audio Directory

Store all music and sound effects here.

## Subdirectories

### Music (background tracks)
Location: `audio/music/`

- `exploration_peaceful.mp3` - Calm exploration ambience
- `combat_intense.mp3` - Action-packed combat music
- `sacred_temple.mp3` - Holy/temple atmosphere
- `boss_battle.mp3` - Epic boss fight music
- `ambient.mp3` - General ambient background
- `puzzle_thinking.mp3` - Puzzle-solving atmosphere
- `victory_fanfare.mp3` - Level/quest complete
- `defeat_theme.mp3` - Death/failure music

### Sound Effects (short audio)
Location: `audio/sfx/`

**Combat Sounds**
- `sword_slash.wav` - Sword attack
- `magic_cast.wav` - Spell casting
- `hit_impact.wav` - Hit/damage sound
- `enemy_death.wav` - Enemy defeated
- `player_hurt.wav` - Player takes damage
- `block_shield.wav` - Shield block

**Movement Sounds**
- `footstep_stone.wav` - Footstep on stone
- `footstep_grass.wav` - Footstep on grass
- `footstep_sand.wav` - Footstep on sand
- `jump.wav` - Character jump

**Environmental Sounds**
- `water_splash.wav` - Water effects
- `wind_ambient.wav` - Wind sound
- `thunder.wav` - Storm sound
- `gate_open.wav` - Door/gate opening
- `gate_close.wav` - Door/gate closing

**UI Sounds**
- `button_click.wav` - Button pressed
- `ui_select.wav` - Menu selection
- `ui_error.wav` - Error/invalid action
- `notification.wav` - Message received

**NPC & Dialogue**
- `npc_talk.wav` - NPC speech start
- `dialogue_open.wav` - Dialogue window opens
- `dialogue_close.wav` - Dialogue closes

**Divine & Special**
- `divine_light.wav` - Holy effect
- `healing.wav` - Healing received
- `blessing.wav` - Buff received
- `curse.wav` - Curse effect
- `teleport.wav` - Teleportation
- `level_up.wav` - Character level up

## Audio Specifications

### Music Tracks
- **Format**: MP3 (primary) + OGG (fallback)
- **Bitrate**: 192-256 kbps
- **Sample Rate**: 44.1 kHz
- **Length**: 2-5 minutes with seamless loop
- **Compression**: Lossy (MP3) or Lossless (OGG)
- **File Size**: 1-3 MB per track

### Sound Effects
- **Format**: WAV (lossless) or MP3
- **Bitrate**: 128 kbps (MP3) or 16-bit PCM (WAV)
- **Sample Rate**: 44.1 kHz
- **Length**: 0.5-3 seconds
- **Compression**: Minimal/lossless preferred
- **File Size**: 10-200 KB per effect
- **Channels**: Mono (preferred for most SFX), Stereo for ambient

## How to Use in Code

### Playing Music
```javascript
// Play specific track
audioManager.playMusic('exploration_peaceful');

// Change music based on game state
audioManager.playStateMusic('combat');    // Plays combat_intense
audioManager.playStateMusic('temple');    // Plays sacred_temple
audioManager.playStateMusic('boss');      // Plays boss_battle
```

### Playing Sound Effects
```javascript
// Play single sound
audioManager.playSFX('sword_slash');

// Play multiple sounds in sequence
audioManager.playMultipleSFX(['sword_slash', 'hit_impact']);

// Play with delay
setTimeout(() => audioManager.playSFX('player_hurt'), 200);
```

### Volume Control
```javascript
// Set volumes (0.0 - 1.0)
audioManager.setMasterVolume(0.8);
audioManager.setMusicVolume(0.5);
audioManager.setSFXVolume(0.7);

// Mute/unmute
audioManager.mute();
audioManager.unmute();
```

## Recording Audio

### Background Music
1. Compose or find royalty-free music
2. Ensure 2-5 minute length with smooth loop
3. Mix at -6dB to -3dB peak volume
4. Export as MP3 (192 kbps) and OGG (128 kbps)
5. Test looping for clicks/pops at seams

### Sound Effects
1. Record or download SFX
2. Edit in Audacity to remove unwanted sounds
3. Normalize to -3dB peak
4. Add slight fade in/out if needed
5. Export as WAV (44.1 kHz, 16-bit, mono)
6. Create MP3 version (128 kbps) as fallback

## Royalty-Free Audio Resources

**Music**
- Incompetech (incompetech.com) - Kevin MacLeod compositions
- Freepd.com - Curated royalty-free music
- OpenGameArt.org - Game-specific music
- YouTube Audio Library - Premium music library

**Sound Effects**
- Freesound.org - Community recorded sounds
- Zapsplat - Free SFX library
- BBC Sound Library - Professional recordings
- OpenGameArt.org - Game audio assets

## Audio Editing Tools
- **Audacity** - Free, open-source audio editor
- **Adobe Audition** - Professional audio software
- **Reaper** - DAWS for music composition
- **FMOD Studio** - Game audio middleware

## Cross-Platform Compatibility

### Browser Audio Formats
```html
<audio>
  <source src="music.mp3" type="audio/mpeg">
  <source src="music.ogg" type="audio/ogg">
</audio>
```

### Web Audio API (Programmatic)
- Uses format-agnostic buffers
- Better for interactive/dynamic sounds
- Supports MP3, OGG, WAV, WebM

## Performance Tips
- Pre-load frequently used SFX
- Use compressed MP3 for music
- Keep SFX under 200KB each
- Limit concurrent sound playback (8-16 max)
- Use lower bitrate for UI sounds
- Cache audio context and buffers
