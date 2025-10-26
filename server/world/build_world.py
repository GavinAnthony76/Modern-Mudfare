"""
World Builder Script for Journey Through Scripture
Populates the Palace of Light from world_data, items, and npcs modules
"""

from evennia import create_object, search_object
from evennia.utils import logger
from typeclasses.rooms import Room, SafeRoom, BossRoom, HiddenRoom
from typeclasses.objects import Item, Weapon, Consumable, QuestItem, Key
from typeclasses.npcs import NPC, Priest, Merchant, Boss, HostileNPC
from world.world_data import ALL_ROOMS, get_room
from world.items import ITEMS, get_item
from world.npcs import NPCS, get_npc


def build_all():
    """
    Master build function - builds entire world.
    Call this from in-game with: @py world.build_world.build_all()
    """
    logger.log_info("=== BUILDING PALACE OF LIGHT ===")

    # Build in order
    rooms = build_rooms()
    logger.log_info(f"Created {len(rooms)} rooms")

    connect_exits(rooms)
    logger.log_info("Connected all exits")

    items = build_items(rooms)
    logger.log_info(f"Created {len(items)} items")

    npcs = build_npcs(rooms)
    logger.log_info(f"Created {len(npcs)} NPCs")

    logger.log_info("=== WORLD BUILD COMPLETE ===")
    logger.log_info(f"The Palace of Light awaits pilgrims!")

    return rooms, items, npcs


def build_rooms():
    """
    Create all rooms from world_data.

    Returns:
        dict: Mapping of room IDs to room objects
    """
    logger.log_info("Building rooms...")
    room_objects = {}

    for room_id, room_data in ALL_ROOMS.items():
        # Determine room typeclass
        room_type = room_data.get('room_type', 'normal')

        if room_type == 'safe':
            typeclass = SafeRoom
        elif room_type == 'boss':
            typeclass = BossRoom
        elif room_type == 'hidden':
            typeclass = HiddenRoom
        else:
            typeclass = Room

        # Create the room
        room = create_object(
            typeclass,
            key=room_data['key'],
            aliases=[room_id]
        )

        # Set room attributes
        room.db.desc = room_data.get('desc', '')
        room.db.floor = room_data.get('floor', 1)
        room.db.room_type = room_type
        room.db.danger_level = room_data.get('danger_level', 0)
        room.db.hint = room_data.get('hint', '')
        room.db.lore = room_data.get('lore', '')
        room.db.ambient_sounds = room_data.get('ambient_sounds', [])
        room.db.is_save_point = room_data.get('is_save_point', False)

        # Boss room specific
        if room_type == 'boss' and 'locked_exit' in room_data:
            locked = room_data['locked_exit']
            room.db.locked_exit_direction = locked.get('direction')
            room.db.locked_exit_destination = locked.get('unlocks_to')

        room_objects[room_id] = room

        logger.log_info(f"  Created: {room_data['key']} ({room_id})")

    return room_objects


def connect_exits(room_objects):
    """
    Connect all room exits.

    Args:
        room_objects (dict): Mapping of room IDs to room objects
    """
    logger.log_info("Connecting exits...")

    for room_id, room_data in ALL_ROOMS.items():
        room = room_objects.get(room_id)
        if not room:
            continue

        exits = room_data.get('exits', {})

        for exit_name, destination_id in exits.items():
            # Skip special exits that aren't actual rooms
            if destination_id.startswith('['):
                continue

            destination = room_objects.get(destination_id)
            if not destination:
                logger.log_warn(f"  Exit '{exit_name}' in {room_id} points to non-existent room: {destination_id}")
                continue

            # Create the exit
            exit_obj = create_object(
                "evennia.objects.objects.DefaultExit",
                key=exit_name,
                location=room,
                destination=destination
            )

            # Check if this is a locked exit (boss room)
            if hasattr(room.db, 'locked_exit_direction') and \
               room.db.locked_exit_direction and \
               exit_name == room.db.locked_exit_direction:
                # Lock the exit
                exit_obj.locks.add("traverse:false()")
                exit_obj.db.locked = True
                exit_obj.db.lock_msg = "The way is blocked by a powerful presence."

    logger.log_info("  All exits connected")


def build_items(room_objects):
    """
    Create all items and place them in rooms.

    Args:
        room_objects (dict): Mapping of room IDs to room objects

    Returns:
        list: All created item objects
    """
    logger.log_info("Building items...")
    item_objects = []

    # Track which items to create in which rooms
    for room_id, room_data in ALL_ROOMS.items():
        room = room_objects.get(room_id)
        if not room:
            continue

        item_ids = room_data.get('items', [])

        for item_id in item_ids:
            item_data = ITEMS.get(item_id)
            if not item_data:
                logger.log_warn(f"  Item {item_id} not found in items database")
                continue

            # Determine item typeclass
            item_type = item_data.get('item_type', 'material')

            if item_type == 'weapon':
                typeclass = Weapon
            elif item_type == 'consumable':
                typeclass = Consumable
            elif item_type == 'quest':
                typeclass = QuestItem
            elif item_type == 'key':
                typeclass = Key
            else:
                typeclass = Item

            # Create the item
            item = create_object(
                typeclass,
                key=item_data['key'],
                location=room,
                aliases=[item_id]
            )

            # Set item attributes
            item.db.desc = item_data.get('desc', '')
            item.db.item_type = item_type
            item.db.value = item_data.get('value', 0)
            item.db.weight = item_data.get('weight', 1.0)
            item.db.stats = item_data.get('stats', {})
            item.db.healing = item_data.get('healing', 0)
            item.db.uses = item_data.get('uses', 1)
            item.db.usable_by = item_data.get('usable_by', ['all'])
            item.db.readable = item_data.get('readable', False)
            item.db.text = item_data.get('text', '')
            item.db.cursed = item_data.get('cursed', False)
            item.db.effect = item_data.get('effect', None)

            # Key specific
            if item_type == 'key':
                item.db.unlocks = item_data.get('unlocks', '')

            item_objects.append(item)

    logger.log_info(f"  Created {len(item_objects)} items")
    return item_objects


def build_npcs(room_objects):
    """
    Create all NPCs and place them in rooms.

    Args:
        room_objects (dict): Mapping of room IDs to room objects

    Returns:
        list: All created NPC objects
    """
    logger.log_info("Building NPCs...")
    npc_objects = []

    for npc_id, npc_data in NPCS.items():
        room_id = npc_data.get('room')
        room = room_objects.get(room_id)

        if not room:
            logger.log_warn(f"  NPC {npc_id} has invalid room: {room_id}")
            continue

        # Determine NPC typeclass
        npc_type = npc_data.get('npc_type', 'friendly')

        if npc_type == 'priest':
            typeclass = Priest
        elif npc_type == 'merchant' or npc_data.get('merchant'):
            typeclass = Merchant
        elif npc_type == 'boss':
            typeclass = Boss
        elif npc_type == 'hostile':
            typeclass = HostileNPC
        else:
            typeclass = NPC

        # Create the NPC
        npc = create_object(
            typeclass,
            key=npc_data['key'],
            location=room,
            aliases=[npc_id]
        )

        # Set NPC attributes
        npc.db.desc = npc_data.get('desc', '')
        npc.db.npc_type = npc_type
        npc.db.dialogue = npc_data.get('dialogue', {})
        npc.db.quest = npc_data.get('quest', None)
        npc.db.merchant = npc_data.get('merchant', False)
        npc.db.shop_inventory = npc_data.get('shop_inventory', [])
        npc.db.shop_prices = npc_data.get('shop_prices', 'fair')
        npc.db.services = npc_data.get('services', [])
        npc.db.can_become_hostile = npc_data.get('can_become_hostile', False)

        # Boss specific
        if npc_type == 'boss' and 'boss_stats' in npc_data:
            stats = npc_data['boss_stats']
            npc.db.hp = stats.get('hp', 100)
            npc.db.max_hp = stats.get('hp', 100)
            npc.db.damage = stats.get('damage', 15)
            npc.db.defense = stats.get('defense', 5)
            npc.db.defeat_unlocks = npc_data.get('defeat_unlocks', '')
            npc.db.defeat_reward = npc_data.get('defeat_reward', [])

        npc_objects.append(npc)

        logger.log_info(f"  Created: {npc_data['key']} in {room.key}")

    logger.log_info(f"  Created {len(npc_objects)} NPCs")
    return npc_objects


def reset_world():
    """
    Destroy all rooms, items, and NPCs for a fresh rebuild.
    USE WITH CAUTION!
    """
    logger.log_warn("=== RESETTING WORLD ===")

    # Delete all custom rooms
    for room_id in ALL_ROOMS.keys():
        rooms = search_object(room_id, typeclass=Room)
        for room in rooms:
            logger.log_info(f"  Deleting room: {room.key}")
            room.delete()

    # Delete all items
    for item_id in ITEMS.keys():
        items = search_object(item_id, typeclass=Item)
        for item in items:
            logger.log_info(f"  Deleting item: {item.key}")
            item.delete()

    # Delete all NPCs
    for npc_id in NPCS.keys():
        npcs = search_object(npc_id, typeclass=NPC)
        for npc in npcs:
            logger.log_info(f"  Deleting NPC: {npc.key}")
            npc.delete()

    logger.log_warn("=== WORLD RESET COMPLETE ===")


def get_start_location():
    """
    Get the starting room for new characters.

    Returns:
        Room: The Approach Path (floor1_approach)
    """
    rooms = search_object("floor1_approach")
    if rooms:
        return rooms[0]

    # Fallback to Limbo
    limbo = search_object("Limbo")
    if limbo:
        return limbo[0]

    return None


# Convenience functions for in-game use

def build():
    """Quick alias for build_all()"""
    return build_all()


def rebuild():
    """Reset and rebuild the world"""
    reset_world()
    return build_all()
