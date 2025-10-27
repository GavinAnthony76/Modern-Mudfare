# Music Directory

Place background music tracks here.

## File Format
- Primary: `.mp3` (192-256 kbps, 44.1 kHz)
- Fallback: `.ogg` (128 kbps, 44.1 kHz)

Example: `exploration_peaceful.mp3` and `exploration_peaceful.ogg`

## Expected Music Tracks

1. **exploration_peaceful.mp3** - General exploration
2. **combat_intense.mp3** - Combat encounters
3. **sacred_temple.mp3** - Temple/holy areas
4. **boss_battle.mp3** - Boss fights
5. **ambient.mp3** - Peaceful ambience
6. **puzzle_thinking.mp3** - Puzzle solving
7. **victory_fanfare.mp3** - Victory music
8. **defeat_theme.mp3** - Defeat music

## Audio Properties
- Length: 2-5 minutes per track
- Sample Rate: 44.1 kHz
- Channels: Stereo
- Loop: Seamless looping at end
- Peak Volume: -3dB to -6dB

## Loading in Code
```javascript
audioManager.playMusic('exploration_peaceful');
```
