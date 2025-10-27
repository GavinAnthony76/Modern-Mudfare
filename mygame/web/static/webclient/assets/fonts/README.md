# Fonts Directory

Place custom font files here for use in the game UI.

## File Formats
- **TTF** (.ttf) - TrueType Font
- **WOFF2** (.woff2) - Web Optimized Font (recommended for web)
- **OTF** (.otf) - OpenType Font

## Recommended Fonts

### Body Text / Story
- `biblical_serif.ttf` - Serif font for biblical text and lore
- `story_text.ttf` - Readable serif for narrative content

### UI / Menus
- `ui_sans.ttf` - Clean sans-serif for interface elements
- `ui_bold.ttf` - Bold version for titles and headers

### Special Purpose
- `monospace_code.ttf` - Monospace for status displays and code
- `ancient_runes.ttf` - Decorative font for biblical aesthetics

## Using Fonts in CSS

```css
@font-face {
  font-family: 'Biblical';
  src: url('/static/webclient/assets/fonts/biblical_serif.ttf') format('truetype');
}

@font-face {
  font-family: 'UIFont';
  src: url('/static/webclient/assets/fonts/ui_sans.woff2') format('woff2');
}

body {
  font-family: 'UIFont', sans-serif;
}

.story-text {
  font-family: 'Biblical', serif;
}
```

## Font Resources

**Free Fonts**
- Google Fonts (fonts.google.com) - Extensive library
- DaFont (dafont.com) - Creative fonts
- 1001 Free Fonts (1001freefonts.com) - Curated collection

**Licensed Fonts**
- Adobe Fonts - Professional quality
- MyFonts - Premium fonts with licenses

## Performance Tips
- Use WOFF2 for web (smaller file size)
- Limit to 2-3 fonts maximum
- Use system fonts as fallback
- Subset fonts to only needed characters
- Use `font-display: swap` for fast loading

Example optimized font loading:
```css
@font-face {
  font-family: 'Biblical';
  src: url('/fonts/biblical_serif.woff2') format('woff2');
  font-display: swap;
}
```
