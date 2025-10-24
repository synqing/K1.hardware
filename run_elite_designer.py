#!/usr/bin/env python3
"""
Wrapper script to run Elite PCB Designer with KiCad Python API support
"""

import sys
import os

# Add KiCad Python modules to path
kicad_python_path = "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages"
if os.path.exists(kicad_python_path) and kicad_python_path not in sys.path:
    sys.path.insert(0, kicad_python_path)

# Now run the elite designer
if __name__ == '__main__':
    # Import after path is configured
    from elite_pcb_designer import main
    sys.exit(main())
