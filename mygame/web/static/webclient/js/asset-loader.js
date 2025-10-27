/**
 * Asset Loader - Manages loading and caching of game assets
 * Supports sprites, tilesets, audio, and UI elements
 */

class AssetLoader {
  constructor() {
    this.sprites = new Map();
    this.tilesets = new Map();
    this.audio = new Map();
    this.uiElements = new Map();
    this.loadedAssets = 0;
    this.totalAssets = 0;
    this.assetRegistry = {};
  }

  /**
   * Load asset registry from JSON file
   */
  async loadRegistry(registryPath = 'assets.json') {
    try {
      const response = await fetch(registryPath);
      if (!response.ok) {
        console.log('Asset registry not found, using defaults');
        this.createDefaultRegistry();
        return;
      }
      this.assetRegistry = await response.json();
      console.log('Asset registry loaded:', this.assetRegistry);
    } catch (e) {
      console.log('Could not load asset registry, using defaults:', e);
      this.createDefaultRegistry();
    }
  }

  /**
   * Create default asset registry (for when assets.json doesn't exist)
   */
  createDefaultRegistry() {
    this.assetRegistry = {
      sprites: {
        player: {
          src: 'assets/sprites/characters/player.png',
          frameWidth: 32,
          frameHeight: 32,
          frames: 4,
          columns: 4
        },
        npc_priest: {
          src: 'assets/sprites/npcs/priest.png',
          frameWidth: 32,
          frameHeight: 32
        },
        npc_merchant: {
          src: 'assets/sprites/npcs/merchant.png',
          frameWidth: 32,
          frameHeight: 32
        },
        npc_elder: {
          src: 'assets/sprites/npcs/elder.png',
          frameWidth: 32,
          frameHeight: 32
        },
        deceiver: {
          src: 'assets/sprites/enemies/deceiver.png',
          frameWidth: 48,
          frameHeight: 48
        },
        demon: {
          src: 'assets/sprites/enemies/demon.png',
          frameWidth: 40,
          frameHeight: 40
        }
      },
      tilesets: {
        palace_floor1: {
          src: 'assets/tiles/palace/floor1/tileset.png',
          frameWidth: 32,
          frameHeight: 32,
          columns: 16
        }
      },
      audio: {
        exploration: {
          src: 'assets/audio/music/exploration.ogg',
          volume: 0.5,
          loop: true
        },
        boss_battle: {
          src: 'assets/audio/music/boss_battle.ogg',
          volume: 0.5,
          loop: true
        }
      }
    };
  }

  /**
   * Load sprite from registry
   */
  async loadSprite(spriteKey) {
    if (this.sprites.has(spriteKey)) {
      return this.sprites.get(spriteKey);
    }

    const spriteConfig = this.assetRegistry.sprites?.[spriteKey];
    if (!spriteConfig) {
      console.log(`Sprite config not found: ${spriteKey}`);
      return null;
    }

    try {
      const img = new Image();
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = spriteConfig.src;
      });

      const sprite = {
        image: img,
        ...spriteConfig
      };

      this.sprites.set(spriteKey, sprite);
      this.loadedAssets++;
      console.log(`Loaded sprite: ${spriteKey}`);
      return sprite;
    } catch (e) {
      console.log(`Failed to load sprite ${spriteKey}:`, e);
      return null;
    }
  }

  /**
   * Load tileset from registry
   */
  async loadTileset(tilesetKey) {
    if (this.tilesets.has(tilesetKey)) {
      return this.tilesets.get(tilesetKey);
    }

    const tilesetConfig = this.assetRegistry.tilesets?.[tilesetKey];
    if (!tilesetConfig) {
      console.log(`Tileset config not found: ${tilesetKey}`);
      return null;
    }

    try {
      const img = new Image();
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = tilesetConfig.src;
      });

      const tileset = {
        image: img,
        ...tilesetConfig
      };

      this.tilesets.set(tilesetKey, tileset);
      this.loadedAssets++;
      console.log(`Loaded tileset: ${tilesetKey}`);
      return tileset;
    } catch (e) {
      console.log(`Failed to load tileset ${tilesetKey}:`, e);
      return null;
    }
  }

  /**
   * Load audio from registry
   */
  async loadAudio(audioKey) {
    if (this.audio.has(audioKey)) {
      return this.audio.get(audioKey);
    }

    const audioConfig = this.assetRegistry.audio?.[audioKey];
    if (!audioConfig) {
      console.log(`Audio config not found: ${audioKey}`);
      return null;
    }

    try {
      const audio = new Audio();
      audio.src = audioConfig.src;
      audio.volume = audioConfig.volume || 0.5;
      audio.loop = audioConfig.loop || false;

      this.audio.set(audioKey, audio);
      this.loadedAssets++;
      console.log(`Loaded audio: ${audioKey}`);
      return audio;
    } catch (e) {
      console.log(`Failed to load audio ${audioKey}:`, e);
      return null;
    }
  }

  /**
   * Load all sprites from registry
   */
  async loadAllSprites() {
    const promises = [];
    for (const spriteKey in this.assetRegistry.sprites || {}) {
      promises.push(this.loadSprite(spriteKey));
    }
    return Promise.all(promises);
  }

  /**
   * Load all tilesets from registry
   */
  async loadAllTilesets() {
    const promises = [];
    for (const tilesetKey in this.assetRegistry.tilesets || {}) {
      promises.push(this.loadTileset(tilesetKey));
    }
    return Promise.all(promises);
  }

  /**
   * Load all audio from registry
   */
  async loadAllAudio() {
    const promises = [];
    for (const audioKey in this.assetRegistry.audio || {}) {
      promises.push(this.loadAudio(audioKey));
    }
    return Promise.all(promises);
  }

  /**
   * Get sprite by key
   */
  getSprite(spriteKey) {
    return this.sprites.get(spriteKey);
  }

  /**
   * Get tileset by key
   */
  getTileset(tilesetKey) {
    return this.tilesets.get(tilesetKey);
  }

  /**
   * Get audio by key
   */
  getAudio(audioKey) {
    return this.audio.get(audioKey);
  }

  /**
   * Get all loaded sprites
   */
  getAllSprites() {
    return Array.from(this.sprites.values());
  }

  /**
   * Get loading progress
   */
  getProgress() {
    return this.totalAssets > 0 ? (this.loadedAssets / this.totalAssets) * 100 : 0;
  }

  /**
   * Log all loaded assets
   */
  logLoadedAssets() {
    console.log('=== Loaded Assets ===');
    console.log(`Sprites (${this.sprites.size}):`);
    this.sprites.forEach((sprite, key) => {
      console.log(`  - ${key}`);
    });
    console.log(`Tilesets (${this.tilesets.size}):`);
    this.tilesets.forEach((tileset, key) => {
      console.log(`  - ${key}`);
    });
    console.log(`Audio (${this.audio.size}):`);
    this.audio.forEach((audio, key) => {
      console.log(`  - ${key}`);
    });
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AssetLoader;
}
