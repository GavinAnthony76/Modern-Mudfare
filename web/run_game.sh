#!/bin/bash

# Journey Through Scripture - Local Server Launcher
# This script starts a simple Python web server to run the game with asset loading

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Journey Through Scripture - Local Game Server            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "Starting web server on http://localhost:8000..."
echo ""
echo "✓ Open this URL in your browser:"
echo "  http://localhost:8000"
echo ""
echo "✓ Press Ctrl+C to stop the server"
echo ""

python3 -m http.server 8000
