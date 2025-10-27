# Particles Directory

Store particle effect images here.

## Particle Types

### Magical Effects
- `spark_yellow.png` - Yellow magical spark (8x8, 16x16)
- `spark_blue.png` - Blue magical spark
- `spark_red.png` - Red/fire spark
- `spark_purple.png` - Purple/dark magic spark

### Healing & Buffs
- `healing_light.png` - Healing effect
- `blessing_glow.png` - Buff/blessing effect
- `light_rays.png` - Divine light

### Damage & Debuffs
- `damage_red.png` - Damage splash
- `blood_drop.png` - Blood effect
- `curse_dark.png` - Curse/debuff effect

### Environmental
- `dust_cloud.png` - Dust/dirt particles
- `smoke.png` - Smoke effect
- `water_splash.png` - Water particles
- `fire_flare.png` - Fire particles

## Specifications
- **Format**: PNG with transparency (RGBA)
- **Size**: 8x8 to 32x32 pixels
- **Colors**: Match game color scheme
- **Style**: Match overall art style (pixel art, hand-drawn, etc.)

## Using Particles in Code

```javascript
// Add particle effect at position
renderer.addParticle(x, y, '#FFD700', 1000);  // Yellow, 1 second duration

// Common colors
renderer.addParticle(x, y, '#FF0000');  // Red (damage)
renderer.addParticle(x, y, '#00FF00');  // Green (healing)
renderer.addParticle(x, y, '#0099FF');  // Blue (magic)
renderer.addParticle(x, y, '#FFD700');  // Gold (success)
renderer.addParticle(x, y, '#8B008B');  // Purple (special)
```

## Tips
- Keep simple and readable (not too detailed)
- Use bright colors for visibility
- Create multiple variations for visual interest
- Ensure transparency for compositing
- Test particle combinations for visual clarity
