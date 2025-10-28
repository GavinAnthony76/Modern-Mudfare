"""
Command sets for Journey Through Scripture
"""

from evennia import default_cmds
from commands.dialogue import CmdTalk, CmdSay, CmdAsk, CmdRead, CmdExamine, CmdLore
from commands.character import (CmdStats, CmdInventory, CmdUse, CmdEquip,
                                CmdUnequip, CmdCalling)
from commands.combat import (CmdAttack, CmdDefend, CmdHeal, CmdFlee,
                             CmdCombatStatus, CmdFight)
from commands.quests import CmdQuests, CmdAccept, CmdAbandon, CmdQuestInfo


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
        self.add(CmdCalling())
        # Quest commands
        self.add(CmdQuests())
        self.add(CmdAccept())
        self.add(CmdAbandon())
        self.add(CmdQuestInfo())
        # Combat commands
        self.add(CmdAttack())
        self.add(CmdDefend())
        self.add(CmdHeal())
        self.add(CmdFlee())
        self.add(CmdCombatStatus())
        self.add(CmdFight())
