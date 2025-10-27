/**
 * Quest System - Track and manage quests
 */

// Quest definitions
const QUESTS = {
  find_truth: {
    id: 'find_truth',
    title: 'Find the Truth',
    description: 'Find the hidden chamber of the Deceiver',
    type: 'main',
    location: 'Floor 1',
    reward: { xp: 100, gold: 50 },
    completed: false,
    objectivesCompleted: 0,
    objectivesTotal: 1
  },
  explore_floor_1: {
    id: 'explore_floor_1',
    title: 'Explore the Palace',
    description: 'Discover all rooms on Floor 1',
    type: 'exploration',
    location: 'Floor 1',
    reward: { xp: 50, gold: 25 },
    completed: false,
    objectivesCompleted: 0,
    objectivesTotal: 9
  },
  speak_with_npcs: {
    id: 'speak_with_npcs',
    title: 'Meet the Pilgrims',
    description: 'Speak with all NPCs on Floor 1',
    type: 'side',
    location: 'Floor 1',
    reward: { xp: 75, gold: 30 },
    completed: false,
    objectivesCompleted: 0,
    objectivesTotal: 9
  },
  defeat_deceiver: {
    id: 'defeat_deceiver',
    title: 'Defeat The Deceiver',
    description: 'Defeat The Deceiver and claim victory on Floor 1',
    type: 'main',
    location: 'Floor 1: Boss Chamber',
    reward: { xp: 200, gold: 100 },
    completed: false,
    objectivesCompleted: 0,
    objectivesTotal: 1,
    unlocks: 'floor2_access'
  }
};

class QuestSystem {
  constructor() {
    this.activeQuests = [];
    this.completedQuests = [];
    this.questLog = {};
    this.trackedQuest = null;

    // Initialize with all available quests
    Object.values(QUESTS).forEach(quest => {
      this.questLog[quest.id] = { ...quest };
    });
  }

  /**
   * Start a quest
   */
  startQuest(questId) {
    if (!this.questLog[questId]) {
      console.log(`Quest not found: ${questId}`);
      return false;
    }

    const quest = this.questLog[questId];

    if (this.activeQuests.find(q => q.id === questId)) {
      console.log(`Quest already active: ${questId}`);
      return false;
    }

    this.activeQuests.push(quest);
    this.trackedQuest = questId;
    console.log(`Started quest: ${quest.title}`);

    return true;
  }

  /**
   * Update quest progress
   */
  updateQuestProgress(questId, progressData) {
    const quest = this.questLog[questId];
    if (!quest) return;

    if (progressData.objectivesCompleted !== undefined) {
      quest.objectivesCompleted = progressData.objectivesCompleted;
    }

    // Check if quest is complete
    if (quest.objectivesCompleted >= quest.objectivesTotal) {
      this.completeQuest(questId);
    }
  }

  /**
   * Complete a quest
   */
  completeQuest(questId) {
    const quest = this.questLog[questId];
    if (!quest || quest.completed) return;

    quest.completed = true;
    const questIndex = this.activeQuests.findIndex(q => q.id === questId);
    if (questIndex !== -1) {
      this.activeQuests.splice(questIndex, 1);
    }

    this.completedQuests.push(quest);

    if (this.trackedQuest === questId) {
      this.trackedQuest = null;
    }

    console.log(`Completed quest: ${quest.title}`);
    console.log(`Rewards: ${quest.reward.xp} XP, ${quest.reward.gold} gold`);

    return quest.reward;
  }

  /**
   * Get quest by ID
   */
  getQuest(questId) {
    return this.questLog[questId];
  }

  /**
   * Get active quests
   */
  getActiveQuests() {
    return this.activeQuests;
  }

  /**
   * Get completed quests
   */
  getCompletedQuests() {
    return this.completedQuests;
  }

  /**
   * Track quest
   */
  trackQuest(questId) {
    const quest = this.getQuest(questId);
    if (!quest) return;

    this.trackedQuest = questId;
  }

  /**
   * Get tracked quest
   */
  getTrackedQuest() {
    return this.trackedQuest ? this.questLog[this.trackedQuest] : null;
  }

  /**
   * Check if quest is completed
   */
  isQuestCompleted(questId) {
    const quest = this.getQuest(questId);
    return quest ? quest.completed : false;
  }

  /**
   * Check if quest is active
   */
  isQuestActive(questId) {
    return this.activeQuests.some(q => q.id === questId);
  }

  /**
   * Get quests by type
   */
  getQuestsByType(type) {
    return Object.values(this.questLog).filter(
      q => q.type === type && !q.completed
    );
  }

  /**
   * Serialize for saving
   */
  serialize() {
    return {
      activeQuests: this.activeQuests.map(q => q.id),
      completedQuests: this.completedQuests.map(q => q.id),
      trackedQuest: this.trackedQuest
    };
  }

  /**
   * Load from saved data
   */
  static deserialize(data) {
    const qs = new QuestSystem();

    if (data.activeQuests) {
      data.activeQuests.forEach(questId => {
        const quest = qs.questLog[questId];
        if (quest && !qs.activeQuests.find(q => q.id === questId)) {
          qs.activeQuests.push(quest);
        }
      });
    }

    if (data.completedQuests) {
      data.completedQuests.forEach(questId => {
        const quest = qs.questLog[questId];
        if (quest && !quest.completed) {
          quest.completed = true;
          qs.completedQuests.push(quest);
        }
      });
    }

    qs.trackedQuest = data.trackedQuest || null;

    return qs;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { QuestSystem, QUESTS };
}
