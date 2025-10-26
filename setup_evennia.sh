#!/bin/bash
#
# Journey Through Scripture - Evennia Setup Script
# Automates the integration of custom files with Evennia
#

echo "=== Journey Through Scripture - Evennia Setup ==="
echo ""

# Check if Python 3.11+ is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"

# Check if Evennia is installed
if ! python3 -c "import evennia" 2>/dev/null; then
    echo ""
    echo "Evennia is not installed. Installing now..."
    pip install evennia
else
    echo "Evennia is already installed"
fi

# Initialize Evennia game directory
if [ ! -d "mygame" ]; then
    echo ""
    echo "Initializing Evennia game directory..."
    evennia --init mygame
else
    echo ""
    echo "Game directory 'mygame' already exists"
fi

# Copy custom files
echo ""
echo "Copying custom files to Evennia structure..."

# Create directories if they don't exist
mkdir -p mygame/typeclasses
mkdir -p mygame/world
mkdir -p mygame/commands

# Copy typeclasses
echo "  - Copying typeclasses..."
cp -r server/typeclasses/* mygame/typeclasses/

# Copy world data
echo "  - Copying world data and builder..."
cp -r server/world/* mygame/world/

# Copy commands
echo "  - Copying commands..."
cp -r server/commands/* mygame/commands/

# Create command set file
echo "  - Creating default command set..."
cat > mygame/commands/default_cmdsets.py << 'EOF'
"""
Command sets for Journey Through Scripture
"""

from evennia import default_cmds
from commands.dialogue import CmdTalk, CmdSay, CmdAsk, CmdRead, CmdExamine, CmdLore
from commands.character import (CmdStats, CmdInventory, CmdUse, CmdEquip,
                                CmdUnequip, CmdQuests, CmdCalling)


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    Extended command set for player characters
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()

        # Add dialogue commands
        self.add(CmdTalk())
        self.add(CmdSay())
        self.add(CmdAsk())
        self.add(CmdRead())
        self.add(CmdExamine())
        self.add(CmdLore())

        # Add character commands
        self.add(CmdStats())
        self.add(CmdInventory())
        self.add(CmdUse())
        self.add(CmdEquip())
        self.add(CmdUnequip())
        self.add(CmdQuests())
        self.add(CmdCalling())
EOF

# Update settings.py
echo "  - Updating Evennia settings..."

# Backup original settings
cp mygame/server/conf/settings.py mygame/server/conf/settings.py.backup

# Add custom settings
cat >> mygame/server/conf/settings.py << 'EOF'

# ===================================================================
# Journey Through Scripture Custom Settings
# ===================================================================

# Set default typeclasses
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"
BASE_OBJECT_TYPECLASS = "typeclasses.objects.Item"

# Starting location
START_LOCATION = "floor1_approach"

# Game branding
SERVERNAME = "Journey Through Scripture"
GAME_SLOGAN = "A Biblical Fantasy MUD"

# Command sets
CMDSET_CHARACTER = "commands.default_cmdsets.CharacterCmdSet"

# Web client
WEBCLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4001
EOF

echo ""
echo "Setup complete! Next steps:"
echo ""
echo "1. Navigate to game directory:"
echo "   cd mygame"
echo ""
echo "2. Run database migrations:"
echo "   evennia migrate"
echo ""
echo "3. Create superuser account:"
echo "   evennia createsuperuser"
echo ""
echo "4. Start the server:"
echo "   evennia start"
echo ""
echo "5. Connect and build the world:"
echo "   Connect to localhost:4000 or http://localhost:4001"
echo "   In-game: @py from world import build_world; build_world.build_all()"
echo ""
echo "See docs/EVENNIA_INTEGRATION.md for complete guide"
echo ""
