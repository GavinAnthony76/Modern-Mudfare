# Free Open-Source Game Assets Sources

This document lists all recommended free/open-source asset sources for Journey Through Scripture.

## 📊 Asset Categories & Sources

### 1. CHARACTER SPRITES (LPC Format)
**Best Source: OpenGameArt.org - LPC Characters**
- URL: https://opengameart.org/art-search-advanced?field_art_tags_tid=14
- Format: PNG spritesheets (32x32 or 64x64 per frame)
- License: CC0/CC-BY-SA
- Recommended packs:
  - "LPC Universal Spritesheet" - Thousands of character variations
  - "LPC Medieval Fantasy Characters"
  - "LPC Priests and Robed Characters"
  - "LPC Merchants and NPCs"

**Download instructions:**
1. Browse: https://opengameart.org/art-search-advanced?field_art_tags_tid=14
2. Look for "LPC" or "Liberated Pixel Cup" in name
3. Download PNG files to: `assets/sprites/characters/`
4. Organize by type: `player/`, `npc/`, `enemies/`

---

### 2. PALACE/DUNGEON TILESET
**Best Source: OpenGameArt.org - Indoor/Castle Tilesets**
- URL: https://opengameart.org/art-search-advanced?field_art_tags_tid=40
- Format: PNG spritesheets (typically 32x32 tiles)
- License: CC0/CC-BY-SA
- Recommended packs:
  - "LPC Dungeon" - Perfect for palace floors
  - "32x32 Indoor Tiles"
  - "Stone Dungeon Tileset"
  - "Medieval Indoor Tileset"
  - "Castle Interior Tileset"

**Download instructions:**
1. Browse: https://opengameart.org/art-search-advanced?field_art_tags_tid=40
2. Filter by "Tile Set" in art type
3. Download PNG tilesets to: `assets/tiles/palace/`
4. Organize as: `floor1/`, `floor2/`, etc.

---

### 3. ENEMY/MONSTER SPRITES
**Best Source: OpenGameArt.org - Enemy/Monster Art**
- URL: https://opengameart.org/art-search-advanced?field_art_tags_tid=13
- Recommended packs:
  - "LPC Monsters and Enemies"
  - "Demon Sprites"
  - "Fantasy Creature Sprites"

**Download to:** `assets/sprites/enemies/`

---

### 4. ITEM SPRITES
**Best Source: OpenGameArt.org - Items**
- URL: https://opengameart.org/art-search-advanced?field_art_tags_tid=28
- Recommended packs:
  - "LPC Items and Objects"
  - "Fantasy Item Icons"
  - "Inventory Items Spritesheet"
  - "Weapons and Armor Sprites"

**Download to:** `assets/sprites/items/`

---

### 5. BACKGROUND MUSIC
**Best Source: OpenGameArt.org - Music**
- URL: https://opengameart.org/art-search-advanced?field_art_tags_tid=27
- Format: OGG, MP3, WAV
- License: CC0/CC-BY-SA
- Recommended tracks:
  - "Medieval Dungeon Ambient"
  - "Fantasy Fantasy Music"
  - "Peaceful Exploration Theme"
  - "Boss Battle Music"

**Download to:** `assets/audio/music/`

---

### 6. SOUND EFFECTS
**Best Source: Freesound.org / OpenGameArt.org**
- Footsteps: Already have footstep_wood.mp3
- Other SFX recommendations:
  - "Sword Strike" sounds
  - "Magic Spell" sounds
  - "NPC Dialogue" effects
  - "Door Open/Close"
  - "Chest Open"

**Download to:** `assets/audio/sfx/`

---

### 7. UI ELEMENTS / FONTS
**Best Source: OpenGameArt.org - UI Art**
- URL: https://opengameart.org/art-search-advanced?field_art_tags_tid=33
- Recommended packs:
  - "RPG UI Buttons and Menus"
  - "Fantasy UI Elements"
  - "Health Bar Graphics"

**Fonts:**
- Google Fonts (for web): https://fonts.google.com/
- Recommended: "Press Start 2P" (retro), "Cinzel" (medieval)

**Download to:** `assets/ui/`

---

## 🎯 Quick Start: Essential Assets to Download First

### Priority 1 (Game Playable):
1. ✅ **LPC Universal Spritesheet** - Character sprites
2. ✅ **LPC Dungeon Tileset** - Palace floors
3. ✅ **LPC Items Spritesheet** - Weapons, potions, quest items
4. ✅ **LPC Monsters** - Enemy sprites (The Deceiver, demons)

### Priority 2 (Enhance Gameplay):
5. **Medieval Dungeon Music** - Ambient background
6. **Sound Effects Pack** - Combat, spells, interactions

### Priority 3 (Polish):
7. **Fantasy UI Pack** - Menus, buttons, HUD elements
8. **Boss Battle Music** - Deceiver fight theme

---

## 📁 Folder Structure

```
assets/
├── sprites/
│   ├── characters/
│   │   ├── player/
│   │   ├── npcs/
│   │   └── pilgrims/
│   ├── enemies/
│   │   ├── deceiver/
│   │   ├── demons/
│   │   └── undead/
│   └── items/
│       ├── weapons/
│       ├── potions/
│       ├── quest_items/
│       └── treasure/
├── tiles/
│   ├── palace/
│   │   ├── floor1/
│   │   ├── floor2/
│   │   ├── floor3/
│   │   └── ...
│   └── nature/
├── audio/
│   ├── music/
│   │   ├── exploration/
│   │   ├── boss_battle/
│   │   └── ambient/
│   └── sfx/
│       ├── combat/
│       ├── spells/
│       ├── ambient/
│       └── ui/
├── ui/
│   ├── buttons/
│   ├── menus/
│   ├── icons/
│   └── fonts/
└── particles/
    ├── magic/
    ├── blood/
    └── effects/
```

---

## 🔗 Alternative Asset Sources

### General:
- **itch.io Assets**: https://itch.io/game-assets
- **Kenney.nl**: https://kenney.nl/ (Excellent free game assets)
- **Pixabay**: https://pixabay.com/ (Free images/music)
- **FreePik**: https://www.freepik.com/ (Some free assets)

### Music Specifically:
- **Freesound.org**: https://freesound.org/
- **YouTube Audio Library**: https://www.youtube.com/audiolibrary
- **Incompetech**: https://incompetech.com/ (Royalty-free music)

### Licenses to Look For:
- ✅ CC0 (Public Domain)
- ✅ CC-BY (Credit required)
- ✅ CC-BY-SA (Credit + Share-alike)
- ✅ CC0-BY-NC (Non-commercial free)
- ❌ Avoid: Proprietary, "For evaluation only"

---

## ⚡ Integration Instructions

### For Character Sprites:
1. Download LPC Character spritesheet PNG
2. Place in `assets/sprites/characters/`
3. Update `renderer.js` sprite references
4. Configure sprite dimensions (usually 32x32 per frame)

### For Tilesets:
1. Download tileset PNG
2. Place in `assets/tiles/palace/floor1/` (for Floor 1)
3. Create tilemap loader (see tile-loader.js)
4. Reference in room definitions

### For Audio:
1. Download MP3/OGG files
2. Place in `assets/audio/music/` or `assets/audio/sfx/`
3. Reference in audio.js playMusic() / playSFX()
4. Ensure format compatibility (MP3 recommended for web)

---

## 📝 License Attribution

Create `ASSET_CREDITS.md` file with all asset attributions:

```markdown
# Asset Credits

## Characters
- LPC Universal Spritesheet by [Author] - CC-BY-SA 3.0

## Tilesets
- LPC Dungeon by [Author] - CC0

## Music
- Medieval Dungeon Ambient by [Author] - CC-BY 4.0

...etc
```

---

## ✅ Next Steps

1. Download Priority 1 assets from sources listed above
2. Extract and organize into folder structure
3. Create asset registry JSON file (see below)
4. Implement asset loader in renderer.js
5. Test rendering with real graphics

---

## 📋 Asset Registry Format

Create `assets.json`:
```json
{
  "sprites": {
    "player": {
      "src": "sprites/characters/lpc_universal.png",
      "frameWidth": 32,
      "frameHeight": 32,
      "frames": 12,
      "columns": 4
    },
    "npc_priest": {
      "src": "sprites/characters/npc_priest.png",
      "frameWidth": 32,
      "frameHeight": 32
    }
  },
  "tiles": {
    "stone_floor": {
      "src": "tiles/palace/floor1/stone_floor.png",
      "frameWidth": 32,
      "frameHeight": 32
    }
  },
  "audio": {
    "exploration": {
      "src": "audio/music/medieval_exploration.ogg",
      "volume": 0.5
    }
  }
}
```

