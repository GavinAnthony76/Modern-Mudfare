# Sprites Directory

Store all character and NPC sprite sheets here.

## Files to Create

### Characters
- `player_idle.png` - Player character standing (32x32)
- `player_walk.png` - Player walking animation (4-8 frames, 32x32 each)
- `player_attack.png` - Player attack animation (32x32)
- `player_hurt.png` - Player taking damage (32x32)

### NPCs
- `npc_elder.png` - Elderly Pilgrim (32x32)
- `npc_priest.png` - Priest Ezra (32x32)
- `npc_merchant.png` - Merchant Deborah (32x32)
- `npc_ghost.png` - Faint Apparition (32x32, semi-transparent)

### Enemies
- `enemy_demon.png` - Demon enemy (40x40)
- `enemy_deceiver.png` - The Deceiver boss (48x48)
- `enemy_leviathan.png` - Sea monster (64x64)
- `enemy_nephilim.png` - Giant creature (48x48)

### Interactive Objects
- `fountain.png` - Sacred fountain (32x32)
- `altar.png` - Holy altar (32x32)
- `statue.png` - Temple statue (32x32)

## Sprite Sheet Format

For animations, use a horizontal spritesheet:
```
Frame 1 | Frame 2 | Frame 3 | Frame 4
(32x32) | (32x32) | (32x32) | (32x32)
```

Example: `player_walk.png` = 128x32 pixels (4 frames)

Reference in code:
```javascript
renderer.loadSprite('player_walk', {
  type: 'spritesheet',
  path: '/static/webclient/assets/sprites/player_walk.png',
  frameWidth: 32,
  frameHeight: 32,
  columns: 4,
  frames: 4
});
```

## Recommended Tools
- **Aseprite** - Professional pixel art editor
- **Piskel** - Free online sprite editor
- **Krita** - Free digital painting
- **Tiled Map Editor** - For tileset organization
