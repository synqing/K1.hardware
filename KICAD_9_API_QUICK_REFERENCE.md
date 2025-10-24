# KiCad 9 Python API - Quick Reference

## Critical Decision Matrix

### Which API Should I Use?

```
Do you need to...                      | Use This
---------------------------------------|-------------------
Load .kicad_pcb file (standalone)?    | SWIG pcbnew (K9) or kicad-cli
Modify open board in KiCad editor?    | IPC API (K9+) or SWIG (K9)
Add footprints programmatically?      | SWIG (K9) or kicad-python wrapper
Export Gerber/manufacturing files?    | kicad-cli (all versions)
Run DRC checks?                        | kicad-cli (fastest)
Work in Docker/CI environment?        | kicad-cli + xvfb (for GUI)
Create traces between pads?           | SWIG pcbnew (most direct)
Repour copper zones?                  | SWIG pcbnew or kicad-python
Write KiCad 10+ compatible code?      | kicad-python wrapper only
```

---

## Command Quick Reference

### Load and Modify Board (SWIG - KiCad 9)

```python
import pcbnew

# Load
board = pcbnew.LoadBoard("design.kicad_pcb")

# Access components
for fp in board.GetFootprints():
    print(fp.GetReference())

# Move component
fp = board.FindFootprintByReference("U1")
fp.SetPosition(pcbnew.wxPointMM(50.0, 50.0))

# Rotate
fp.SetOrientation(45 * 10)  # 45 degrees (10ths of degrees)

# Save
board.Save("design.kicad_pcb")
```

### Add Footprint and Connect to Net

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

# Load footprint from library
fp = pcbnew.FootprintLoad(
    "/path/to/library",
    "Resistor_SMD.pretty",
    "R_0603_1608Metric"
)

# Position
fp.SetPosition(pcbnew.wxPointMM(25.4, 50.8))
board.Add(fp)

# Connect to net
net = board.FindNet("GND")
for pad in fp.Pads():
    pad.SetNet(net)

board.Save("design.kicad_pcb")
```

### Create Trace

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

track = pcbnew.PCB_TRACK(board)
track.SetStart(pcbnew.wxPointMM(10, 10))
track.SetEnd(pcbnew.wxPointMM(20, 10))
track.SetWidth(pcbnew.FromMM(0.25))
track.SetLayer(pcbnew.F_Cu)
board.Add(track)

board.Save("design.kicad_pcb")
```

### Create Via

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

via = pcbnew.PCB_VIA(board)
via.SetPosition(pcbnew.wxPointMM(15, 15))
via.SetWidth(pcbnew.FromMM(0.8))
via.SetDrill(pcbnew.FromMM(0.4))
via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)

net = board.FindNet("GND")
via.SetNet(net)
board.Add(via)

board.Save("design.kicad_pcb")
```

### Create Copper Zone

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

# Create zone
zone = board.AddArea(pcbnew.F_Cu, 0, 0, pcbnew.PCB_SHAPE_TYPE_POLYGON)

# Define polygon
zone.AppendCorner(pcbnew.wxPointMM(5, 5))
zone.AppendCorner(pcbnew.wxPointMM(15, 5))
zone.AppendCorner(pcbnew.wxPointMM(15, 15))
zone.AppendCorner(pcbnew.wxPointMM(5, 15))

# Connect to net
net = board.FindNet("GND")
zone.SetNet(net)

# Refill
zone.SetNeedRefill(True)
board.RefillAllZones()

board.Save("design.kicad_pcb")
```

### Repour All Zones

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

for zone in board.GetAreas():
    zone.SetNeedRefill(True)

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.GetAreas())

board.Save("design.kicad_pcb")
```

---

## kicad-cli Quick Reference

### Generate Gerber Files

```bash
kicad-cli pcb export gerbers \
  --output ./gerbers \
  --layers F_Cu,B_Cu,F_SilkS,B_SilkS,F_Mask,B_Mask,Edge_Cuts \
  design.kicad_pcb
```

### Generate Drill Files

```bash
kicad-cli pcb export drill \
  --output design.drill \
  design.kicad_pcb
```

### Generate Position File (Pick & Place)

```bash
kicad-cli pcb export pos \
  --format csv \
  --output design.pos \
  design.kicad_pcb
```

### Export STEP Model

```bash
kicad-cli pcb export step \
  --output design_3d.step \
  design.kicad_pcb
```

### Run DRC

```bash
# Text report
kicad-cli pcb drc \
  --output drc_report.txt \
  design.kicad_pcb

# JSON report
kicad-cli pcb drc \
  --format json \
  --output drc_report.json \
  design.kicad_pcb

# Only errors
kicad-cli pcb drc \
  --severity-error \
  --exit-code-violations \
  design.kicad_pcb
```

---

## Coordinate Conversion

### KiCad Internal Units

KiCad stores coordinates in **millionths of millimeters** (nm):

```python
# CORRECT: Convert mm to KiCad units
coord_mm = 25.4
coord_internal = int(coord_mm * 1000000)

# OR: Use helper functions
from_mm = pcbnew.FromMM(25.4)
wxPoint = pcbnew.wxPointMM(25.4, 50.8)

# REVERSE: Convert internal to mm
coord_mm = coord_internal / 1000000.0
```

### Layer Constants

```python
# Copper layers
pcbnew.F_Cu      # Front copper
pcbnew.B_Cu      # Back copper
pcbnew.In1_Cu    # Inner layer 1
pcbnew.In2_Cu    # Inner layer 2
# ... up to In30_Cu

# Silk screen
pcbnew.F_SilkS   # Front silkscreen
pcbnew.B_SilkS   # Back silkscreen

# Solder mask
pcbnew.F_Mask    # Front mask
pcbnew.B_Mask    # Back mask

# Other
pcbnew.Edge_Cuts # Board edge
pcbnew.Margin    # Margin
pcbnew.F_Fab     # Front fab
pcbnew.B_Fab     # Back fab
```

---

## Common Patterns

### Pattern: Find Component and Get Its Properties

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

fp = board.FindFootprintByReference("U1")
if fp:
    print(f"Reference: {fp.GetReference()}")
    print(f"Value: {fp.GetValue()}")
    print(f"Footprint: {fp.GetFPID().GetFootprintName()}")

    pos = fp.GetPosition()
    x = pos.x / 1000000.0  # Convert to mm
    y = pos.y / 1000000.0
    print(f"Position: ({x:.3f}, {y:.3f})")

    rot = fp.GetOrientation() / 10.0  # Convert to degrees
    print(f"Rotation: {rot}°")

    # List pads
    for pad in fp.Pads():
        print(f"  Pad {pad.GetNumber()}: {pad.GetNet().GetNetname()}")
```

### Pattern: Find All Nets on Board

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

for netinfo in board.GetNetInfo().NetsByName().values():
    print(f"Net: {netinfo.GetNetname()} (code: {netinfo.GetNetCode()})")
```

### Pattern: Iterate All Traces

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

for track in board.GetTracks():
    if track.GetClass() == "PCB_TRACK":
        start = track.GetStart()
        end = track.GetEnd()
        width = track.GetWidth()
        layer = track.GetLayer()
        net = track.GetNet().GetNetname()

        print(f"Track: {net} on layer {layer}, "
              f"from ({start.x},{start.y}) to ({end.x},{end.y}), "
              f"width {width}")
```

### Pattern: Find All Vias

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

for track in board.GetTracks():
    if track.GetClass() == "PCB_VIA":
        via = track
        pos = via.GetPosition()
        width = via.GetWidth()
        drill = via.GetDrillValue()
        net = via.GetNet().GetNetname()

        print(f"Via: {net} @ ({pos.x},{pos.y}), "
              f"size {width}, drill {drill}")
```

---

## Installation

### Install kicad-cli

**macOS**:
```bash
# Already included with KiCad installation
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli --version
```

**Linux**:
```bash
# Usually in PATH after KiCad installation
kicad-cli --version

# Or explicit path
/usr/bin/kicad-cli --version
```

**Windows**:
```bash
# Usually in PATH after KiCad installation
kicad-cli --version

# Or:
"C:\Program Files\KiCad\bin\kicad-cli.exe" --version
```

### Install kicad-python Wrapper

```bash
# Install from PyPI
pip install kicad-python

# Or from source (atait fork)
git clone https://github.com/atait/kicad-python.git
cd kicad-python
pip install -e .
```

---

## Troubleshooting

### Error: "No module named 'pcbnew'"

**Cause**: KiCad Python bindings not installed or wrong Python version

**Solution**:
```bash
# Check KiCad installation
which kicad

# Use KiCad's bundled Python
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 -c "import pcbnew"

# Or set PYTHONPATH
export PYTHONPATH=/Applications/KiCad/KiCad.app/Contents/SharedSupport/python:$PYTHONPATH
```

### Error: "Coordinate units are wrong (very small)"

**Cause**: Mixing mm and internal units

**Solution**:
```python
# WRONG
fp.SetPosition(wxPoint(100, 200))  # Too small!

# CORRECT
fp.SetPosition(pcbnew.wxPointMM(100, 200))  # 100mm, 200mm
```

### Error: "Object doesn't appear on board"

**Cause**: Object not added to board with `board.Add()`

**Solution**:
```python
track = pcbnew.PCB_TRACK(board)
# ... set properties ...
board.Add(track)  # MUST DO THIS

board.Save("design.kicad_pcb")
```

### Error: "Board is locked / in use"

**Cause**: Board open in KiCad editor while script modifies it

**Solution**: Close the board in KiCad before running script
```python
# Alternative: Use IPC API if KiCad must stay open
from kicad.pcbnew import board
b = board.Board.from_editor()
```

### Error: "Cannot assign net to pad"

**Cause**: Net doesn't exist in board

**Solution**:
```python
# Create net if it doesn't exist
net = board.FindNet("GND")
if not net:
    net = pcbnew.NETINFO_ITEM(board, "GND")

# Then add footprint
board.Add(fp)

# Then assign net
pad.SetNet(net)
```

---

## Performance Tips

1. **Batch Operations**: Multiple `board.Add()` calls before single `board.Save()`
2. **Zone Refill**: Only call `ZONE_FILLER` once with all zones
3. **Close GUI**: Close KiCad editor before modifying with SWIG
4. **Use kicad-cli for Exports**: Much faster than loading/saving in Python

---

## KiCad 9 vs KiCad 10 Migration

### Key Breaking Changes

| What | KiCad 9 | KiCad 10 |
|-----|---------|----------|
| `import pcbnew` | ✅ Works | ❌ Removed |
| File loading | Direct | Via IPC only |
| Standalone scripts | ✅ Works | Must use kicad-cli |

### Migration Strategy

```python
# KiCad 9 compatible code
try:
    import pcbnew
    KICAD_VERSION = 9
except ImportError:
    from kicad.pcbnew import board
    KICAD_VERSION = 10

if KICAD_VERSION == 9:
    board = pcbnew.LoadBoard("design.kicad_pcb")
else:
    # KiCad 10+: Use IPC API with running KiCad
    board = board.Board.from_editor()
```

---

## Useful Snippets

### Extract BOM

```python
import pcbnew
import csv

board = pcbnew.LoadBoard("design.kicad_pcb")

with open("bom.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Reference", "Value", "Footprint"])

    for fp in board.GetFootprints():
        writer.writerow([
            fp.GetReference(),
            fp.GetValue(),
            fp.GetFPID().GetFootprintName()
        ])
```

### Check All Nets

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

nets = board.GetNetInfo().NetsByName()
for net_name, net_info in nets.items():
    pad_count = len(board.FindNet(net_name).GetPads())
    print(f"{net_name}: {pad_count} pads")
```

### Measure Board Size

```python
import pcbnew

board = pcbnew.LoadBoard("design.kicad_pcb")

bbox = board.ComputeBoundingBox()
width_mm = bbox.GetWidth() / 1000000.0
height_mm = bbox.GetHeight() / 1000000.0

print(f"Board size: {width_mm:.1f}mm x {height_mm:.1f}mm")
```

---

## Reference Links

- **Official Docs**: https://dev-docs.kicad.org/en/apis-and-binding/
- **Doxygen (K9)**: https://docs.kicad.org/doxygen-python-9.0/
- **kicad-python**: https://github.com/atait/kicad-python
- **Forum**: https://forum.kicad.info/c/external-plugins/17
- **CLI Docs**: https://docs.kicad.org/9.0/en/cli/cli.html

---

**Last Updated**: October 24, 2025
**Tested On**: KiCad 9.0
**License**: Public Domain
