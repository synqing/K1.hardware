# JLCPCB PCB Panelization Guidelines

## Panelization Overview

JLCPCB supports panelized PCB manufacturing to optimize cost and manufacturing efficiency. Panelization involves combining multiple board designs into a larger substrate.

## Panelization Methods

### V-Cuts (Preferred)

**What it is**: V-shaped grooves routed partway through the substrate, allowing boards to be snapped apart by hand.

**Advantages**:
- Clean board edges after separation
- Professional appearance
- Recommended by JLCPCB for most projects
- Lower cost than other methods

**Specifications**:
- Typical groove depth: 50% of PCB thickness (e.g., 0.8mm for 1.6mm board)
- Groove angle: 45° (V-cut)
- Minimum spacing from V-cut to traces: 0.2mm clearance

**When to use**: Standard PCBs that don't require fully routed edges.

### Mouse-Bites

**What it is**: Array of small perforations (holes) around the board edge for mechanical separation.

**Advantages**:
- Fully routed board edges possible
- Precise control over separation path
- Works for odd-shaped boards

**Disadvantages**:
- Leaves small witness marks/holes at break points
- Slightly higher cost
- Requires bit more cleanup post-manufacturing

**Specifications**:
- Hole diameter: 0.8-1.0mm typical
- Hole spacing: 2-4mm (typical: 3mm)
- Hole depth: Through the entire panel (not the individual board)

**When to use**: Non-rectangular boards or designs requiring custom edge profiles.

### Routed Edges (Full Tab Routing)

**What it is**: Complete routing around board perimeter, leaving only small tabs or bridges for holding.

**Advantages**:
- Maximum design flexibility
- Fully routed edges on final product
- Custom shapes possible

**Disadvantages**:
- Higher cost
- Requires careful tab positioning
- More manual labor for separation

**When to use**: Complex shapes, or when clean fully-routed edges are critical.

## Design Rules for Panelization

### Minimum Spacing
- **Between boards**: 0.5-1.0mm minimum (0.8mm recommended)
- **From edge to traces**: 0.2mm clearance
- **From edge to vias**: 0.3mm clearance

### Fiducial Placement
- Place fiducials for assembly outside individual boards
- Typically on panel borders
- 3mm diameter pads recommended

### Component Clearance
- No components within 5mm of cut line (for hand breakage)
- No fine pitch components near cut edges

### Copper Balancing
- Maintain uniform copper density on both sides
- Unbalanced designs can warp during manufacturing
- Add copper pours near cut lines if needed

## Panel Dimensions

- **Maximum panel size**: 510mm × 610mm
- **Recommended panels**: 200mm × 250mm to 400mm × 500mm
- **Minimum board size**: 10mm × 10mm
- **Typical panel utilization**: 60-80%

## Tooling & Registration

- Tooling holes: 3.2mm diameter, typically 4-8 holes per panel
- 1-2 registration marks per board for placement verification
- Fiducial marks for solder paste dispensing

## Assembly Considerations (if using JLCPCB SMT)

- Provide single-panel design to JLCPCB (they can panelize internally)
- If submitting panelized board:
  - Clearly mark individual board boundaries
  - Provide bill of materials for each board
  - Ensure component placement doesn't cross board boundaries

### iBOM Generation
- JLCPCB iBOM typically generated per individual board, not panel
- Use KiKit or similar tools to separate boards back into individual files for reference

## Cost Implications

- Panelization reduces per-unit cost (shared panel cost)
- V-cuts are cheapest separation method
- More panels needed = lower per-unit cost but higher upfront panel cost
- Use panelization when ordering 50+ units

## Typical JLCPCB Panel Workflow

1. Design single board in KiCad
2. Use KiKit to panelize (grid layout with V-cuts)
3. Export Gerbers from panelized board
4. Export BOM and CPL from individual board (for assembly reference)
5. Submit panelized Gerbers to JLCPCB
6. Manually snap boards after receiving panelized PCB

## Example Specifications

For K1 Lightwave 4×2 panel:
- Board size: 80mm × 60mm (example)
- Panel layout: 4 boards wide × 2 boards tall
- Separation: V-cuts between boards
- Total panel: ~335mm × 130mm
- Cost per board: ~50% reduction vs. single board manufacturing

**Note**: Exact specifications should be verified with current JLCPCB design rules, as requirements may change.

Source: JLCPCB Community Documentation (cached)
