#!/bin/bash
#
# auto_populate_board.sh
#
# Automated board population helper for K1 Fab Pack
#
# This script opens the K1 Lightwave board in KiCad and runs the
# K1_ImportAndPlace plugin to populate it with footprints from the netlist.
#
# Requirements:
#  - KiCad 9.x installed
#  - K1_ImportAndPlace plugin installed in KiCad plugins directory
#  - Netlist file with footprint assignments (k1_motherboard_revA.net)
#
# Usage:
#   bash tools/auto_populate_board.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

BOARD="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb"
NETLIST="hardware/k1-lightwave/k1_motherboard_revA.net"
CONFIG="tools/k1_config.json"

echo "============================================================"
echo "K1 Fab Pack: Automated Board Population"
echo "============================================================"
echo ""

# Check files exist
if [ ! -f "$BOARD" ]; then
    echo "❌ Board file not found: $BOARD"
    exit 1
fi

if [ ! -f "$NETLIST" ]; then
    echo "❌ Netlist not found: $NETLIST"
    exit 1
fi

if [ ! -f "$CONFIG" ]; then
    echo "❌ Config not found: $CONFIG"
    exit 1
fi

# Check board size
BOARD_SIZE=$(stat -f%z "$BOARD" 2>/dev/null || stat -c%s "$BOARD" 2>/dev/null)
if [ "$BOARD_SIZE" -lt 5000 ]; then
    echo "⚠️  Board appears to be empty ($BOARD_SIZE bytes)"
    echo "   After plugin completes, board should be ~50+ KB"
fi

echo "📋 Configuration:"
echo "   Board: $(basename $BOARD)"
echo "   Netlist: $(basename $NETLIST)"
echo ""

echo "⚠️  MANUAL STEP REQUIRED"
echo "============================================================"
echo ""
echo "The K1_ImportAndPlace plugin cannot run completely headless"
echo "on macOS. You need to:"
echo ""
echo "1. Open KiCad (or if already open, switch to PCB Editor):"
echo "   open -a 'KiCad' '$BOARD'"
echo ""
echo "2. In KiCad PCB Editor, go to:"
echo "   Tools → External Plugins → K1: Import Netlist + Place"
echo ""
echo "3. Click OK in the confirmation dialog"
echo ""
echo "4. KiCad will auto-populate the board and save automatically"
echo ""
echo "5. Close KiCad"
echo ""
echo "============================================================"
echo ""
echo "After plugin completion, proceed to:"
echo "   python3 tools/k1_route_validate_export.py"
echo ""

echo "Opening KiCad with board file..."
echo ""

# Open KiCad with board
if [ "$(uname)" = "Darwin" ]; then
    open -a "KiCad" "$BOARD"
elif [ "$(uname)" = "Linux" ]; then
    nohup kicad "$BOARD" &
else
    kicad "$BOARD" &
fi

echo "✓ KiCad opening..."
echo "⏳ Waiting for you to complete the plugin step..."
echo ""
echo "Once board is populated and saved, press Enter to continue..."
read -p "→ "

echo "✓ Proceeding with routing and export..."
