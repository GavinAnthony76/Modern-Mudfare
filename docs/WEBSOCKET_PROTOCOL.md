# WebSocket Communication Protocol

## Overview
The web client communicates with the Evennia MUD server via WebSocket. The protocol uses JSON-formatted messages to exchange game state, commands, and events.

## Connection Details
- **Server WebSocket Endpoint**: `ws://localhost:4001/ws`
- **Message Format**: JSON
- **Authentication**: Handled by Evennia's session system

## Message Types

### Client -> Server Messages

#### 1. Command Message
Player executes a command in the game world.
```json
{
  "type": "command",
  "text": "north"
}
```

#### 2. Look Message
Request current room description.
```json
{
  "type": "look"
}
```

#### 3. Get Room State
Request full room state (for initial load/refresh).
```json
{
  "type": "get_room_state"
}
```

#### 4. Get Character State
Request current character stats and inventory.
```json
{
  "type": "get_character_state"
}
```

#### 5. Equipment Action
Equip or unequip an item.
```json
{
  "type": "equip",
  "item_key": "weapon_staff_moses",
  "slot": "weapon"
}
```

#### 6. Combat Action
Perform a combat action in battle.
```json
{
  "type": "combat_action",
  "action": "attack",
  "target_id": "enemy_id_123"
}
```

### Server -> Client Messages

#### 1. Room Update
Sent when player moves or room state changes.
```json
{
  "type": "room_update",
  "room": {
    "id": "floor1_sanctuary",
    "name": "The Sacred Sanctuary",
    "description": "A holy place...",
    "characters": [
      {
        "id": "char_player_id",
        "name": "David",
        "class": "warrior",
        "sprite": "soldier_idle"
      }
    ],
    "objects": [
      {
        "id": "item_key",
        "name": "Golden Key",
        "type": "key",
        "sprite": "key_gold"
      }
    ],
    "exits": ["north", "south", "east", "west"]
  }
}
```

#### 2. Character Update
Sent when character stats/inventory changes.
```json
{
  "type": "character_update",
  "character": {
    "id": "char_player_id",
    "name": "David",
    "class": "warrior",
    "level": 5,
    "stats": {
      "faith": 6,
      "wisdom": 5,
      "strength": 8,
      "courage": 8,
      "righteousness": 7
    },
    "health": {
      "current": 95,
      "max": 120
    },
    "xp": {
      "current": 450,
      "next_level": 500
    },
    "inventory": [
      {
        "id": "item_sword_1",
        "name": "Sword of the Spirit",
        "type": "weapon",
        "equipped": true
      }
    ],
    "currency": 250
  }
}
```

#### 3. Text Output
Server sends text messages to display.
```json
{
  "type": "text",
  "text": "You attack the enemy!",
  "class": "narrative"
}
```

Supported classes:
- `narrative`: Descriptive text
- `system`: System messages
- `success`: Positive feedback
- `warning`: Warnings
- `error`: Error messages
- `combat`: Combat messages
- `command-echo`: Echoed command (client may also send this)

#### 4. Combat Event
Sent when combat state changes or during combat.
```json
{
  "type": "combat_event",
  "event": "combat_started",
  "enemy": {
    "id": "enemy_orc_1",
    "name": "Orc Warrior",
    "creature_type": "orc",
    "health": 45,
    "max_health": 45,
    "level": 3,
    "sprite": "orc_idle"
  }
}
```

Combat event types:
- `combat_started`: Player entered combat
- `combat_action`: Action was performed in combat
- `enemy_attacked`: Enemy performed action
- `health_updated`: Health changed
- `combat_ended`: Combat finished (victory/defeat)

#### 5. Quest Update
Sent when quest status changes.
```json
{
  "type": "quest_update",
  "quest": {
    "id": "quest_meet_elder",
    "name": "Meet the Elder",
    "status": "active",
    "objectives": [
      {
        "id": "obj_1",
        "description": "Find the Elder's chamber",
        "completed": false
      }
    ],
    "reward": {
      "xp": 100,
      "currency": 50
    }
  }
}
```

#### 6. Dialogue Event
Sent when NPC dialogue changes.
```json
{
  "type": "dialogue",
  "npc_id": "npc_priest_samuel",
  "npc_name": "Priest Samuel",
  "dialogue": "Welcome, traveler. What brings you to this sacred place?",
  "options": [
    {
      "id": "opt_1",
      "text": "I seek the blessing of the elders"
    },
    {
      "id": "opt_2",
      "text": "Just passing through"
    }
  ]
}
```

#### 7. Notification
Sent for important notifications (level up, item pickup, etc.).
```json
{
  "type": "notification",
  "title": "Level Up!",
  "message": "You reached level 6!",
  "class": "success"
}
```

#### 8. Error
Server sends error information.
```json
{
  "type": "error",
  "message": "Unknown command",
  "command": "xyz"
}
```

#### 9. Ping/Pong
Keepalive messages.
```json
{
  "type": "ping"
}
```

Server responds with:
```json
{
  "type": "pong"
}
```

## Game State Synchronization

### Initial Connection Flow
1. Client connects to WebSocket
2. Server sends welcome message
3. Client requests character state: `{"type": "get_character_state"}`
4. Server sends character update
5. Client requests room state: `{"type": "get_room_state"}`
6. Server sends room update

### State Consistency
- Server is authoritative for all game state
- Client updates display based on server messages
- Optimistic prediction NOT used (turned-based gameplay)
- All commands wait for server confirmation

### Movement Flow
1. Client sends: `{"type": "command", "text": "north"}`
2. Server processes movement
3. Server sends updated room state: `room_update`
4. Client updates display based on new room
5. Server sends character update with new position

### Combat Flow
1. Player encounters enemy (server sends `combat_event: combat_started`)
2. Client displays combat UI
3. Player selects action
4. Client sends: `{"type": "combat_action", "action": "attack", "target_id": "..."}`
5. Server processes combat
6. Server sends `combat_event` messages with results
7. Combat continues until victory/defeat
8. Server sends `combat_event: combat_ended`
9. Client returns to normal game view

## Error Handling

### Connection Errors
- Client handles `onerror` and `onclose` events
- Automatic reconnection with exponential backoff
- User notified of connection status

### Message Errors
- Server validates all messages
- Invalid messages return `error` type
- Client logs errors for debugging

### Timeout Handling
- Client implements message timeouts for command responses
- Server sends keepalive pings periodically
- Client responds with pongs

## Implementation Notes

### Evennia Integration
- Evennia's WebSocket support is enabled
- Messages routed through web_plugins system
- Character objects handle game logic
- Room objects manage state

### Performance Considerations
- Large room updates batched
- Character updates sent on change only
- UI updates debounced client-side
- Asset loading independent of WebSocket

### Data Validation
- Client validates UI inputs before sending
- Server validates all commands and data
- Sanitizes text for display
- Prevents injection attacks

## Future Extensions

### Planned Features
- Player-to-player messaging
- Guild/group messaging
- Leaderboard updates
- Server maintenance notifications
- Dynamic difficulty adjustment
- Real-time multiplayer syncing

### Version History
- **v1.0**: Initial protocol (current)
- Future: Enhanced with additional message types as needed
