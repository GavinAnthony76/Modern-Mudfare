/**
 * Audio Manager - Handles music and sound effects
 * Uses Web Audio API for sound effects and HTML5 Audio for music
 */

class AudioManager {
    constructor() {
        this.initialized = false;
        this.musicEnabled = true;
        this.sfxEnabled = true;
        this.musicVolume = 0.5;
        this.sfxVolume = 0.7;

        this.currentMusic = null;
        this.audioContext = null;
        this.sfxBuffers = {};

        // Music tracks
        this.musicTracks = {
            menu: 'assets/audio/music/menu-theme.mp3',
            exploration: 'assets/audio/music/exploration.mp3',
            combat: 'assets/audio/music/combat.mp3',
            victory: 'assets/audio/music/victory.mp3',
            sacred: 'assets/audio/music/sacred-place.mp3'
        };

        // Sound effects
        this.sfxFiles = {
            click: 'assets/audio/sfx/click.mp3',
            footstep: 'assets/audio/sfx/footstep.mp3',
            sword: 'assets/audio/sfx/sword-swing.mp3',
            hit: 'assets/audio/sfx/hit.mp3',
            heal: 'assets/audio/sfx/heal.mp3',
            divine: 'assets/audio/sfx/divine-intervention.mp3'
        };
    }

    init() {
        // Audio context requires user interaction to start
        // This should be called after a user click/touch event
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.initialized = true;
            console.log('Audio Manager initialized');
        } catch (e) {
            console.warn('Web Audio API not supported:', e);
        }

        // Load saved preferences
        this.loadPreferences();
    }

    playMusic(trackName, loop = true) {
        if (!this.musicEnabled || !this.musicTracks[trackName]) {
            return;
        }

        // Stop current music if playing
        if (this.currentMusic) {
            this.currentMusic.pause();
            this.currentMusic.currentTime = 0;
        }

        // Create new audio element
        this.currentMusic = new Audio(this.musicTracks[trackName]);
        this.currentMusic.volume = this.musicVolume;
        this.currentMusic.loop = loop;

        // Play (may fail without user interaction)
        const playPromise = this.currentMusic.play();
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.warn('Music playback failed:', error);
            });
        }

        console.log(`Playing music: ${trackName}`);
    }

    stopMusic() {
        if (this.currentMusic) {
            this.currentMusic.pause();
            this.currentMusic.currentTime = 0;
        }
    }

    fadeOutMusic(duration = 1000) {
        if (!this.currentMusic) return;

        const startVolume = this.currentMusic.volume;
        const fadeStep = startVolume / (duration / 50);

        const fadeInterval = setInterval(() => {
            if (this.currentMusic.volume > fadeStep) {
                this.currentMusic.volume -= fadeStep;
            } else {
                this.currentMusic.volume = 0;
                this.stopMusic();
                clearInterval(fadeInterval);
            }
        }, 50);
    }

    playSFX(sfxName) {
        if (!this.sfxEnabled || !this.initialized) {
            return;
        }

        // Simple implementation using Audio elements
        // In production, would use Web Audio API for better performance
        const sfx = new Audio(this.sfxFiles[sfxName]);
        sfx.volume = this.sfxVolume;

        const playPromise = sfx.play();
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.warn(`SFX playback failed (${sfxName}):`, error);
            });
        }
    }

    setMusicVolume(volume) {
        this.musicVolume = Math.max(0, Math.min(1, volume));
        if (this.currentMusic) {
            this.currentMusic.volume = this.musicVolume;
        }
        this.savePreferences();
    }

    setSFXVolume(volume) {
        this.sfxVolume = Math.max(0, Math.min(1, volume));
        this.savePreferences();
    }

    toggleMusic() {
        this.musicEnabled = !this.musicEnabled;
        if (!this.musicEnabled) {
            this.stopMusic();
        }
        this.savePreferences();
        return this.musicEnabled;
    }

    toggleSFX() {
        this.sfxEnabled = !this.sfxEnabled;
        this.savePreferences();
        return this.sfxEnabled;
    }

    loadPreferences() {
        const prefs = localStorage.getItem('audioPreferences');
        if (prefs) {
            const parsed = JSON.parse(prefs);
            this.musicEnabled = parsed.musicEnabled ?? true;
            this.sfxEnabled = parsed.sfxEnabled ?? true;
            this.musicVolume = parsed.musicVolume ?? 0.5;
            this.sfxVolume = parsed.sfxVolume ?? 0.7;
        }
    }

    savePreferences() {
        localStorage.setItem('audioPreferences', JSON.stringify({
            musicEnabled: this.musicEnabled,
            sfxEnabled: this.sfxEnabled,
            musicVolume: this.musicVolume,
            sfxVolume: this.sfxVolume
        }));
    }
}
