#!/usr/bin/env python3
"""
Populate K1 Lightwave PCB with footprints - MANUAL METHOD

Creates footprint placeholders manually using pcbnew API
instead of loading from libraries (workaround for FootprintLoad issues)
"""

import sys
import re
from pathlib import Path

# Initialize wx first
try:
    import wx
    app = wx.App()
except:
    pass

import pcbnew

# Footprint rules mapping component references to footprint specs
FOOTPRINTS = {
    # Pattern: (regex, lib:name, width_mm, height_mm, pad_count)
    (r'^R\d+$|R_(USB|SPI|LED|FET|READY|PDM|LVT|BYPASS).*', 'Resistor_SMD:R_0603_1608Metric', 1.6, 0.8, 2),
    (r'^C\d+$|C_(BIN|BOUT|INA).*', 'Capacitor_SMD:C_0603_1608Metric', 1.6, 0.8, 2),
    (r'^D\d+$|D_ESD_.*|D_IDEAL$', 'Diode_SMD:D_SOD-323', 1.8, 1.3, 2),
    (r'^F\d+$|F_USB$', 'Fuse:Fuse_1206_3216Metric', 3.2, 1.6, 2),
    (r'^SW\d+$', 'Button_Switch_SMD:SW_SPST_TL3342', 3.5, 2.5, 2),
}

def parse_netlist(netlist_path):
    """Parse netlist and extract component references"""
    with open(netlist_path, 'r') as f:
        content = f.read()

    # Extract components: (comp (ref "XXX") (value "YYY") ...)
    comp_pattern = r'\(comp\s+\(ref "([^"]+)"\)\s+\(value "([^"]+)"\)'
    return re.findall(comp_pattern, content)

def get_footprint_spec(ref):
    """Get footprint specification for a component"""
    for pattern, spec, w, h, pads in FOOTPRINTS:
        if re.match(pattern, ref):
            return (spec, w, h, pads)
    return None

def create_simple_footprint(board, ref, spec, width_mm, height_mm):
    """Create a simple two-pad footprint manually"""
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)

    # Set position
    fp.SetPosition(pcbnew.VECTOR2I(0, 0))

    # Create two pads (simple 2-pad component like resistor/capacitor)
    pad1 = pcbnew.PAD(fp)
    pad1.SetNumber("1")
    pad1.SetShape(pcbnew.PAD_SHAPE_OVAL)
    pad1.SetSize(pcbnew.VECTOR2I(
        pcbnew.FromMM(width_mm * 0.4),
        pcbnew.FromMM(height_mm * 0.5)
    ))
    pad1.SetPosition(pcbnew.VECTOR2I(
        pcbnew.FromMM(-width_mm / 2 + 0.3),
        0
    ))
    pad1.SetType(pcbnew.PAD_TYPE_SMD)
    pad1.SetLayerSet(pad1.StandardMask())
    fp.Add(pad1)

    pad2 = pcbnew.PAD(fp)
    pad2.SetNumber("2")
    pad2.SetShape(pcbnew.PAD_SHAPE_OVAL)
    pad2.SetSize(pcbnew.VECTOR2I(
        pcbnew.FromMM(width_mm * 0.4),
        pcbnew.FromMM(height_mm * 0.5)
    ))
    pad2.SetPosition(pcbnew.VECTOR2I(
        pcbnew.FromMM(width_mm / 2 - 0.3),
        0
    ))
    pad2.SetType(pcbnew.PAD_TYPE_SMD)
    pad2.SetLayerSet(pad2.StandardMask())
    fp.Add(pad2)

    return fp

def populate_board(board_path, netlist_path, output_path=None):
    """Populate board with manually created footprints"""

    if output_path is None:
        output_path = board_path

    print(f"\n{'='*70}")
    print(f"Populating board - MANUAL METHOD")
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
        print("ERROR: No components found")
        return False

    # Load board
    print(f"\nLoading board...")
    board = pcbnew.LoadBoard(str(board_path))
    if not board:
        print("ERROR: Failed to load board")
        return False

    print(f"Board loaded, current footprints: {len(board.GetFootprints())}")

    # Add footprints
    print(f"\nAdding footprints...")
    added_count = 0
    skipped_count = 0

    for ref, value in components:
        spec = get_footprint_spec(ref)

        if not spec:
            print(f"  ⚠️  {ref:15} - No matching rule, skipping")
            skipped_count += 1
            continue

        try:
            footprint_name, width, height, pads = spec

            # Create footprint manually
            fp = create_simple_footprint(board, ref, footprint_name, width, height)

            # Add to board
            board.Add(fp)

            print(f"  ✅ {ref:15} - Created manually")
            added_count += 1

        except Exception as e:
            print(f"  ❌ {ref:15} - Error: {str(e)}")
            skipped_count += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"Results:")
    print(f"  ✅ Added:   {added_count} footprints")
    print(f"  ⚠️  Skipped: {skipped_count} components")
    print(f"{'='*70}\n")

    if added_count == 0:
        print("ERROR: No footprints were added")
        return False

    # Save board
    print(f"Saving board to: {output_path}")
    board.Save(str(output_path))

    # Verify
    saved_board = pcbnew.LoadBoard(str(output_path))
    final_count = len(saved_board.GetFootprints())
    print(f"Verification: Saved board has {final_count} footprints")

    print(f"\n✅ SUCCESS: Board populated with {added_count} footprints")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 populate_board_manual.py <board.kicad_pcb> <netlist.net> [output.kicad_pcb]")
        sys.exit(1)

    board_path = Path(sys.argv[1])
    netlist_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else board_path

    if not board_path.exists():
        print(f"ERROR: Board not found: {board_path}")
        sys.exit(1)

    if not netlist_path.exists():
        print(f"ERROR: Netlist not found: {netlist_path}")
        sys.exit(1)

    success = populate_board(board_path, netlist_path, output_path)
    sys.exit(0 if success else 1)
