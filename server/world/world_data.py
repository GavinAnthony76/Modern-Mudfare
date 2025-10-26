"""
Journey Through Scripture - World Data
Complete definition of all rooms, floors, and world structure
"""

# FLOOR 1: THE OUTER COURT - Fully Detailed
FLOOR_1_ROOMS = {
    "floor1_approach": {
        "key": "The Approach to the Palace",
        "desc": """A worn stone path leads up to massive bronze gates. Olive trees line both
sides, their leaves rustling in the breeze. The path is well-traveled, marked by countless
pilgrim footsteps over the ages. Ahead, the Palace of Light rises majestically, its white
marble walls gleaming in the sun. Small oil lamps flicker along the path, even in daylight—a
tradition kept by faithful servants.""",
        "floor": 1,
        "room_type": "normal",
        "exits": {
            "forward": "floor1_entrance",
            "north": "floor1_entrance"
        },
        "items": ["worn_walking_staff", "pilgrim_journal", "olive_branch"],
        "npcs": ["elderly_pilgrim"],
        "danger_level": 0,
        "hint": "The beginning of your journey. The air is peaceful here.",
        "lore": """Thousands have walked this path. Some completed their journey. Others turned
back. A few were never seen again.""",
        "ambient_sounds": ["rustling leaves", "distant chanting", "birdsong"]
    },

    "floor1_entrance": {
        "key": "The Entrance Gate",
        "desc": """Massive bronze gates tower three stories high, engraved with intricate scenes
from sacred history—creation, the exodus, prophets receiving visions. The metalwork is
breathtaking, each figure rendered in stunning detail. The gates stand open, welcoming pilgrims.
Beyond them, you see a vast courtyard. To your left, you hear the trickling of water from a
garden. A stone inscription above reads: 'Enter with reverence, seek with humility, find with joy.'""",
        "floor": 1,
        "room_type": "normal",
        "exits": {
            "back": "floor1_approach",
            "south": "floor1_approach",
            "through gate": "floor1_courtyard",
            "north": "floor1_courtyard",
            "west": "floor1_garden"
        },
        "items": ["bronze_gate_fragment", "offering_bowl", "temple_map"],
        "npcs": ["gate_keeper_samuel"],
        "danger_level": 0,
        "hint": "The threshold between the outer world and sacred space.",
        "lore": """These gates were forged in ancient times and have never been forced closed.
It is said they will only shut when darkness finally claims the world.""",
        "ambient_sounds": ["echoing footsteps", "creaking metal", "courtyard sounds"]
    },

    "floor1_courtyard": {
        "key": "Courtyard of Beginnings",
        "desc": """A vast open courtyard paved with smooth white stones, each one inscribed with
a pilgrim's name and date of entry. In the center stands a bronze fountain depicting seven
streams of water flowing from a central basin—representing the seven floors above. Pilgrims
gather here in small groups, some praying, others conversing. Columned walkways line three sides
of the courtyard. To the north, stairs lead upward to a rest area. East leads to a hall, west
to gardens.""",
        "floor": 1,
        "room_type": "normal",
        "exits": {
            "south": "floor1_entrance",
            "north": "floor1_pilgrim_rest",
            "up": "floor1_pilgrim_rest",
            "east": "floor1_hall_testing",
            "west": "floor1_garden"
        },
        "items": ["inscribed_stone", "fountain_water", "forgotten_coin", "prayer_shawl"],
        "npcs": ["young_priest", "water_bearer", "various_pilgrims"],
        "danger_level": 1,
        "hint": "The heart of the outer court. Many paths diverge from here.",
        "lore": """Every pilgrim who enters the palace has their name added to these stones.
Somewhere here, your name will be written.""",
        "ambient_sounds": ["splashing fountain", "murmured prayers", "footsteps", "laughter"]
    },

    "floor1_pilgrim_rest": {
        "key": "The Pilgrim's Rest",
        "desc": """A peaceful chamber with cushioned benches lining the walls. Woven tapestries
depict pilgrims' journeys—some triumphant, others cautionary. A stone altar stands at the far
end, seven candles burning eternally upon it. The air smells of frankincense and myrrh. Priest
Ezra tends the altar, ready to assist weary travelers. Sleeping mats are rolled in one corner.
A small shelf holds scrolls and supplies. This is a place of sanctuary—no violence can occur here.""",
        "floor": 1,
        "room_type": "safe",
        "exits": {
            "down": "floor1_courtyard",
            "south": "floor1_courtyard"
        },
        "items": ["healing_bread", "clean_water", "scroll_of_psalms", "sleeping_mat", "anointing_oil"],
        "npcs": ["priest_ezra"],
        "danger_level": 0,
        "hint": "Perfect peace resides here. Rest, save your journey, and be healed.",
        "lore": """This chamber has provided refuge for ten thousand years. Not even the darkest
forces can breach its sanctity.""",
        "ambient_sounds": ["crackling candles", "soft breathing", "pages turning", "hymns"],
        "is_save_point": True
    },

    "floor1_garden": {
        "key": "Garden of Reflection",
        "desc": """A lush garden enclosed by stone walls covered in climbing jasmine. Fig trees
provide shade over stone benches. A small reflecting pool mirrors the sky perfectly. Herbs grow
in neat rows—rosemary, hyssop, mint. The air is thick with floral scent. This garden is meant
for meditation and quiet contemplation. A few pilgrims sit in silence. A narrow path at the far
end leads to a more secluded area.""",
        "floor": 1,
        "room_type": "normal",
        "exits": {
            "east": "floor1_courtyard",
            "north": "floor1_entrance",
            "narrow path": "floor1_hidden_alcove",
            "hidden": "floor1_hidden_alcove"
        },
        "items": ["fresh_figs", "hyssop_branch", "gardening_tools", "meditation_stone", "pressed_flower"],
        "npcs": ["garden_keeper_ruth", "meditating_pilgrim"],
        "danger_level": 0,
        "hint": "A place of peace and growth. Look carefully—gardens hide secrets.",
        "lore": """It is said that those who truly see themselves in the pool's reflection gain
wisdom. Most see only their face.""",
        "ambient_sounds": ["buzzing bees", "rustling leaves", "trickling water", "birdsong"]
    },

    "floor1_hall_testing": {
        "key": "Hall of Testing",
        "desc": """A long colonnade hall with marble pillars on both sides. The floor is polished
stone that reflects like glass. Along the walls, bronze plaques commemorate pilgrims who completed
great trials. The hall feels more serious than the courtyard—this is where pilgrims prove their
readiness. Small alcoves between pillars contain statues of ancient teachers. At the far end, an
archway leads to what sounds like a bustling market area.""",
        "floor": 1,
        "room_type": "normal",
        "exits": {
            "west": "floor1_courtyard",
            "east": "floor1_merchant_corner",
            "through archway": "floor1_merchant_corner"
        },
        "items": ["bronze_plaque_rubbing", "testing_scroll", "previous_pilgrim_weapon", "incense_burner"],
        "npcs": ["stern_teacher", "confused_pilgrim"],
        "enemies": ["confused_pilgrim_hostile"],
        "danger_level": 2,
        "hint": "Tests come in many forms. Not all require combat.",
        "lore": """The Hall of Testing has claimed the unprepared, but never the humble. Pride has
felled more pilgrims here than any blade.""",
        "ambient_sounds": ["echoing footsteps", "whispered debates", "shuffling robes", "distant haggling"]
    },

    "floor1_merchant_corner": {
        "key": "Merchant's Corner",
        "desc": """A bustling alcove where merchants have set up shop beneath colorful awnings.
The smell of spices, leather, and fresh bread mingles in the air. Merchants call out their
wares—travel supplies, religious items, food, and curiosities. Not all merchants are honest;
some peddle fake relics or overcharge desperate pilgrims. Tables are laden with goods. A few
pilgrims browse and haggle. A suspicious narrow door in the back corner is easy to miss among
the chaos.""",
        "floor": 1,
        "room_type": "normal",
        "exits": {
            "west": "floor1_hall_testing",
            "back": "floor1_hall_testing",
            "hidden door": "floor1_hidden_alcove",
            "secret": "floor1_hidden_alcove"
        },
        "items": ["overpriced_relic", "fresh_bread", "travel_supplies", "mysterious_key", "spice_pouch"],
        "npcs": ["honest_merchant_deborah", "corrupt_merchant_zadok"],
        "enemies": ["corrupt_merchant_zadok"],
        "danger_level": 3,
        "hint": "Not all dangers are physical. Guard your coin and your trust.",
        "lore": """Commerce in the temple has always been controversial. Some merchants serve,
others exploit. Discernment is required.""",
        "ambient_sounds": ["haggling voices", "clinking coins", "rustling fabric", "merchant calls"]
    },

    "floor1_hidden_alcove": {
        "key": "Hidden Alcove of Secrets",
        "desc": """A small, secret chamber accessible only through the narrow garden path or the
hidden merchant door. Stone walls are lined with shelves holding ancient scrolls and forgotten
artifacts. Dust motes dance in a shaft of light from a high window. This place feels untouched
by time. A small writing desk holds a journal—entries from pilgrims who discovered this place.
Most notably, a locked chest sits in the corner, and a passage leads downward deeper into the
palace structure—toward the boss chamber.""",
        "floor": 1,
        "room_type": "hidden",
        "exits": {
            "garden": "floor1_garden",
            "west": "floor1_garden",
            "merchant door": "floor1_merchant_corner",
            "east": "floor1_merchant_corner",
            "down": "floor1_boss_chamber",
            "passage": "floor1_boss_chamber"
        },
        "items": ["ancient_scroll", "pilgrim_journal_collection", "silver_key", "rare_herb",
                  "forgotten_sword", "cryptic_map"],
        "npcs": ["ghost_of_past_pilgrim"],
        "danger_level": 1,
        "hint": "Secrets are rewarded to the curious and observant.",
        "lore": """This alcove was built by the first pilgrims as a place to record their discoveries.
Few find it. Fewer still understand what they find here.""",
        "ambient_sounds": ["silence", "distant echoes", "creaking", "phantom quills"]
    },

    "floor1_boss_chamber": {
        "key": "Chamber of the Deceiver",
        "desc": """A circular chamber with a domed ceiling painted with stars that seem to move.
The Deceiver stands at the center on a raised platform, surrounded by confused pilgrims sitting
in a trance. False scriptures hang on the walls—twisted versions of truth. Braziers burn with
sickly green flame. The air feels thick, oppressive. This false prophet has been leading pilgrims
astray, and now blocks your progress upward. The stairs to Floor 2 are visible behind him, locked
by his presence. This is your first true test.""",
        "floor": 1,
        "room_type": "boss",
        "exits": {
            "up": "floor1_hidden_alcove",
            "back": "floor1_hidden_alcove"
        },
        "items": ["false_scripture", "brazier_ash", "deceiver_staff"],
        "npcs": ["the_deceiver"],
        "enemies": ["the_deceiver"],
        "boss": "the_deceiver",
        "danger_level": 5,
        "hint": "The first great trial. You cannot proceed without facing him—in combat or in truth.",
        "lore": """The Deceiver was once a true teacher, but pride corrupted him. Now he feeds on
the devotion of those he misleads. Defeat him with blade or with truth.""",
        "ambient_sounds": ["eerie chanting", "crackling flames", "smooth voice", "whispers"],
        "locked_exit": {
            "direction": "stairs up",
            "unlocks_to": "floor2_ascending_stairs",
            "requires": "defeated_the_deceiver"
        }
    }
}

# FLOOR 2: THE COURT OF WISDOM
FLOOR_2_ROOMS = {
    "floor2_ascending_stairs": {
        "key": "Ascending Stairway to Wisdom",
        "desc": """Marble stairs wind upward from Floor 1. The walls display carved teachings and
proverbs. Each step is inscribed with a word of wisdom. The air grows quieter, more contemplative
as you climb.""",
        "floor": 2,
        "room_type": "normal",
        "exits": {
            "down": "floor1_boss_chamber",
            "up": "floor2_library"
        },
        "danger_level": 0
    },

    "floor2_library": {
        "key": "Library of Sacred Scrolls",
        "desc": """Endless shelves of scrolls and codices line the walls of this vast library.
Scribes work silently at desks. Priest Miriam tends the altar at the center, surrounded by
candles. The smell of parchment and ink fills the air. This is a place of study and sanctuary.""",
        "floor": 2,
        "room_type": "safe",
        "exits": {
            "down": "floor2_ascending_stairs",
            "east": "floor2_debate_hall"
        },
        "npcs": ["priest_miriam", "scribes"],
        "items": ["ancient_texts", "writing_supplies", "illuminated_manuscript"],
        "danger_level": 0,
        "is_save_point": True
    },

    "floor2_debate_hall": {
        "key": "Hall of Debate",
        "desc": """A circular room with tiered seating rising toward the ceiling. In the center,
a speaking platform. Scholars and pilgrims engage in theological debates here. Some debates are
friendly; others grow heated. A false teacher occasionally appears, challenging truth with clever lies.""",
        "floor": 2,
        "room_type": "normal",
        "exits": {
            "west": "floor2_library",
            "up": "floor3_ascending_stairs"
        },
        "npcs": ["scholar_teachers", "false_teacher"],
        "enemies": ["false_teacher"],
        "danger_level": 4
    }
}

# FLOOR 3: THE COURT OF SERVICE
FLOOR_3_ROOMS = {
    "floor3_ascending_stairs": {
        "key": "Servants' Stairway",
        "desc": """Unlike the grand stairs below, these are simple stone steps worn smooth by
countless servants carrying supplies upward. The walls are plain but clean. Sounds of hammering
and cooking drift from above.""",
        "floor": 3,
        "room_type": "normal",
        "exits": {
            "down": "floor2_debate_hall",
            "up": "floor3_workshop"
        },
        "danger_level": 0
    },

    "floor3_workshop": {
        "key": "Workshop of Sacred Crafts",
        "desc": """Craftsmen labor here creating items for the temple—candle holders, altar cloths,
tools. The sound of hammering metal and sawing wood fills the air. A master craftsman oversees
the work. Some items here are needed for your quest to furnish the sanctuary.""",
        "floor": 3,
        "room_type": "normal",
        "exits": {
            "down": "floor3_ascending_stairs",
            "east": "floor3_healing_chambers"
        },
        "npcs": ["master_craftsman", "apprentices"],
        "items": ["bronze_tools", "unfinished_altar_piece", "sacred_lamp"],
        "danger_level": 2
    },

    "floor3_healing_chambers": {
        "key": "Healing Chambers of Compassion",
        "desc": """A warm, well-lit room with beds for the sick and injured. Herbs hang drying
from the ceiling. Priest-Healer Tobias tends to patients with gentle care. The altar here is
surrounded by medicinal supplies. The air smells of healing herbs and incense.""",
        "floor": 3,
        "room_type": "safe",
        "exits": {
            "west": "floor3_workshop",
            "north": "floor3_kitchen"
        },
        "npcs": ["priest_tobias", "herbalist"],
        "items": ["medicinal_herbs", "healing_ointment", "bandages"],
        "danger_level": 0,
        "is_save_point": True
    },

    "floor3_kitchen": {
        "key": "Temple Kitchen & Storehouse",
        "desc": """A bustling kitchen where bread is baked and offerings prepared. Large clay ovens,
grinding stones, storage jars of grain and oil. The smell is heavenly. Servants work efficiently.
A greedy steward sometimes hoards supplies meant for pilgrims.""",
        "floor": 3,
        "room_type": "normal",
        "exits": {
            "south": "floor3_healing_chambers",
            "up": "floor4_ascending_stairs"
        },
        "npcs": ["head_cook", "greedy_steward"],
        "enemies": ["greedy_steward"],
        "items": ["fresh_bread", "olive_oil", "grain", "cooking_supplies"],
        "danger_level": 3
    }
}

# FLOOR 4-7: Sketched rooms (can expand later)
FLOOR_4_ROOMS = {
    "floor4_ascending_stairs": {
        "key": "Darkening Stairway",
        "desc": """The stairs here are steeper, narrower. Light seems dimmer. The carvings on walls
shift from encouraging to warning. You sense you're entering more dangerous territory.""",
        "floor": 4,
        "room_type": "normal",
        "exits": {"down": "floor3_kitchen", "up": "floor4_prayer_sanctuary"},
        "danger_level": 5
    },
    "floor4_prayer_sanctuary": {
        "key": "Sanctuary of Deep Prayer",
        "desc": """A stark, simple room with stone walls and a single altar. Priest-Warrior Caleb
kneels in constant prayer. This is a place for serious spiritual preparation before facing greater trials.""",
        "floor": 4,
        "room_type": "safe",
        "exits": {"down": "floor4_ascending_stairs", "north": "floor4_trial_chamber"},
        "npcs": ["priest_caleb"],
        "is_save_point": True,
        "danger_level": 0
    },
    "floor4_trial_chamber": {
        "key": "Chamber of Inner Trials",
        "desc": """A dimly lit room where pilgrims face manifestations of their inner struggles—doubt,
fear, pride. Shadowy figures appear, reflecting your weaknesses.""",
        "floor": 4,
        "room_type": "normal",
        "exits": {"south": "floor4_prayer_sanctuary", "up": "floor5_ascending_stairs"},
        "enemies": ["shadow_of_doubt", "manifestation_of_pride"],
        "danger_level": 7
    }
}

FLOOR_5_ROOMS = {
    "floor5_ascending_stairs": {
        "key": "Stairs of Relinquishment",
        "desc": """Each step upward feels heavier. Altars line the stairway where pilgrims have left
behind possessions.""",
        "floor": 5,
        "exits": {"down": "floor4_trial_chamber", "up": "floor5_altar_room"},
        "danger_level": 5
    },
    "floor5_altar_room": {
        "key": "The Altar of Surrender",
        "desc": """A massive stone altar dominates this solemn chamber. Priest-Elder Sarah stands vigil.""",
        "floor": 5,
        "room_type": "safe",
        "exits": {"down": "floor5_ascending_stairs", "forward": "floor5_guardian_gate"},
        "npcs": ["priest_sarah"],
        "is_save_point": True,
        "danger_level": 0
    },
    "floor5_guardian_gate": {
        "key": "The Guardian's Gate",
        "desc": """A formidable angel guards the passage upward. Not hostile, but will not permit
passage without proof of worthy sacrifice.""",
        "floor": 5,
        "exits": {"back": "floor5_altar_room", "up": "floor6_ascending_stairs"},
        "enemies": ["guardian_angel_raphael"],
        "danger_level": 8
    }
}

FLOOR_6_ROOMS = {
    "floor6_ascending_stairs": {
        "key": "Stairway of Visions",
        "desc": """Light and shadow play strangely here. The walls shimmer with prophetic imagery.""",
        "floor": 6,
        "exits": {"down": "floor5_guardian_gate", "up": "floor6_revelation_sanctuary"},
        "danger_level": 6
    },
    "floor6_revelation_sanctuary": {
        "key": "Sanctuary of Unveiled Truth",
        "desc": """A crystalline chamber where light refracts through precious stones. Priest-Seer
Ezekiel interprets visions.""",
        "floor": 6,
        "room_type": "safe",
        "exits": {"down": "floor6_ascending_stairs", "west": "floor6_vision_chamber"},
        "npcs": ["priest_ezekiel"],
        "is_save_point": True,
        "danger_level": 0
    },
    "floor6_vision_chamber": {
        "key": "Chamber of Prophetic Visions",
        "desc": """Reality seems fluid here. Prophetic visions manifest—some true, some false.""",
        "floor": 6,
        "exits": {"east": "floor6_revelation_sanctuary", "up": "floor7_final_stairs"},
        "enemies": ["false_prophet_of_visions"],
        "danger_level": 9
    }
}

FLOOR_7_ROOMS = {
    "floor7_final_stairs": {
        "key": "The Final Ascent",
        "desc": """Pure white marble stairs ascend into brilliant light. Each step requires effort—only
the worthy can climb.""",
        "floor": 7,
        "exits": {"down": "floor6_vision_chamber", "up": "floor7_preparation_chamber"},
        "danger_level": 7
    },
    "floor7_preparation_chamber": {
        "key": "Chamber of Final Preparation",
        "desc": """The last sanctuary before the Holy of Holies. High Priest Aaron stands ready to
perform final rites.""",
        "floor": 7,
        "room_type": "safe",
        "exits": {"down": "floor7_final_stairs", "north": "floor7_veil_chamber"},
        "npcs": ["high_priest_aaron"],
        "is_save_point": True,
        "danger_level": 0
    },
    "floor7_veil_chamber": {
        "key": "The Veil Before the Holy of Holies",
        "desc": """A thick veil separates you from the innermost sanctuary. The final guardian stands
here—a corrupted cherub.""",
        "floor": 7,
        "room_type": "boss",
        "exits": {"south": "floor7_preparation_chamber"},
        "enemies": ["corrupted_cherub"],
        "boss": "corrupted_cherub",
        "danger_level": 10,
        "locked_exit": {
            "direction": "through veil",
            "unlocks_to": "floor7_holy_holies",
            "requires": "defeated_corrupted_cherub"
        }
    },
    "floor7_holy_holies": {
        "key": "The Holy of Holies",
        "desc": """You have arrived. The innermost sanctuary glows with divine presence. The Ark stands
before you, the completed furnishings arranged perfectly. You have fulfilled your calling. Peace beyond
understanding fills this space.""",
        "floor": 7,
        "room_type": "completion",
        "exits": {},
        "danger_level": 0
    }
}

# Combine all rooms
ALL_ROOMS = {}
ALL_ROOMS.update(FLOOR_1_ROOMS)
ALL_ROOMS.update(FLOOR_2_ROOMS)
ALL_ROOMS.update(FLOOR_3_ROOMS)
ALL_ROOMS.update(FLOOR_4_ROOMS)
ALL_ROOMS.update(FLOOR_5_ROOMS)
ALL_ROOMS.update(FLOOR_6_ROOMS)
ALL_ROOMS.update(FLOOR_7_ROOMS)

# Helper function to get room by ID
def get_room(room_id):
    """Get room data by ID"""
    return ALL_ROOMS.get(room_id)

# Helper function to get all rooms on a floor
def get_floor_rooms(floor_number):
    """Get all rooms on a specific floor"""
    return {k: v for k, v in ALL_ROOMS.items() if v.get('floor') == floor_number}

# Helper function to get all safe rooms
def get_safe_rooms():
    """Get all safe room locations"""
    return {k: v for k, v in ALL_ROOMS.items() if v.get('room_type') == 'safe'}
