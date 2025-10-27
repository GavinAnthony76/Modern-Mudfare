# Development Roadmap - Journey Through Scripture

Strategic roadmap for completing the Biblical Fantasy MUD from current state to full release.

## Current Status (Commit: 961c1eb)

### ✓ Completed
- HTML5 Canvas graphics renderer
- Game loop (60 FPS)
- Input handling (keyboard, mouse, touch)
- Placeholder sprite system
- SVG sprite generation for all NPCs/items
- Audio system with Web Audio API
- Footstep sound effects (using footstep_wood.mp3)
- Responsive UI with stats, inventory, quests panels
- Mobile-responsive design
- Floor 1 complete data structure
- 9 NPCs with full dialogue trees
- 20+ items with properties
- Asset management system

### 🔄 In Progress
- Graphics visibility (fixed in latest commit)
- Audio playback integration

### 📋 Remaining Work
- Evennia backend integration
- Combat system
- Quest system
- Character stats and progression
- Inventory management
- Floors 2-7 implementation
- Save/load functionality

## Phase 1: Core Gameplay Systems (2 weeks)

### Week 1: Combat & Character Systems

#### Task 1.1: Implement Character Stats Engine
**Files**: `mygame/web/static/webclient/js/character.js` (new)

```javascript
class Character {
  constructor(name, classType) {
    this.name = name;
    this.classType = classType;

    // Stats based on class
    this.stats = {
      faith: 5,      // Divine power
      wisdom: 5,     // Perception & spellcasting
      strength: 5,   // Physical damage
      courage: 5,    // Fear resistance
      righteousness: 5  // Alignment
    };

    // Health & Resources
    this.health = 100;
    this.maxHealth = 100;
    this.mana = 50;
    this.maxMana = 50;

    // Experience
    this.level = 1;
    this.xp = 0;
    this.xpToLevel = 100;
  }

  takeDamage(amount) { }
  heal(amount) { }
  gainXP(amount) { }
  levelUp() { }
}
```

**Subtasks**:
- [ ] Create character.js module
- [ ] Implement stat calculations by class
- [ ] Add health/mana management
- [ ] Create experience system
- [ ] Integrate with game.js

#### Task 1.2: Implement Combat System
**Files**: `mygame/web/static/webclient/js/combat.js` (new)

```javascript
class Combat {
  constructor(player, enemy) {
    this.player = player;
    this.enemy = enemy;
    this.turn = 'player'; // or 'enemy'
    this.log = []; // Combat log
  }

  playerAttack() { }
  enemyAttack() { }
  playerCastSpell(spell) { }
  resolveRound() { }
  calculateDamage(attacker, defender) { }
  determineWinner() { }
}
```

**Subtasks**:
- [ ] Create combat.js module
- [ ] Implement turn-based system
- [ ] Add damage calculation
- [ ] Create combat log UI
- [ ] Add animation feedback

#### Task 1.3: Implement Inventory System
**Files**: `mygame/web/static/webclient/js/inventory.js` (new)

```javascript
class Inventory {
  constructor(maxSize = 20) {
    this.items = [];
    this.maxSize = maxSize;
    this.equipped = {
      weapon: null,
      armor: null,
      accessory: null
    };
  }

  addItem(item) { }
  removeItem(itemId) { }
  equipItem(itemId) { }
  unequipItem(slot) { }
  getStatBonuses() { }
}
```

**Subtasks**:
- [ ] Create inventory.js module
- [ ] Implement item management
- [ ] Add equipment system
- [ ] Update UI to show items
- [ ] Add item usage (consumables)

### Week 2: Quest & Dialogue Systems

#### Task 2.1: Implement Quest System
**Files**: `mygame/web/static/webclient/js/quests.js` (new)

```javascript
class QuestSystem {
  constructor() {
    this.activeQuests = [];
    this.completedQuests = [];
    this.questLog = {};
  }

  startQuest(questId) { }
  updateQuestProgress(questId, progressData) { }
  completeQuest(questId) { }
  getQuestRewards(questId) { }
}
```

**Subtasks**:
- [ ] Create quests.js module
- [ ] Load quests from data files
- [ ] Implement quest tracking
- [ ] Add quest completion logic
- [ ] Integrate with NPC dialogue

#### Task 2.2: Implement Dialogue System
**Files**: `mygame/web/static/webclient/js/dialogue.js` (new)

```javascript
class DialogueSystem {
  constructor() {
    this.currentNPC = null;
    this.currentDialogueTree = null;
    this.visitedNodes = [];
  }

  startDialogue(npc) { }
  chooseOption(optionNum) { }
  checkCondition(condition) { }
  executeAction(action) { }
  endDialogue() { }
}
```

**Subtasks**:
- [ ] Create dialogue.js module
- [ ] Implement dialogue tree traversal
- [ ] Add conditional responses
- [ ] Create dialogue UI panel
- [ ] Support quest-triggered dialogue

#### Task 2.3: Implement Calling System
**Files**: `mygame/web/static/webclient/js/calling.js` (new)

After defeating The Deceiver, players choose a calling that affects their path:
- Calling of Wisdom
- Calling of Service
- Calling of Trial
- Calling of Sacrifice
- Calling of Revelation

**Subtasks**:
- [ ] Create calling.js module
- [ ] Store player calling choice
- [ ] Apply stat bonuses per calling
- [ ] Unlock calling-specific quests
- [ ] Update UI to show calling

## Phase 2: World Integration (2 weeks)

### Week 3: Evennia Backend Integration

#### Task 3.1: Set Up Evennia Server
**Commands**:
```bash
cd mygame
evennia --init .
evennia migrate
evennia createsuperuser
evennia start
```

**Subtasks**:
- [ ] Initialize Evennia
- [ ] Configure database
- [ ] Create superuser account
- [ ] Test server startup
- [ ] Configure ports

#### Task 3.2: Create World Builder Script
**Files**: `mygame/world/build_world.py` (update)

Should create all rooms, items, and NPCs automatically when run:
```python
@py from world import build_world; build_world.build_all()
```

**Subtasks**:
- [ ] Create room builder
- [ ] Create item builder
- [ ] Create NPC builder
- [ ] Add dialogue integration
- [ ] Test world creation

#### Task 3.3: Implement WebSocket Communication
**Files**: `mygame/web/static/webclient/js/websocket.js` (update)

Client ↔ Server Protocol:
```
Client → Server:
  {action: 'move', direction: 'north'}
  {action: 'talk', npc: 'gate_keeper_samuel', option: 1}
  {action: 'combat', target: 'enemy_id'}

Server → Client:
  {type: 'room_update', room_id: '...', description: '...'}
  {type: 'combat_update', damage: 15, attacker: 'player'}
  {type: 'quest_complete', quest_id: 'find_truth'}
```

**Subtasks**:
- [ ] Implement WebSocket client
- [ ] Create message protocol
- [ ] Handle connection errors
- [ ] Add reconnection logic
- [ ] Test server communication

### Week 4: Floor 1 Completion

#### Task 4.1: Build Floor 1 Rooms in Evennia
**Rooms to create**: 9 total
- floor1_approach (starting)
- floor1_entrance (Gate Keeper Samuel)
- floor1_courtyard (central hub)
- floor1_pilgrim_rest (SAFE - Priest Ezra)
- floor1_hall_testing (Stern Teacher)
- floor1_merchant_corner (Merchant area)
- floor1_hidden_alcove (secret area)
- floor1_garden (Garden Keeper Ruth)
- floor1_boss_chamber (The Deceiver)

**Subtasks**:
- [ ] Create room typeclasses
- [ ] Add room descriptions
- [ ] Set up room exits
- [ ] Place NPCs in rooms
- [ ] Place items in rooms

#### Task 4.2: Implement Enemies & Combat Encounters
**Enemy Types**:
- The Deceiver (Boss) - 50 HP, 8 damage
- Desert creatures (future)

**Subtasks**:
- [ ] Create enemy typeclasses
- [ ] Implement enemy AI
- [ ] Add boss encounter
- [ ] Create loot drops
- [ ] Balance difficulty

#### Task 4.3: Implement Sanctuaries (Safe Rooms)
**Features**:
- Healing service
- Save game
- Blessings

**Subtasks**:
- [ ] Create sanctuary typeclass
- [ ] Implement healing command
- [ ] Add save system
- [ ] Create blessing buff system

## Phase 3: Content Expansion (3 weeks)

### Week 5: Floors 2-4

#### Task 5.1: Floor 2 - Court of Wisdom
- 3 rooms
- Priest Miriam
- Library with books
- Debate encounters

#### Task 5.2: Floor 3 - Court of Service
- 4 rooms
- Priest-Healer Tobias
- Healing chambers
- Crafting mechanics

#### Task 5.3: Floor 4 - Court of Trial
- 3 rooms
- Priest-Warrior Caleb
- Trial challenges
- Shadow enemies

### Week 6: Floors 5-7

#### Task 6.1: Floor 5 - Court of Sacrifice
- 3 rooms
- Priest-Elder Sarah
- Guardian Angel encounter
- Sacrifice mechanic

#### Task 6.2: Floor 6 - Court of Revelation
- 3 rooms
- Priest-Seer Ezekiel
- Vision chambers
- Truth/Deception encounters

#### Task 6.3: Floor 7 - Holy of Holies
- 4 rooms
- High Priest Aaron
- Final boss (Corrupted Cherub)
- Victory sequence

### Week 7: Content Polish

#### Task 7.1: Refine Enemy AI
- Add special abilities
- Implement patterns
- Balance encounters

#### Task 7.2: Complete Quest Lines
- Main story quests
- Side quests
- Divine missions

#### Task 7.3: Add Ambient Content
- Readable lore items
- Environmental storytelling
- Hidden secrets

## Phase 4: Graphics & Audio (1 week)

### Week 8: Replace Placeholders

#### Task 8.1: Integrate Custom Sprites
- Load real character art
- Load NPC sprites
- Load tile sets

**Current Status**: Using SVG placeholders
**Next**: Accept PNG files from users

#### Task 8.2: Add Audio Assets
- Background music tracks
- Sound effects
- Ambient sounds

**Current**: footstep_wood.mp3 working
**Next**: Add all other audio files

## Phase 5: Testing & Optimization (1 week)

### Week 9: QA & Performance

#### Task 9.1: Performance Optimization
- Profile rendering
- Optimize sprite loading
- Reduce network latency

#### Task 9.2: Cross-Browser Testing
- Test on Chrome, Firefox, Safari, Edge
- Mobile browser testing
- Touch control testing

#### Task 9.3: Balance & Polish
- Adjust difficulty curves
- Fix bugs
- Balance rewards

## Implementation Checklist

### Graphics & Rendering
- [x] Canvas renderer
- [x] Placeholder sprites
- [x] Game loop (60 FPS)
- [x] Camera system
- [ ] Real sprite loading
- [ ] Animation system
- [ ] Particle effects polish
- [ ] Lighting effects

### Audio & Sound
- [x] Audio manager
- [x] Footstep sounds
- [ ] Background music
- [ ] Combat sounds
- [ ] NPC dialogue sounds
- [ ] UI feedback sounds
- [ ] Victory fanfares

### Gameplay Systems
- [ ] Character creation
- [ ] Character stats
- [ ] Combat system
- [ ] Inventory system
- [ ] Equipment system
- [ ] Quest system
- [ ] Dialogue system
- [ ] Calling system
- [ ] Experience & leveling
- [ ] Item drops & loot

### World & Content
- [ ] Floor 1 full implementation
- [ ] Floors 2-7 implementation
- [ ] Room descriptions
- [ ] NPC placement
- [ ] Item placement
- [ ] Enemy encounters
- [ ] Boss fights
- [ ] Secret areas
- [ ] Lore items
- [ ] Environmental storytelling

### Backend Integration
- [ ] Evennia world builder
- [ ] WebSocket communication
- [ ] Room persistence
- [ ] Character saving
- [ ] NPC AI
- [ ] Combat resolution
- [ ] Quest tracking
- [ ] Dialogue state management

### Polish & Optimization
- [ ] Performance tuning
- [ ] Mobile optimization
- [ ] Cross-browser compatibility
- [ ] Accessibility features
- [ ] User tutorials
- [ ] In-game help
- [ ] Balance adjustments
- [ ] Bug fixes

## Success Criteria

Game is ready for public beta when:
1. ✓ All 7 floors playable
2. ✓ Combat system functional
3. ✓ Quests completable
4. ✓ Saving/loading works
5. ✓ 60+ NPCs and encounters
6. ✓ 200+ items and equipment
7. ✓ Custom graphics loaded
8. ✓ Audio system complete
9. ✓ Mobile-friendly
10. ✓ Cross-browser tested

## Timeline

| Phase | Duration | Target Completion |
|-------|----------|------------------|
| Phase 1 | 2 weeks | Core systems ready |
| Phase 2 | 2 weeks | Backend integrated |
| Phase 3 | 3 weeks | All content added |
| Phase 4 | 1 week | Graphics/audio |
| Phase 5 | 1 week | Testing & polish |
| **Total** | **9 weeks** | **Full release** |

## Priority Levels

**P0 (Critical)**: Must have for playable game
- Combat system
- Inventory system
- Quest system
- Dialogue system
- Evennia integration

**P1 (Important)**: Expected features
- All 7 floors
- Character progression
- Boss encounters
- Real graphics
- Audio system

**P2 (Nice to have)**: Polish features
- Animations
- Particle effects
- Leaderboards
- Achievements
- Multiplayer

## Next Immediate Actions

1. **Test graphics visibility** - Confirm character and NPCs render
2. **Start character stats** - Implement stat system
3. **Begin combat** - Create basic combat mechanics
4. **Set up Evennia** - Initialize backend server
5. **Create world builder** - Automate room/NPC creation

---

*"Enter with reverence, seek with humility, find with joy."*
