# Tiles Directory

Store all environment tile sets here (32x32 pixels per tile).

## Tile Categories

### Floor Tiles
- `floor_stone.png` - Stone floor (32x32)
- `floor_grass.png` - Grass/garden (32x32)
- `floor_sand.png` - Desert sand (32x32)
- `floor_water.png` - Water/river (32x32)
- `floor_marble.png` - Holy temple marble (32x32)

### Wall & Structure Tiles
- `wall_stone.png` - Stone wall (32x32)
- `wall_wood.png` - Wooden wall (32x32)
- `wall_temple.png` - Temple wall (32x32)
- `wall_cave.png` - Cave stone (32x32)
- `door_closed.png` - Closed door (32x32)
- `door_open.png` - Open doorway (32x32)

### Decorative Tiles
- `tree.png` - Tree (32x32 or larger)
- `rock.png` - Rock formation (32x32)
- `column.png` - Temple column (32x32)
- `torch.png` - Lit torch (32x32)
- `bookshelf.png` - Library shelf (32x32)

### Special Tiles
- `void.png` - Empty/void space (32x32) - placeholder
- `glow_divine.png` - Divine light effect (32x32)
- `shadow_dark.png` - Shadow/darkness (32x32)

## How to Use in Game

Reference tiles in your world building code:
```javascript
// In world/build_world.py (Evennia)
map_data = [
  ['floor_stone', 'floor_stone', 'wall_stone'],
  ['floor_stone', 'door_open', 'wall_stone'],
  ['floor_grass', 'floor_grass', 'tree']
]
```

## Tileset Tips
- Keep consistent style across all tiles
- Ensure tiles blend seamlessly at edges
- Use 32x32 as standard size
- Create variations (damaged, lit, etc.)
- Test tiling patterns for visual issues

## Tools
- **Tiled Map Editor** - Organize and visualize tilesets
- **LibreSprite** - Create pixel art tiles
- **Krita** - Digital tile creation
