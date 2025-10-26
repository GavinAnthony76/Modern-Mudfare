# Setup Guide - Journey Through Scripture

This guide will walk you through setting up the Biblical Fantasy MUD on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package manager (included with Python 3.4+)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Modern-Mudfare.git
cd Modern-Mudfare
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies:

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when the virtual environment is active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Evennia and all required dependencies.

### 4. Initialize Evennia

First-time setup requires initializing the Evennia game directory:

```bash
evennia --init server
```

This creates the `server/` directory with all necessary Evennia files.

### 5. Configure Database

Run Django migrations to set up the database:

```bash
cd server
evennia migrate
```

### 6. Create Admin Account

Create your superuser account (admin):

```bash
evennia createsuperuser
```

Follow the prompts to set:
- Username
- Email (optional)
- Password

### 7. Start the Server

```bash
evennia start
```

You should see output indicating the server is running:
```
Evennia Server started!
Portal started!
```

To check server status:
```bash
evennia status
```

To stop the server:
```bash
evennia stop
```

## Accessing the Game

### Option 1: Custom Graphical Client (Recommended)

1. Open `web/index.html` in your web browser
2. Click "New Character" to create your character
3. Enter a name and select a class
4. Begin your journey!

**Note**: If the Evennia server is not running, the client will work in offline demo mode with limited functionality.

### Option 2: Evennia Default Web Client

Visit: `http://localhost:4001`

This provides Evennia's standard text-based web interface.

### Option 3: Telnet Client

Connect via telnet:
```bash
telnet localhost 4000
```

## VS Code Setup (Recommended)

### Install Extensions

1. Open VS Code
2. Install recommended extensions:
   - Python (Microsoft)
   - Pylance
   - Live Server (for web client testing)

### Configure Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

### Open Project in VS Code

```bash
code .
```

## Troubleshooting

### Port Already in Use

If ports 4000 or 4001 are already in use:

1. Edit `server/server/settings.py`
2. Change `WEBSERVER_PORTS` and `AMP_PORT`
3. Restart the server

### Database Errors

If you encounter database issues:

```bash
cd server
evennia migrate
```

### Python Version Issues

Ensure you're using Python 3.11+:

```bash
python --version
```

### Permission Errors

On Linux/macOS, you may need to make scripts executable:

```bash
chmod +x venv/bin/evennia
```

## Development Workflow

### Making Changes

1. Edit game files in `server/world/`, `server/commands/`, etc.
2. Reload the server to apply changes:
   ```bash
   evennia reload
   ```

### Viewing Logs

Check server logs:
```bash
evennia --log
```

Or view log files directly:
```bash
tail -f server/server/logs/server.log
```

### Testing Web Client

Use Live Server in VS Code:
1. Right-click `web/index.html`
2. Select "Open with Live Server"
3. Client opens at `http://localhost:5500`

## Next Steps

- Read [GAME_DESIGN.md](GAME_DESIGN.md) for game mechanics
- Check [API.md](API.md) for client-server communication
- Explore Evennia docs: https://www.evennia.com/docs/

## Getting Help

- **Evennia Documentation**: https://www.evennia.com/docs/
- **Evennia Discord**: https://discord.gg/AJJpcRUhtF
- **GitHub Issues**: Report bugs and request features

---

Happy coding! May your journey through scripture be enlightening.
