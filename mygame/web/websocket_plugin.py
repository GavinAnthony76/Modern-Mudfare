"""
WebSocket Plugin for Journey Through Scripture

Handles real-time communication between web client and Evennia server.
Sends game state updates and processes player commands.
"""

import json
import logging
from evennia.server.sessionhandler import SESSIONS
from evennia.utils.utils import inherits_from

logger = logging.getLogger(__name__)


class WebSocketHandler:
    """
    Handles WebSocket connections and messages from the web client.
    """

    @staticmethod
    def get_character_state(character):
        """
        Get complete character state for sending to client.

        Args:
            character: The character object

        Returns:
            dict: Complete character state data
        """
        if not character:
            return None

        # Build inventory list
        inventory = []
        for item in character.contents:
            if not inherits_from(item, "typeclasses.objects.Item"):
                continue

            is_equipped = (
                item == character.db.equipped_weapon or
                item == character.db.equipped_armor
            )

            inventory.append({
                "id": item.key,
                "name": item.get_display_name(character),
                "type": getattr(item.db, "item_type", "misc"),
                "equipped": is_equipped,
                "description": item.db.description or ""
            })

        # Get stats based on class
        character_class = character.db.character_class or "shepherd"

        return {
            "id": character.key,
            "name": character.get_display_name(character),
            "class": character_class,
            "level": character.db.level or 1,
            "stats": {
                "faith": character.db.faith or 5,
                "wisdom": character.db.wisdom or 5,
                "strength": character.db.strength or 5,
                "courage": character.db.courage or 5,
                "righteousness": character.db.righteousness or 5
            },
            "health": {
                "current": character.db.hp or 100,
                "max": character.db.max_hp or 100
            },
            "xp": {
                "current": character.db.xp or 0,
                "next_level": character.db.xp_to_next_level or 100
            },
            "inventory": inventory,
            "currency": character.db.currency or 0,
            "position": {
                "floor": character.db.current_floor or 1,
                "room": character.location.key if character.location else "unknown"
            }
        }

    @staticmethod
    def get_room_state(character, room):
        """
        Get complete room state for sending to client.

        Args:
            character: The character object
            room: The room object

        Returns:
            dict: Complete room state data
        """
        if not room:
            return None

        # Get characters in room
        characters = []
        for obj in room.contents:
            if inherits_from(obj, "typeclasses.characters.Character"):
                characters.append({
                    "id": obj.key,
                    "name": obj.get_display_name(character),
                    "class": obj.db.character_class or "shepherd",
                    "sprite": f"{obj.db.character_class or 'shepherd'}_idle"
                })

        # Get items in room
        objects = []
        for obj in room.contents:
            if inherits_from(obj, "typeclasses.objects.Item"):
                objects.append({
                    "id": obj.key,
                    "name": obj.get_display_name(character),
                    "type": getattr(obj.db, "item_type", "misc"),
                    "sprite": getattr(obj.db, "sprite", "item_default")
                })

        # Get exits
        exits = []
        for exit_obj in room.exits:
            if exit_obj:
                direction = getattr(exit_obj.db, "direction", None)
                if direction:
                    exits.append(direction)

        return {
            "id": room.key,
            "name": room.get_display_name(character),
            "description": room.db.description or room.db.desc or "A place of mystery.",
            "floor": room.db.floor or 1,
            "characters": characters,
            "objects": objects,
            "exits": exits,
            "flavor": getattr(room.db, "flavor", "")
        }

    @staticmethod
    def handle_command(character, command_text):
        """
        Handle a player command.

        Args:
            character: The character object
            command_text: The command string

        Returns:
            dict: Response message
        """
        # Let Evennia's command system handle this
        # The character.execute_cmd will route to the proper command handler
        character.execute_cmd(command_text)

        # Command results are sent back to client via character.msg()
        return {"type": "command_processed", "command": command_text}

    @staticmethod
    def handle_equip(character, item_key, slot):
        """
        Handle equipment of an item.

        Args:
            character: The character object
            item_key: The key of the item to equip
            slot: The equipment slot (weapon, armor, etc.)

        Returns:
            dict: Response message
        """
        # Find the item in inventory
        item = None
        for obj in character.contents:
            if obj.key == item_key:
                item = obj
                break

        if not item:
            return {
                "type": "error",
                "message": f"Item {item_key} not found in inventory"
            }

        # Handle equipping based on slot
        if slot == "weapon":
            # Unequip previous weapon
            if character.db.equipped_weapon:
                character.db.equipped_weapon = None
            # Equip new weapon
            character.db.equipped_weapon = item
            character.msg(f"You equip {item.get_display_name(character)}.")
            return {"type": "equipment_updated", "slot": "weapon", "item": item_key}
        elif slot == "armor":
            if character.db.equipped_armor:
                character.db.equipped_armor = None
            character.db.equipped_armor = item
            character.msg(f"You don {item.get_display_name(character)}.")
            return {"type": "equipment_updated", "slot": "armor", "item": item_key}
        else:
            return {"type": "error", "message": f"Unknown equipment slot: {slot}"}


def at_websocket_message_receive(session, message):
    """
    This hook is called when a WebSocket client sends a message.
    The message has already been validated by Evennia.

    Args:
        session: The player session
        message: The message dict (already parsed from JSON)
    """
    try:
        character = session.puppet
        if not character:
            session.msg({"type": "error", "message": "No character loaded"})
            return

        message_type = message.get("type", "unknown")

        if message_type == "command":
            # Handle a player command
            cmd_text = message.get("text", "").strip()
            if cmd_text:
                WebSocketHandler.handle_command(character, cmd_text)

        elif message_type == "look":
            # Send room description
            room = character.location
            if room:
                character.msg({
                    "type": "text",
                    "text": room.db.description or room.db.desc or "You see nothing special.",
                    "class": "narrative"
                })

        elif message_type == "get_character_state":
            # Send character state
            char_state = WebSocketHandler.get_character_state(character)
            if char_state:
                session.msg({"type": "character_update", "character": char_state})

        elif message_type == "get_room_state":
            # Send room state
            room = character.location
            if room:
                room_state = WebSocketHandler.get_room_state(character, room)
                if room_state:
                    session.msg({"type": "room_update", "room": room_state})

        elif message_type == "equip":
            # Handle equipment
            item_key = message.get("item_key", "")
            slot = message.get("slot", "weapon")
            response = WebSocketHandler.handle_equip(character, item_key, slot)
            session.msg(response)

        elif message_type == "ping":
            # Respond to keepalive
            session.msg({"type": "pong"})

        else:
            logger.warning(f"Unknown WebSocket message type: {message_type}")
            session.msg({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            })

    except Exception as e:
        logger.exception(f"Error handling WebSocket message: {e}")
        try:
            session.msg({
                "type": "error",
                "message": f"Server error: {str(e)}"
            })
        except:
            pass


def at_character_room_change(character, new_room):
    """
    Hook called when a character changes rooms.
    Send updated room state to web client.

    Args:
        character: The character that moved
        new_room: The room they moved to
    """
    try:
        # Get the character's session(s)
        sessions = character.sessions.all()
        for session in sessions:
            # Check if this is a web session
            if hasattr(session, 'ws') and session.ws:
                # Send room update
                room_state = WebSocketHandler.get_room_state(character, new_room)
                if room_state:
                    session.msg({"type": "room_update", "room": room_state})

                # Send character position update
                char_state = WebSocketHandler.get_character_state(character)
                if char_state:
                    session.msg({"type": "character_update", "character": char_state})
    except Exception as e:
        logger.exception(f"Error in at_character_room_change: {e}")


def at_character_stat_change(character, stat_name, old_value, new_value):
    """
    Hook called when a character's stats change.
    Send updated character state to web client.

    Args:
        character: The character
        stat_name: Name of the stat that changed
        old_value: Previous value
        new_value: New value
    """
    try:
        sessions = character.sessions.all()
        for session in sessions:
            if hasattr(session, 'ws') and session.ws:
                char_state = WebSocketHandler.get_character_state(character)
                if char_state:
                    session.msg({"type": "character_update", "character": char_state})
    except Exception as e:
        logger.exception(f"Error in at_character_stat_change: {e}")
