#!/usr/bin/env python
"""
Simple world builder for Journey Through Scripture.
This is a standalone script that uses Evennia's APIs to build the world.
"""

if __name__ == "__main__":
    import os
    import sys
    import django

    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.conf.settings')
    django.setup()

    # Now import Evennia after Django is setup
    from evennia import create_object, search_object

    print("=" * 60)
    print("BUILDING SIMPLE GAME WORLD")
    print("=" * 60)

    try:
        # Try to build a simple starting room
        from server.conf.settings import START_LOCATION

        # Check if room already exists
        existing = search_object(START_LOCATION)
        if existing:
            print(f"\nStarting room '{START_LOCATION}' already exists!")
            print(f"Found {len(existing)} object(s)")
        else:
            print(f"\nCreating starting room '{START_LOCATION}'...")
            room = create_object(
                key=START_LOCATION,
                attributes=[("description", "A place of mystery.")]
            )
            print(f"✓ Created room: {room}")

        # List all rooms
        all_rooms = search_object("")
        print(f"\nTotal objects in game: {len(all_rooms)}")

        print("\n" + "=" * 60)
        print("WORLD BUILD COMPLETE!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
