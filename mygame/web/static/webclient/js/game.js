/**
 * Main Game Controller
 * Handles game loop, input, and coordination between renderer and server
 */

class BiblicalMUDGame {
  constructor() {
    this.renderer = null;
    this.websocket = null;
    this.gameState = {
      playerName: 'Pilgrim',
      location: 'Floor 1: Outer Court',
      status: 'Exploring',
      health: 100,
      maxHealth: 100,
      inventory: []
    };

    this.gameObjects = [];
    this.gameRunning = false;
    this.frameCount = 0;
    this.lastFrameTime = Date.now();
    this.fps = 0;

    this.inputManager = new InputManager();
    this.audioManager = null;
  }

  /**
   * Initialize the game
   */
  async initialize() {
    console.log('Initializing Biblical MUD Game...');

    // Initialize renderer
    this.renderer = new GameRenderer('gameCanvas', 800, 600);
    this.renderer.registerPlaceholderAssets();

    // Wait for sprites to load
    await this.waitForSpritesLoaded();

    // Initialize audio
    this.audioManager = new AudioManager();

    // Set up input handling
    this.setupInputHandling();

    // Setup WebSocket connection
    this.setupWebSocket();

    // Setup responsive design
    this.setupResponsiveDesign();

    // Create demo world
    this.createDemoWorld();

    // Start game loop
    this.startGameLoop();

    console.log('Game initialized successfully!');
  }

  /**
   * Wait for all sprites to load
   */
  waitForSpritesLoaded(timeout = 5000) {
    return new Promise((resolve) => {
      // Give SVG sprites a moment to initialize
      setTimeout(() => {
        let loaded = true;
        let spriteCount = 0;

        this.renderer.sprites.forEach(sprite => {
          spriteCount++;
          // SVG data URIs load immediately, so check if image exists
          if (sprite.image && !sprite.image.src) {
            loaded = false;
          }
        });

        // If sprites exist, consider them loaded
        if (spriteCount > 0 && loaded) {
          console.log(`Loaded ${spriteCount} sprites`);
          resolve();
        } else {
          // Try a more lenient approach - just wait a bit then proceed
          const startTime = Date.now();
          const checkInterval = setInterval(() => {
            if (Date.now() - startTime > timeout) {
              clearInterval(checkInterval);
              console.log('Sprite loading timeout, proceeding anyway');
              resolve();
            }
          }, 100);
        }
      }, 100);
    });
  }

  /**
   * Set up input handling
   */
  setupInputHandling() {
    const canvas = this.renderer.canvas;

    // Keyboard input
    document.addEventListener('keydown', (e) => {
      this.inputManager.handleKeyDown(e.key);
      this.handleInput(this.inputManager.getPressedKeys());
    });

    document.addEventListener('keyup', (e) => {
      this.inputManager.handleKeyUp(e.key);
    });

    // Mouse input
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      this.handleCanvasClick(x, y);
    });

    // Touch input
    canvas.addEventListener('touchstart', (e) => {
      const touch = e.touches[0];
      const rect = canvas.getBoundingClientRect();
      const x = touch.clientX - rect.left;
      const y = touch.clientY - rect.top;
      this.handleCanvasClick(x, y);
    });
  }

  /**
   * Handle keyboard/gamepad input
   */
  handleInput(keys) {
    const player = this.gameObjects.find(obj => obj.type === 'player');
    if (!player) return;

    const moveSpeed = 5;
    const oldX = player.x;
    const oldY = player.y;

    if (keys.has('ArrowUp') || keys.has('w') || keys.has('W')) {
      player.y -= moveSpeed;
    }
    if (keys.has('ArrowDown') || keys.has('s') || keys.has('S')) {
      player.y += moveSpeed;
    }
    if (keys.has('ArrowLeft') || keys.has('a') || keys.has('A')) {
      player.x -= moveSpeed;
    }
    if (keys.has('ArrowRight') || keys.has('d') || keys.has('D')) {
      player.x += moveSpeed;
    }

    // Check collision with boundaries
    if (player.x < 0) player.x = 0;
    if (player.y < 0) player.y = 0;
    if (player.x + 32 > 2560) player.x = 2560 - 32;
    if (player.y + 32 > 1920) player.y = 1920 - 32;

    // Update camera to follow player and play footstep sound
    if (oldX !== player.x || oldY !== player.y) {
      this.renderer.updateCamera(player.x + 16, player.y + 16);
      this.checkCollisions(player);

      // Play footstep sound on movement
      if (this.audioManager && Math.random() > 0.7) {
        this.audioManager.playSFX('footstep_wood');
      }
    }
  }

  /**
   * Handle canvas click
   */
  handleCanvasClick(x, y) {
    // Convert screen coordinates to world coordinates
    const worldX = x + this.renderer.camera.x;
    const worldY = y + this.renderer.camera.y;

    // Find clicked object
    const clicked = this.gameObjects.find(obj => {
      return obj.x < worldX && obj.x + 32 > worldX &&
             obj.y < worldY && obj.y + 32 > worldY;
    });

    if (clicked && clicked.type === 'npc') {
      this.interactWithNPC(clicked);
    }
  }

  /**
   * Interact with NPC
   */
  interactWithNPC(npc) {
    this.gameState.status = `Talking to ${npc.label}`;
    console.log(`Interacting with: ${npc.label}`);

    // Show dialogue in UI
    const messageEl = document.getElementById('gameMessage');
    if (messageEl) {
      messageEl.textContent = `${npc.label}: ${npc.dialogue || 'Welcome, traveler!'}`;
    }

    // Send to server if connected
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify({
        action: 'interact',
        target: npc.id
      }));
    }
  }

  /**
   * Check collisions between player and NPCs/objects
   */
  checkCollisions(player) {
    this.gameObjects.forEach(obj => {
      if (obj.type === 'npc' || obj.type === 'enemy') {
        const distance = Math.hypot(obj.x - player.x, obj.y - player.y);
        if (distance < 50) {
          obj.nearby = true;
        } else {
          obj.nearby = false;
        }
      }
    });
  }

  /**
   * Set up WebSocket connection
   */
  setupWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/game/`;

    try {
      this.websocket = new WebSocket(wsUrl);

      this.websocket.onopen = () => {
        console.log('Connected to game server');
        this.gameState.status = 'Connected';
      };

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleServerMessage(data);
      };

      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.gameState.status = 'Connection Error';
      };

      this.websocket.onclose = () => {
        console.log('Disconnected from server');
        this.gameState.status = 'Offline';
      };
    } catch (e) {
      console.log('WebSocket not available, running in demo mode');
      this.gameState.status = 'Demo Mode';
    }
  }

  /**
   * Handle messages from server
   */
  handleServerMessage(data) {
    switch (data.type) {
      case 'game_state':
        this.updateGameState(data);
        break;
      case 'npc_dialogue':
        this.showDialogue(data);
        break;
      case 'combat':
        this.handleCombat(data);
        break;
      case 'notification':
        this.showNotification(data.message);
        break;
    }
  }

  /**
   * Update game state from server
   */
  updateGameState(data) {
    if (data.player) {
      Object.assign(this.gameState, data.player);
    }
    if (data.objects) {
      this.gameObjects = data.objects;
    }
  }

  /**
   * Show NPC dialogue
   */
  showDialogue(data) {
    const messageEl = document.getElementById('gameMessage');
    if (messageEl) {
      messageEl.textContent = `${data.npcName}: ${data.dialogue}`;
    }
  }

  /**
   * Handle combat
   */
  handleCombat(data) {
    console.log(`Combat: ${data.attacker} deals ${data.damage} damage to ${data.defender}`);
    this.renderer.addParticle(data.x, data.y, '#FF0000');
    this.gameState.status = 'In Combat!';
  }

  /**
   * Show notification message
   */
  showNotification(message) {
    const messageEl = document.getElementById('gameMessage');
    if (messageEl) {
      messageEl.textContent = message;
    }
  }

  /**
   * Set up responsive design
   */
  setupResponsiveDesign() {
    window.addEventListener('resize', () => {
      this.resizeCanvas();
    });
    this.resizeCanvas();
  }

  /**
   * Resize canvas for responsive design
   */
  resizeCanvas() {
    const container = document.getElementById('gameContainer');
    if (container) {
      const width = Math.min(container.clientWidth, 1200);
      const height = Math.min(container.clientHeight, 800);
      this.renderer.resize(width, height);
    }
  }

  /**
   * Create demo world with NPCs and objects
   */
  createDemoWorld() {
    // Create player
    const player = {
      id: 'player',
      type: 'player',
      x: 400,
      y: 300,
      sprite: 'player',
      label: 'You',
      health: 100,
      maxHealth: 100,
      visible: true
    };
    this.gameObjects.push(player);

    // Create NPCs
    const npcs = [
      {
        id: 'elder1',
        type: 'npc',
        x: 200,
        y: 200,
        sprite: 'npc_elder',
        label: 'Elderly Pilgrim',
        dialogue: 'The Palace of Light is ancient beyond measure...',
        visible: true
      },
      {
        id: 'priest1',
        type: 'npc',
        x: 600,
        y: 250,
        sprite: 'npc_priest',
        label: 'Priest Ezra',
        dialogue: 'Welcome to the Pilgrim\'s Rest. You are safe here.',
        visible: true
      },
      {
        id: 'merchant1',
        type: 'npc',
        x: 500,
        y: 450,
        sprite: 'npc_merchant',
        label: 'Merchant Deborah',
        dialogue: 'I have supplies for your journey. Fair prices!',
        visible: true
      }
    ];

    npcs.forEach(npc => this.gameObjects.push(npc));

    // Create some decorative items
    const items = [
      {
        id: 'item1',
        type: 'item',
        x: 150,
        y: 150,
        sprite: 'item_generic',
        label: 'Scroll',
        visible: true
      },
      {
        id: 'item2',
        type: 'item',
        x: 700,
        y: 400,
        sprite: 'item_weapon',
        label: 'Staff',
        visible: true
      }
    ];

    items.forEach(item => this.gameObjects.push(item));

    // Update player position in game state
    this.gameState.health = player.health;
    this.gameState.maxHealth = player.maxHealth;
  }

  /**
   * Main game loop
   */
  startGameLoop() {
    this.gameRunning = true;
    const gameLoop = () => {
      if (!this.gameRunning) return;

      // Update
      this.update();

      // Render
      this.renderer.gameObjects = this.gameObjects;
      this.renderer.render(this.gameState);

      // Calculate FPS
      this.frameCount++;
      const now = Date.now();
      if (now - this.lastFrameTime >= 1000) {
        this.fps = this.frameCount;
        this.frameCount = 0;
        this.lastFrameTime = now;
        console.log(`FPS: ${this.fps}`);
      }

      requestAnimationFrame(gameLoop);
    };

    gameLoop();
  }

  /**
   * Update game state each frame
   */
  update() {
    // Update game logic here
    // This is called every frame
  }

  /**
   * Pause game
   */
  pause() {
    this.gameRunning = false;
  }

  /**
   * Resume game
   */
  resume() {
    this.gameRunning = true;
    this.startGameLoop();
  }

  /**
   * Stop game
   */
  stop() {
    this.gameRunning = false;
    if (this.websocket) {
      this.websocket.close();
    }
  }
}

/**
 * Input Manager - Handle keyboard and gamepad input
 */
class InputManager {
  constructor() {
    this.pressedKeys = new Set();
    this.gamepadStates = new Map();
  }

  handleKeyDown(key) {
    this.pressedKeys.add(key);
  }

  handleKeyUp(key) {
    this.pressedKeys.delete(key);
  }

  getPressedKeys() {
    return this.pressedKeys;
  }

  isKeyPressed(key) {
    return this.pressedKeys.has(key);
  }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
  const game = new BiblicalMUDGame();
  await game.initialize();

  // Store game instance globally for debugging
  window.game = game;

  // Handle page visibility for pausing when tab is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      game.pause();
    } else {
      game.resume();
    }
  });
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BiblicalMUDGame;
}
