/**
 * Combat System - Turn-based combat engine
 */

class Combat {
  constructor(player, enemy) {
    this.player = player;
    this.enemy = enemy;
    this.combatActive = true;
    this.currentTurn = this.determineTurn();
    this.log = [];
    this.round = 0;
  }

  /**
   * Determine who goes first based on wisdom
   */
  determineTurn() {
    const playerWisdom = this.player.getStat('wisdom') + Math.random() * 10;
    const enemyWisdom = this.enemy.getStat('wisdom') + Math.random() * 10;

    return playerWisdom >= enemyWisdom ? 'player' : 'enemy';
  }

  /**
   * Player attacks
   */
  playerAttack() {
    if (this.currentTurn !== 'player') return;

    const damage = this.calculateDamage(this.player, this.enemy);
    const actualDamage = this.enemy.takeDamage(damage);
    const isCritical = Math.random() < this.calculateCritChance(this.player);

    const message = isCritical
      ? `${this.player.name} lands a CRITICAL HIT for ${actualDamage} damage!`
      : `${this.player.name} attacks for ${actualDamage} damage!`;

    this.log.push(message);
    console.log(message);

    if (!this.enemy.isAlive()) {
      this.endCombat('player');
    } else {
      this.currentTurn = 'enemy';
    }
  }

  /**
   * Player casts spell (uses mana)
   */
  playerCastSpell(spellName) {
    if (this.currentTurn !== 'player') return;

    const spells = {
      heal: {
        cost: 20,
        effect: () => {
          const healed = this.player.heal(30);
          this.log.push(`${this.player.name} casts Heal, restoring ${healed} health!`);
          return healed;
        }
      },
      smite: {
        cost: 25,
        effect: () => {
          const damage = this.calculateDamage(this.player, this.enemy, 15);
          const actualDamage = this.enemy.takeDamage(damage);
          this.log.push(`${this.player.name} casts Smite for ${actualDamage} damage!`);
          return actualDamage;
        }
      },
      shield: {
        cost: 15,
        effect: () => {
          this.player.bonusStats.faith = (this.player.bonusStats.faith || 0) + 2;
          this.log.push(`${this.player.name} casts Shield, increasing defense!`);
          return 0;
        }
      }
    };

    const spell = spells[spellName];
    if (!spell) {
      this.log.push(`Unknown spell: ${spellName}`);
      return;
    }

    if (this.player.mana < spell.cost) {
      this.log.push(`Not enough mana! (need ${spell.cost}, have ${this.player.mana})`);
      return;
    }

    this.player.mana -= spell.cost;
    spell.effect();

    if (!this.enemy.isAlive()) {
      this.endCombat('player');
    } else {
      this.currentTurn = 'enemy';
    }
  }

  /**
   * Enemy attacks
   */
  enemyAttack() {
    if (this.currentTurn !== 'enemy') return;

    const damage = this.calculateDamage(this.enemy, this.player);
    const actualDamage = this.player.takeDamage(damage);

    const message = `${this.enemy.label || 'Enemy'} attacks for ${actualDamage} damage!`;
    this.log.push(message);
    console.log(message);

    if (!this.player.isAlive()) {
      this.endCombat('enemy');
    } else {
      this.currentTurn = 'player';
    }
  }

  /**
   * Calculate damage
   */
  calculateDamage(attacker, defender, bonusDamage = 0) {
    const baseDamage = attacker.calculateDamage(bonusDamage);
    const defense = defender.calculateDefense();
    const actualDamage = Math.max(1, baseDamage - defense);

    return actualDamage;
  }

  /**
   * Calculate critical chance
   */
  calculateCritChance(attacker) {
    const wisdom = attacker.getStat('wisdom');
    return Math.min(0.5, wisdom * 0.05); // Max 50% crit chance
  }

  /**
   * End combat
   */
  endCombat(winner) {
    this.combatActive = false;

    if (winner === 'player') {
      const xpReward = this.enemy.xpReward || 50;
      const goldReward = this.enemy.goldReward || 25;

      this.player.gainXP(xpReward);
      this.log.push(`Victory! Gained ${xpReward} XP and ${goldReward} gold!`);
    } else {
      this.log.push(`Defeat! You have been defeated...`);
      this.player.reset();
    }
  }

  /**
   * Get combat status
   */
  getStatus() {
    return {
      playerHealth: this.player.health,
      playerMaxHealth: this.player.maxHealth,
      playerMana: this.player.mana,
      playerMaxMana: this.player.maxMana,
      enemyHealth: this.enemy.health,
      enemyMaxHealth: this.enemy.maxHealth,
      enemyLabel: this.enemy.label || 'Enemy',
      currentTurn: this.currentTurn,
      log: this.log,
      combatActive: this.combatActive
    };
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Combat;
}
