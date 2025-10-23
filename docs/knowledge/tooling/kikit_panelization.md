# KiKit: Automated PCB Panelization and Fab Prep

## Overview

KiKit is a Python library, KiCAD plugin, and CLI tool designed to automate common KiCAD workflows:
- Board panelization (regular and arbitrarily shaped boards)
- Manufacturing data export using manufacturer presets
- Multi-board project organization
- Presentation page generation
- Mouse-bite and V-cut creation
- Design rule check (DRC) compliance for panelized boards

## Key Principle

Everything KiKit does can be done manually in KiCAD's Pcbnew. KiKit simplifies repetitive tasks through CLI commands, Python scripting, or a KiCAD GUI plugin.

## Panelization Methods

### 1. CLI Usage
The simplest approach for standard panelization:
```bash
kikit panelize --layout grid 4 2 board.kicad_pcb output.kicad_pcb
```

### 2. GUI Plugin
For users preferring visual tools, KiKit integrates into KiCAD's plugin ecosystem.

### 3. Python Scripting
For advanced customization and multi-board workflows:
```python
from kikit.panelize import Panel
panel = Panel("board.kicad_pcb")
panel.appendBoard([0, 0], "board.kicad_pcb")
panel.save("panelized.kicad_pcb")
```

## Panelization Features

### Board Arrangement
- **Grid layout**: Arrange boards in rows and columns
- **Multiple instances**: Add same board multiple times
- **Substrate bridges**: Connect boards with support material
- **Custom positioning**: Place boards at specific coordinates

### Separation Methods

#### Mouse-Bites
- Small perforations around board edge
- Manual breaking after manufacturing
- Better for boards that need fully routed edges
- Leaves small defects where bites were

#### V-Cuts
- V-shaped grooves routed into substrate
- Can be snapped by hand or machine
- Better for panels that need clean edges
- JLC generally prefers for most boards

#### Tabs
- Solid material connections
- User breaks manually or tools for breaking
- Simple, reliable method

## Manufacturer Presets

KiKit includes presets for common PCB manufacturers:

### JLC Preset
Optimized for JLCPCB panelization:
```bash
kikit fab jlcpcb board.kicad_pcb output.kicad_pcb
```

Features:
- Automatic DRC compliance
- JLC-specific feature clearances
- iBOM generation for assembly
- BOM and placement file creation

## Common Workflows

### Simple 4x2 Grid Panelization
```bash
kikit panelize --layout grid 4 2 --separation 2 \
  --verticalCuts --horizontalCuts \
  board.kicad_pcb panelized.kicad_pcb
```

### JLC Assembly Prep
```bash
kikit fab jlcpcb --assembly board.kicad_pcb fab_output/
# Generates: PCB file, iBOM HTML, assembly BOM/POS files
```

### JLCPCB with Custom Spacing
```bash
kikit panelize --layout grid 4 8 \
  --separation 2 \
  --verticalCuts --mousebites --horiztontalCuts \
  board.kicad_pcb output.kicad_pcb
```

## Output Files

After panelization, expect:
- `panelized.kicad_pcb` - Ready for Gerber export
- `board.kicad_sch` - Schematic (unchanged)
- Optional: BOM, placement, iBOM HTML

## For K1 Lightwave

Typical workflow:
```bash
# Create panelized board (4x2 grid)
kikit fab jlcpcb --assembly hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb fab_output/

# Export Gerbers from panelized board
kicad-cli pcb export gerbers fab_output/K1_Lightwave.kicad_pcb

# Submit fab_output/ to JLCPCB
```

## License & Support

Distributed under MIT License. Developer accepts sponsorship via GitHub Sponsors, Patreon, and Ko-fi.

Source: KiKit GitHub Repository
