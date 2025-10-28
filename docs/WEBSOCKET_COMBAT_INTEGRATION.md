# WebSocket and Combat System Integration Guide

## Overview

This document explains the integration of the WebSocket communication system and the turn-based combat system for Journey Through Scripture.

## Part 1: WebSocket Communication

### Architecture

The WebSocket system uses a two-way JSON message protocol:

```
Web Client (JavaScript) <--WebSocket--> Evennia Server (Python)
```

### Connection Flow

1. **Player loads game** → Web client initializes
2. **Game starts** → Client attempts WebSocket connection to `ws://localhost:4001/ws`
3. **Connection established** → Server recognizes web client session
4. **Client requests state** → Sends `get_character_state` and `get_room_state` messages
5. **Server responds** → Sends character and room updates
6. **Game loop begins** → Client renders and handles input

### Key Files

**Server-side (Python):**
- `mygame/web/websocket_plugin.py` - WebSocket message handlers
- `mygame/typeclasses/characters.py` - Character WebSocket methods
- `mygame/server/conf/settings.py` - WebSocket configuration

**Client-side (JavaScript):**
- `web/js/websocket.js` - WebSocket client class
- `web/js/game.js` - Game controller with message handlers
- `web/js/renderer.js` - Visual rendering
- `web/js/ui.js` - User interface updates

### Message Types

See `docs/WEBSOCKET_PROTOCOL.md` for complete protocol specification.

Key message types:
- `command` - Player executes a command
- `character_update` - Character stats/inventory changed
- `room_update` - Room state changed
- `text` - Output text to player
- `combat_event` - Combat action occurred
- `error` - Error message

### Server-Side Implementation

#### Character WebSocket Methods

The Character class includes these WebSocket-specific methods:

```python
# Send a message to web client
character.send_to_web_client({"type": "text", "text": "Hello"})

# Send complete character state
character.send_character_update()

# Send current room state
character.send_room_update()

# Send text output
character.send_text_output("Your message", "narrative")
```

#### WebSocket Message Handler

The `websocket_plugin.py` handles incoming messages:

```python
def at_websocket_message_receive(session, message):
    """Called when web client sends a message"""
    message_type = message.get("type")

    if message_type == "command":
        # Handle player command
        character.execute_cmd(message.get("text"))
    elif message_type == "get_character_state":
        # Send character state
        session.msg({"type": "character_update", "character": char_state})
    elif message_type == "equip":
        # Handle equipment action
        WebSocketHandler.handle_equip(character, item_key, slot)
```

### Client-Side Implementation

#### WebSocket Connection

The `WebSocketClient` class manages the connection:

```javascript
// Create and connect
const ws = new WebSocketClient();
await ws.connect('ws://localhost:4001/ws');

// Send a message
ws.send({type: 'command', text: 'north'});

// Listen for messages
ws.on('message', (data) => {
    // Handle server message
});
```

#### Message Handling in Game

The `Game` class processes server messages:

```javascript
onServerMessage(data) {
    if (data.type === 'character_update') {
        this.onCharacterUpdate(data.character);
    } else if (data.type === 'room_update') {
        this.onRoomUpdate(data.room);
    } else if (data.type === 'combat_event') {
        this.onCombatEvent(data);
    }
}
```

## Part 2: Combat System

### Architecture

The combat system is turn-based with the following flow:

```
Player Initiates Combat
        ↓
CombatHandler Created
        ↓
Combat Event Sent to Client
        ↓
Player Takes Action (attack, defend, heal, flee)
        ↓
Server Processes Action
        ↓
Combat Event Sent to Client
        ↓
Enemy Counter-attacks (if alive)
        ↓
Repeat until Combat Ends
```

### Combat Files

**Server-side:**
- `mygame/combat.py` - Core combat system
- `mygame/commands/combat.py` - Combat commands
- `mygame/typeclasses/characters.py` - Character combat methods

**Client-side:**
- `web/js/game.js` - Combat event handling
- `web/js/ui.js` - Combat UI display

### Combat Commands

Players use these commands during combat:

```
attack      - Strike your enemy
defend      - Reduce damage next turn
heal        - Restore health
flee        - Attempt to escape
status      - Check health/enemy status
fight <type> - Initiate combat with creature type
```

### Creature Types

Available creatures to fight:

```
orc         - 30 HP, 8 damage
demon       - 45 HP, 12 damage
leviathan   - 100 HP, 18 damage (boss)
behemoth    - 80 HP, 15 damage (boss)
nephilim    - 60 HP, 14 damage
dark_knight - 55 HP, 13 damage
serpent     - 40 HP, 10 damage
```

### Combat System Classes

#### CombatHandler

Manages individual combat encounters:

```python
combat = CombatHandler(attacker, defender)

# Process attacker's turn
result = combat.attacker_turn()
# Returns: {
#     "hit": bool,
#     "damage": int,
#     "message": str,
#     "combat_ended": bool
# }

# End combat
combat.end_combat(victory=True)
```

#### Creature

Creates enemy creatures with stats:

```python
creature_stats = Creature.create_creature('orc', level=1)
# Returns: {
#     'name': 'Orc',
#     'hp': 30,
#     'damage': 8,
#     'strength': 7,
#     'courage': 6,
#     'xp_reward': 100,
#     'currency_reward': 50,
#     'level': 1,
#     'sprite': 'orc_idle'
# }
```

### Combat Mechanics

#### Damage Calculation

```
Base Damage = character.damage + weapon_damage + (strength - 5) * 0.5
Variance = ±20%
Final Damage = randomize(Base Damage, Variance)
```

#### Accuracy

```
Base Accuracy = 75%
Attacker Bonus = courage * 10%
Defender Penalty = courage * 5%
Final Accuracy = Base + Bonus - Penalty
Result = Clamp(10%, 100%)
```

#### Experience & Rewards

When defeating an enemy:

```
XP Gained = creature.xp_reward * level_multiplier
Currency = creature.currency_reward * level_multiplier
```

### Combat Flow Example

1. **Initiate Combat**
   ```
   Player: "fight orc"
   Server: Creates combat with Orc
   Server → Client: {
       "type": "combat_event",
       "event": "combat_started",
       "enemy": {...orc_stats...}
   }
   ```

2. **Player Attacks**
   ```
   Player: "attack"
   Server: Rolls to hit (75% + bonuses)
   Server: Calculates damage if hit
   Server → Client: {
       "type": "combat_event",
       "event": "combat_action",
       "message": "You hit the Orc for 12 damage!"
   }
   ```

3. **Enemy Counter-attacks**
   ```
   Server: Enemy attacks player
   Server: Calculates damage
   Server → Client: {
       "type": "text",
       "text": "Orc attacks you for 8 damage!",
       "class": "combat"
   }
   ```

4. **Combat Ends (Victory)**
   ```
   Orc HP reaches 0
   Server → Client: {
       "type": "combat_event",
       "event": "combat_ended",
       "victory": true,
       "xp_gained": 100,
       "currency_gained": 50
   }
   ```

## Integration Points

### Character Takes Damage

When `character.take_damage()` is called:
1. HP is reduced
2. Text message sent to client
3. If dead, character dies
4. Combat state updated

### Character Gains XP

When `character.gain_xp()` is called:
1. XP increases
2. Level-up check performed
3. Character update sent to client
4. If leveled up, stats increased

### Character Moves

When `character` moves to new room:
1. Room update sent to client
2. Character update sent to client
3. Combat ends if in combat

### Character Takes Action

When `character.execute_cmd()` is called:
1. Command routed to appropriate handler
2. If combat command, combat system processes it
3. WebSocket events sent as needed
4. Client receives updates

## Testing the System

### Manual Testing

1. **Start Evennia Server**
   ```bash
   cd mygame
   evennia start
   ```

2. **Open Web Client**
   ```
   Open web/index.html in browser or run:
   python -m http.server 8000 -d web
   ```

3. **Create Character**
   - Select class
   - Enter name
   - Start game

4. **Test WebSocket**
   - Open browser console (F12)
   - See WebSocket connection message
   - Type "fight orc" to start combat
   - Check console for WebSocket messages

5. **Test Combat**
   - Fight an enemy: "fight orc"
   - Attack: "attack"
   - Check health: "status"
   - Defend: "defend"
   - Flee: "flee"

### Expected Output

**Server Console:**
```
WebSocket connected: <character_name>
Received message: {'type': 'command', 'text': 'fight orc'}
Combat started: <character_name> vs Orc
```

**Client Console:**
```
WebSocket connected
Server message: {type: "combat_event", event: "combat_started", ...}
Combat event: combat_started
```

**Browser Display:**
```
Combat started! You face Orc!

> attack
You strike the Orc for 12 damage!
Orc attacks you for 8 damage!

> status
Your Health: 92/100
Orc Health: 18/30
```

## Debugging

### Enable Debug Mode

In web client, type in console:
```javascript
window.DEBUG = true;
```

This enables:
- Grid display on canvas
- Detailed WebSocket logging
- Console output for all events

### Check Server Logs

Watch Evennia server output:
```bash
tail -f mygame/server/logs/server.log
```

Look for:
- WebSocket connection/disconnection
- Command execution
- Combat events
- Error messages

### Network Inspector

1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter for "ws" (WebSocket)
4. Watch WebSocket frames
5. Inspect message payloads

## Common Issues

### WebSocket Not Connecting
- Check Evennia server is running
- Verify port 4001 is not blocked
- Check browser console for connection errors
- Ensure correct WebSocket URL

### Combat Not Starting
- Verify character has combat methods
- Check creature type is valid
- Look for Python errors in server logs
- Try fighting with a different creature type

### Stats Not Updating
- Check character.send_character_update() is called
- Verify WebSocket connection is active
- Check UI has update methods
- Look for JavaScript errors in console

### Combat Events Not Received
- Verify character.send_to_web_client() is called
- Check message format matches protocol
- Inspect WebSocket frame in Network tab
- Check client message handler is registered

## Future Enhancements

- [ ] Party/group combat
- [ ] Special abilities and spells
- [ ] Item effects during combat
- [ ] Creature AI behavior trees
- [ ] Combat animations on canvas
- [ ] Damage numbers floating effect
- [ ] Boss encounters with mechanics
- [ ] Combat challenges and events
