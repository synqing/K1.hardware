#!/usr/bin/env python3
"""
Populate K1 Lightwave PCB with footprints from netlist

This script:
1. Reads the netlist file
2. Applies footprint assignment rules
3. Uses pcbnew to load and add footprints to the board
4. Saves the populated board file

Usage:
    /path/to/kicad/python3 populate_board_from_netlist.py <board.kicad_pcb> <netlist.net>
"""

import sys
import re
from pathlib import Path

# Must initialize wxApp before importing pcbnew
try:
    import wx
    app = wx.App()
except Exception as e:
    print(f"Note: wx initialization: {e}")

# Now import pcbnew
import pcbnew

# Footprint assignment rules
FOOTPRINT_RULES = [
    # Resistors - 0603
    (r'^R\d+$', 'Resistor_SMD:R_0603_1608Metric'),
    (r'^R_(USB|SPI|LED|FET|READY|PDM|LVT|BYPASS).*', 'Resistor_SMD:R_0603_1608Metric'),

    # Capacitors
    (r'^C\d+$', 'Capacitor_SMD:C_0603_1608Metric'),
    (r'^C_(BIN|BOUT|INA).*', 'Capacitor_SMD:C_1206_3216Metric'),

    # Diodes
    (r'^D_ESD_.*', 'Diode_SMD:D_SOD-323'),
    (r'^D\d+$', 'Diode_SMD:D_SOD-323'),
    (r'^D_IDEAL$', 'Diode_SMD:D_SOD-123'),

    # Fuses
    (r'^F\d+$', 'Fuse:Fuse_1206_3216Metric'),
    (r'^F_USB$', 'Fuse:Fuse_1206_3216Metric'),

    # Buttons
    (r'^SW\d+$', 'Button_Switch_SMD:SW_SPST_TL3342'),
]

def get_footprint_for_component(ref, value):
    """Determine footprint for a component based on reference and value"""
    for pattern, footprint in FOOTPRINT_RULES:
        if re.match(pattern, ref):
            return footprint
    return None

def parse_netlist(netlist_path):
    """Parse netlist and extract component references and values"""
    with open(netlist_path, 'r') as f:
        content = f.read()

    # Extract components: (comp (ref "XXX") (value "YYY") ...)
    comp_pattern = r'\(comp\s+\(ref "([^"]+)"\)\s+\(value "([^"]+)"\)'
    components = re.findall(comp_pattern, content)

    return components

def populate_board(board_path, netlist_path, output_path=None):
    """Populate board with footprints from netlist"""

    if output_path is None:
        output_path = board_path

    print(f"\n{'='*70}")
    print(f"Populating board with footprints from netlist")
    print(f"{'='*70}")
    print(f"Netlist: {netlist_path}")
    print(f"Input Board: {board_path}")
    print(f"Output Board: {output_path}")
    print()

    # Parse netlist
    print(f"Parsing netlist...")
    components = parse_netlist(netlist_path)
    print(f"Found {len(components)} components")

    if not components:
        print("ERROR: No components found in netlist")
        return False

    # Load board
    print(f"\nLoading board...")
    board = pcbnew.LoadBoard(str(board_path))
    if not board:
        print("ERROR: Failed to load board")
        return False

    print(f"Board loaded successfully")
    print(f"Current footprints on board: {len(board.GetFootprints())}")

    # Add footprints
    print(f"\nAdding footprints...")
    added_count = 0
    failed_count = 0
    skipped_count = 0

    for ref, value in components:
        try:
            # Get footprint
            footprint_name = get_footprint_for_component(ref, value)

            if not footprint_name:
                print(f"  ⚠️  {ref:12} ({value:15}) - No matching footprint rule")
                skipped_count += 1
                continue

            # Parse library and footprint
            if ':' not in footprint_name:
                print(f"  ❌ {ref:12} - Invalid footprint format: {footprint_name}")
                failed_count += 1
                continue

            lib_name, fp_name = footprint_name.split(':', 1)

            # Load footprint
            footprint = pcbnew.FootprintLoad(lib_name, fp_name)

            if not footprint:
                print(f"  ❌ {ref:12} - Failed to load {footprint_name}")
                failed_count += 1
                continue

            # Configure and add to board
            footprint.SetReference(ref)
            footprint.SetPosition(pcbnew.VECTOR2I(0, 0))  # Origin, will be placed later
            board.Add(footprint)

            print(f"  ✅ {ref:12} - {footprint_name}")
            added_count += 1

        except Exception as e:
            print(f"  ❌ {ref:12} - Error: {str(e)}")
            failed_count += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"Results:")
    print(f"  ✅ Added:       {added_count} footprints")
    print(f"  ❌ Failed:      {failed_count} components")
    print(f"  ⚠️  Skipped:     {skipped_count} components")
    print(f"  Total on board: {len(board.GetFootprints())} footprints")
    print(f"{'='*70}\n")

    if added_count == 0:
        print("ERROR: No footprints were added to the board")
        return False

    # Save board
    print(f"Saving board to: {output_path}")
    board.Save(str(output_path))

    # Verify
    saved_board = pcbnew.LoadBoard(str(output_path))
    final_count = len(saved_board.GetFootprints())
    print(f"Verification: Saved board has {final_count} footprints")

    if final_count != added_count:
        print(f"WARNING: Expected {added_count} footprints but board has {final_count}")

    print(f"\n✅ SUCCESS: Board populated with {added_count} footprints")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 populate_board_from_netlist.py <board.kicad_pcb> <netlist.net> [output.kicad_pcb]")
        sys.exit(1)

    board_path = Path(sys.argv[1])
    netlist_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else board_path

    # Verify files exist
    if not board_path.exists():
        print(f"ERROR: Board file not found: {board_path}")
        sys.exit(1)

    if not netlist_path.exists():
        print(f"ERROR: Netlist file not found: {netlist_path}")
        sys.exit(1)

    # Populate board
    success = populate_board(board_path, netlist_path, output_path)

    sys.exit(0 if success else 1)
