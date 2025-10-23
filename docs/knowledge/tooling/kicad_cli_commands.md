# KiCad CLI Commands Reference

## Overview

KiCad v8+ CLI enables headless automation of schematics, PCBs, and manufacturing exports. All commands support JSON output for programmatic processing.

## Electrical Rule Check (ERC)

### Command
```bash
kicad-cli sch erc [options] <schematic_file>
```

### Key Options
- `--output <file>`: Specify report filename
- `--format <format>`: Choose "report" (default) or "json"
- `--severity-all/error/warning/exclusions`: Filter violation types
- `--exit-code-violations`: Return exit code 5 if violations found

### Example
```bash
kicad-cli sch erc --output test_erc.json --format json project.kicad_sch
```

## Design Rule Check (DRC)

### Command
```bash
kicad-cli pcb drc [options] <board_file>
```

### Key Options
- `--output <file>`: Set report destination
- `--format <format>`: Select "report" or "json"
- `--schematic-parity`: Test PCB-to-schematic alignment
- `--all-track-errors`: Report every track violation
- `--exit-code-violations`: Exit with code 5 on violations

### Example
```bash
kicad-cli pcb drc --output test_drc.json --format json --schematic-parity project.kicad_pcb project.kicad_sch
```

## PCB Export Operations

### Gerber Export
```bash
kicad-cli pcb export gerbers <board_file>
# or single-layer variant
kicad-cli pcb export gerber <board_file>
```

### 3D Model Export
```bash
# STEP (Solid modeling)
kicad-cli pcb export step <board_file>

# GLB (Glitch-free, suitable for web/Babylon.js)
kicad-cli pcb export glb <board_file>

# VRML (Legacy 3D format)
kicad-cli pcb export vrml <board_file>
```

### Additional PCB Exports
- `pcb export pdf` - PDF drawings
- `pcb export svg` - SVG vector graphics
- `pcb export dxf` - AutoCAD format
- `pcb export drill` - NC drill files
- `pcb export pos` - Component placement coordinates (pick & place)
- `pcb export ipc2581` - Unified manufacturing format (IPC-2581)

## Schematic Export Operations

### Bill of Materials
```bash
kicad-cli sch export bom <schematic_file>
# Formats: csv, tsv, xml, json (with --format)
```

### Netlist Export
```bash
kicad-cli sch export netlist <schematic_file>
# Formats: kicad (default), eagle, pads, cadstar, spice, ipc
```

### Drawing Exports
- `sch export pdf` - PDF of schematic
- `sch export svg` - SVG vector graphics
- `sch export dxf` - AutoCAD format
- `sch export hpgl` - HP plotter format
- `sch export ps` - PostScript

## Symbol & Footprint Exports

```bash
kicad-cli sym export svg <symbol_file>
kicad-cli fp export svg <footprint_file>
```

## Common Patterns for K1 Lightwave

### Complete Validation Flow
```bash
# Run ERC on schematic
kicad-cli sch erc --format json --output reports/erc.json hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch

# Run DRC with schematic parity check
kicad-cli pcb drc --format json --output reports/drc.json \
  --schematic-parity \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch

# Export BOM for component lookup
kicad-cli sch export bom --format json --output reports/bom.json \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch

# Export 3D model
kicad-cli pcb export glb --output reports/K1_Lightwave.glb \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
```

### Manufacturing Export
```bash
# Gerbers for PCB fab
kicad-cli pcb export gerbers --output gerbers/ \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb

# Component placement for assembly
kicad-cli pcb export pos --output placement.csv \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb

# Drill file for CAM
kicad-cli pcb export drill --output drill.txt \
  hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb
```

## Return Codes

- `0` - Success, no violations
- `1` - General error (missing file, invalid format)
- `5` - Violations found (with `--exit-code-violations`)

## Notes

- JSON output is recommended for programmatic processing
- All paths support both absolute and relative paths
- Use `--help` for complete option listing
- Most exports require project files to be valid

Source: KiCad v8 CLI Documentation
