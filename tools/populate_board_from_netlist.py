#!/usr/bin/env python3
"""
populate_board_from_netlist.py

Populates an empty KiCad PCB board with footprints from a netlist file.
Uses the K1_ImportAndPlace plugin logic but as a standalone script that
can be run via KiCad's Python console or as a plugin trigger.

This is a helper for the K1 Fab Pack pipeline - run this BEFORE running
the end-to-end orchestrator (k1_route_validate_export.py).
"""

import os
import sys
import json
from pathlib import Path

def ensure_kicad_libs():
    """Ensure KiCad can find footprint libraries"""
    kicad_user = Path.home() / ".config" / "kicad"
    if sys.platform == "darwin":
        kicad_user = Path.home() / "Library" / "Preferences" / "kicad"

    kicad_lib_table = kicad_user / "9.0" / "fp-lib-table"
    if not kicad_lib_table.exists():
        print(f"⚠️  KiCad library table not found at {kicad_lib_table}")
        print("   This may cause FootprintLoad to fail.")
        return False
    return True

def load_config(config_path="tools/k1_config.json"):
    """Load K1 Fab Pack configuration"""
    if not os.path.exists(config_path):
        raise RuntimeError(f"Config not found: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)

def parse_netlist_sexp(netlist_path):
    """Parse KiCad S-expression netlist"""
    with open(netlist_path, "r", encoding="utf-8") as f:
        content = f.read()

    comps = {}
    nets = {}

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

    try:
        tokens = tokenize(content)
        sexp, _ = parse_sexp(tokens, 0)

        if not sexp or sexp[0] != "export":
            raise RuntimeError("Invalid netlist: expected (export ...)")

        for item in sexp[1:]:
            if isinstance(item, list) and len(item) > 0:
                if item[0] == "components":
                    for comp_item in item[1:]:
                        if isinstance(comp_item, list) and len(comp_item) > 1 and comp_item[0] == "comp":
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
                                comps[ref] = {"footprint": fp, "value": val or ""}

                elif item[0] == "nets":
                    for net_item in item[1:]:
                        if isinstance(net_item, list) and len(net_item) > 1 and net_item[0] == "net":
                            net_name = None
                            nodes = []

                            for field in net_item[1:]:
                                if isinstance(field, list) and len(field) >= 2:
                                    if field[0] == "name":
                                        net_name = field[1].strip('"')
                                    elif field[0] == "node":
                                        ref = None
                                        pin = None
                                        for attr in field[1:]:
                                            if isinstance(attr, list):
                                                if attr[0] == "ref":
                                                    ref = attr[1].strip('"') if len(attr) > 1 else None
                                                elif attr[0] == "pin":
                                                    pin = attr[1].strip('"') if len(attr) > 1 else None
                                        if ref and pin:
                                            nodes.append((ref, pin))

                            if net_name:
                                nets[net_name] = nodes

    except Exception as e:
        raise RuntimeError(f"Failed to parse netlist: {str(e)}")

    return comps, nets

def populate_board_with_pcbnew(board_path, netlist_path, config):
    """Populate board using pcbnew API (requires KiCad environment)"""
    try:
        import pcbnew
    except ImportError:
        print("ERROR: pcbnew module not available")
        print("This script must be run from within KiCad or with proper PYTHONPATH.")
        return False

    try:
        print(f"📂 Loading board: {board_path}")
        board = pcbnew.LoadBoard(board_path)

        print(f"📋 Parsing netlist: {netlist_path}")
        comps, nets = parse_netlist_sexp(netlist_path)
        print(f"   ✓ Found {len(comps)} components")
        print(f"   ✓ Found {len(nets)} nets")

        # Get existing footprints
        existing_refs = set(fp.GetReference() for fp in board.GetFootprints())
        print(f"   ✓ Board has {len(existing_refs)} existing footprints")

        # Try to add missing footprints
        added = 0
        failed = []

        for ref, meta in comps.items():
            if ref in existing_refs:
                continue

            try:
                fp = pcbnew.FootprintLoad(meta["footprint"].split(":")[0], meta["footprint"].split(":")[1])
                if fp:
                    fp.SetReference(ref)
                    fp.SetValue(meta.get("value", ""))
                    fp.SetPosition(pcbnew.VECTOR2I(0, 0))
                    board.Add(fp)
                    added += 1
                else:
                    failed.append((ref, meta["footprint"], "FootprintLoad returned None"))
            except Exception as e:
                failed.append((ref, meta["footprint"], str(e)))

        print(f"✅ Added {added} footprints to board")
        if failed:
            print(f"⚠️  Failed to load {len(failed)} footprints:")
            for ref, fp, err in failed[:5]:
                print(f"   - {ref}: {fp} ({err})")
            if len(failed) > 5:
                print(f"   ... and {len(failed) - 5} more")

        # Assign nets to pads
        assigned = 0
        for net_name, nodes in nets.items():
            try:
                nii = board.FindNet(net_name)
                if not nii:
                    nii = pcbnew.NETINFO_ITEM(board, net_name)
                    board.Add(nii)

                for ref, pin in nodes:
                    fp = board.FindFootprintByReference(ref)
                    if fp:
                        pad = fp.FindPadByNumber(pin)
                        if pad:
                            pad.SetNet(nii)
                            assigned += 1
            except:
                pass

        print(f"✅ Assigned {assigned} pads to nets")

        # Save board
        print(f"💾 Saving board: {board_path}")
        board.Save(board_path)
        print(f"✅ Board saved successfully")

        return len(failed) == 0

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Determine project root
    script_dir = Path(__file__).parent
    proj_root = script_dir.parent
    os.chdir(proj_root)

    config = load_config("tools/k1_config.json")
    board_path = config["board_file"]
    netlist_path = config["netlist_file"]

    print("=" * 60)
    print("K1 Fab Pack: Board Population Helper")
    print("=" * 60)

    if not os.path.exists(board_path):
        print(f"❌ Board file not found: {board_path}")
        return 1

    if not os.path.exists(netlist_path):
        print(f"❌ Netlist not found: {netlist_path}")
        return 1

    print(f"\n📊 Status:")
    board_size = os.path.getsize(board_path)
    print(f"   Board: {board_path} ({board_size/1024:.1f} KB)")
    print(f"   Netlist: {netlist_path}")

    # Check if pcbnew is available
    try:
        import pcbnew
        print(f"   Python environment: ✓ KiCad pcbnew module available")
        success = populate_board_with_pcbnew(board_path, netlist_path, config)
        return 0 if success else 1
    except ImportError:
        print(f"   Python environment: ⚠️  KiCad pcbnew module NOT available")
        print("\n⚠️  This script requires KiCad Python environment.")
        print("\nAlternatives:")
        print("1. Run from KiCad's Python console (Tools → Python Console)")
        print("2. Run the K1_ImportAndPlace plugin manually (Tools → External Plugins)")
        print("3. Configure PYTHONPATH to include KiCad's Python libraries")
        print("\nFor manual plugin usage:")
        print(f"   - Open {board_path} in KiCad PCB Editor")
        print("   - Go to Tools → External Plugins → K1: Import Netlist + Place")
        print("   - Plugin will populate board from netlist automatically")
        return 2

if __name__ == "__main__":
    sys.exit(main())
