/**
 * Main Game Controller
 * Handles game loop, input, and coordination between renderer and server
 */

class BiblicalMUDGame {
  constructor() {
    this.renderer = null;
    this.websocket = null;
    this.player = null; // Character instance
    this.questSystem = null;
    this.dialogueSystem = null;
    this.combatSystem = null;
    this.gameState = {
      playerName: 'Pilgrim',
      location: 'Floor 1: Outer Court',
      status: 'Exploring',
      health: 100,
      maxHealth: 100,
      mana: 100,
      maxMana: 100,
      xp: 0,
      level: 1,
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

    // Initialize game systems
    this.initializeGameSystems();

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
   * Initialize game systems (character, quest, dialogue, combat)
   */
  initializeGameSystems() {
    console.log('Initializing game systems...');

    // Create player character
    this.player = new Character('Pilgrim', 'prophet');
    this.gameState.playerName = this.player.name;
    this.gameState.health = this.player.health;
    this.gameState.maxHealth = this.player.maxHealth;
    this.gameState.mana = this.player.mana;
    this.gameState.maxMana = this.player.maxMana;
    this.gameState.level = this.player.level;

    // Create quest system
    this.questSystem = new QuestSystem();

    // Create dialogue system
    this.dialogueSystem = new DialogueSystem(this.questSystem);

    console.log(`Player created: ${this.player.name} (${this.player.classType})`);
    console.log(`Stats: Faith=${this.player.faith}, Wisdom=${this.player.wisdom}, Strength=${this.player.strength}`);
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

    // Handle combat actions
    if (this.combatSystem && this.combatSystem.combatActive) {
      if (keys.has('a') || keys.has('A')) {
        this.playerAttackInCombat();
        keys.delete('a');
        keys.delete('A');
      }
      if (keys.has('h') || keys.has('H')) {
        this.playerCastSpellInCombat('heal');
        keys.delete('h');
        keys.delete('H');
      }
      if (keys.has('s') || keys.has('S')) {
        this.playerCastSpellInCombat('smite');
        keys.delete('s');
        keys.delete('S');
      }
      // Enemy turn after player action
      if (this.combatSystem && this.combatSystem.combatActive && this.combatSystem.currentTurn === 'enemy') {
        setTimeout(() => {
          this.enemyAttackInCombat();
        }, 500);
      }
      return;
    }

    // Normal movement handling
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

    // Create NPC data structure for dialogue system
    const npcData = {
      label: npc.label,
      dialogue: {
        greeting: npc.dialogue || 'Welcome, traveler!',
        main_menu: {
          1: { text: 'Tell me about yourself', response: 'farewell' },
          2: { text: 'Goodbye', response: 'farewell' }
        },
        responses: {
          farewell: 'Farewell, traveler. May your path be blessed.'
        }
      }
    };

    // Start dialogue with dialogue system
    if (this.dialogueSystem) {
      const dialogueResponse = this.dialogueSystem.startDialogue(npcData);
      console.log('Dialogue options:', dialogueResponse.options);

      // Show dialogue in UI
      const messageEl = document.getElementById('gameMessage');
      if (messageEl) {
        messageEl.innerHTML = `
          <div style="font-weight: bold;">${dialogueResponse.npc}</div>
          <div>${dialogueResponse.text}</div>
          ${dialogueResponse.options.map(opt =>
            `<div style="margin-top: 5px; cursor: pointer; color: #0066cc;">
              ${opt.number}. ${opt.text}
            </div>`
          ).join('')}
        `;
      }
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
   * Start combat with an enemy
   */
  startCombat(enemy) {
    if (!this.player || this.combatSystem) {
      console.log('Combat already in progress or player not ready');
      return;
    }

    // Create enemy character object
    const enemyChar = {
      name: enemy.label || 'Enemy',
      health: enemy.health || 30,
      maxHealth: enemy.health || 30,
      mana: 0,
      stats: {
        faith: 10,
        wisdom: 8,
        strength: 12,
        courage: 10,
        righteousness: 9
      },
      getStat: function(stat) { return this.stats[stat] || 10; },
      takeDamage: function(damage) {
        this.health = Math.max(0, this.health - damage);
        return damage;
      },
      calculateDamage: function(bonus = 0) {
        return this.stats.strength * 2 + bonus + Math.floor(Math.random() * 5);
      },
      calculateDefense: function() {
        return Math.floor(this.stats.faith / 2);
      },
      isAlive: function() { return this.health > 0; }
    };

    // Initialize combat system
    this.combatSystem = new Combat(this.player, enemyChar);
    this.gameState.status = `In Combat with ${enemy.label}!`;
    console.log(`Combat started with ${enemy.label}!`);

    // Show combat status
    this.showCombatStatus();
  }

  /**
   * Player attacks in combat
   */
  playerAttackInCombat() {
    if (!this.combatSystem) return;

    this.combatSystem.playerAttack();
    this.showCombatStatus();

    if (!this.combatSystem.combatActive) {
      this.endCombat();
    }
  }

  /**
   * Player casts spell in combat
   */
  playerCastSpellInCombat(spellName) {
    if (!this.combatSystem) return;

    this.combatSystem.playerCastSpell(spellName);
    this.showCombatStatus();

    if (!this.combatSystem.combatActive) {
      this.endCombat();
    }
  }

  /**
   * Enemy attacks
   */
  enemyAttackInCombat() {
    if (!this.combatSystem) return;

    this.combatSystem.enemyAttack();
    this.showCombatStatus();

    if (!this.combatSystem.combatActive) {
      this.endCombat();
    }
  }

  /**
   * Show combat status in UI
   */
  showCombatStatus() {
    if (!this.combatSystem) return;

    const status = this.combatSystem.getStatus();
    const messageEl = document.getElementById('gameMessage');

    if (messageEl) {
      messageEl.innerHTML = `
        <div style="color: #8B0000; font-weight: bold;">COMBAT</div>
        <div style="margin-top: 5px;">
          <div>${this.player.name} HP: ${status.playerHealth}/${status.playerMaxHealth}</div>
          <div>${status.enemyLabel} HP: ${status.enemyHealth}/${status.enemyMaxHealth}</div>
          <div style="margin-top: 10px; color: #0066cc;">${status.log[status.log.length - 1] || 'Combat started!'}</div>
          ${status.combatActive ? `
            <div style="margin-top: 10px;">
              <div style="cursor: pointer; color: green;">A - Attack</div>
              <div style="cursor: pointer; color: blue;">H - Heal Spell (cost: 20 mana)</div>
              <div style="cursor: pointer; color: orange;">S - Smite Spell (cost: 25 mana)</div>
            </div>
          ` : ''}
        </div>
      `;
    }

    // Sync player stats back
    if (this.player) {
      this.player.health = status.playerHealth;
      this.player.mana = status.playerMana;
    }
  }

  /**
   * End combat
   */
  endCombat() {
    if (!this.combatSystem) return;

    const status = this.combatSystem.getStatus();
    console.log('Combat ended!');
    console.log(status.log[status.log.length - 1]);

    this.combatSystem = null;
    this.gameState.status = 'Exploring';
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
    // Create player game object from character instance
    const playerObj = {
      id: 'player',
      type: 'player',
      x: 400,
      y: 300,
      sprite: 'player',
      label: this.player.name,
      health: this.player.health,
      maxHealth: this.player.maxHealth,
      mana: this.player.mana,
      maxMana: this.player.maxMana,
      level: this.player.level,
      visible: true
    };
    this.gameObjects.push(playerObj);

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
    // Sync player character stats to game state
    if (this.player) {
      this.gameState.health = this.player.health;
      this.gameState.maxHealth = this.player.maxHealth;
      this.gameState.mana = this.player.mana;
      this.gameState.maxMana = this.player.maxMana;
      this.gameState.level = this.player.level;
      this.gameState.xp = this.player.xp;

      // Update player object in game world
      const playerObj = this.gameObjects.find(obj => obj.id === 'player');
      if (playerObj) {
        playerObj.health = this.player.health;
        playerObj.mana = this.player.mana;
        playerObj.level = this.player.level;
      }
    }

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
