# Interactive HTML BOM (iBOM) Guide

## Overview

Interactive HTML BOM (iBOM) is a KiCad plugin that generates a single self-contained HTML file serving as an interactive bill of materials (BOM) for assembly and component verification.

## Key Features

### Interactive Functionality
- **Click to highlight**: Click any component in the BOM list to highlight it on the board
- **Board visualization**: Embedded KiCad PCB rendering showing component placement
- **Searchable BOM**: Filter components by value, reference, or footprint
- **Component details**: Hover or click to see component properties

### Export Formats
- Single HTML file (self-contained, no external dependencies)
- No web server required (fully static)
- Works offline and in any modern browser
- Mobile-responsive design

## Installation

### As KiCad Plugin
iBOM is typically installed as a KiCad plugin:
```bash
pip install InteractiveHtmlBom
```

Or within KiCad's plugin manager:
1. Open KiCad → Preferences → Plugin Manager
2. Search for "Interactive HTML BOM"
3. Install and enable

### Command-Line Usage
```bash
kibot -c ibom_config.yaml project.kicad_pcb
# or
python -m InteractiveHtmlBom.cli project.kicad_pcb
```

## Configuration Options

### iBOM-Specific Fields

Custom fields can be added to components for assembly purposes:

| Field | Purpose | Example |
|-------|---------|------|
| `LCSC` | LCSC C-number | C12345 |
| `MPN` | Manufacturer part number | ESP32-S3-WROOM-1 |
| `Supplier` | Component source | LCSC, Digi-Key |
| `DNP` | Do Not Populate | Yes/No |
| `Quantity Per` | Quantity needed per unit | 1, 2, etc. |

### Common Configurations

```yaml
# KiBot configuration for iBOM
outputs:
  - name: ibom
    comment: Interactive BOM
    type: ibom
    options:
      name: "K1_Lightwave"
      dark_mode: true
      copy_net: true
      show_fields:
        - Value
        - Footprint
        - LCSC
        - MPN
      extra_fields:
        - LCSC
        - MPN
        - DNP
```

## Assembly Workflow

### Step 1: Generate iBOM
After completing schematic and PCB layout:
```bash
kibot -c bom_config.yaml K1_Lightwave.kicad_pcb
```

Output: `K1_Lightwave.html` (ready to open in any browser)

### Step 2: Populate BOM Fields
In KiCad, fill in custom fields for each component:
1. Open schematic
2. Edit each symbol to add LCSC, MPN, or other fields
3. Re-export iBOM to include new fields

### Step 3: Assembly Reference
During assembly:
1. Open `K1_Lightwave.html` in browser
2. Click each component in the BOM list
3. Component highlights on board rendering
4. Technician places component at marked location
5. Check off in BOM or use assembly guide

## Customization

### Custom HTML/CSS
iBOM can be customized with:
- Company logo
- Custom CSS styling
- Additional assembly notes
- Work instructions per component

### Multi-Board BOM
For panelized designs:
1. Generate iBOM from single-board design (not panelized board)
2. Multiply quantities by number of boards in panel
3. Use for assembly planning across panel

## Output File Details

The generated HTML file contains:
- Embedded SVG rendering of PCB (no image files needed)
- Component list with all properties
- JavaScript for interactivity (no external libraries)
- File size: typically 1-5 MB depending on board complexity

## Best Practices

### BOM Completeness
- Ensure all components have RefDes (reference designators) in schematic
- Populate LCSC/MPN fields for all components
- Use meaningful values (e.g., "10µF" not just "C")
- Flag DNP components clearly

### Assembly Clarity
- Organize components by function (power, signal, passives)
- Include assembly notes in component description field
- Use consistent naming for similar components
- Add solder type notes if mixed lead-free / leaded

### File Management
- Regenerate iBOM whenever schematic changes
- Include iBOM in fab pack documentation
- Version iBOM with the PCB revision
- Archive with manufacturing files

## For K1 Lightwave

Typical workflow:
```bash
# After final schematic and layout
kibot -c ibom.yaml hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb

# Output: K1_Lightwave_bom.html
# Use for assembly planning and component picking
```

## Advantages Over CSV BOM

| Feature | iBOM | CSV BOM |
|---------|------|---------|
| Visual feedback | Yes | No |
| Interactive highlighting | Yes | No |
| No external tools | Yes | Needs spreadsheet |
| Self-contained | Yes | No (references external) |
| Assembly-friendly | Yes | Requires reference |
| Mobile-friendly | Yes | Limited |

## Troubleshooting

### iBOM shows blank board
- Ensure KiCad PCB file is valid
- Check that board was rendered in KiCad before exporting
- Try regenerating with KiBot instead of plugin

### Components don't highlight
- Refresh browser cache (Ctrl+F5 or Cmd+Shift+R)
- Check that component RefDes matches between schematic and PCB
- Verify component footprints are assigned correctly

Source: Interactive HTML BOM GitHub/KiCad Documentation (cached)
