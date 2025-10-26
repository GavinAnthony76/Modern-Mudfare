"""
Journey Through Scripture - Item Database
All collectible items, equipment, consumables, and quest items
"""

ITEMS = {
    # FLOOR 1 ITEMS - Approach Path
    "worn_walking_staff": {
        "key": "Worn Walking Staff",
        "desc": "A simple wooden staff, weathered from countless journeys. It provides support and can serve as a basic weapon.",
        "item_type": "weapon",
        "stats": {"damage": 3, "strength_bonus": 1},
        "value": 10,
        "weight": 3,
        "usable_by": ["all"]
    },

    "pilgrim_journal": {
        "key": "Pilgrim's Journal",
        "desc": "A leather-bound journal with faded entries from a previous pilgrim. Contains hints about the palace and warnings about trials ahead.",
        "item_type": "lore",
        "value": 5,
        "weight": 1,
        "readable": True,
        "text": """Day 1: I have entered the Palace of Light. The gates are magnificent.
Day 3: Beware the merchant in the corner - not all who trade are honest.
Day 7: I found a hidden place in the garden. Secret knowledge awaits the curious.
Day 10: The Deceiver blocks the way upward. I must prepare myself..."""
    },

    "olive_branch": {
        "key": "Olive Branch",
        "desc": "A fresh olive branch from the trees lining the approach. A symbol of peace.",
        "item_type": "material",
        "value": 2,
        "weight": 0.1
    },

    # Entrance Gate Items
    "bronze_gate_fragment": {
        "key": "Bronze Gate Fragment",
        "desc": "A small piece of bronze that fell from the ancient gates. Beautifully engraved with scriptural scenes.",
        "item_type": "treasure",
        "value": 20,
        "weight": 1
    },

    "offering_bowl": {
        "key": "Offering Bowl",
        "desc": "A stone bowl for placing offerings. Currently empty.",
        "item_type": "container",
        "value": 15,
        "weight": 2
    },

    "temple_map": {
        "key": "Crude Temple Map",
        "desc": "A hand-drawn map sketched by a previous pilgrim. Shows some of Floor 1's layout.",
        "item_type": "map",
        "value": 10,
        "weight": 0.5,
        "reveals": ["floor1_courtyard", "floor1_garden", "floor1_hall_testing"]
    },

    # Courtyard Items
    "inscribed_stone": {
        "key": "Inscribed Stone",
        "desc": "A loose white stone inscribed with a pilgrim's name from 100 years ago: 'Matthias, son of Isaac, Year 1925'",
        "item_type": "lore",
        "value": 5,
        "weight": 2
    },

    "fountain_water": {
        "key": "Fountain Water",
        "desc": "Clear, pure water from the seven-streamed fountain. Refreshing and restorative.",
        "item_type": "consumable",
        "healing": 5,
        "value": 0,
        "weight": 0.5,
        "uses": 1
    },

    "forgotten_coin": {
        "key": "Forgotten Coin",
        "desc": "An old temple shekel lying near the fountain.",
        "item_type": "currency",
        "value": 1,
        "weight": 0.1
    },

    "prayer_shawl": {
        "key": "Prayer Shawl",
        "desc": "A simple white shawl dropped by a pilgrim. Wearing it increases faith.",
        "item_type": "clothing",
        "stats": {"faith_bonus": 2},
        "value": 15,
        "weight": 1
    },

    # Pilgrim's Rest Items (Safe Room)
    "healing_bread": {
        "key": "Healing Bread",
        "desc": "Blessed bread from the altar. Restores health and provides nourishment.",
        "item_type": "consumable",
        "healing": 10,
        "value": 5,
        "weight": 0.5,
        "uses": 1
    },

    "clean_water": {
        "key": "Clean Water",
        "desc": "Pure water from the sanctuary pitcher. Refreshing.",
        "item_type": "consumable",
        "healing": 5,
        "value": 2,
        "weight": 1,
        "uses": 3
    },

    "scroll_of_psalms": {
        "key": "Scroll of Psalms",
        "desc": "An ancient scroll containing sacred psalms. Reading it grants +1 Faith permanently.",
        "item_type": "consumable",
        "value": 30,
        "weight": 1,
        "uses": 1,
        "effect": "faith_permanent_+1"
    },

    "sleeping_mat": {
        "key": "Sleeping Mat",
        "desc": "A rolled mat for resting. Cannot be carried, but provides rest here.",
        "item_type": "furniture",
        "value": 5,
        "weight": 5,
        "immovable": True
    },

    "anointing_oil": {
        "key": "Anointing Oil",
        "desc": "Sacred oil in a small vial. Provides temporary blessing (+2 to all stats for 10 turns).",
        "item_type": "consumable",
        "value": 25,
        "weight": 0.2,
        "uses": 1,
        "effect": "all_stats_+2_10turns"
    },

    # Garden Items
    "fresh_figs": {
        "key": "Fresh Figs",
        "desc": "Ripe figs from the garden tree. Sweet and nourishing.",
        "item_type": "consumable",
        "healing": 3,
        "value": 2,
        "weight": 0.3,
        "uses": 3
    },

    "hyssop_branch": {
        "key": "Hyssop Branch",
        "desc": "A medicinal herb used for cleansing and healing.",
        "item_type": "material",
        "value": 10,
        "weight": 0.2,
        "crafting_ingredient": True
    },

    "gardening_tools": {
        "key": "Gardening Tools",
        "desc": "Simple tools left by the garden keeper. Could be useful.",
        "item_type": "tool",
        "value": 15,
        "weight": 3
    },

    "meditation_stone": {
        "key": "Meditation Stone",
        "desc": "A smooth river stone perfect for meditation. Holding it grants +1 Wisdom.",
        "item_type": "trinket",
        "stats": {"wisdom_bonus": 1},
        "value": 20,
        "weight": 0.5
    },

    "pressed_flower": {
        "key": "Pressed Flower",
        "desc": "A flower pressed as a bookmark in a hidden scroll. Delicate and beautiful.",
        "item_type": "treasure",
        "value": 5,
        "weight": 0.1
    },

    # Hall of Testing Items
    "bronze_plaque_rubbing": {
        "key": "Bronze Plaque Rubbing",
        "desc": "Someone's charcoal rubbing of a commemorative plaque. Shows a pilgrim's achievement.",
        "item_type": "lore",
        "value": 3,
        "weight": 0.2
    },

    "testing_scroll": {
        "key": "Testing Scroll",
        "desc": "A scroll containing a riddle or challenge left for pilgrims.",
        "item_type": "quest",
        "value": 10,
        "weight": 0.5,
        "readable": True,
        "text": "The proud stumble, the humble rise. Strength without wisdom is but a fool's prize."
    },

    "previous_pilgrim_weapon": {
        "key": "Bronze Short Sword",
        "desc": "A serviceable bronze sword left behind by a pilgrim who passed the test.",
        "item_type": "weapon",
        "stats": {"damage": 5, "strength_bonus": 2},
        "value": 30,
        "weight": 4,
        "usable_by": ["warrior", "shepherd"]
    },

    "incense_burner": {
        "key": "Incense Burner",
        "desc": "A bronze burner, still warm with fragrant incense smoke.",
        "item_type": "tool",
        "value": 20,
        "weight": 2
    },

    # Merchant's Corner Items
    "overpriced_relic": {
        "key": "Suspicious Relic",
        "desc": "The merchant swears this is a genuine holy artifact, but it looks like painted clay.",
        "item_type": "junk",
        "value": 1,
        "merchant_price": 50,
        "weight": 1
    },

    "fresh_bread": {
        "key": "Fresh Bread Loaf",
        "desc": "Warm, freshly baked bread. Smells wonderful.",
        "item_type": "consumable",
        "healing": 8,
        "value": 5,
        "weight": 0.8,
        "uses": 2
    },

    "travel_supplies": {
        "key": "Travel Supplies",
        "desc": "A bundle containing rope, torches, and other useful items.",
        "item_type": "equipment",
        "value": 25,
        "weight": 5,
        "contains": ["rope", "torch", "torch", "flint"]
    },

    "mysterious_key": {
        "key": "Mysterious Bronze Key",
        "desc": "An ornate bronze key. The merchant says it opens a hidden door, but is charging a premium.",
        "item_type": "key",
        "value": 30,
        "merchant_price": 75,
        "weight": 0.3,
        "unlocks": "floor1_merchant_corner_hidden_door"
    },

    "spice_pouch": {
        "key": "Pouch of Spices",
        "desc": "Exotic spices from distant lands. Valuable for trading.",
        "item_type": "trade_good",
        "value": 40,
        "weight": 0.5
    },

    # Hidden Alcove Items
    "ancient_scroll": {
        "key": "Ancient Scroll of Wisdom",
        "desc": "A very old scroll containing lost knowledge. Reading it grants +1 Wisdom permanently.",
        "item_type": "consumable",
        "value": 100,
        "weight": 1,
        "uses": 1,
        "effect": "wisdom_permanent_+1"
    },

    "pilgrim_journal_collection": {
        "key": "Collection of Pilgrim Journals",
        "desc": "Multiple journals from past pilgrims who found this secret place. Full of lore.",
        "item_type": "lore",
        "value": 50,
        "weight": 3,
        "readable": True,
        "text": """Many voices across centuries, all seeking the same truth. Some succeeded. Some fell to pride. Some were deceived. The pattern is clear: humility and discernment are the keys to ascending."""
    },

    "silver_key": {
        "key": "Silver Key",
        "desc": "A beautiful silver key found in the locked chest. Needed for upper floors.",
        "item_type": "key",
        "value": 50,
        "weight": 0.3,
        "unlocks": "floor2_special_door"
    },

    "rare_herb": {
        "key": "Rare Healing Herb",
        "desc": "An extremely rare herb with powerful medicinal properties. Restores 25 HP.",
        "item_type": "consumable",
        "healing": 25,
        "value": 60,
        "weight": 0.2,
        "uses": 1
    },

    "forgotten_sword": {
        "key": "Sword of the Faithful",
        "desc": "An exceptional weapon abandoned by a pilgrim long ago. Blessed with divine power.",
        "item_type": "weapon",
        "stats": {"damage": 8, "strength_bonus": 3, "faith_bonus": 2},
        "value": 100,
        "weight": 4,
        "usable_by": ["warrior", "shepherd", "prophet"]
    },

    "cryptic_map": {
        "key": "Cryptic Map of Upper Floors",
        "desc": "A partially complete map showing hints about floors 2-4.",
        "item_type": "map",
        "value": 75,
        "weight": 0.5,
        "reveals": ["floor2_library", "floor3_workshop", "floor4_trial_chamber"]
    },

    # Boss Chamber Items
    "false_scripture": {
        "key": "False Scripture",
        "desc": "A scroll with twisted, corrupted teachings. Dangerous to believe, but studying it reveals the Deceiver's methods.",
        "item_type": "lore",
        "value": 10,
        "weight": 1,
        "readable": True,
        "text": "Truth twisted just enough to lead astray. The lies that destroy are those closest to truth."
    },

    "brazier_ash": {
        "key": "Brazier Ash",
        "desc": "Ash from the sickly green flames. Could be a crafting component.",
        "item_type": "material",
        "value": 15,
        "weight": 0.5,
        "crafting_ingredient": True
    },

    "deceiver_staff": {
        "key": "The Deceiver's Staff",
        "desc": "A twisted staff wielded by the false prophet. Powerful, but using it risks corruption.",
        "item_type": "weapon",
        "stats": {"damage": 10, "wisdom_bonus": 4, "righteousness_penalty": -2},
        "value": 150,
        "weight": 3,
        "usable_by": ["prophet", "scribe"],
        "cursed": True,
        "warning": "Using this staff may corrupt your spirit"
    },

    # FLOOR 2+ ITEMS (Examples - can expand)
    "ancient_texts": {
        "key": "Ancient Religious Texts",
        "desc": "Invaluable scrolls and codices from the Library. Studying them increases wisdom.",
        "item_type": "lore",
        "value": 80,
        "weight": 5,
        "effect": "wisdom_bonus_+2"
    },

    "writing_supplies": {
        "key": "Scribe's Writing Supplies",
        "desc": "High-quality quill, ink, and parchment.",
        "item_type": "tool",
        "value": 30,
        "weight": 2,
        "usable_by": ["scribe"]
    },

    "illuminated_manuscript": {
        "key": "Illuminated Manuscript",
        "desc": "A beautifully illustrated holy text. A masterwork of art and faith.",
        "item_type": "treasure",
        "value": 200,
        "weight": 4
    },

    # Generic Currency
    "temple_shekel": {
        "key": "Temple Shekel",
        "desc": "Standard currency used within the Palace.",
        "item_type": "currency",
        "value": 1,
        "weight": 0.1
    }
}

# Item categories for easy filtering
CONSUMABLES = {k: v for k, v in ITEMS.items() if v.get('item_type') == 'consumable'}
WEAPONS = {k: v for k, v in ITEMS.items() if v.get('item_type') == 'weapon'}
LORE_ITEMS = {k: v for k, v in ITEMS.items() if v.get('item_type') == 'lore'}
QUEST_ITEMS = {k: v for k, v in ITEMS.items() if v.get('item_type') == 'quest'}
KEYS = {k: v for k, v in ITEMS.items() if v.get('item_type') == 'key'}

def get_item(item_id):
    """Get item data by ID"""
    return ITEMS.get(item_id)

def get_items_by_type(item_type):
    """Get all items of a specific type"""
    return {k: v for k, v in ITEMS.items() if v.get('item_type') == item_type}

def get_items_in_room(room_items):
    """Get full item data for a list of item IDs"""
    return {item_id: ITEMS[item_id] for item_id in room_items if item_id in ITEMS}
