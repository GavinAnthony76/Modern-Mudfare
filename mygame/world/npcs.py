"""
Journey Through Scripture - NPC Database
All NPCs with dialogue, quests, and interactions
"""

NPCS = {
    # FLOOR 1 NPCs
    "elderly_pilgrim": {
        "key": "Elderly Pilgrim",
        "desc": "An old pilgrim resting against a tree, looking weary but content.",
        "room": "floor1_approach",
        "npc_type": "friendly",
        "dialogue": {
            "greeting": "Ah, another traveler. I've walked this path many times, young one.",
            "main_menu": {
                1: {"text": "What can you tell me about the Palace?", "response": "tell_about_palace"},
                2: {"text": "Why are you resting here?", "response": "why_resting"},
                3: {"text": "Have you completed your journey?", "response": "journey_status"},
                4: {"text": "Farewell", "response": "farewell"}
            },
            "responses": {
                "tell_about_palace": """The Palace of Light is ancient beyond measure. Seven floors
rise above, each representing a deeper level of spiritual truth. Not all who enter complete the
journey. Some lack the courage. Others the wisdom. The first floor is merely the beginning.""",
                "why_resting": """These old bones need frequent rest! But truly, I stop here to pray
for those who are just beginning their ascent. I've seen too many turn back.""",
                "journey_status": """I have walked all seven floors many times, but the journey is
never complete. There is always more to learn, more to understand. I return to guide others now.""",
                "farewell": "Walk in wisdom, pilgrim. May your path be blessed."
            }
        },
        "quest": None,
        "merchant": False
    },

    "gate_keeper_samuel": {
        "key": "Gate Keeper Samuel",
        "desc": "A dignified man in simple robes stands watch at the gate, welcoming pilgrims with a gentle smile.",
        "room": "floor1_entrance",
        "npc_type": "friendly",
        "dialogue": {
            "greeting": "Welcome, pilgrim, to the Palace of Light. I am Samuel, keeper of the gates.",
            "main_menu": {
                1: {"text": "What is this place?", "response": "explain_palace"},
                2: {"text": "Can you tell me about the inscription?", "response": "inscription"},
                3: {"text": "What should I know before entering?", "response": "advice"},
                4: {"text": "Thank you", "response": "farewell"}
            },
            "responses": {
                "explain_palace": """This is the Palace of Light, a sacred dwelling built in ages past.
It rises seven floors, each representing a court of spiritual ascent. You begin in the Outer Court,
where all are welcome. To climb higher, you must prove yourself worthy through trials, wisdom, and faith.""",
                "inscription": """'Enter with reverence, seek with humility, find with joy.' These
words have welcomed pilgrims for millennia. Remember them. Pride has felled more travelers than
any enemy within these walls.""",
                "advice": """Explore thoroughly. Speak with all you meet. Not every challenge requires
combat—many can be overcome with wisdom and compassion. And remember: the Pilgrim's Rest on each
floor is a sanctuary. Seek them when weary.""",
                "farewell": "Go with peace, and may your journey be fruitful."
            }
        },
        "quest": None,
        "merchant": False
    },

    "young_priest": {
        "key": "Young Priest",
        "desc": "A young priest in white robes teaches a small group of pilgrims about the fountain.",
        "room": "floor1_courtyard",
        "npc_type": "friendly",
        "dialogue": {
            "greeting": "Peace be with you, traveler. Are you new to the Palace?",
            "main_menu": {
                1: {"text": "Tell me about the fountain", "response": "fountain_lore"},
                2: {"text": "What are the seven floors?", "response": "seven_floors"},
                3: {"text": "Continue your teaching", "response": "farewell"}
            },
            "responses": {
                "fountain_lore": """This fountain represents the seven floors above. Each stream
flows from the central basin, representing how all wisdom flows from a single divine source. The
water is pure and healing—pilgrims may drink freely.""",
                "seven_floors": """The seven floors are: The Outer Court (where we stand), the Court
of Wisdom, the Court of Service, the Court of Trial, the Court of Sacrifice, the Court of Revelation,
and finally, the Holy of Holies. Each floor tests and teaches different virtues.""",
                "farewell": "May your studies be blessed."
            }
        },
        "quest": None,
        "merchant": False
    },

    "water_bearer": {
        "key": "Water Bearer",
        "desc": "A servant carrying water jugs to and from the fountain.",
        "room": "floor1_courtyard",
        "npc_type": "neutral",
        "dialogue": {
            "greeting": "Service is the highest calling. How may I help you?",
            "main_menu": {
                1: {"text": "Can I have some water?", "response": "give_water"},
                2: {"text": "You serve faithfully", "response": "about_service"},
                3: {"text": "Continue your work", "response": "farewell"}
            },
            "responses": {
                "give_water": "Of course! Take as much as you need. The fountain never runs dry.",
                "about_service": """Many pilgrims seek glory in the higher floors, but true greatness
is found in humble service. I am content here, providing for those who thirst.""",
                "farewell": "Walk well, pilgrim."
            }
        },
        "quest": None,
        "merchant": False,
        "gives_item": "fountain_water"
    },

    "priest_ezra": {
        "key": "Priest Ezra",
        "desc": "An elderly priest with kind eyes tends the altar with reverent care. His presence radiates peace.",
        "room": "floor1_pilgrim_rest",
        "npc_type": "priest",
        "dialogue": {
            "greeting": "Welcome to the Pilgrim's Rest. You are safe here, child. How may I serve you?",
            "main_menu": {
                1: {"text": "I need healing", "response": "healing"},
                2: {"text": "Can I save my progress here?", "response": "save_game"},
                3: {"text": "Tell me about this sanctuary", "response": "sanctuary_lore"},
                4: {"text": "What is my calling?", "response": "calling", "requires": "defeated_deceiver"},
                5: {"text": "Thank you for your service", "response": "farewell"}
            },
            "responses": {
                "healing": "[GAME ACTION: Heal player to full HP] May the divine light restore you. You are renewed.",
                "save_game": "[GAME ACTION: Save game] Your journey is recorded. You may return to this point if needed.",
                "sanctuary_lore": """This chamber has stood for ten thousand years as a place of
refuge. No evil can enter here—it is protected by ancient wards. Every floor has such a sanctuary,
tended by a priest. Seek them when you are weary.""",
                "calling": """[Only available after defeating The Deceiver] You have proven yourself
in your first trial. Tell me, what path calls to your heart? Are you drawn to Wisdom, Service,
Trial, Sacrifice, or Revelation? Your answer will shape your journey.""",
                "farewell": "Go in peace. Return whenever you need rest."
            }
        },
        "quest": None,
        "merchant": False,
        "services": ["heal", "save", "bless"]
    },

    "garden_keeper_ruth": {
        "key": "Garden Keeper Ruth",
        "desc": "A gentle woman tends the garden with loving care, humming hymns as she works.",
        "room": "floor1_garden",
        "npc_type": "friendly",
        "dialogue": {
            "greeting": "Oh! A visitor. Welcome to my garden. Isn't it beautiful?",
            "main_menu": {
                1: {"text": "Your garden is magnificent", "response": "thank_you"},
                2: {"text": "Can you teach me about the herbs?", "response": "herb_lore"},
                3: {"text": "I notice a narrow path...", "response": "secret_path"},
                4: {"text": "I'll let you return to your work", "response": "farewell"}
            },
            "responses": {
                "thank_you": """Thank you, dear. I've tended it for forty years. Every plant has
a purpose—some for healing, some for teaching, some just for beauty. Gardens are mirrors of the
soul, you know.""",
                "herb_lore": """Ah! Hyssop is for cleansing and healing. Rosemary for remembrance.
Mint for clarity of mind. Take what you need, but use them wisely. Nature's gifts are powerful.""",
                "secret_path": """[She smiles knowingly] The curious are often rewarded. That path
leads to a place few discover. But I'll say no more—some things must be found, not told.""",
                "farewell": "May you bloom where you are planted, dear pilgrim."
            }
        },
        "quest": None,
        "merchant": False
    },

    "meditating_pilgrim": {
        "key": "Meditating Pilgrim",
        "desc": "A pilgrim sits cross-legged by the reflecting pool, eyes closed in deep meditation.",
        "room": "floor1_garden",
        "npc_type": "neutral",
        "dialogue": {
            "greeting": "[Opens eyes slowly] ...Yes?",
            "main_menu": {
                1: {"text": "What are you meditating on?", "response": "meditation"},
                2: {"text": "Sorry to disturb you", "response": "farewell"}
            },
            "responses": {
                "meditation": """The nature of truth. The pool shows only what is—no illusions, no
distortions. I seek to see myself as clearly as the water shows my reflection.""",
                "farewell": "[Closes eyes and returns to silence]"
            }
        },
        "quest": None,
        "merchant": False
    },

    "stern_teacher": {
        "key": "Stern Teacher",
        "desc": "A severe-looking teacher watches pilgrims with critical eyes, testing their readiness.",
        "room": "floor1_hall_testing",
        "npc_type": "neutral",
        "dialogue": {
            "greeting": "So. Another pilgrim seeks to ascend. Do you have what it takes?",
            "main_menu": {
                1: {"text": "What must I do to prove myself?", "response": "test_info"},
                2: {"text": "I'm ready for any test", "response": "test_response"},
                3: {"text": "I'll return when better prepared", "response": "farewell"}
            },
            "responses": {
                "test_info": """Tests come in many forms. Some are of strength, others of wisdom or
character. The greatest test is often recognizing when NOT to fight. Remember that.""",
                "test_response": """Confidence is good. Arrogance is deadly. I've seen too many fall
because they thought themselves ready. Explore thoroughly. Speak to everyone. Learn before you act.""",
                "farewell": "Hmph. At least you know your limits. That's wisdom."
            }
        },
        "quest": None,
        "merchant": False
    },

    "confused_pilgrim": {
        "key": "Confused Pilgrim",
        "desc": "A pilgrim wanders the hall looking lost and agitated, muttering to themselves.",
        "room": "floor1_hall_testing",
        "npc_type": "neutral",
        "dialogue": {
            "greeting": "Who...who are you? Friend or foe? I can't tell anymore!",
            "main_menu": {
                1: {"text": "I'm a friend. What's wrong?", "response": "explain_confusion"},
                2: {"text": "Calm yourself", "response": "calm_attempt"},
                3: {"text": "Back away slowly", "response": "farewell"}
            },
            "responses": {
                "explain_confusion": """[Breathing heavily] The Deceiver...his words...they twist
everything! I don't know what's true anymore. Truth and lies blend together. He's below, in a
hidden chamber. Beware him!""",
                "calm_attempt": "[WISDOM CHECK] You either calm them with soothing words, or they become hostile. Choose your approach carefully.",
                "farewell": "[Continues muttering and pacing]"
            }
        },
        "quest": None,
        "merchant": False
    },

    "honest_merchant_deborah": {
        "key": "Merchant Deborah",
        "desc": "A friendly merchant woman arranges her wares with care, greeting customers warmly.",
        "room": "floor1_merchant_corner",
        "npc_type": "merchant",
        "dialogue": {
            "greeting": "Welcome, traveler! I have supplies for your journey. Fair prices, quality goods!",
            "main_menu": {
                1: {"text": "Show me your wares", "response": "shop"},
                2: {"text": "Tell me about the other merchant", "response": "warn_about_zadok"},
                3: {"text": "Thank you, I'm just looking", "response": "farewell"}
            },
            "responses": {
                "shop": "[GAME ACTION: Open shop interface] Browse at your leisure!",
                "warn_about_zadok": """[Lowers voice] Be careful with Zadok. He sells some fake relics
and overcharges. Not all merchants here are honest. I try to keep my prices fair—I serve pilgrims,
not profit.""",
                "farewell": "Safe travels! Come back anytime."
            }
        },
        "quest": None,
        "merchant": True,
        "shop_inventory": ["fresh_bread", "travel_supplies", "hyssop_branch", "clean_water", "rope"],
        "shop_prices": "fair"
    },

    "corrupt_merchant_zadok": {
        "key": "Merchant Zadok",
        "desc": "A sly-looking merchant with an oily smile, hawking his wares aggressively.",
        "room": "floor1_merchant_corner",
        "npc_type": "merchant_hostile",
        "dialogue": {
            "greeting": "Ah! A new customer! I have RARE artifacts! Once-in-a-lifetime deals!",
            "main_menu": {
                1: {"text": "Show me your rare artifacts", "response": "show_fakes"},
                2: {"text": "These look fake to me", "response": "expose_fraud"},
                3: {"text": "I'll pass", "response": "farewell"}
            },
            "responses": {
                "show_fakes": "[Shows overpriced, fake items] This relic is from the first temple! Only 100 shekels! The mysterious key—opens secret doors! Only 75 shekels!",
                "expose_fraud": """[WISDOM CHECK] If successful, you expose his fraud. He may become
hostile, or flee, depending on your approach. If failed, he convinces others you're the liar.""",
                "farewell": "Your loss! These deals won't last!"
            }
        },
        "quest": None,
        "merchant": True,
        "shop_inventory": ["overpriced_relic", "mysterious_key", "spice_pouch"],
        "shop_prices": "inflated",
        "can_become_hostile": True
    },

    "ghost_of_past_pilgrim": {
        "key": "Faint Apparition",
        "desc": "A translucent figure, barely visible, seems to be writing at the desk.",
        "room": "floor1_hidden_alcove",
        "npc_type": "ghost",
        "dialogue": {
            "greeting": "[A whisper] ...you found it...few do...",
            "main_menu": {
                1: {"text": "Who are you?", "response": "identity"},
                2: {"text": "What is this place?", "response": "alcove_purpose"},
                3: {"text": "Leave the spirit in peace", "response": "farewell"}
            },
            "responses": {
                "identity": """...I was a seeker...like you...I recorded my findings here...so others
might learn...read the journals...heed the warnings...""",
                "alcove_purpose": """...a place of secrets...knowledge hidden from the proud...given
freely to the humble...take what you need...but beware...the Deceiver lies below...""",
                "farewell": "[The apparition fades into silence]"
            }
        },
        "quest": None,
        "merchant": False
    },

    "the_deceiver": {
        "key": "The Deceiver",
        "desc": """A charismatic figure in elaborate robes stands on the platform, radiating false
authority. His voice is smooth and persuasive, but his eyes are empty.""",
        "room": "floor1_boss_chamber",
        "npc_type": "boss",
        "dialogue": {
            "greeting": "Ah, another seeker of truth. But what IS truth, really? Come, sit with my followers. I will teach you...",
            "main_menu": {
                1: {"text": "I challenge your false teachings!", "response": "confront"},
                2: {"text": "Listen to his words", "response": "listen_danger"},
                3: {"text": "Attack immediately", "response": "combat"}
            },
            "responses": {
                "confront": """[WISDOM CHECK] If successful, you expose his lies and break his hold
on the entranced pilgrims. If failed, combat begins. Either way, you must defeat him.""",
                "listen_danger": """[FAITH CHECK] His words are seductive, twisting truth just enough
to mislead. Roll to resist his influence, or become confused yourself!""",
                "combat": "[INITIATE COMBAT] The Deceiver laughs. 'Violence? How primitive. Very well.'"
            }
        },
        "quest": None,
        "merchant": False,
        "boss_stats": {
            "hp": 50,
            "damage": 8,
            "defense": 3,
            "special_ability": "confusion_attack",
            "weakness": "truth_exposure"
        },
        "defeat_unlocks": "floor2_ascending_stairs",
        "defeat_reward": ["deceiver_staff", "experience_100", "access_floor_2"]
    },

    # FLOOR 2+ NPCs (Examples - can expand)
    "priest_miriam": {
        "key": "Priest Miriam",
        "desc": "A scholarly priest surrounded by ancient texts, radiating quiet wisdom.",
        "room": "floor2_library",
        "npc_type": "priest",
        "dialogue": {
            "greeting": "Welcome to the Court of Wisdom, seeker. Knowledge and understanding await you here.",
            "main_menu": {
                1: {"text": "I need healing", "response": "healing"},
                2: {"text": "Can I save my progress?", "response": "save_game"},
                3: {"text": "Tell me about this floor", "response": "floor_info"},
                4: {"text": "May I study here?", "response": "study"},
                5: {"text": "Thank you", "response": "farewell"}
            },
            "responses": {
                "healing": "[GAME ACTION: Heal to full] Be renewed in body and mind.",
                "save_game": "[GAME ACTION: Save] Your progress is preserved.",
                "floor_info": """The Court of Wisdom tests your understanding and discernment. False
teachers will challenge you with twisted logic. Truth must be defended with both knowledge and faith.""",
                "study": """Of course. The scrolls here contain deep wisdom. Study them well—they
will aid you in debates ahead.""",
                "farewell": "Walk in wisdom."
            }
        },
        "services": ["heal", "save", "bless"]
    }
}

# NPC categories
PRIESTS = {k: v for k, v in NPCS.items() if v.get('npc_type') == 'priest'}
MERCHANTS = {k: v for k, v in NPCS.items() if v.get('merchant') == True}
BOSSES = {k: v for k, v in NPCS.items() if v.get('npc_type') == 'boss'}
FRIENDLY_NPCS = {k: v for k, v in NPCS.items() if v.get('npc_type') == 'friendly'}

def get_npc(npc_id):
    """Get NPC data by ID"""
    return NPCS.get(npc_id)

def get_npcs_in_room(room_id):
    """Get all NPCs in a specific room"""
    return {k: v for k, v in NPCS.items() if v.get('room') == room_id}

def get_npc_dialogue(npc_id, dialogue_key):
    """Get specific dialogue from an NPC"""
    npc = NPCS.get(npc_id)
    if npc and 'dialogue' in npc:
        return npc['dialogue'].get(dialogue_key)
    return None
