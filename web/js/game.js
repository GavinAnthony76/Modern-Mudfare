/**
 * Journey Through Scripture - Main Game Controller
 * Manages game state, screens, and coordination between modules
 */

class Game {
    constructor() {
        this.currentScreen = 'welcome';
        this.gameState = {
            character: null,
            connected: false,
            inGame: false
        };

        this.screens = {
            welcome: document.getElementById('welcome-screen'),
            charCreation: document.getElementById('character-creation'),
            game: document.getElementById('game-screen'),
            about: document.getElementById('about-screen')
        };

        this.loadingOverlay = document.getElementById('loading-overlay');

        // Initialize modules
        this.audio = new AudioManager();
        this.websocket = new WebSocketClient();
        this.renderer = new GameRenderer('game-canvas');
        this.ui = new UIManager(this);

        this.init();
    }

    async init() {
        console.log('Initializing Journey Through Scripture...');

        // Set up event listeners
        this.setupEventListeners();

        // Show welcome screen
        this.showScreen('welcome');

        // Initialize audio (user interaction required)
        this.audio.init();

        // Load real assets from assets.json (CORS-safe)
        try {
            // Only attempt to fetch if not on file:// protocol
            if (window.location.protocol !== 'file:') {
                const response = await fetch('assets.json');
                const assetsConfig = await response.json();
                console.log('Loaded assets.json, attempting to load real assets...');
                await this.renderer.loadRealAssets(assetsConfig);
            } else {
                console.log('Running from file:// - use a local web server for asset loading');
                console.log('Quick fix: python -m http.server 8000');
            }
        } catch (e) {
            console.error('Failed to load assets.json:', e);
            console.log('Continuing with placeholder graphics...');
        }

        console.log('Game initialized successfully');
    }

    setupEventListeners() {
        // Welcome screen buttons
        document.getElementById('btn-new-game')?.addEventListener('click', () => {
            this.showScreen('charCreation');
        });

        document.getElementById('btn-continue')?.addEventListener('click', () => {
            this.continueGame();
        });

        document.getElementById('btn-about')?.addEventListener('click', () => {
            this.showScreen('about');
        });

        // Character creation
        document.getElementById('btn-create-character')?.addEventListener('click', () => {
            this.createCharacter();
        });

        document.getElementById('btn-back-to-menu')?.addEventListener('click', () => {
            this.showScreen('welcome');
        });

        // Name suggestions
        document.querySelectorAll('.suggestion').forEach(suggestion => {
            suggestion.addEventListener('click', (e) => {
                document.getElementById('char-name').value = e.target.textContent;
            });
        });

        // Class selection
        document.querySelectorAll('.class-card').forEach(card => {
            card.addEventListener('click', (e) => {
                document.querySelectorAll('.class-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
            });
        });

        // About screen
        document.getElementById('btn-back-from-about')?.addEventListener('click', () => {
            this.showScreen('welcome');
        });

        // Command input
        document.getElementById('command-input')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendCommand();
            }
        });

        document.getElementById('btn-send-command')?.addEventListener('click', () => {
            this.sendCommand();
        });

        // Mobile controls
        document.querySelectorAll('.dpad-btn[data-direction]').forEach(btn => {
            btn.addEventListener('click', () => {
                const direction = btn.dataset.direction;
                this.sendCommand(direction);
            });
        });

        document.querySelectorAll('.dpad-btn[data-action]').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.sendCommand(action);
            });
        });

        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.sendCommand(action);
            });
        });

        // Panel tabs
        document.querySelectorAll('.panel-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const panelName = tab.dataset.panel;
                this.ui.switchPanel(panelName);
            });
        });

        // Game control buttons
        document.getElementById('btn-inventory')?.addEventListener('click', () => {
            this.ui.toggleInventory();
        });

        document.getElementById('btn-quests')?.addEventListener('click', () => {
            this.ui.toggleQuests();
        });

        document.getElementById('btn-map')?.addEventListener('click', () => {
            this.ui.toggleMap();
        });

        document.getElementById('btn-settings')?.addEventListener('click', () => {
            this.ui.toggleSettings();
        });

        // WebSocket events
        this.websocket.on('connected', () => {
            this.onConnected();
        });

        this.websocket.on('disconnected', () => {
            this.onDisconnected();
        });

        this.websocket.on('message', (data) => {
            this.onServerMessage(data);
        });

        this.websocket.on('error', (error) => {
            this.onServerError(error);
        });
    }

    showScreen(screenName) {
        // Hide all screens
        Object.values(this.screens).forEach(screen => {
            screen.classList.remove('active');
        });

        // Show requested screen
        if (this.screens[screenName]) {
            this.screens[screenName].classList.add('active');
            this.currentScreen = screenName;
            console.log(`Showing screen: ${screenName}`);
        }
    }

    showLoading(message = 'Loading...') {
        this.loadingOverlay.classList.add('active');
        document.getElementById('loading-text').textContent = message;
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('active');
    }

    createCharacter() {
        const name = document.getElementById('char-name').value.trim();
        const selectedClass = document.querySelector('.class-card.selected');

        if (!name) {
            this.ui.showNotification('Please enter a character name', 'warning');
            return;
        }

        if (!selectedClass) {
            this.ui.showNotification('Please select a class', 'warning');
            return;
        }

        const characterData = {
            name: name,
            class: selectedClass.dataset.class
        };

        this.gameState.character = characterData;

        console.log('Creating character:', characterData);
        this.ui.showNotification(`Welcome, ${name} the ${selectedClass.dataset.class}!`, 'success');

        // Connect to server and start game
        this.startGame();
    }

    startGame() {
        this.showLoading('Loading game...');

        // Try to connect to Evennia server (optional - game works offline too)
        // Default Evennia WebSocket: ws://localhost:4001/ws
        this.websocket.connect('ws://localhost:4001/ws')
            .then(() => {
                console.log('Connected to game server');
                this.showScreen('game');
                this.hideLoading();
                this.gameState.inGame = true;

                // Start game loop
                this.startGameLoop();

                // Send initial game message
                if (this.gameState.character) {
                    this.ui.addTextOutput(`You are ${this.gameState.character.name}, a ${this.gameState.character.class}.`, 'system');
                }
                this.ui.addTextOutput('Type "help" for available commands.', 'system');
            })
            .catch((error) => {
                console.error('Failed to connect:', error);
                this.hideLoading();

                // Start in offline/demo mode (NO notification needed - it's normal)
                this.showScreen('game');
                this.gameState.inGame = true;
                this.startGameLoop();

                this.ui.addTextOutput(`Welcome ${this.gameState.character.name}, the ${this.gameState.character.class}!`, 'system');
                this.ui.addTextOutput('You stand at the edge of a vast palace.', 'narrative');
                this.ui.addTextOutput('Ancient stones stretch before you, mysterious and beautiful.', 'narrative');
                this.ui.addTextOutput('Type "help" for available commands.', 'system');
            });
    }

    continueGame() {
        // Load saved character from localStorage
        const savedChar = localStorage.getItem('savedCharacter');
        if (savedChar) {
            this.gameState.character = JSON.parse(savedChar);
            this.startGame();
        } else {
            this.ui.showNotification('No saved character found', 'warning');
        }
    }

    sendCommand(command) {
        const input = document.getElementById('command-input');
        const cmd = command || input.value.trim();

        if (!cmd) return;

        // Echo command
        this.ui.addTextOutput(`> ${cmd}`, 'command-echo');

        // Send to server if connected
        if (this.gameState.connected && this.websocket.isConnected()) {
            this.websocket.send({
                type: 'command',
                text: cmd
            });
        } else {
            // Offline mode - handle basic commands locally
            this.handleOfflineCommand(cmd);
        }

        // Clear input
        if (!command) {
            input.value = '';
        }
    }

    handleOfflineCommand(cmd) {
        const command = cmd.toLowerCase();

        if (command === 'help') {
            this.ui.addTextOutput('Available commands:', 'system');
            this.ui.addTextOutput('- look: Examine your surroundings', 'system');
            this.ui.addTextOutput('- north/south/east/west: Move in a direction', 'system');
            this.ui.addTextOutput('- inventory: Check your inventory', 'system');
            this.ui.addTextOutput('- help: Show this help message', 'system');
        } else if (command === 'look') {
            this.ui.addTextOutput('The Desert Wilderness stretches endlessly around you.', 'narrative');
            this.ui.addTextOutput('Golden sands shimmer in the heat. You see paths leading in all directions.', 'narrative');
        } else if (['north', 'south', 'east', 'west', 'n', 's', 'e', 'w'].includes(command)) {
            this.ui.addTextOutput('You walk across the shifting sands...', 'narrative');
            this.ui.addTextOutput('(Connect to server to explore the full world)', 'system');
        } else if (command === 'inventory' || command === 'inv') {
            this.ui.addTextOutput('Your inventory is empty.', 'system');
            this.ui.addTextOutput('(Start your journey to collect items!)', 'system');
        } else {
            this.ui.addTextOutput(`Unknown command: ${cmd}`, 'system');
            this.ui.addTextOutput('Type "help" for available commands.', 'system');
        }
    }

    onConnected() {
        this.gameState.connected = true;
        this.ui.showNotification('Connected to server', 'success');
        console.log('WebSocket connected');
    }

    onDisconnected() {
        this.gameState.connected = false;
        this.ui.showNotification('Disconnected from server', 'warning');
        console.log('WebSocket disconnected');
    }

    onServerMessage(data) {
        console.log('Server message:', data);

        // Handle different message types
        if (data.type === 'text') {
            const textClass = data.class || 'narrative';
            this.ui.addTextOutput(data.text, textClass);
        } else if (data.type === 'error') {
            this.ui.addTextOutput(data.message || data.text, 'error');
        } else if (data.type === 'character_update') {
            this.onCharacterUpdate(data.character);
        } else if (data.type === 'room_update') {
            this.onRoomUpdate(data.room);
        } else if (data.type === 'notification') {
            this.ui.showNotification(data.message, data.class || 'info');
        } else if (data.type === 'combat_event') {
            this.onCombatEvent(data);
        } else if (data.type === 'dialogue') {
            this.onDialogue(data);
        } else if (data.type === 'quest_update') {
            this.onQuestUpdate(data.quest);
        } else if (data.type === 'pong') {
            // Ignore pong responses
        }
    }

    onCharacterUpdate(character) {
        console.log('Character update:', character);

        // Update UI with character stats
        this.gameState.character = Object.assign(
            this.gameState.character || {},
            character
        );

        // Update visible stats panels if they exist
        const statsPanel = document.getElementById('stats-panel');
        if (statsPanel && statsPanel.classList.contains('active')) {
            this.ui.updateStatsDisplay(character);
        }

        const inventoryPanel = document.getElementById('inventory-panel');
        if (inventoryPanel && inventoryPanel.classList.contains('active')) {
            this.ui.updateInventoryDisplay(character.inventory || []);
        }
    }

    onRoomUpdate(room) {
        console.log('Room update:', room);

        // Update game state with room info
        this.gameState.currentRoom = room;

        // Display room description
        if (room.description) {
            this.ui.addTextOutput(room.name, 'system');
            this.ui.addTextOutput(room.description, 'narrative');
        }

        // Update renderer with new room state
        if (this.renderer) {
            this.renderer.setCurrentRoom(room);
        }
    }

    onCombatEvent(event) {
        console.log('Combat event:', event);

        const eventType = event.event;

        if (eventType === 'combat_started') {
            this.gameState.inCombat = true;
            this.ui.showCombatUI(event.enemy);
            this.ui.addTextOutput(`Combat started! You face ${event.enemy.name}!`, 'combat');
        } else if (eventType === 'combat_action') {
            this.ui.addTextOutput(event.message, 'combat');
        } else if (eventType === 'health_updated') {
            this.ui.updateCombatHealth(event.attacker_health, event.target_health);
        } else if (eventType === 'combat_ended') {
            this.gameState.inCombat = false;
            this.ui.hideCombatUI();

            if (event.victory) {
                this.ui.addTextOutput('Victory! You have defeated your enemy!', 'success');
                if (event.xp_gained) {
                    this.ui.addTextOutput(`You gained ${event.xp_gained} experience!`, 'success');
                }
            } else {
                this.ui.addTextOutput('You have been defeated...', 'error');
            }
        }
    }

    onDialogue(data) {
        console.log('Dialogue:', data);

        this.ui.showDialogue({
            npcName: data.npc_name,
            text: data.dialogue,
            options: data.options
        });
    }

    onQuestUpdate(quest) {
        console.log('Quest update:', quest);

        // Update quest in UI
        this.ui.updateQuest(quest);
    }

    onServerError(error) {
        console.error('Server error:', error);
        this.ui.showNotification('Server error occurred', 'warning');
    }

    startGameLoop() {
        // Main game loop for rendering
        const loop = () => {
            if (this.gameState.inGame) {
                this.renderer.render();
                requestAnimationFrame(loop);
            }
        };
        loop();
    }

    saveGame() {
        if (this.gameState.character) {
            localStorage.setItem('savedCharacter', JSON.stringify(this.gameState.character));
            this.ui.showNotification('Game saved', 'success');
        }
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new Game();
});
