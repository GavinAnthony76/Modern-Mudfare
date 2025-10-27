/**
 * Dialogue System - Handle NPC conversations
 */

class DialogueSystem {
  constructor(questSystem) {
    this.currentNPC = null;
    this.currentDialogueKey = null;
    this.visitedDialogues = {};
    this.questSystem = questSystem;
    this.inDialogue = false;
  }

  /**
   * Start dialogue with NPC
   */
  startDialogue(npc) {
    this.currentNPC = npc;
    this.currentDialogueKey = 'greeting';
    this.inDialogue = true;

    const dialogue = npc.dialogue[this.currentDialogueKey];

    return {
      npc: npc.label,
      text: dialogue,
      options: this.getDialogueOptions(npc)
    };
  }

  /**
   * Get available dialogue options
   */
  getDialogueOptions(npc) {
    if (!npc.dialogue.main_menu) return [];

    const options = [];
    const mainMenu = npc.dialogue.main_menu;

    Object.keys(mainMenu).forEach(optionNum => {
      const option = mainMenu[optionNum];

      // Check if option has requirements
      if (option.requires) {
        if (!this.meetsRequirements(option.requires)) {
          return; // Skip this option
        }
      }

      options.push({
        number: parseInt(optionNum),
        text: option.text,
        responseKey: option.response
      });
    });

    return options;
  }

  /**
   * Choose dialogue option
   */
  chooseOption(optionNumber) {
    if (!this.currentNPC) return null;

    const mainMenu = this.currentNPC.dialogue.main_menu;
    const option = mainMenu[optionNumber];

    if (!option) return null;

    const responseKey = option.response;
    const response = this.currentNPC.dialogue.responses[responseKey];

    this.currentDialogueKey = responseKey;

    // Execute dialogue actions
    this.executeDialogueActions(option);

    // Check if this ends the dialogue
    if (responseKey === 'farewell') {
      this.endDialogue();
    }

    return {
      npc: this.currentNPC.label,
      text: response,
      options: responseKey === 'farewell' ? [] : this.getDialogueOptions(this.currentNPC)
    };
  }

  /**
   * Execute dialogue actions
   */
  executeDialogueActions(option) {
    if (!option.action) return;

    switch (option.action) {
      case 'start_quest':
        if (this.questSystem) {
          this.questSystem.startQuest(option.questId);
        }
        break;
      case 'complete_quest':
        if (this.questSystem) {
          const reward = this.questSystem.completeQuest(option.questId);
          console.log(`Quest completed! Reward:`, reward);
        }
        break;
      case 'heal':
        if (window.game && window.game.player) {
          window.game.player.heal(100);
        }
        break;
      case 'save':
        console.log('Game saved!');
        break;
    }
  }

  /**
   * Check if requirements are met
   */
  meetsRequirements(requirement) {
    if (!requirement) return true;

    // Check if quest is completed
    if (this.questSystem) {
      return this.questSystem.isQuestCompleted(requirement);
    }

    return true;
  }

  /**
   * End dialogue
   */
  endDialogue() {
    this.inDialogue = false;
    this.currentNPC = null;
    this.currentDialogueKey = null;
  }

  /**
   * Check if in dialogue
   */
  isInDialogue() {
    return this.inDialogue;
  }

  /**
   * Get current NPC
   */
  getCurrentNPC() {
    return this.currentNPC;
  }

  /**
   * Serialize for saving
   */
  serialize() {
    return {
      visitedDialogues: this.visitedDialogues
    };
  }

  /**
   * Load from saved data
   */
  static deserialize(data, questSystem) {
    const ds = new DialogueSystem(questSystem);
    ds.visitedDialogues = data.visitedDialogues || {};
    return ds;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DialogueSystem;
}
