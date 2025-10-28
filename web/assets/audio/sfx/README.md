# Sound Effects Directory

Place short sound effect files here.

## File Format
- Format: `.wav` or `.mp3`
- Sample Rate: 44.1 kHz
- Bit Depth: 16-bit (WAV) or 128 kbps (MP3)
- Channels: Mono (recommended) or Stereo
- Length: 0.5 - 3 seconds

## Sound Effect Categories

### Combat (sword_slash, magic_cast, hit_impact, etc.)
### Movement (footstep_*, jump, etc.)
### UI (button_click, ui_select, ui_error, etc.)
### Environmental (water_splash, wind, thunder, etc.)
### Dialogue (npc_talk, dialogue_open, etc.)
### Special (divine_light, healing, level_up, etc.)

## Example Loading
```javascript
audioManager.playSFX('sword_slash');
audioManager.playSFX('footstep_stone');
audioManager.playSFX('button_click');
```

See parent directory (audio/) README for full list of expected SFX files.
