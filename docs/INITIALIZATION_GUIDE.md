# Game Initialization & Startup Guide

## Structure Fixes Applied ✅

### Fixed Issues:
1. ✅ Created `mygame/web/__init__.py` - WebSocket package initialization
2. ✅ Updated `mygame/__init__.py` - Main package initialization
3. ✅ Updated `mygame/server/conf/web_plugins.py` - WebSocket documentation
4. ✅ Fixed logger in `combat.py` - Proper logging import
5. ✅ Verified `settings.py` - WebSocket and typeclass configuration

### File Structure Status:
```
mygame/
├── __init__.py              ✅ Created/Updated
├── combat.py                ✅ Fixed imports
├── quests.py                ✅ Complete
├── encounters.py            ✅ Complete
├── commands/
│   ├── __init__.py          ✅ OK
│   ├── default_cmdsets.py   ✅ OK
│   ├── combat.py            ✅ OK
│   ├── quests.py            ✅ OK
│   └── ...
├── typeclasses/
│   ├── __init__.py          ✅ OK
│   ├── characters.py        ✅ OK
│   ├── npcs.py              ✅ OK
│   └── ...
├── world/
│   ├── __init__.py          ✅ OK
│   ├── world_data.py        ✅ OK
│   └── ...
├── web/
│   ├── __init__.py          ✅ Created
│   ├── websocket_plugin.py  ✅ OK
│   └── ...
└── server/
    ├── conf/
    │   ├── settings.py      ✅ OK
    │   └── web_plugins.py   ✅ Updated
    └── ...
```

## Startup Sequence

### 1. Server Initialization
```bash
cd mygame
evennia start
```

**Expected output:**
```
Starting Evennia server...
Initializing database...
Loading configuration from settings.py...
WebSocket enabled on port 4001
Server started successfully!
```

### 2. World Building
```bash
evennia shell
@py from world import build_world; build_world.build_all()
```

**Expected output:**
```
=== BUILDING PALACE OF LIGHT ===
Building rooms...
Created 30+ rooms
Connected all exits
Creating items...
Created 50+ items
Creating NPCs...
Created 20+ NPCs
=== WORLD BUILD COMPLETE ===
```

### 3. Creating Superuser
```bash
evennia createsuperuser
```

**Follow prompts to create admin account**

### 4. Web Client Setup
```bash
cd web
python -m http.server 8000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8000...
```

### 5. Access Game
Open browser to: `http://localhost:8000`

## Verification Checklist

### Server Checks
- [ ] Server starts without errors
- [ ] Database initializes
- [ ] WebSocket port 4001 is available
- [ ] Settings load correctly

### Import Checks
```python
# In evennia shell (@py)
from mygame import combat, quests, encounters
from mygame.typeclasses.characters import Character
from mygame.commands.default_cmdsets import CharacterCmdSet
print("All imports successful!")
```

### Character Creation Checks
```
> create
(follow character creation prompts)
> look
> stats
> quests
```

### Combat System Checks
```
> fight orc
Combat started! You face Orc!
> attack
> status
> flee
```

### Quest System Checks
```
> quests
(should show available quests)
> accept quest_trial_of_strength
> quests
(should show active quest)
> fight orc
(after victory)
> quests
(should show progress update)
```

### WebSocket Checks
1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter for "ws"
4. Should see connection to `ws://localhost:4001/ws`
5. Send a command in game
6. Should see WebSocket frames

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'mygame'"

**Solution:**
```bash
cd mygame
python -c "from mygame import combat; print('OK')"
```

If error persists, ensure you're in the correct directory with settings.py

### Problem: "ImportError: cannot import name 'QuestManager'"

**Solution:**
Check that `mygame/quests.py` exists and contains `QuestManager` class

### Problem: WebSocket not connecting

**Solution:**
1. Check port 4001 is not in use: `netstat -tuln | grep 4001`
2. Verify WEBSOCKET_CLIENT_PORT = 4001 in settings.py
3. Check browser console for WebSocket errors

### Problem: Commands not loading

**Solution:**
1. Verify `mygame/commands/default_cmdsets.py` imports all commands
2. Check that CharacterCmdSet.at_cmdset_creation() adds all commands
3. Reload commands: `@py from evennia.utils import evtools; evtools.flush_cache()`

### Problem: Characters don't have quest_manager

**Solution:**
Add to Character.at_post_puppet():
```python
def at_post_puppet(self, **kwargs):
    super().at_post_puppet(**kwargs)
    if not hasattr(self, 'quest_manager'):
        from mygame.quests import QuestManager
        self.quest_manager = QuestManager(self)
```

## Log Files

### Server Logs
Location: `mygame/server/logs/`

**Key files:**
- `server.log` - Main server log
- `database.log` - Database operations
- `errors.log` - Error messages

### View Logs
```bash
tail -f mygame/server/logs/server.log
```

## Database Management

### Backup Database
```bash
cd mygame
python manage.py dumpdata > backup.json
```

### Reset Database
```bash
cd mygame
python manage.py flush --no-input
python manage.py migrate
```

**Warning:** This deletes all characters and world data!

### Check Database Status
```bash
cd mygame
evennia shell
@py from django.core.management import call_command; call_command('check')
```

## Configuration Files

### Critical Settings
**Location:** `mygame/server/conf/settings.py`

Key settings for your game:
```python
# Server
SERVERNAME = "Journey Through Scripture"

# WebSocket
WEBSOCKET_CLIENT_PORT = 4001
WEBCLIENT_ENABLED = True

# Typeclasses
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"
BASE_OBJECT_TYPECLASS = "typeclasses.objects.Item"

# Commands
CMDSET_CHARACTER = "commands.default_cmdsets.CharacterCmdSet"

# Starting location
START_LOCATION = "floor1_approach"
```

### Web Configuration
**Location:** `web/index.html`

Update game server URL if needed:
```javascript
// In game.js
const WEBSOCKET_URL = 'ws://localhost:4001/ws';
```

## Performance Tuning

### Increase Cache Size
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 10000  # Increase from default 300
        }
    }
}
```

### Database Connection Pooling
```python
# settings.py
DATABASES = {
    'default': {
        ...
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Disable Debug in Production
```python
# settings.py
DEBUG = False
```

## Monitoring

### Check Active Sessions
```python
# In evennia shell
@py from evennia.server.sessionhandler import SESSIONS; print(SESSIONS.all())
```

### Monitor WebSocket Connections
```bash
# In server logs
grep -i websocket mygame/server/logs/server.log
```

### Performance Stats
```python
# In evennia shell
@py from evennia import management; management.commands.about()
```

## Deployment Checklist

### Before Going Live
- [ ] Change DEBUG = False
- [ ] Set SECRET_KEY to random value
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL/HTTPS
- [ ] Configure database (production)
- [ ] Test all major features
- [ ] Backup database
- [ ] Set up monitoring
- [ ] Create admin backup account

### Initial Content
- [ ] Build world (build_all())
- [ ] Create starting room descriptions
- [ ] Place NPCs
- [ ] Create initial quests
- [ ] Test combat encounters
- [ ] Verify progression

## Maintenance

### Daily
- [ ] Monitor server logs
- [ ] Check disk space
- [ ] Monitor WebSocket connections

### Weekly
- [ ] Backup database
- [ ] Review error logs
- [ ] Test critical features

### Monthly
- [ ] Performance review
- [ ] Security updates
- [ ] Database optimization

## Development Workflow

### Adding New Features

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Write code in appropriate module
   - Update imports if needed
   - Add documentation

3. **Test changes**
   ```bash
   # Restart server to reload modules
   evennia restart

   # Test in game
   > command
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

5. **Merge to main**
   ```bash
   git checkout main
   git merge feature/my-feature
   ```

## Getting Help

### Check Documentation
- `docs/QUEST_SYSTEM.md` - Quest system
- `docs/WEBSOCKET_PROTOCOL.md` - WebSocket messages
- `STRUCTURE_FIXES.md` - Structure fixes applied
- Evennia docs: https://www.evennia.com/docs/

### Check Server Logs
```bash
tail -100 mygame/server/logs/server.log | grep -i error
```

### Run Diagnostics
```python
# In evennia shell
@py
import sys
print("Python version:", sys.version)
print("Evennia version:", evennia.__version__)
from mygame import combat, quests
print("Core modules loaded")
print("Diagnostics complete")
```

## Next Steps

1. **Start server** - `evennia start`
2. **Build world** - `@py from world import build_world; build_world.build_all()`
3. **Create account** - Create superuser account
4. **Test game** - Create character and test features
5. **Monitor logs** - Watch for errors
6. **Develop content** - Add more quests, encounters, items

---

**Game initialization complete! Ready for gameplay!**
