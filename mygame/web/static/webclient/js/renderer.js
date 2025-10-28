/**
 * Game Renderer - HTML5 Canvas Graphics Engine
 * Handles sprite rendering, animations, and viewport management
 */

class GameRenderer {
  constructor(canvasId, width = 800, height = 600) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.width = width;
    this.height = height;
    this.canvas.width = width;
    this.canvas.height = height;

    // Sprite management
    this.sprites = new Map();
    this.animations = new Map();
    this.camera = { x: 0, y: 0 };
    this.scale = 1;

    // Grid settings for tile-based rendering
    this.tileSize = 32;
    this.gridWidth = Math.ceil(width / this.tileSize);
    this.gridHeight = Math.ceil(height / this.tileSize);

    // Game objects to render
    this.gameObjects = [];
    this.particles = [];
  }

  /**
   * Load or create placeholder sprite
   */
  loadSprite(key, data) {
    if (data.type === 'placeholder') {
      this.sprites.set(key, this.createPlaceholderSprite(data));
    } else if (data.type === 'spritesheet') {
      this.sprites.set(key, {
        image: data.image,
        frameWidth: data.frameWidth,
        frameHeight: data.frameHeight,
        columns: data.columns,
        frames: data.frames
      });
    }
  }

  /**
   * Generate SVG placeholder sprite
   */
  createPlaceholderSprite(data) {
    const width = data.width || 32;
    const height = data.height || 32;
    const color = data.color || '#4CAF50';
    const shape = data.shape || 'rect';

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    if (shape === 'rect') {
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('width', width);
      rect.setAttribute('height', height);
      rect.setAttribute('fill', color);
      rect.setAttribute('stroke', '#333');
      rect.setAttribute('stroke-width', '2');
      svg.appendChild(rect);
    } else if (shape === 'circle') {
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', width / 2);
      circle.setAttribute('cy', height / 2);
      circle.setAttribute('r', width / 2 - 2);
      circle.setAttribute('fill', color);
      circle.setAttribute('stroke', '#333');
      circle.setAttribute('stroke-width', '2');
      svg.appendChild(circle);
    } else if (shape === 'character') {
      // Simple character shape
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');

      // Head
      const head = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      head.setAttribute('cx', width / 2);
      head.setAttribute('cy', width / 4);
      head.setAttribute('r', width / 6);
      head.setAttribute('fill', color);
      head.setAttribute('stroke', '#333');
      head.setAttribute('stroke-width', '1');
      g.appendChild(head);

      // Body
      const body = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      body.setAttribute('x', width / 4);
      body.setAttribute('y', width / 3);
      body.setAttribute('width', width / 2);
      body.setAttribute('height', width / 3);
      body.setAttribute('fill', color);
      body.setAttribute('stroke', '#333');
      body.setAttribute('stroke-width', '1');
      g.appendChild(body);

      // Legs
      const leg1 = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      leg1.setAttribute('x', width / 3);
      leg1.setAttribute('y', (2 * width) / 3);
      leg1.setAttribute('width', width / 8);
      leg1.setAttribute('height', width / 3);
      leg1.setAttribute('fill', color);
      leg1.setAttribute('stroke', '#333');
      leg1.setAttribute('stroke-width', '1');
      g.appendChild(leg1);

      const leg2 = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      leg2.setAttribute('x', (5 * width) / 12);
      leg2.setAttribute('y', (2 * width) / 3);
      leg2.setAttribute('width', width / 8);
      leg2.setAttribute('height', width / 3);
      leg2.setAttribute('fill', color);
      leg2.setAttribute('stroke', '#333');
      leg2.setAttribute('stroke-width', '1');
      g.appendChild(leg2);

      svg.appendChild(g);
    }

    // Convert SVG to canvas image
    const svgString = new XMLSerializer().serializeToString(svg);
    const img = new Image();
    img.src = 'data:image/svg+xml;base64,' + btoa(svgString);

    return {
      image: img,
      width: width,
      height: height,
      type: 'placeholder'
    };
  }

  /**
   * Register placeholder assets for common game objects
   */
  registerPlaceholderAssets() {
    // Character sprites
    this.loadSprite('player', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#2196F3',
      shape: 'character'
    });

    // NPC sprites
    this.loadSprite('npc_elder', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#FF9800',
      shape: 'character'
    });

    this.loadSprite('npc_priest', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#9C27B0',
      shape: 'character'
    });

    this.loadSprite('npc_merchant', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#FFC107',
      shape: 'character'
    });

    // Enemy sprites
    this.loadSprite('deceiver', {
      type: 'placeholder',
      width: 48,
      height: 48,
      color: '#F44336',
      shape: 'circle'
    });

    this.loadSprite('demon', {
      type: 'placeholder',
      width: 40,
      height: 40,
      color: '#8B0000',
      shape: 'circle'
    });

    // Tile sprites
    this.loadSprite('floor_stone', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#BDBDBD',
      shape: 'rect'
    });

    this.loadSprite('floor_grass', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#4CAF50',
      shape: 'rect'
    });

    this.loadSprite('floor_sand', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#DEB887',
      shape: 'rect'
    });

    this.loadSprite('wall', {
      type: 'placeholder',
      width: 32,
      height: 32,
      color: '#795548',
      shape: 'rect'
    });

    // Item sprites
    this.loadSprite('item_generic', {
      type: 'placeholder',
      width: 16,
      height: 16,
      color: '#FFD700',
      shape: 'circle'
    });

    this.loadSprite('item_weapon', {
      type: 'placeholder',
      width: 16,
      height: 16,
      color: '#C0C0C0',
      shape: 'rect'
    });
  }

  /**
   * Add game object to render queue
   */
  addObject(obj) {
    this.gameObjects.push(obj);
  }

  /**
   * Remove game object from render queue
   */
  removeObject(obj) {
    const index = this.gameObjects.indexOf(obj);
    if (index > -1) {
      this.gameObjects.splice(index, 1);
    }
  }

  /**
   * Update camera position (follow player)
   */
  updateCamera(targetX, targetY) {
    this.camera.x = targetX - this.width / 2;
    this.camera.y = targetY - this.height / 2;
  }

  /**
   * Add particle effect
   */
  addParticle(x, y, color = '#FFD700', duration = 1000) {
    this.particles.push({
      x: x,
      y: y,
      color: color,
      startTime: Date.now(),
      duration: duration,
      vx: (Math.random() - 0.5) * 100,
      vy: (Math.random() - 0.5) * 100 - 50
    });
  }

  /**
   * Render single frame
   */
  render(gameState = {}) {
    // Clear canvas
    this.ctx.fillStyle = '#1a1a1a';
    this.ctx.fillRect(0, 0, this.width, this.height);

    // Draw background grid pattern
    this.drawGrid();

    // Save context for camera transforms
    this.ctx.save();
    this.ctx.translate(-this.camera.x, -this.camera.y);

    // Draw game objects
    this.gameObjects.sort((a, b) => (a.y || 0) - (b.y || 0)); // Sort by Y for proper depth

    // Debug: Log object count on first render
    if (!this.debugLogged) {
      console.log(`Rendering ${this.gameObjects.length} game objects`);
      this.gameObjects.forEach(obj => {
        console.log(`  - ${obj.label || obj.id}: ${obj.type} at (${obj.x}, ${obj.y}), sprite: ${obj.sprite}, visible: ${obj.visible}`);
      });
      this.debugLogged = true;
    }

    this.gameObjects.forEach(obj => this.renderObject(obj));

    // Draw particles
    this.particles = this.particles.filter(p => {
      const elapsed = Date.now() - p.startTime;
      if (elapsed > p.duration) return false;
      this.renderParticle(p, elapsed);
      return true;
    });

    this.ctx.restore();

    // Draw UI overlays (not affected by camera)
    this.drawUI(gameState);
  }

  /**
   * Render individual game object
   */
  renderObject(obj) {
    if (!obj.visible) return;

    const x = obj.x || 0;
    const y = obj.y || 0;
    const spriteKey = obj.sprite || 'item_generic';
    const sprite = this.sprites.get(spriteKey);

    if (!sprite) return;

    if (obj.isAnimated && this.animations.has(spriteKey)) {
      this.renderAnimatedSprite(sprite, x, y, spriteKey);
    } else {
      this.renderSprite(sprite, x, y);
    }

    // Draw health bar for characters
    if (obj.health !== undefined && obj.maxHealth !== undefined) {
      this.drawHealthBar(x, y - 10, obj.health, obj.maxHealth);
    }

    // Draw label
    if (obj.label) {
      this.drawLabel(x, y - 20, obj.label);
    }
  }

  /**
   * Render sprite to canvas
   */
  renderSprite(sprite, x, y) {
    if (!sprite) return;

    const width = sprite.width || 32;
    const height = sprite.height || 32;

    // For placeholder sprites, draw as colored geometric shapes
    if (sprite.type === 'placeholder') {
      this.drawPlaceholderSprite(sprite, x, y, width, height);
      return;
    }

    // For regular images, try to draw the image
    if (sprite.image && sprite.image.complete && sprite.image.naturalHeight > 0) {
      try {
        // Use sprite dimensions if available, otherwise use defaults
        const displayWidth = sprite.width || width || 32;
        const displayHeight = sprite.height || height || 32;
        this.ctx.drawImage(sprite.image, x, y, displayWidth, displayHeight);
        return;
      } catch (e) {
        console.log('Error drawing image:', e);
      }
    }

    // Fallback: draw as colored rectangle
    this.ctx.fillStyle = sprite.color || '#999';
    this.ctx.fillRect(x, y, width, height);
    this.ctx.strokeStyle = '#666';
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(x, y, width, height);
  }

  /**
   * Draw placeholder sprite as geometric shape
   */
  drawPlaceholderSprite(sprite, x, y, width, height) {
    const color = sprite.color || '#999';
    const shape = sprite.shape || 'rect';

    this.ctx.fillStyle = color;
    this.ctx.strokeStyle = '#333';
    this.ctx.lineWidth = 2;

    if (shape === 'rect') {
      this.ctx.fillRect(x, y, width, height);
      this.ctx.strokeRect(x, y, width, height);
    } else if (shape === 'circle') {
      this.ctx.beginPath();
      this.ctx.arc(x + width / 2, y + height / 2, Math.max(width, height) / 2 - 1, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.stroke();
    } else if (shape === 'character') {
      // Draw simple character: head, body, legs
      const scale = width / 32;

      // Head
      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.arc(x + width / 2, y + 8 * scale, 4 * scale, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.stroke();

      // Body
      this.ctx.fillRect(x + 8 * scale, y + 12 * scale, 16 * scale, 10 * scale);
      this.ctx.strokeRect(x + 8 * scale, y + 12 * scale, 16 * scale, 10 * scale);

      // Legs
      this.ctx.fillRect(x + 10 * scale, y + 22 * scale, 4 * scale, 8 * scale);
      this.ctx.strokeRect(x + 10 * scale, y + 22 * scale, 4 * scale, 8 * scale);
      this.ctx.fillRect(x + 18 * scale, y + 22 * scale, 4 * scale, 8 * scale);
      this.ctx.strokeRect(x + 18 * scale, y + 22 * scale, 4 * scale, 8 * scale);
    }
  }

  /**
   * Render animated sprite
   */
  renderAnimatedSprite(sprite, x, y, key) {
    const anim = this.animations.get(key);
    if (!anim) return;

    const frame = anim.currentFrame;
    const frameWidth = sprite.frameWidth || 32;
    const frameHeight = sprite.frameHeight || 32;
    const col = frame % sprite.columns;
    const row = Math.floor(frame / sprite.columns);

    this.ctx.drawImage(
      sprite.image,
      col * frameWidth,
      row * frameHeight,
      frameWidth,
      frameHeight,
      x,
      y,
      frameWidth,
      frameHeight
    );
  }

  /**
   * Render particle effect
   */
  renderParticle(particle, elapsed) {
    const progress = elapsed / particle.duration;
    const alpha = 1 - progress;
    const x = particle.x + particle.vx * progress;
    const y = particle.y + particle.vy * progress;

    this.ctx.save();
    this.ctx.globalAlpha = alpha;
    this.ctx.fillStyle = particle.color;
    this.ctx.fillRect(x, y, 4, 4);
    this.ctx.restore();
  }

  /**
   * Draw health bar above object
   */
  drawHealthBar(x, y, health, maxHealth) {
    const barWidth = 30;
    const barHeight = 4;
    const percentage = Math.max(0, health / maxHealth);

    // Background
    this.ctx.fillStyle = '#333';
    this.ctx.fillRect(x - barWidth / 2, y, barWidth, barHeight);

    // Health
    this.ctx.fillStyle = percentage > 0.5 ? '#4CAF50' : percentage > 0.25 ? '#FFC107' : '#F44336';
    this.ctx.fillRect(x - barWidth / 2, y, barWidth * percentage, barHeight);

    // Border
    this.ctx.strokeStyle = '#666';
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(x - barWidth / 2, y, barWidth, barHeight);
  }

  /**
   * Draw label above object
   */
  drawLabel(x, y, text) {
    this.ctx.save();
    this.ctx.font = '10px Arial';
    this.ctx.fillStyle = '#FFF';
    this.ctx.textAlign = 'center';
    this.ctx.fillText(text, x + 16, y);
    this.ctx.restore();
  }

  /**
   * Draw background grid
   */
  drawGrid() {
    const gridSize = this.tileSize;
    this.ctx.strokeStyle = '#333';
    this.ctx.lineWidth = 0.5;

    for (let x = -this.camera.x; x < this.width - this.camera.x; x += gridSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.height);
      this.ctx.stroke();
    }

    for (let y = -this.camera.y; y < this.height - this.camera.y; y += gridSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.width, y);
      this.ctx.stroke();
    }
  }

  /**
   * Draw UI overlay
   */
  drawUI(gameState) {
    const margin = 10;
    const lineHeight = 20;
    let yPos = margin;

    this.ctx.save();
    this.ctx.font = '12px Arial';
    this.ctx.fillStyle = '#FFF';

    // Game title
    this.ctx.font = 'bold 16px Arial';
    this.ctx.fillText('Journey Through Scripture', margin, yPos);
    yPos += lineHeight + 5;

    // Game state info
    this.ctx.font = '12px Arial';
    if (gameState.playerName) {
      this.ctx.fillText(`Player: ${gameState.playerName}`, margin, yPos);
      yPos += lineHeight;
    }

    if (gameState.location) {
      this.ctx.fillText(`Location: ${gameState.location}`, margin, yPos);
      yPos += lineHeight;
    }

    if (gameState.status) {
      this.ctx.fillText(`Status: ${gameState.status}`, margin, yPos);
    }

    this.ctx.restore();
  }

  /**
   * Resize canvas for responsive design
   */
  resize(width, height) {
    this.width = width;
    this.height = height;
    this.canvas.width = width;
    this.canvas.height = height;
    this.gridWidth = Math.ceil(width / this.tileSize);
    this.gridHeight = Math.ceil(height / this.tileSize);
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GameRenderer;
}
