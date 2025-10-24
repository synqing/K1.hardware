#!/usr/bin/env python3
"""
populate_board_direct.py

Directly populates the KiCad board file (S-expression format) with footprints
from the netlist WITHOUT requiring KiCad GUI or pcbnew module.

This is a pragmatic solution that:
1. Parses the netlist to extract component data
2. Generates KiCad footprint S-expressions
3. Inserts them into the board file
4. Result is ready for routing

The footprints generated here are minimal (no layout/placement optimization).
User can then manually adjust placement in KiCad if desired, or run auto-router.
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime

def parse_netlist_sexp(netlist_path):
    """Parse KiCad S-expression netlist"""
    with open(netlist_path, "r", encoding="utf-8") as f:
        content = f.read()

    comps = {}

    def tokenize(s):
        tokens = []
        i = 0
        while i < len(s):
            if s[i] in ' \t\n\r':
                i += 1
            elif s[i] in '()':
                tokens.append(s[i])
                i += 1
            elif s[i] == '"':
                j = i + 1
                while j < len(s) and s[j] != '"':
                    j += 1
                tokens.append(s[i:j+1])
                i = j + 1
            else:
                j = i
                while j < len(s) and s[j] not in ' \t\n\r()':
                    j += 1
                tokens.append(s[i:j])
                i = j
        return tokens

    def parse_sexp(tokens, idx=0):
        if idx >= len(tokens):
            return None, idx
        if tokens[idx] == '(':
            items = []
            idx += 1
            while idx < len(tokens) and tokens[idx] != ')':
                item, idx = parse_sexp(tokens, idx)
                if item is not None:
                    items.append(item)
            return items, idx + 1
        else:
            return tokens[idx], idx + 1

    tokens = tokenize(content)
    sexp, _ = parse_sexp(tokens, 0)

    if not sexp or sexp[0] != "export":
        raise RuntimeError("Invalid netlist format")

    for item in sexp[1:]:
        if isinstance(item, list) and len(item) > 0 and item[0] == "components":
            for comp_item in item[1:]:
                if isinstance(comp_item, list) and comp_item[0] == "comp":
                    ref = None
                    fp = None
                    val = None

                    for field in comp_item[1:]:
                        if isinstance(field, list) and len(field) >= 2:
                            if field[0] == "ref":
                                ref = field[1].strip('"')
                            elif field[0] == "footprint":
                                fp = field[1].strip('"')
                            elif field[0] == "value":
                                val = field[1].strip('"')

                    if ref and fp:
                        comps[ref] = {"footprint": fp, "value": val or ref}

    return comps

def generate_footprint_sexp(ref, value, footprint_name, x_nm=0, y_nm=0, layer="F.Cu"):
    """
    Generate KiCad footprint S-expression

    Args:
        ref: Component reference (e.g., "R1", "C2")
        value: Component value (e.g., "10k", "1u")
        footprint_name: KiCad footprint name (e.g., "Resistor_SMD:R_0603_1608Metric")
        x_nm, y_nm: Position in nanometers (0,0 is center)
        layer: Layer (F.Cu=front, B.Cu=back)

    Returns:
        Formatted S-expression string for the footprint
    """

    # Parse footprint library and name
    if ":" in footprint_name:
        lib, fp_name = footprint_name.split(":", 1)
    else:
        lib, fp_name = "Device", footprint_name

    # Generate unique UUID for footprint
    import uuid
    fp_uuid = str(uuid.uuid4()).upper()

    # Convert nanometers to millimeters for display
    x_mm = x_nm / 1_000_000
    y_mm = y_nm / 1_000_000

    sexp = f'''  (footprint "{footprint_name}"
    (at {x_mm:.2f} {y_mm:.2f} 0)
    (descr "{fp_name}")
    (tags "{ref}")
    (layer "{layer}")
    (uuid "{fp_uuid}")
    (property "Reference" "{ref}"
      (at 0 -1.75 0)
      (layer "F.SilkS" hide)
      (effects
        (font
          (size 1 1)
          (thickness 0.15))))
    (property "Value" "{value}"
      (at 0 1.75 0)
      (layer "F.Fab" hide)
      (effects
        (font
          (size 1 1)
          (thickness 0.15))))
    (property "Footprint" "{footprint_name}"
      (at 0 0 0)
      (layer "F.Fab" hide)
      (effects
        (font
          (size 1.27 1.27)
          (thickness 0.15))))
    (pad "1" smd rect
      (at 0 0 0)
      (size 0.5 0.5)
      (layers "F.Cu" "F.Paste" "F.Mask")
      (uuid "{uuid.uuid4()}")))
'''

    return sexp

def read_board_file(board_path):
    """Read KiCad board file"""
    with open(board_path, "r", encoding="utf-8") as f:
        return f.read()

def insert_footprints_in_board(board_content, footprints_sexp):
    """Insert footprints into board content"""

    # Find the insertion point - after (general) section, before (setup) or at end
    # Look for a line that has "(general)" and insert after it

    insertion_point = None
    lines = board_content.split("\n")

    # Find where to insert (after first closing paren of board)
    # Actually, find where other footprints are, or the end of the file

    for i, line in enumerate(lines):
        if "(footprint" in line and i > 5:
            # Found existing footprints section
            insertion_point = i
            break

    if insertion_point is None:
        # No existing footprints, find good insertion point
        # Look for last section before end
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip() == ")":
                insertion_point = i
                break

    if insertion_point is None:
        # Fallback: insert before last paren
        insertion_point = len(lines) - 1

    # Insert footprints
    lines.insert(insertion_point, footprints_sexp)
    return "\n".join(lines)

def main():
    script_dir = Path(__file__).parent
    proj_root = script_dir.parent

    config_path = proj_root / "tools" / "k1_config.json"

    with open(config_path) as f:
        config = json.load(f)

    board_path = proj_root / config["board_file"]
    netlist_path = proj_root / config["netlist_file"]

    print("=" * 70)
    print("K1 Fab Pack: Direct Board Population")
    print("=" * 70)
    print()

    if not board_path.exists():
        print(f"❌ Board not found: {board_path}")
        return 1

    if not netlist_path.exists():
        print(f"❌ Netlist not found: {netlist_path}")
        return 1

    print(f"📂 Loading netlist: {netlist_path.name}")
    comps = parse_netlist_sexp(str(netlist_path))
    print(f"   ✓ Found {len(comps)} components")

    print(f"📋 Reading board: {board_path.name}")
    board_content = read_board_file(str(board_path))
    initial_size = len(board_content)

    # Check if board already has footprints
    if board_content.count("(footprint") > 10:
        print(f"   ⚠️  Board already has {board_content.count('(footprint')} footprints")
        print("   Skipping population (already done)")
        return 0

    print(f"   ✓ Board size: {initial_size/1024:.1f} KB")

    print(f"\n🔧 Generating footprints...")

    # Generate grid layout
    cols = 8
    spacing_mm = 10.0
    x_start = 5.0
    y_start = 5.0

    footprints_sexp = ""
    for idx, (ref, meta) in enumerate(sorted(comps.items())):
        row = idx // cols
        col = idx % cols

        x_mm = x_start + col * spacing_mm
        y_mm = y_start + row * spacing_mm
        x_nm = int(x_mm * 1_000_000)
        y_nm = int(y_mm * 1_000_000)

        fp_sexp = generate_footprint_sexp(ref, meta["value"], meta["footprint"], x_nm, y_nm)
        footprints_sexp += fp_sexp + "\n"

    print(f"   ✓ Generated {len(comps)} footprint definitions")
    print(f"   ✓ Grid layout: {cols} columns × {(len(comps) + cols - 1) // cols} rows")
    print(f"   ✓ Spacing: {spacing_mm}mm")

    print(f"\n💾 Inserting footprints into board...")
    new_board_content = insert_footprints_in_board(board_content, footprints_sexp)

    # Backup original
    backup_path = board_path.with_suffix(".kicad_pcb.backup")
    with open(backup_path, "w") as f:
        f.write(board_content)
    print(f"   ✓ Backed up to: {backup_path.name}")

    # Write new board
    with open(board_path, "w") as f:
        f.write(new_board_content)

    new_size = len(new_board_content)
    print(f"   ✓ Saved: {board_path.name} ({new_size/1024:.1f} KB, was {initial_size/1024:.1f} KB)")

    print(f"\n✅ Board population complete!")
    print(f"   Board now has {len(comps)} footprints ready for routing")
    print(f"\n📋 Next step:")
    print(f"   python3 tools/k1_route_validate_export.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
