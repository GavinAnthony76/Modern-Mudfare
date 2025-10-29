#!/usr/bin/env python
"""
Script to build the game world for Journey Through Scripture.
Run this from the mygame directory.
"""

import os
import sys
import django

# Change to mygame directory if needed
if os.path.basename(os.getcwd()) != 'mygame':
    mygame_dir = os.path.join(os.path.dirname(__file__), 'mygame')
    if os.path.isdir(mygame_dir):
        os.chdir(mygame_dir)
    else:
        print("Error: Could not find mygame directory")
        sys.exit(1)

# Add current dir to path
sys.path.insert(0, os.getcwd())

# Setup Django and Evennia
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.conf.settings')
django.setup()

# Now import and build
from world import build_world

print("=" * 60)
print("BUILDING GAME WORLD")
print("=" * 60)

try:
    build_world.build_all()
    print("\n" + "=" * 60)
    print("WORLD BUILD COMPLETE!")
    print("=" * 60)
except Exception as e:
    print(f"\nError building world: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
