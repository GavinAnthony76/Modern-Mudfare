/**
 * Game Renderer - Handles HTML5 Canvas rendering
 * Renders game world, characters, and sprites
 */

class GameRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;

        if (!this.ctx) {
            console.error('Failed to get canvas context');
            return;
        }

        this.width = 800;
        this.height = 600;
        this.tileSize = 32;

        // Camera
        this.camera = {
            x: 0,
            y: 0
        };

        // Player sprite position (center of view)
        this.player = {
            x: this.width / 2,
            y: this.height / 2,
            sprite: null
        };

        // Sprites and assets
        this.sprites = {};
        this.tiles = {};
        this.loaded = false;

        this.init();
    }

    init() {
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());

        // Load placeholder graphics
        this.loadPlaceholderGraphics();

        console.log('Renderer initialized');
    }

    resizeCanvas() {
        if (!this.canvas) return;

        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
        this.width = this.canvas.width;
        this.height = this.canvas.height;
    }

    loadPlaceholderGraphics() {
        // Create simple placeholder graphics using canvas
        // In production, would load actual sprite images

        // Player sprite
        this.player.sprite = this.createPlaceholderSprite(this.tileSize, this.tileSize, '#4169e1');

        // Ground tiles
        this.tiles.desert = this.createPlaceholderSprite(this.tileSize, this.tileSize, '#f4a460');
        this.tiles.grass = this.createPlaceholderSprite(this.tileSize, this.tileSize, '#90ee90');
        this.tiles.stone = this.createPlaceholderSprite(this.tileSize, this.tileSize, '#808080');

        this.loaded = true;
    }

    createPlaceholderSprite(width, height, color) {
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = color;
        ctx.fillRect(0, 0, width, height);

        // Add border
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.strokeRect(0, 0, width, height);

        return canvas;
    }

    render() {
        if (!this.ctx || !this.loaded) return;

        // Clear canvas
        this.ctx.fillStyle = '#1a1410';
        this.ctx.fillRect(0, 0, this.width, this.height);

        // Render ground tiles
        this.renderTiles();

        // Render player
        this.renderPlayer();

        // Render grid (for debugging)
        if (window.DEBUG) {
            this.renderGrid();
        }
    }

    renderTiles() {
        const tilesX = Math.ceil(this.width / this.tileSize) + 1;
        const tilesY = Math.ceil(this.height / this.tileSize) + 1;

        const startX = Math.floor(this.camera.x / this.tileSize);
        const startY = Math.floor(this.camera.y / this.tileSize);

        for (let y = 0; y < tilesY; y++) {
            for (let x = 0; x < tilesX; x++) {
                const tileX = (x - startX) * this.tileSize;
                const tileY = (y - startY) * this.tileSize;

                // Use desert tile as default
                const tile = this.tiles.desert;
                if (tile) {
                    this.ctx.drawImage(tile, tileX, tileY);
                }
            }
        }
    }

    renderPlayer() {
        if (this.player.sprite) {
            this.ctx.drawImage(
                this.player.sprite,
                this.player.x - this.tileSize / 2,
                this.player.y - this.tileSize / 2
            );
        }

        // Draw player name above sprite
        this.ctx.fillStyle = '#d4af37';
        this.ctx.font = '12px Georgia';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(
            'You',
            this.player.x,
            this.player.y - this.tileSize
        );
    }

    renderGrid() {
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;

        // Vertical lines
        for (let x = 0; x < this.width; x += this.tileSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.height);
            this.ctx.stroke();
        }

        // Horizontal lines
        for (let y = 0; y < this.height; y += this.tileSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.width, y);
            this.ctx.stroke();
        }
    }

    moveCamera(dx, dy) {
        this.camera.x += dx;
        this.camera.y += dy;
    }

    centerCameraOn(x, y) {
        this.camera.x = x - this.width / 2;
        this.camera.y = y - this.height / 2;
    }

    loadSprite(name, url) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.sprites[name] = img;
                resolve(img);
            };
            img.onerror = reject;
            img.src = url;
        });
    }

    drawSprite(spriteName, x, y, width, height) {
        const sprite = this.sprites[spriteName];
        if (sprite) {
            this.ctx.drawImage(sprite, x, y, width || sprite.width, height || sprite.height);
        }
    }
}
