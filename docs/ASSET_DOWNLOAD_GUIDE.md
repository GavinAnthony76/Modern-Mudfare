# Asset Download Guide - Journey Through Scripture

## Quick Start

This game uses **100% free, open-source assets** from OpenGameArt.org, Freesound.org, and other sources. You need to download these assets and place them in the correct folders for the game to work properly.

**Time to download all assets: ~30-45 minutes**

---

## Priority 1: Must Have (Download These First!)

### 1. LPC Character Sprites
**URL:** https://opengameart.org/art-search-advanced?field_art_tags_tid=14

Look for and download these:
- **"LPC Universal Spritesheet"** (best option - has thousands of character variations)
- Extract the PNG file to: `assets/sprites/characters/`
- Rename to: `player.png`

For NPCs, either download separate NPC packs or use:
- **"LPC Medieval Fantasy Characters"** - use for priest, merchant, elder
- Extract and name as:
  - `npc_priest.png`
  - `npc_merchant.png`
  - `npc_elder.png`
  - `pilgrim.png`

### 2. Palace/Dungeon Tileset
**URL:** https://opengameart.org/art-search-advanced?field_art_tags_tid=40

Look for:
- **"LPC Dungeon"** or **"LPC Indoor Tileset"** (most popular)
- Download the PNG tileset file
- Extract to: `assets/tiles/palace/floor1/`
- Rename to: `indoor_tileset.png`

For additional floors, download more tilesets:
- Create `assets/tiles/palace/floor2/` and `floor3/` folders
- Copy/reuse tileset or download variations

### 3. Enemy Sprites
**URL:** https://opengameart.org/art-search-advanced?field_art_tags_tid=13

Download:
- **"LPC Monsters"** spritesheet
- Extract PNG to: `assets/sprites/enemies/`
- Rename to:
  - `deceiver.png` (main boss - use demon/devil sprite)
  - `demon.png` (enemy type)
  - `undead.png` (enemy type)

### 4. Item Sprites
**URL:** https://opengameart.org/art-search-advanced?field_art_tags_tid=28

Download:
- **"LPC Items"** or **"LPC Items and Objects"**
- Extract PNG to: `assets/sprites/items/`
- Split into categories (optional):
  - `weapons.png`
  - `potions.png`
  - `quest_items.png`
  - `treasure.png`

---

## Priority 2: Enhance Audio

### Background Music
**URL:** https://opengameart.org/art-search-advanced?field_art_tags_tid=27

Search for and download:
- "Medieval Dungeon" or "Fantasy Music" tracks
- Format: OGG or MP3
- Download to: `assets/audio/music/`
- Rename to:
  - `medieval_exploration.ogg`
  - `boss_battle.ogg`
  - `ambient_palace.ogg`

**Alternative:** Incompetech.com (https://incompetech.com/)
- Search "dungeon" or "medieval"
- Download and convert to OGG if needed

### Sound Effects
**URL:** https://freesound.org/

Search for and download:
- "sword strike" → `assets/audio/sfx/combat_hit.wav`
- "magic spell" → `assets/audio/sfx/magic_spell.wav`
- "door open" → `assets/audio/sfx/door_open.wav`
- "chest open" → `assets/audio/sfx/chest_open.wav`
- "footstep" (you already have one)

---

## Priority 3: UI & Polish

### UI Elements
**URL:** https://opengameart.org/art-search-advanced?field_art_tags_tid=33

Download:
- **"RPG UI Pack"** or similar
- Extract buttons, bars, icons to: `assets/ui/`

### Fonts (Optional - Using Google Fonts)
No download needed! The game loads from Google Fonts:
- "Press Start 2P" (retro style)
- "Cinzel" (medieval style)

These are automatically loaded from Google Fonts CDN.

---

## Folder Structure - Where to Put Everything

```
mygame/web/static/webclient/assets/
│
├── sprites/
│   ├── characters/
│   │   ├── player.png (32x32 per frame)
│   │   ├── npc_priest.png
│   │   ├── npc_merchant.png
│   │   ├── npc_elder.png
│   │   └── pilgrim.png
│   │
│   ├── enemies/
│   │   ├── deceiver.png (48x48)
│   │   ├── demon.png (40x40)
│   │   └── undead.png (32x32)
│   │
│   └── items/
│       ├── weapons.png
│       ├── potions.png
│       ├── quest_items.png
│       └── treasure.png
│
├── tiles/
│   └── palace/
│       ├── floor1/
│       │   └── indoor_tileset.png (32x32 tiles)
│       ├── floor2/
│       │   └── indoor_tileset.png
│       └── floor3/
│           └── indoor_tileset.png
│
├── audio/
│   ├── music/
│   │   ├── medieval_exploration.ogg
│   │   ├── boss_battle.ogg
│   │   └── ambient_palace.ogg
│   │
│   └── sfx/
│       ├── footstep_wood.mp3 (already exists)
│       ├── combat_hit.wav
│       ├── magic_spell.wav
│       ├── door_open.wav
│       └── chest_open.wav
│
└── ui/
    ├── buttons/
    │   ├── button_normal.png
    │   └── button_hover.png
    └── health_bar.png
```

---

## Step-by-Step Download Instructions

### For OpenGameArt.org Assets:

1. Go to https://opengameart.org/
2. In the search, click "Advanced Search"
3. Use Art Tags filter (look for "LPC", "16-bit", "32-bit")
4. Filter by:
   - Art Type: "Sprite" or "Tile Set"
   - License: "CC0" or "CC-BY-SA" (safest)
5. Click asset to open details
6. Look for "Download" button
7. Save PNG to your computer
8. Extract if zipped
9. Move to appropriate `assets/` subfolder
10. Rename to match `assets.json` names

### For Freesound.org Assets:

1. Go to https://freesound.org/
2. Search for sound (e.g., "sword strike")
3. Filter by License: Creative Commons
4. Click download
5. Save to `assets/audio/sfx/`

---

## Recommended Free Asset Packs (Copy-Paste URLs)

### Character Sprites:
- https://opengameart.org/content/lpc-universal-spritesheet
- https://opengameart.org/content/lpc-medieval-fantasy-characters

### Tilesets:
- https://opengameart.org/content/lpc-dungeon
- https://opengameart.org/content/32x32-indoor-tiles

### Enemies/Monsters:
- https://opengameart.org/content/lpc-monsters

### Items:
- https://opengameart.org/content/lpc-items-objects

### Music:
- https://opengameart.org/content/medieval-dungeon-ambient
- https://incompetech.com/ (search "dungeon")

### Sound Effects:
- https://freesound.org/search/?q=sword+strike
- https://freesound.org/search/?q=magic+spell
- https://freesound.org/search/?q=door+open

---

## Technical Details

### Image Formats:
- **Sprites & Tilesets:** PNG (32x32 or 64x64 pixels per frame recommended)
- **UI Elements:** PNG (various sizes)

### Audio Formats:
- **Music:** OGG (preferred for web) or MP3
- **SFX:** WAV, OGG, or MP3

### Important Sprite Info:
When downloading, look for these specs:
- **Character sprites:** 32x32 pixels per frame (4 frames per row typical)
- **Enemy sprites:** 32x32 or 48x48 pixels
- **Tilesets:** 32x32 pixels per tile (with columns/rows info)
- **Item icons:** 16x16 pixels

### File Naming:
- Use **lowercase** with **underscores**: `my_sprite.png` ✅
- Match names in `assets.json` exactly
- No spaces in filenames

---

## Verification Checklist

After downloading, verify you have:

### Sprites (Essential):
- [ ] `assets/sprites/characters/player.png`
- [ ] `assets/sprites/characters/npc_priest.png`
- [ ] `assets/sprites/characters/npc_merchant.png`
- [ ] `assets/sprites/characters/npc_elder.png`
- [ ] `assets/sprites/enemies/deceiver.png`
- [ ] `assets/sprites/enemies/demon.png`

### Tilesets (Essential):
- [ ] `assets/tiles/palace/floor1/indoor_tileset.png`

### Audio (Recommended):
- [ ] `assets/audio/music/medieval_exploration.ogg`
- [ ] `assets/audio/music/boss_battle.ogg`
- [ ] `assets/audio/sfx/combat_hit.wav`

---

## Troubleshooting

### "Asset not loading" error:
- Check filename matches `assets.json` exactly
- Ensure file is in correct folder
- Verify PNG/OGG format

### "Image dimensions seem wrong":
- Most LPC sprites are 32x32 per frame
- Tilesets are typically 32x32 per tile
- Check asset download page for dimensions

### "Audio not playing":
- Use OGG for music (MP3 has licensing issues)
- Use WAV for sound effects
- Test audio file in browser first

### "Can't find asset pack":
- Try alternative keywords: "fantasy", "medieval", "RPG"
- Check license (must be free/open)
- Try different artists on OpenGameArt

---

## Asset Attribution

Create a file `ASSET_CREDITS.md` with attributions:

```markdown
# Asset Credits

Game assets are from these generous open-source creators:

## Characters
- LPC Universal Spritesheet by [Artist Name] - CC-BY-SA 3.0
- https://opengameart.org/content/[asset-name]

## Tilesets
- LPC Dungeon by [Artist Name] - CC0
- https://opengameart.org/content/[asset-name]

## Music
- Medieval Exploration by [Artist Name] - CC-BY 4.0
- https://opengameart.org/content/[asset-name]

...etc

All assets are free and open-source.
Find original creator and license on OpenGameArt.org or Freesound.org
```

---

## Next Steps After Downloading

1. ✅ Download all Priority 1 assets
2. ✅ Organize into correct folders
3. ✅ Update `assets.json` with filenames if different
4. ✅ Refresh the game in browser
5. ✅ Verify sprites and sounds display
6. ✅ Download Priority 2 (audio) assets
7. ✅ Test game with real graphics!

---

## Questions?

If assets won't load:
1. Check browser console for errors (F12)
2. Verify file paths match `assets.json`
3. Ensure PNG/OGG files are valid (try opening in image viewer)
4. Check file permissions
5. Clear browser cache and reload

Good luck! The game should look amazing once you add the free assets! 🎮
