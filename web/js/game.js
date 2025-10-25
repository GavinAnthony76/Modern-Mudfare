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

    init() {
        console.log('Initializing Journey Through Scripture...');

        // Set up event listeners
        this.setupEventListeners();

        // Show welcome screen
        this.showScreen('welcome');

        // Initialize audio (user interaction required)
        this.audio.init();

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
        this.showLoading('Connecting to server...');

        // Try to connect to Evennia server
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
                this.ui.showNotification('Could not connect to server. Running in offline mode.', 'warning');

                // Start in offline/demo mode
                this.showScreen('game');
                this.gameState.inGame = true;
                this.startGameLoop();

                this.ui.addTextOutput('=== OFFLINE DEMO MODE ===', 'system');
                this.ui.addTextOutput(`Welcome ${this.gameState.character.name}, the ${this.gameState.character.class}!`, 'narrative');
                this.ui.addTextOutput('You stand at the edge of the Desert Wilderness.', 'narrative');
                this.ui.addTextOutput('Ancient sands stretch before you, endless and mysterious.', 'narrative');
                this.ui.addTextOutput('(Server not running - this is a demo. Start Evennia server to play online)', 'system');
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
            this.ui.addTextOutput(data.text, 'narrative');
        } else if (data.type === 'error') {
            this.ui.addTextOutput(data.text, 'system');
        }
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
