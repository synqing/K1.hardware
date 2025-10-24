#!/bin/bash
# Wrapper script to run component placement tests with KiCad's Python

# KiCad Python path
KICAD_PYTHON="/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3"

# Check if KiCad Python exists
if [ ! -f "$KICAD_PYTHON" ]; then
    echo "ERROR: KiCad Python not found at $KICAD_PYTHON"
    exit 1
fi

# Run the test with KiCad's Python
echo "Using KiCad Python: $KICAD_PYTHON"
echo ""

exec "$KICAD_PYTHON" test_component_placement.py "$@"
