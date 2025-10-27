/**
 * Character System - Handle player stats, health, progression
 * Implements biblical character classes and stat systems
 */

// Character class definitions
const CHARACTER_CLASSES = {
  prophet: {
    name: 'Prophet',
    description: 'Divine caster, healer, buffer',
    stats: {
      faith: 5,
      wisdom: 5,
      strength: 2,
      courage: 3,
      righteousness: 4
    },
    health: 80,
    mana: 80,
    startingEquipment: ['staff_of_moses', 'simple_robe', 'scroll_wisdom']
  },
  warrior: {
    name: 'Warrior',
    description: 'Melee fighter, tank, protector',
    stats: {
      faith: 3,
      wisdom: 2,
      strength: 5,
      courage: 5,
      righteousness: 4
    },
    health: 120,
    mana: 40,
    startingEquipment: ['bronze_sword', 'leather_armor', 'shield']
  },
  shepherd: {
    name: 'Shepherd',
    description: 'Balanced support, leader, versatile',
    stats: {
      faith: 4,
      wisdom: 4,
      strength: 4,
      courage: 4,
      righteousness: 4
    },
    health: 100,
    mana: 60,
    startingEquipment: ['staff', 'sling', 'shepherds_cloak']
  },
  scribe: {
    name: 'Scribe',
    description: 'Knowledge-based, strategic, spell variety',
    stats: {
      faith: 4,
      wisdom: 5,
      strength: 2,
      courage: 3,
      righteousness: 5
    },
    health: 70,
    mana: 100,
    startingEquipment: ['quill', 'tome', 'scholars_robe']
  }
};

/**
 * Character class - represents player character
 */
class Character {
  constructor(name, classType = 'prophet') {
    this.name = name;
    this.classType = classType;

    // Get class definition
    const classDef = CHARACTER_CLASSES[classType];
    if (!classDef) {
      throw new Error(`Invalid character class: ${classType}`);
    }

    // Base stats from class
    this.baseStats = { ...classDef.stats };
    this.bonusStats = {
      faith: 0,
      wisdom: 0,
      strength: 0,
      courage: 0,
      righteousness: 0
    };

    // Health and resources
    this.maxHealth = classDef.health;
    this.health = classDef.health;
    this.maxMana = classDef.mana;
    this.mana = classDef.mana;

    // Progression
    this.level = 1;
    this.xp = 0;
    this.xpToLevel = 100;
    this.skillPoints = 0;

    // Calling (chosen after defeating The Deceiver)
    this.calling = null;

    // Inventory
    this.inventory = [];
    this.equipped = {
      weapon: null,
      armor: null,
      shield: null,
      accessory: null
    };

    // Combat stats
    this.armor = 0;
    this.damageBonus = 0;

    // Quest tracking
    this.completedQuests = [];
    this.activeQuests = [];
    this.defeatedEnemies = [];

    // Dialogue state
    this.npcMemory = {}; // Remember interactions with NPCs

    // Cosmetics
    this.sprite = 'player';
  }

  /**
   * Get effective stat (base + bonuses from equipment/buffs)
   */
  getStat(statName) {
    return (this.baseStats[statName] || 0) + (this.bonusStats[statName] || 0);
  }

  /**
   * Calculate total stats including equipment bonuses
   */
  calculateTotalStats() {
    const total = { ...this.baseStats };

    // Add equipment bonuses
    if (this.equipped.weapon && this.equipped.weapon.statBonuses) {
      Object.keys(this.equipped.weapon.statBonuses).forEach(stat => {
        total[stat] = (total[stat] || 0) + this.equipped.weapon.statBonuses[stat];
      });
    }

    if (this.equipped.armor && this.equipped.armor.statBonuses) {
      Object.keys(this.equipped.armor.statBonuses).forEach(stat => {
        total[stat] = (total[stat] || 0) + this.equipped.armor.statBonuses[stat];
      });
    }

    if (this.equipped.shield && this.equipped.shield.statBonuses) {
      Object.keys(this.equipped.shield.statBonuses).forEach(stat => {
        total[stat] = (total[stat] || 0) + this.equipped.shield.statBonuses[stat];
      });
    }

    if (this.equipped.accessory && this.equipped.accessory.statBonuses) {
      Object.keys(this.equipped.accessory.statBonuses).forEach(stat => {
        total[stat] = (total[stat] || 0) + this.equipped.accessory.statBonuses[stat];
      });
    }

    // Add bonus stats (from buffs, etc)
    Object.keys(this.bonusStats).forEach(stat => {
      total[stat] = (total[stat] || 0) + this.bonusStats[stat];
    });

    return total;
  }

  /**
   * Take damage
   */
  takeDamage(amount) {
    const totalStats = this.calculateTotalStats();
    const mitigation = Math.floor(totalStats.faith * 0.5); // Faith reduces damage
    const actualDamage = Math.max(1, amount - mitigation);
    this.health = Math.max(0, this.health - actualDamage);
    return actualDamage;
  }

  /**
   * Heal
   */
  heal(amount) {
    const oldHealth = this.health;
    this.health = Math.min(this.maxHealth, this.health + amount);
    return this.health - oldHealth;
  }

  /**
   * Gain XP and check for level up
   */
  gainXP(amount) {
    this.xp += amount;

    while (this.xp >= this.xpToLevel) {
      this.levelUp();
    }
  }

  /**
   * Level up
   */
  levelUp() {
    this.level++;
    this.xp -= this.xpToLevel;
    this.xpToLevel = Math.floor(this.xpToLevel * 1.1); // Increase XP requirement
    this.skillPoints += 3; // Gain skill points

    // Increase health and mana on level up
    this.maxHealth += 10;
    this.health = this.maxHealth;
    this.maxMana += 5;
    this.mana = this.maxMana;

    console.log(`Level Up! You are now level ${this.level}`);
  }

  /**
   * Set character calling
   */
  setCalling(calling) {
    const validCallings = [
      'wisdom',
      'service',
      'trial',
      'sacrifice',
      'revelation'
    ];

    if (!validCallings.includes(calling)) {
      throw new Error(`Invalid calling: ${calling}`);
    }

    this.calling = calling;

    // Apply calling bonuses
    this.applyCallingBonuses(calling);
  }

  /**
   * Apply calling-specific stat bonuses
   */
  applyCallingBonuses(calling) {
    const callingBonuses = {
      wisdom: { wisdom: 2, faith: 1 },
      service: { wisdom: 1, courage: 2 },
      trial: { strength: 2, courage: 1 },
      sacrifice: { righteousness: 2, faith: 1 },
      revelation: { wisdom: 2, righteousness: 1 }
    };

    const bonuses = callingBonuses[calling] || {};
    Object.keys(bonuses).forEach(stat => {
      this.bonusStats[stat] = (this.bonusStats[stat] || 0) + bonuses[stat];
    });
  }

  /**
   * Add item to inventory
   */
  addItem(item) {
    if (this.inventory.length >= 20) {
      return false; // Inventory full
    }
    this.inventory.push(item);
    return true;
  }

  /**
   * Remove item from inventory
   */
  removeItem(itemId) {
    const index = this.inventory.findIndex(item => item.id === itemId);
    if (index !== -1) {
      this.inventory.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * Find item in inventory
   */
  findItem(itemId) {
    return this.inventory.find(item => item.id === itemId);
  }

  /**
   * Equip item
   */
  equipItem(itemId) {
    const item = this.findItem(itemId);
    if (!item) return false;

    // Unequip current item in that slot
    if (this.equipped[item.type]) {
      this.unequipItem(item.type);
    }

    // Equip new item
    this.equipped[item.type] = item;
    return true;
  }

  /**
   * Unequip item
   */
  unequipItem(slot) {
    this.equipped[slot] = null;
  }

  /**
   * Calculate damage for attack
   */
  calculateDamage(weaponBonus = 0) {
    const totalStats = this.calculateTotalStats();
    const baseDamage = totalStats.strength * 2; // Strength determines damage
    const equippedWeapon = this.equipped.weapon || {};
    const weaponDamage = equippedWeapon.damage || 0;

    return baseDamage + weaponDamage + weaponBonus;
  }

  /**
   * Calculate defense
   */
  calculateDefense() {
    const totalStats = this.calculateTotalStats();
    let baseDefense = totalStats.faith * 0.5; // Faith helps with defense

    const equippedArmor = this.equipped.armor || {};
    const equippedShield = this.equipped.shield || {};

    const armorDefense = equippedArmor.defense || 0;
    const shieldDefense = equippedShield.defense || 0;

    return baseDefense + armorDefense + shieldDefense;
  }

  /**
   * Get character sheet data for UI
   */
  getCharacterSheet() {
    const totalStats = this.calculateTotalStats();

    return {
      name: this.name,
      classType: this.classType,
      level: this.level,
      xp: this.xp,
      xpToLevel: this.xpToLevel,
      health: this.health,
      maxHealth: this.maxHealth,
      mana: this.mana,
      maxMana: this.maxMana,
      skillPoints: this.skillPoints,
      calling: this.calling,
      stats: totalStats,
      equipment: this.equipped,
      inventoryCount: this.inventory.length,
      completedQuests: this.completedQuests.length
    };
  }

  /**
   * Reset to defaults (on death, etc)
   */
  reset() {
    this.health = this.maxHealth;
    this.mana = this.maxMana;
  }

  /**
   * Check if character is alive
   */
  isAlive() {
    return this.health > 0;
  }

  /**
   * Export character data for saving
   */
  serialize() {
    return {
      name: this.name,
      classType: this.classType,
      baseStats: this.baseStats,
      bonusStats: this.bonusStats,
      health: this.health,
      maxHealth: this.maxHealth,
      mana: this.mana,
      maxMana: this.maxMana,
      level: this.level,
      xp: this.xp,
      xpToLevel: this.xpToLevel,
      skillPoints: this.skillPoints,
      calling: this.calling,
      inventory: this.inventory,
      equipped: this.equipped,
      completedQuests: this.completedQuests,
      activeQuests: this.activeQuests,
      defeatedEnemies: this.defeatedEnemies,
      npcMemory: this.npcMemory
    };
  }

  /**
   * Load character data from save
   */
  static deserialize(data) {
    const char = new Character(data.name, data.classType);

    Object.assign(char, data);

    return char;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Character, CHARACTER_CLASSES };
}
