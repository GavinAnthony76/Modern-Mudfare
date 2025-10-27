"""
Dialogue and NPC interaction commands for Journey Through Scripture
"""

from evennia import Command


class CmdTalk(Command):
    """
    Talk to an NPC to start a dialogue.

    Usage:
        talk <npc>
        talk to <npc>

    This initiates a conversation with an NPC, showing their dialogue options.
    """

    key = "talk"
    aliases = ["speak", "talk to", "speak to"]
    locks = "cmd:all()"
    help_category = "Dialogue"

    def parse(self):
        """Parse the command"""
        self.target = self.args.strip()
        # Remove 'to' if present
        if self.target.startswith("to "):
            self.target = self.target[3:].strip()

    def func(self):
        """Execute the talk command"""
        if not self.target:
            self.caller.msg("Talk to whom?")
            return

        # Find the NPC in the room
        npc = self.caller.search(self.target, location=self.caller.location)

        if not npc:
            return

        # Check if it's an NPC
        if not hasattr(npc, 'talk_to'):
            self.caller.msg(f"{npc.name} doesn't seem interested in conversation.")
            return

        # Start dialogue
        npc.talk_to(self.caller)


class CmdSay(Command):
    """
    Respond to an NPC in dialogue.

    Usage:
        say <number>
        <number>

    When in dialogue with an NPC, use this to choose a dialogue option.
    You can just type the number without 'say'.
    """

    key = "say"
    aliases = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    locks = "cmd:all()"
    help_category = "Dialogue"

    def func(self):
        """Execute the say command"""
        # Check if in dialogue
        if not self.caller.db.talking_to:
            # If not in dialogue and user just typed a number, ignore
            if self.cmdstring in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                return
            self.caller.msg("You are not in a conversation.")
            return

        # Get the choice (either from args or from the command itself)
        choice = self.args.strip() if self.args.strip() else self.cmdstring

        # Validate choice is a number
        try:
            choice_num = int(choice)
        except ValueError:
            self.caller.msg("Please enter a number.")
            return

        # Pass to NPC
        npc = self.caller.db.talking_to
        npc.respond(self.caller, choice_num)


class CmdAsk(Command):
    """
    Ask an NPC about something.

    Usage:
        ask <npc> about <topic>

    Ask an NPC about a specific topic. Some NPCs have special knowledge about certain subjects.
    """

    key = "ask"
    locks = "cmd:all()"
    help_category = "Dialogue"

    def parse(self):
        """Parse the command"""
        parts = self.args.split(" about ")
        if len(parts) == 2:
            self.target = parts[0].strip()
            self.topic = parts[1].strip()
        else:
            self.target = ""
            self.topic = ""

    def func(self):
        """Execute the ask command"""
        if not self.target or not self.topic:
            self.caller.msg("Usage: ask <npc> about <topic>")
            return

        # Find the NPC
        npc = self.caller.search(self.target, location=self.caller.location)
        if not npc:
            return

        # Check if NPC has knowledge of topic
        if hasattr(npc.db, 'knowledge') and self.topic.lower() in npc.db.knowledge:
            response = npc.db.knowledge[self.topic.lower()]
            self.caller.msg(f"{npc.name} says, \"{response}\"")
        else:
            self.caller.msg(f"{npc.name} doesn't seem to know about {self.topic}.")


class CmdRead(Command):
    """
    Read a book, scroll, or other readable item.

    Usage:
        read <item>

    Read an item in your inventory or in the current room. Many items contain valuable lore and hints.
    """

    key = "read"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Execute the read command"""
        if not self.args:
            self.caller.msg("Read what?")
            return

        # Search for item in inventory or room
        item = self.caller.search(
            self.args,
            location=[self.caller, self.caller.location],
            nofound_string=f"You don't see '{self.args}' here."
        )

        if not item:
            return

        # Try to read it
        if hasattr(item, 'read'):
            item.read(self.caller)
        else:
            self.caller.msg(f"You cannot read {item.name}.")


class CmdExamine(Command):
    """
    Examine something closely.

    Usage:
        examine <object>
        ex <object>

    Look at something in detail. This may reveal hidden properties or information.
    """

    key = "examine"
    aliases = ["ex", "inspect"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Execute the examine command"""
        if not self.args:
            self.caller.msg("Examine what?")
            return

        # Search for object
        obj = self.caller.search(
            self.args,
            location=[self.caller, self.caller.location]
        )

        if not obj:
            return

        # Show detailed appearance
        self.caller.msg(obj.return_appearance(self.caller))

        # Check for special examine text
        if hasattr(obj.db, 'examine_text'):
            self.caller.msg(f"\n{obj.db.examine_text}")


class CmdLore(Command):
    """
    View the lore of your current location.

    Usage:
        lore

    Reveals the deeper history and significance of the room you're in.
    """

    key = "lore"
    aliases = ["history", "story"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Execute the lore command"""
        room = self.caller.location

        if hasattr(room, 'get_lore'):
            lore_text = room.get_lore()
            self.caller.msg(f"\n|w=== LORE ===|n")
            self.caller.msg(lore_text)
            self.caller.msg("|w" + "=" * 40 + "|n\n")
        else:
            self.caller.msg("This place holds no special lore.")
