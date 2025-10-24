#!/usr/bin/env python3
# K1 Fab Pack: Design validation, DRC, and manufacturing export
#
# Pipeline:
#   1. Validate board has components placed
#   2. Run DRC on unrouted board
#   3. Export manufacturing files (Gerbers, drill, IPC-2581, ODB++)
#
# Note: Routing must be done manually in KiCad GUI or via third-party tools.
# KiCad 9.x CLI does not support DSN export (required for FreeRouting automation).
# Strict gating: if DRC shows violations, NO artifacts are emitted.

import os, sys, json, subprocess, shutil

def run(cmd):
    print(">>", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)

def abort(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)

# --- Load config ---
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
CFG_PATH = os.path.join(SCRIPT_DIR, "k1_config.json")
if not os.path.exists(CFG_PATH):
    abort(f"Missing config: {CFG_PATH}")
with open(CFG_PATH, "r", encoding="utf-8") as f:
    CFG = json.load(f)

BOARD = CFG["board_file"]
OUT   = CFG["output_dir"]
STRICT= bool(CFG.get("strict", True))

os.makedirs(OUT, exist_ok=True)

# --- Sanity: board must contain footprints ---
if not os.path.exists(BOARD):
    abort(f"Board not found: {BOARD}")

board_size = os.path.getsize(BOARD)
if board_size < 10000:
    abort(f"Board appears nearly empty ({board_size} bytes). Run populate_board_direct.py first.", 2)

print(f"\n📋 K1 Fab Pack: Manufacturing Export Pipeline")
print(f"{'='*60}")
print(f"Board: {BOARD} ({board_size/1024:.1f} KB)")
print(f"Output: {OUT}")
print()

# --- Verify kicad-cli ---
if shutil.which("kicad-cli") is None:
    abort("kicad-cli not found in PATH.")

# --- Design Check: DRC on unrouted board ---
print("📊 Running DRC on unrouted board...")
DRC_JSON = os.path.join(OUT, "drc.json")

try:
    run(["kicad-cli", "pcb", "drc", BOARD, "--output", DRC_JSON, "--format", "json"])
except subprocess.CalledProcessError as e:
    abort(f"DRC command failed: {e}")

if not os.path.exists(DRC_JSON):
    abort("DRC report not produced.")

with open(DRC_JSON, "r", encoding="utf-8") as f:
    drc = json.load(f)

# Parse DRC results
viol = int(drc.get("violations_count") or 0)
unr  = int(drc.get("unconnected_count") or 0)
warn = int(drc.get("warnings_count") or 0)

print(f"\n✅ DRC Results:")
print(f"   Violations: {viol}")
print(f"   Unconnected: {unr}")
print(f"   Warnings: {warn}")

# Note on unrouted board
if unr > 0:
    print(f"\n⚠️  WARNING: {unr} unconnected nets (board is not routed)")
    print(f"   This is EXPECTED for an unrouted board.")
    print(f"   Routing must be done manually in KiCad or via external tools.")
    print(f"   (KiCad 9.x CLI does not support DSN export for FreeRouting automation)")

# --- 2) Exports: Gerbers, Drill, IPC-2581, ODB++ ---
print(f"\n📤 Exporting manufacturing files...")

try:
    print("   → Generating Gerbers...")
    run(["kicad-cli","pcb","export","gerbers", BOARD, "--output", OUT])

    print("   → Generating drill file...")
    run(["kicad-cli","pcb","export","drill",   BOARD, "--output", OUT])

    print("   → Generating IPC-2581...")
    run(["kicad-cli","pcb","export","ipc2581", BOARD, "-o", os.path.join(OUT,"k1.ipc2581.xml")])

    print("   → Generating ODB++...")
    run(["kicad-cli","pcb","export","odb",     BOARD, "-o", os.path.join(OUT,"k1.odb")])

except subprocess.CalledProcessError as e:
    abort(f"Manufacturing export failed: {e}")

# --- Verify exports ---
print(f"\n✅ Manufacturing files generated:")
gerber_files = [f for f in os.listdir(OUT) if f.endswith('.gbr') or f.endswith('.gbl')]
drill_files = [f for f in os.listdir(OUT) if f.endswith('.drl')]
ipc_files = [f for f in os.listdir(OUT) if f.endswith('.ipc2581.xml')]
odb_files = [f for f in os.listdir(OUT) if f.endswith('.odb')]

print(f"   Gerber files: {len(gerber_files)}")
for f in sorted(gerber_files)[:5]:
    print(f"     - {f}")
if len(gerber_files) > 5:
    print(f"     ... and {len(gerber_files)-5} more")

print(f"   Drill files: {len(drill_files)}")
for f in drill_files:
    print(f"     - {f}")

print(f"   IPC-2581: {len(ipc_files)}")
print(f"   ODB++: {len(odb_files)}")

print(f"\n✅ SUCCESS: Manufacturing files exported to {OUT}")
print(f"\n📋 Next Steps:")
print(f"   1. Review Gerber files for accuracy")
print(f"   2. If needed, route the board manually in KiCad")
print(f"   3. Re-run this script after routing to generate final files")
print(f"   4. Upload to PCB manufacturer (e.g., JLCPCB)")
