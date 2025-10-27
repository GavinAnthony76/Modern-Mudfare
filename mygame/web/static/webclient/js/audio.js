/**
 * Audio Manager - Handle music and sound effects
 * Uses Web Audio API and HTML5 Audio elements
 */

class AudioManager {
  constructor() {
    this.bgMusic = new Audio();
    this.sfxPool = [];
    this.masterVolume = 0.7;
    this.musicVolume = 0.5;
    this.sfxVolume = 0.7;
    this.audioContext = this.initAudioContext();

    // Preload placeholder sound
    this.initPlaceholderSounds();
  }

  /**
   * Initialize Web Audio API context
   */
  initAudioContext() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      return new AudioContext();
    } catch (e) {
      console.log('Web Audio API not supported');
      return null;
    }
  }

  /**
   * Initialize placeholder sounds using Web Audio API
   */
  initPlaceholderSounds() {
    this.sounds = {
      footstep: () => this.generateTone(200, 0.1),
      success: () => this.generateTone(800, 0.2),
      error: () => this.generateTone(300, 0.2),
      ambient: () => this.generateAmbientSound(),
      combat_hit: () => this.generateTone(500, 0.15),
      divine_light: () => this.generateTone(1200, 0.3)
    };
  }

  /**
   * Generate simple tone using Web Audio API
   */
  generateTone(frequency, duration) {
    if (!this.audioContext) return null;

    const ctx = this.audioContext;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.frequency.value = frequency;
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + duration);

    return {
      frequency: frequency,
      duration: duration
    };
  }

  /**
   * Generate ambient sound
   */
  generateAmbientSound() {
    if (!this.audioContext) return null;

    const ctx = this.audioContext;
    const bufferSize = ctx.sampleRate * 2;
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const output = buffer.getChannelData(0);

    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }

    return buffer;
  }

  /**
   * Play background music
   */
  playMusic(musicKey, loop = true) {
    const bgAudioUrl = `assets/audio/music/${musicKey}.mp3`;

    // For demo, create a simple generated music or use silence
    if (!this.bgMusic.src) {
      this.bgMusic.src = 'data:audio/wav;base64,UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAA=='; // Silent audio
      this.bgMusic.loop = loop;
      this.bgMusic.volume = this.musicVolume * this.masterVolume;

      try {
        this.bgMusic.play().catch(e => console.log('Music playback prevented:', e));
      } catch (e) {
        console.log('Music playback error:', e);
      }
    }
  }

  /**
   * Stop background music
   */
  stopMusic() {
    this.bgMusic.pause();
    this.bgMusic.currentTime = 0;
  }

  /**
   * Play sound effect (from file or generated)
   */
  playSFX(soundKey) {
    // Try to load actual audio file first (for real assets like footstep_wood)
    const audioPath = `assets/audio/sfx/${soundKey}.mp3`;
    const audio = new Audio();
    audio.src = audioPath;
    audio.volume = this.sfxVolume * this.masterVolume;

    audio.play().catch(e => {
      // Fallback to generated sounds if file doesn't exist
      if (this.sounds[soundKey] && this.audioContext) {
        try {
          const sound = this.sounds[soundKey]();
          if (sound) {
            const gain = this.audioContext.createGain();
            gain.gain.value = this.sfxVolume * this.masterVolume;
            gain.connect(this.audioContext.destination);
          }
        } catch (err) {
          console.log('SFX playback error:', err);
        }
      }
    });
  }

  /**
   * Play multiple overlapping sounds
   */
  playMultipleSFX(soundKeys) {
    soundKeys.forEach(key => {
      setTimeout(() => this.playSFX(key), Math.random() * 500);
    });
  }

  /**
   * Set master volume (0.0 - 1.0)
   */
  setMasterVolume(value) {
    this.masterVolume = Math.max(0, Math.min(1, value));
    this.bgMusic.volume = this.musicVolume * this.masterVolume;
  }

  /**
   * Set music volume (0.0 - 1.0)
   */
  setMusicVolume(value) {
    this.musicVolume = Math.max(0, Math.min(1, value));
    this.bgMusic.volume = this.musicVolume * this.masterVolume;
  }

  /**
   * Set SFX volume (0.0 - 1.0)
   */
  setSFXVolume(value) {
    this.sfxVolume = Math.max(0, Math.min(1, value));
  }

  /**
   * Mute all audio
   */
  mute() {
    this.bgMusic.volume = 0;
  }

  /**
   * Unmute audio
   */
  unmute() {
    this.bgMusic.volume = this.musicVolume * this.masterVolume;
  }

  /**
   * Play music based on game state
   */
  playStateMusic(state) {
    switch (state) {
      case 'exploration':
        this.playMusic('exploration_peaceful');
        break;
      case 'combat':
        this.playMusic('combat_intense');
        break;
      case 'temple':
        this.playMusic('sacred_temple');
        break;
      case 'boss':
        this.playMusic('boss_battle');
        break;
      default:
        this.playMusic('ambient');
    }
  }

  /**
   * Play combat sequence sounds
   */
  playCombatSequence() {
    this.playSFX('combat_hit');
    setTimeout(() => this.playSFX('success'), 200);
  }

  /**
   * Play divine intervention effect
   */
  playDivineEffect() {
    this.playSFX('divine_light');
  }

  /**
   * Cleanup resources
   */
  destroy() {
    this.stopMusic();
    if (this.audioContext) {
      this.audioContext.close();
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AudioManager;
}
