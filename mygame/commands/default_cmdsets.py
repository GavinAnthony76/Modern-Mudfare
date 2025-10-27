﻿"""
Command sets for Journey Through Scripture
"""

from evennia import default_cmds
from commands.dialogue import CmdTalk, CmdSay, CmdAsk, CmdRead, CmdExamine, CmdLore
from commands.character import (CmdStats, CmdInventory, CmdUse, CmdEquip,
                                CmdUnequip, CmdQuests, CmdCalling)


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdTalk())
        self.add(CmdSay())
        self.add(CmdAsk())
        self.add(CmdRead())
        self.add(CmdExamine())
        self.add(CmdLore())
        self.add(CmdStats())
        self.add(CmdInventory())
        self.add(CmdUse())
        self.add(CmdEquip())
        self.add(CmdUnequip())
        self.add(CmdQuests())
        self.add(CmdCalling())
