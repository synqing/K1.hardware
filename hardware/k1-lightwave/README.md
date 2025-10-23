# K1 Lightwave Hardware Design — Tooling Guide

This folder contains the KiCad schematic, PCB layout, and supporting design files for the K1 Lightwave dual-ESP32-S3 music visualizer.

---

## Folder Structure

```
k1-lightwave/
├── kicad/
│   ├── K1_Lightwave.kicad_sch      ← Master schematic
│   ├── K1_Lightwave.kicad_pcb      ← PCB layout
│   ├── K1_Lightwave.kicad_pro      ← KiCad project file
│   ├── symbols/                    ← Custom/library symbols
│   ├── footprints/                 ← Custom/library footprints
│   └── 3d_models/                  ← 3D STEP/VRML models
├── skidl/
│   └── hello_board.py              ← Example SKiDL schematic generator
└── README.md                         ← You are here
```

---

## MCP Tool Commands

All tools are wired as Claude Code MCP servers. Use them to validate design changes.

### **Electrical Rules Check (ERC)**

```
sch_erc(schematic, out="erc.json", format="json", exit_code_violations=True)
```

**Example:**
```python
result = sch_erc("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch", out="erc.json")
# Returns: {"returncode": 0, "ok": true, "summary": {"errors": 0, "warnings": 0}}
```

**Pass criteria:** `error_count == 0`

---

### **Design Rules Check (DRC)**

```
pcb_drc(board, out="drc.json", format="json", exit_code_violations=True)
```

**Example:**
```python
result = pcb_drc("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out="drc.json")
# Returns: {"returncode": 0, "ok": true, "summary": {"violations": 0}}
```

**Pass criteria:** `violations == 0` (JLC 4-layer rules in `design_rules.kicad_dru`)

---

### **Bill of Materials (BOM) Export**

```
sch_export_bom(schematic, out_csv="bom.csv", fields="*")
```

**Example:**
```python
result = sch_export_bom("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch", out_csv="bom.csv")
# Exports: bom.csv with all component fields
```

---

### **Netlist Export** (for routing/SKiDL)

```
sch_export_netlist(schematic, out_net="project.net", fmt="kicadsexpr")
```

**Example:**
```python
result = sch_export_netlist("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch", out_net="k1.net")
# Exports: S-expression netlist for DSN → routing workflow
```

---

### **Gerber/Drill/STEP/IPC-2581 Exports**

```
pcb_export_gerbers(board, out_dir="fab/gerbers")
pcb_export_drill(board, out_dir="fab/drill")
pcb_export_step(board, out_file="mechanical/board.step")
pcb_export_ipc2581(board, out_file="fab/board.ipc")
```

**Example:**
```python
pcb_export_gerbers("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_dir="fab/gerbers")
pcb_export_drill("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_dir="fab/drill")
pcb_export_step("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_file="fab/board.step")
# Creates fab-ready artifacts
```

---

### **Netlist Generation from SKiDL**

```
skidl_gen_netlist(script_path="skidl/hello_board.py", out_net="skidl_out.net")
```

**Example:**
```python
result = skidl_gen_netlist("hardware/k1-lightwave/skidl/hello_board.py", out_net="k1.net")
# Returns: {"parts": 12, "nets": 8, "output": "/path/to/k1.net"}
```

---

### **Component Lookup (Nexar/LCSC)**

```
parts_search(q="ESP32-S3-WROOM-1", limit=3)
best_datasheet_url(mpn="WS2812B")
lcsc_search(keyword="C2653")
```

**Example:**
```python
result = parts_search("ESP32-S3-WROOM-1", limit=3)
# Returns: MPN, manufacturer, best_datasheet URL

ds = best_datasheet_url("WS2812B")
# Returns: {"mpn": "WS2812B", "url": "https://...", "ok": true}

item = lcsc_search("C2653")
# Returns: LCSC product info (pricing, stock, etc.)
```

---

### **Panelization (KiKit)**

```
kikit_panelize_grid(input_pcb, output_pcb, rows=4, cols=8, space_mm="2mm", tabs="full", cuts="vcuts; clearance: 0.4mm", rails_mm="5mm")
```

**Example:**
```python
result = kikit_panelize_grid(
    "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    "hardware/k1-lightwave/kicad/K1_Lightwave_PANEL_4x8.kicad_pcb",
    rows=4, cols=8, space_mm="2mm", rails_mm="5mm"
)
# Creates panelized board with V-cuts and mousebites
```

---

### **JLC Assembly Pack (KiKit)**

```
kikit_fab_jlcpcb(board_or_panel, out_dir="fab/jlc", assembly=True, schematic="...", field="LCSC", autoname=True)
```

**Example:**
```python
result = kikit_fab_jlcpcb(
    "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_dir="fab/jlc",
    assembly=True,
    schematic="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch",
    field="LCSC"
)
# Generates: gerbers.zip, bom.csv, pos.csv (JLC-ready)
```

---

### **Interactive BOM (iBOM)**

```
generate(board_kicad_pcb, out_dir="docs/ibom", name_format="ibom", extra_fields="LCSC,MPN,Manufacturer")
```

**Example:**
```python
result = generate("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_dir="docs/ibom")
# Creates: docs/ibom/ibom.html (self-contained assembly guide)
```

---

### **CI Automation (KiBot)**

```
kibot_run(project_dir="hardware/k1-lightwave", config_yaml="kibot.yaml", out_dir="_artifacts", schematic="...", board="...")
```

**Example:**
```python
result = kibot_run(
    project_dir="hardware/k1-lightwave",
    config_yaml="kibot.yaml",
    out_dir="_artifacts",
    schematic="kicad/K1_Lightwave.kicad_sch",
    board="kicad/K1_Lightwave.kicad_pcb"
)
# Runs full KiBot pipeline (ERC, DRC, exports, docs)
```

---

### **Autorouting (FreeRouting)**

```
route(dsn="export.dsn", ses_out="routed.ses", ignore_nets="", timeout_sec=300)
```

**Example:**
```python
result = route("kicad/K1_Lightwave.dsn", ses_out="kicad/K1_Lightwave.ses")
# Routes board from KiCad DSN export → SES session file
```

---

## ⚠️ Critical Safety: Dual 5V Rails

> **External LED 5V required.** USB-C 5V powers the controller only. Do not power LED strips from USB-C.
> Use the **LED_5V_IN** connector, one polyfuse per LED output, and keep LED return paths short.
>
> **Power-domain guard enabled:** Schematic-level check prevents shorts between `VBUS_USB_5V` and `LED_5V` nets.
> If any component accidentally ties both nets, the fab pipeline will reject the design.

---

## Design Rules & Constraints

### **Manufacturing (JLC PCBWay 4-layer)**

- **Minimum trace width:** 0.1mm
- **Minimum clearance:** 0.1mm
- **Via diameter (finished):** 0.3mm min
- **Stackup:** Signal / Plane / Plane / Signal
- **Impedance (controlled):** 50Ω differential for high-speed signals

### **Electrical (K1 Lightwave)**

- **VCC (3.3V logic):** ±0.1V regulation
- **Power (5V input):** 5A budget, adjust per LED load
- **USB 5V (controller):** Powers MCUs + audio codec only via LDO
- **LED 5V (external):** Separate connector; never tied to USB rail
- **I2S audio:** BCLK/LRCLK/SD differential, <0.5mm lengths matched
- **SPI (LED data):** <5mm tracklength to level shifter + MCU
- **Ground:** Multi-point return (polygon fill on both internal planes)

### **Thermal**

- **LED driver max dissipation:** 1.5W (estimate via chain coverage)
- **MCU under full load:** Monitor thermal rise via STEP export
- **Thermal vias under high-current:** 8–16× 0.3mm vias per component

### **Layout Best Practices**

- **RF keepout:** 5mm from ESP32 module antenna edge
- **Audio coupling:** Ground guard on I2S traces; min 0.5mm clearance from LED switching
- **Power distribution:** Use star grounding; separate analog/digital returns only if needed
- **Test points:** Add TP for each major rail + UART + LED data/clock

---

## Validation Checklist

Before committing design changes, run:

```bash
# 1. ERC
sch_erc("kicad/K1_Lightwave.kicad_sch", out="erc.json")
# Expected: error_count == 0

# 2. DRC
pcb_drc("kicad/K1_Lightwave.kicad_pcb", out="drc.json")
# Expected: violations == 0

# 3. BOM & component availability
sch_export_bom("kicad/K1_Lightwave.kicad_sch", out_csv="bom.csv")
parts_search("ESP32-S3-WROOM-1", limit=3)  # verify stock
best_datasheet_url("SPH0645")  # verify datasheets available

# 4. Mechanical (3D check)
pcb_export_step("kicad/K1_Lightwave.kicad_pcb", out_file="fab/board.step")
# View in 3D viewer to catch clearance issues

# 5. Manufacturing data
pcb_export_ipc2581("kicad/K1_Lightwave.kicad_pcb", out_file="fab/board.ipc")
# For DFM analysis at fab
```

---

## Documentation

- **Hardware PRD:** `/docs/prd/02-hardware-prd.md`
- **Validation Plan:** `/docs/prd/03-validation-plan.md`
- **Datasheets:** `/docs/datasheets/` (ESP32-S3, SPH0645, IM69D130, WS2812B, SN74AHCT125, etc.)
- **Governance:** `/claude/GOVERNANCE.md` (design change protocol)

---

## References

- **KiCad CLI:** https://docs.kicad.org/cli/
- **KiCad Project:** K1_Lightwave.kicad_pro (PCBNew, Schematic Editor)
- **JLC/PCBWay DRC:** `/docs/datasheets/jlc-pcbway-4layer-drc.pdf`
- **ESP32-S3 Datasheet:** `/docs/datasheets/esp32-s3_datasheet_en.pdf`

---

**Last updated:** Oct 23, 2025
**Status:** Project scaffold — ready for design work
