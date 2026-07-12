#!/bin/bash
# Run K1 Lightwave component placement demo with KiCad's Python

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# KiCad Python path
KICAD_PYTHON="/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3"

# Check if KiCad Python exists
if [ ! -f "$KICAD_PYTHON" ]; then
    echo "ERROR: KiCad Python not found at $KICAD_PYTHON"
    exit 1
fi

# Run the demo with KiCad's Python
echo "Using KiCad Python: $KICAD_PYTHON"
echo ""

exec "$KICAD_PYTHON" "$SCRIPT_DIR/demo_placement.py" "$@"
