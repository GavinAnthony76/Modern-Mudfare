# Game Design Document - Journey Through Scripture

## Overview

Journey Through Scripture is a graphical MUD set in a biblical fantasy world. Players explore ancient lands inspired by scripture, encounter mythical creatures from biblical lore, and receive guidance from divine messengers.

## Core Gameplay Loop

1. **Exploration**: Navigate through biblical lands
2. **Combat**: Battle mythical creatures
3. **Progression**: Gain experience and improve stats
4. **Quests**: Receive guidance from divine messengers
5. **Discovery**: Find sacred items and unlock new areas

## Character System

### Character Creation

Players choose:
- **Name**: Biblical or custom name
- **Class**: Prophet, Warrior, Shepherd, or Scribe

### Character Classes

#### Prophet
- **Role**: Divine caster, healer, buffer
- **Primary Stats**: Faith (5), Wisdom (5), Righteousness (4)
- **Secondary Stats**: Strength (2), Courage (3)
- **Special Ability**: Divine Insight - Receive visions and guidance
- **Starting Equipment**: Staff, Simple Robe, Scroll of Wisdom

#### Warrior
- **Role**: Melee fighter, tank, protector
- **Primary Stats**: Strength (5), Courage (5), Righteousness (4)
- **Secondary Stats**: Faith (3), Wisdom (2)
- **Special Ability**: Righteous Strike - Powerful melee attack
- **Starting Equipment**: Bronze Sword, Leather Armor, Shield

#### Shepherd
- **Role**: Balanced support, leader, versatile
- **Primary Stats**: All stats at (4)
- **Secondary Stats**: Slight bonus to Wisdom
- **Special Ability**: Rally - Inspire allies (future multiplayer)
- **Starting Equipment**: Staff, Sling, Shepherd's Cloak

#### Scribe
- **Role**: Knowledge-based, strategic, spell variety
- **Primary Stats**: Wisdom (5), Intelligence (5), Faith (4)
- **Secondary Stats**: Strength (2), Courage (3)
- **Special Ability**: Ancient Knowledge - Identify items and lore
- **Starting Equipment**: Quill, Tome, Scholar's Robe

### Character Stats

1. **Faith**: Determines divine magic power and resistance to evil
2. **Wisdom**: Affects decision-making, perception, and spell effectiveness
3. **Strength**: Physical damage and carrying capacity
4. **Courage**: Resistance to fear, morale in combat
5. **Righteousness**: Alignment stat, affects NPC interactions and divine favor

### Progression

- **Experience Points (XP)**: Gained from combat, quests, and exploration
- **Levels**: 1-50 (MVP: 1-20)
- **Skill Points**: Allocated to improve stats and unlock abilities

## World Design

### Regions

#### 1. Desert Wilderness (Starting Area)
- **Level Range**: 1-5
- **Description**: Vast sandy expanse where wanderers begin their journey
- **Creatures**: Serpents, Scorpions, Desert Bandits
- **Points of Interest**: Oasis, Nomad Camps, Ancient Markers

#### 2. Jordan Valley
- **Level Range**: 5-10
- **Description**: Fertile river valley with settlements
- **Creatures**: Wild Boars, River Spirits, Bandits
- **Points of Interest**: River Crossing, Small Villages

#### 3. Mountains of Sinai
- **Level Range**: 10-15
- **Description**: Treacherous peaks where divine revelation occurs
- **Creatures**: Mountain Lions, Eagles, Stone Golems
- **Points of Interest**: Sacred Cave, Burning Bush Site

#### 4. Ancient Cities (Jerusalem, Jericho)
- **Level Range**: 15-20
- **Description**: Bustling cities with temples and markets
- **Creatures**: City Guards (if hostile), Thieves, Corrupt Officials
- **Points of Interest**: Temple, Market, Royal Palace

#### 5. The Depths (End-game)
- **Level Range**: 20+
- **Description**: Dark realm where great evils dwell
- **Creatures**: Leviathan, Behemoth, Demons, Fallen Angels
- **Points of Interest**: Abyssal Gate, Corrupted Temple

### Navigation

- **Cardinal Directions**: North, South, East, West
- **Additional**: Up, Down (for elevation changes)
- **Fast Travel**: Unlocked through quest completion
- **Map System**: Mini-map shows explored areas

## Combat System

### Combat Mechanics

- **Turn-Based**: Players and enemies take turns
- **Initiative**: Determined by Wisdom + random roll
- **Actions per Turn**: Move, Attack, Use Item, or Cast Spell

### Damage Calculation

```
Physical Damage = (Strength × Weapon Multiplier) - Enemy Defense
Magical Damage = (Faith × Spell Power) - Enemy Resistance
Critical Hit = Base Damage × 1.5 (when Righteousness check succeeds)
```

### Creature Types

#### Common Creatures (Level 1-5)
- **Desert Serpent**: Fast, poisonous
- **Scorpion**: High defense, slow
- **Wild Dog**: Pack tactics

#### Uncommon Creatures (Level 5-10)
- **Lion**: Powerful melee
- **Bear**: High health, strong
- **Bandit**: Uses weapons and tactics

#### Rare Creatures (Level 10-15)
- **Giant**: Massive health and damage
- **Demon Scout**: Dark magic user
- **Possessed Beast**: Corrupted animal

#### Epic Creatures (Level 15-20)
- **Nephilim**: Ancient giant warrior
- **Fallen Angel**: Dark magic, flight
- **Sea Monster**: Aquatic boss

#### Legendary Creatures (Level 20+)
- **Leviathan**: Massive sea dragon, chaos incarnate
- **Behemoth**: Unstoppable land beast
- **Abaddon**: Demon lord of destruction

### Loot System

- **Common**: Basic supplies (food, water, cloth)
- **Uncommon**: Improved weapons and armor
- **Rare**: Magical items with special properties
- **Epic**: Unique named items from scripture
- **Legendary**: Artifact-level items (Ark fragments, etc.)

## Quest System

### Quest Types

1. **Main Quests**: Story-driven, unlock new areas
2. **Side Quests**: Optional tasks from NPCs
3. **Divine Missions**: Given by angelic messengers
4. **Exploration Quests**: Discover hidden locations
5. **Collection Quests**: Gather specific items

### Divine Messengers

Angelic NPCs that appear at key moments:

- **Gabriel**: Main story quests, major revelations
- **Michael**: Combat training, warrior quests
- **Raphael**: Healing quests, medical knowledge
- **Uriel**: Wisdom quests, puzzle solving

### Quest Rewards

- Experience Points
- Gold/Resources
- Equipment
- Unlockable Areas
- Divine Favor (affects ending)

## Item System

### Equipment Slots

- **Weapon**: Primary damage source
- **Armor**: Chest protection
- **Shield**: Block chance (Warrior/Shepherd)
- **Accessory**: Special bonuses
- **Consumables**: Quick-use items

### Notable Items

#### Weapons
- **Staff of Moses**: Transforms into serpent in combat
- **Sword of the Spirit**: Holy damage bonus
- **David's Sling**: Ranged weapon, critical vs giants
- **Shepherd's Crook**: Support bonuses

#### Armor
- **Armor of God**: Full set (Ephesians 6)
  - Breastplate of Righteousness
  - Shield of Faith
  - Helmet of Salvation
  - Belt of Truth
  - Shoes of the Gospel

#### Consumables
- **Manna**: Restores health over time
- **Water from the Rock**: Instant health restoration
- **Anointing Oil**: Temporary stat boost
- **Healing Herbs**: Basic healing

## Multiplayer Features (Future)

### Planned Features

- **Party System**: Group up with other players
- **Trading**: Exchange items and resources
- **PvP Arenas**: Optional combat zones
- **Guilds**: Form communities
- **Shared Quests**: Cooperative missions

## Progression Milestones

### Level 1-5: The Wanderer
- Learn basic commands
- Complete tutorial quests
- First divine encounter
- Acquire basic equipment

### Level 5-10: The Seeker
- Explore multiple regions
- First major combat victory
- Unlock fast travel
- Choose specialization path

### Level 10-15: The Faithful
- Access to cities
- Advanced quest lines
- Divine favor accumulation
- Epic equipment acquisition

### Level 15-20: The Chosen
- Face legendary creatures
- Major story revelations
- Prepare for end-game
- Unlock final areas

### Level 20+: The Righteous
- End-game boss battles
- Complete main story
- Unlock New Game+
- Maximum divine favor

## User Interface

### HUD Elements

- **Health Bar**: Red, top-left
- **Faith/Mana Bar**: Blue, below health
- **Character Info**: Name and level
- **Mini-map**: Top-right corner
- **Quick Slots**: Bottom center (items/skills)

### Panels

- **Inventory**: Grid-based, drag-and-drop
- **Quests**: Active and completed quests
- **Map**: Full-screen exploration map
- **Character**: Stats and equipment

### Mobile Adaptations

- **Virtual D-Pad**: Movement control
- **Action Buttons**: Combat and interaction
- **Swipe Gestures**: Menu navigation
- **Tap**: Selection and confirmation

## Sound Design

### Music Tracks

- **Menu Theme**: Peaceful, mysterious
- **Exploration**: Ambient, atmospheric
- **Combat**: Intense, rhythmic
- **Victory**: Triumphant, short
- **Sacred Places**: Ethereal, holy

### Sound Effects

- **Footsteps**: Different per terrain
- **Combat**: Sword clashes, spell effects
- **Environment**: Wind, water, animals
- **Divine**: Angelic choir, light effects
- **UI**: Clicks, confirmations

## Technical Specifications

### Client-Server Communication

- **Protocol**: WebSocket (JSON messages)
- **Update Rate**: Real-time for combat, polling for world state
- **Compression**: Optional for large data transfers

### Data Persistence

- **Player Data**: Saved on server
- **Auto-save**: Every 5 minutes
- **Manual Save**: Via command or button

### Performance Targets

- **FPS**: 60 (rendering)
- **Latency**: <100ms (commands)
- **Load Time**: <3s (initial)
- **Memory**: <200MB (client)

## Future Enhancements

- Voice acting for key NPCs
- Seasonal events (biblical holidays)
- Dynamic weather system
- Housing/base building
- Achievement system
- Leaderboards
- Mobile native apps

---

*"For we walk by faith, not by sight." - 2 Corinthians 5:7*
