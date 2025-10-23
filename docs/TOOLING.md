# K1 Lightwave — MCP Tools Reference & Examples

This document provides practical examples of using Claude Code MCP servers for K1 Lightwave hardware design and validation.

---

## MCP Server Commands

All tools are available as Claude Code tools via the MCP servers in `/mcp/`.

### **1. Schematic Electrical Rules Check (ERC)**

```python
# Run ERC on schematic, save results as JSON
result = sch_erc(
    schematic="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch",
    out="erc.json",
    format="json",
    exit_code_violations=True
)

# Result structure:
# {
#   "cmd": "kicad-cli sch erc ...",
#   "returncode": 0,
#   "ok": true,
#   "stdout": "...",
#   "output": "/full/path/to/erc.json",
#   "summary": {
#     "errors": 0,
#     "warnings": 0,
#     "exclusions": 0
#   }
# }
```

**When to use:** After every schematic edit (especially GPIO routing, power, signal integrity)

**Pass criteria:** `error_count == 0`

---

### **2. PCB Design Rules Check (DRC)**

```python
# Run DRC on board against JLC 4-layer rules
result = pcb_drc(
    board="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out="drc.json",
    format="json",
    exit_code_violations=True
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/drc.json",
#   "summary": {
#     "violations": 0,
#     "unconnected": 0
#   }
# }
```

**When to use:** After every PCB layout change; before gerber export

**Pass criteria:** `violations == 0`

**DRC rules file:** `hardware/k1-lightwave/kicad/design_rules.kicad_dru` (JLC/PCBWay 4-layer presets)

---

### **3. Bill of Materials Export**

```python
# Export BOM in CSV format with all fields
result = sch_export_bom(
    schematic="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch",
    out_csv="bom.csv",
    fields="*"  # Export all fields: Reference, Value, Footprint, Datasheet, LCSC, etc.
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/bom.csv"
# }

# BOM CSV contains:
# Reference,Value,Footprint,Quantity,Datasheet,LCSC
# R1,10k,R_0603,1,...,C25741
# C1,100uF,C_1206,1,...,C15849
# U1,ESP32-S3-WROOM-1U,BGA-48,2,...,C3040137
```

**When to use:** During component selection and DFM verification

**Next step:** Copy LCSC C-numbers to assembly BOM

---

### **4. Netlist Export (for routing)**

```python
# Export netlist in KiCad S-expression format (compatible with FreeRouting)
result = sch_export_netlist(
    schematic="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch",
    out_net="k1_lightwave.net",
    fmt="kicadsexpr"  # Options: kicadsexpr, kicadxml, cadstar, orcadpcb2, spice
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/k1_lightwave.net"
# }
```

**When to use:** Manual routing or preparation for FreeRouting autorouter

---

### **5. Gerber Export (for fabrication)**

```python
# Export Gerber files (one per layer)
result = pcb_export_gerbers(
    board="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_dir="fab/gerbers"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/fab/gerbers"
# }

# Output files:
# fab/gerbers/K1_Lightwave-F_Cu.gbr     (layer 1, front copper)
# fab/gerbers/K1_Lightwave-B_Cu.gbr     (layer 4, back copper)
# fab/gerbers/K1_Lightwave-F_SilkS.gbr  (front silkscreen)
# fab/gerbers/K1_Lightwave-B_SilkS.gbr  (back silkscreen)
# fab/gerbers/K1_Lightwave-F_Mask.gbr   (front solder mask)
# fab/gerbers/K1_Lightwave-B_Mask.gbr   (back solder mask)
# fab/gerbers/K1_Lightwave-PTH.drl      (drill file)
```

**When to use:** Final prep for fab; upload to JLC/PCBWay

---

### **6. Drill File Export**

```python
# Export drill file (via/hole coordinates)
result = pcb_export_drill(
    board="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_dir="fab/drill"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/fab/drill"
# }

# Output:
# fab/drill/K1_Lightwave.drl  (Excellon format)
# fab/drill/K1_Lightwave-NPTH.drl (non-plated holes)
```

**Note:** Gerbers already include drill layer; this is for reference/DFM review

---

### **7. STEP 3D Model Export**

```python
# Export 3D mechanical model (STEP format)
result = pcb_export_step(
    board="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_file="fab/K1_Lightwave.step"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/fab/K1_Lightwave.step"
# }
```

**When to use:** Mechanical clearance check; enclosure design; CAD assembly

**Tools:** FreeCAD, SolidWorks, Fusion 360 (all open STEP files)

---

### **8. IPC-2581 Manufacturing Data**

```python
# Export IPC-2581 file (comprehensive manufacturing dataset)
result = pcb_export_ipc2581(
    board="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_file="fab/K1_Lightwave.ipc"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/fab/K1_Lightwave.ipc"
# }
```

**When to use:** Advanced DFM analysis; digital manufacturing data exchange

---

### **9. Component Search (Nexar/Octopart)**

```python
# Search for components by name/MPN
result = parts_search(
    q="ESP32-S3-WROOM-1",
    limit=3
)

# Result:
# {
#   "data": {
#     "supSearch": {
#       "hits": {
#         "results": [
#           {
#             "part": {
#               "mpn": "ESP32-S3-WROOM-1",
#               "manufacturer": { "name": "Espressif" },
#               "bestDatasheet": { "url": "https://..." }
#             }
#           },
#           ...
#         ]
#       }
#     }
#   }
# }
```

**When to use:** Component sourcing, datasheets, alternates, pricing

---

### **10. Best Datasheet URL**

```python
# Get datasheet URL for a specific MPN
result = best_datasheet_url(mpn="WS2812B")

# Result:
# {
#   "mpn": "WS2812B",
#   "url": "https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf",
#   "ok": true
# }

# Use with fetch MCP to download:
# fetch(url, prompt="Extract electrical specifications")
```

**When to use:** Quick datasheet lookup during design

---

### **11. LCSC Part Search (JLC Assembly)**

```python
# Search LCSC for parts by keyword or C-number
result = lcsc_search(keyword="C2653")  # or MPN search

# Result:
# {
#   "code": 200,
#   "msg": "success",
#   "data": {
#     "products": [
#       {
#         "productCode": "C2653",
#         "productName": "...",
#         "totalPrice": 0.012,
#         "minBuy": 1,
#         "stockNumber": 50000,
#         ...
#       }
#     ]
#   }
# }
```

**When to use:** BOM verification for JLC assembly; pricing checks

---

### **12. Panelization (KiKit)**

```python
# Create a 4×8 panel with V-cuts and rails
result = kikit_panelize_grid(
    input_pcb="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    output_pcb="hardware/k1-lightwave/kicad/K1_Lightwave_PANEL_4x8.kicad_pcb",
    rows=4,
    cols=8,
    space_mm="2mm",
    tabs="full",
    cuts="vcuts; clearance: 0.4mm",
    rails_mm="5mm"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/K1_Lightwave_PANEL_4x8.kicad_pcb"
# }

# Output: Panelized board ready for DRC + gerber export
```

**When to use:** Cost optimization; batch manufacturing

---

### **13. JLC Assembly Pack (KiKit)**

```python
# Generate JLCPCB-ready fab pack (gerbers, BOM, pick-and-place)
result = kikit_fab_jlcpcb(
    board_or_panel="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_dir="fab/jlc",
    assembly=True,
    schematic="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch",
    field="LCSC"  # Use LCSC C-numbers for component lookup
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output_dir": "/full/path/to/fab/jlc"
# }

# Output:
# fab/jlc/gerbers.zip              (all gerber files)
# fab/jlc/bom.csv                  (assembly BOM with LCSC C-numbers)
# fab/jlc/pos.csv                  (pick-and-place coordinates)
# fab/jlc/K1_Lightwave-top.pdf     (top assembly layer)
```

**When to use:** Final assembly prep for JLCPCB submit

---

### **14. Interactive BOM (HTML Assembly Guide)**

```python
# Generate self-contained HTML BOM for assembly/reference
result = generate(
    board_kicad_pcb="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_dir="docs/ibom",
    name_format="ibom",
    extra_fields="LCSC,MPN,Manufacturer"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output_dir": "/full/path/to/docs/ibom"
# }

# Output:
# docs/ibom/ibom.html  (single HTML file; open in browser)
```

**When to use:** Assembly guide for production; maker reference

---

### **15. SKiDL Netlist Generation**

```python
# Generate netlist from Python SKiDL script
result = skidl_gen_netlist(
    script_path="hardware/k1-lightwave/skidl/hello_board.py",
    out_net="hello_board.net"
)

# Result:
# {
#   "output": "/full/path/to/hello_board.net",
#   "parts": 12,
#   "nets": 8,
#   "ok": true
# }
```

**When to use:** Automated schematic generation from Python; CI/CD builds

---

### **16. FreeRouting Autorouter**

```python
# Route board from KiCad DSN export
result = route(
    dsn="hardware/k1-lightwave/kicad/K1_Lightwave.dsn",
    ses_out="hardware/k1-lightwave/kicad/K1_Lightwave.ses",
    ignore_nets="",  # Optional: "GND,VCC" to skip specific nets
    timeout_sec=300  # 5 min timeout
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "output": "/full/path/to/K1_Lightwave.ses"
# }

# Workflow:
# 1. Export DSN from KiCad PCB Editor (File > Export > Specctra DSN)
# 2. Run route() above
# 3. Import .ses back into KiCad (File > Import > Specctra Session)
```

**When to use:** Batch autorouting for dense layouts

---

### **17. KiBot CI Automation**

```python
# Run KiBot config for complete fab/doc generation
result = kibot_run(
    project_dir="hardware/k1-lightwave",
    config_yaml="kibot.yaml",
    out_dir="_artifacts",
    schematic="kicad/K1_Lightwave.kicad_sch",
    board="kicad/K1_Lightwave.kicad_pcb"
)

# Result:
# {
#   "returncode": 0,
#   "ok": true,
#   "cwd": "hardware/k1-lightwave",
#   "output": "_artifacts/"
# }

# Typical kibot.yaml outputs:
# - Schematic PDF
# - PCB top/bottom layers (PDF)
# - Gerbers + drill
# - Pick-and-place
# - Assembly steps
# - 3D rendering
```

**When to use:** CI/CD automation; GitHub Actions

**Example kibot.yaml:**
```yaml
kibot:
  version: 1

outputs:
  - name: schematic
    comment: Schematic PDF
    type: pdf_sch
    dir: docs

  - name: gerbers
    comment: Gerbers for fabrication
    type: gerber
    dir: fab

  - name: drill
    comment: Drill files
    type: drill
    dir: fab

  - name: ibom
    comment: Interactive HTML BOM
    type: ibom
    dir: docs

  - name: bom_csv
    comment: Bill of materials (CSV)
    type: bom
    dir: docs
```

---

## Workflow Examples

### **Example 1: Full Design Validation**

```python
# 1. Check schematic
erc_result = sch_erc("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch", out="erc.json")
if erc_result["summary"]["errors"] > 0:
    print("❌ ERC failed; fix schematic")
else:
    print("✅ ERC passed")

# 2. Check PCB layout
drc_result = pcb_drc("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out="drc.json")
if drc_result["summary"]["violations"] > 0:
    print("❌ DRC failed; fix layout")
else:
    print("✅ DRC passed")

# 3. Export BOM and verify parts
bom_result = sch_export_bom("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch", out_csv="bom.csv")
print(f"✅ BOM exported: {bom_result['output']}")

# 4. Check component availability
esp32_search = parts_search("ESP32-S3-WROOM-1U", limit=1)
print(f"✅ ESP32-S3-WROOM-1U available from {esp32_search['data']['supSearch']['hits']['results'][0]['part']['manufacturer']['name']}")

# 5. Export manufacturing data
gerbers = pcb_export_gerbers("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_dir="fab/gerbers")
drill = pcb_export_drill("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_dir="fab/drill")
step = pcb_export_step("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_file="fab/K1_Lightwave.step")
print("✅ Manufacturing files exported")

# 6. Generate assembly pack
jlc_pack = kikit_fab_jlcpcb(
    "hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb",
    out_dir="fab/jlc",
    assembly=True,
    schematic="hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch",
    field="LCSC"
)
print(f"✅ JLC assembly pack ready: {jlc_pack['output_dir']}")
```

---

### **Example 2: Component Datasheet Lookup**

```python
# Get datasheets for all critical components
components = [
    ("ESP32-S3-WROOM-1U", "MCU"),
    ("SPH0645", "Microphone"),
    ("WS2812B", "LED"),
    ("SN74AHCT125", "Level shifter")
]

for mpn, desc in components:
    ds = best_datasheet_url(mpn)
    if ds["ok"] and ds["url"]:
        print(f"✅ {desc} ({mpn}): {ds['url']}")
    else:
        print(f"❌ {desc} ({mpn}): No datasheet found")
```

---

## MCP Server Configuration

All servers are in `/mcp/` with Python scripts:

| Server | Path | Command |
|--------|------|---------|
| KiCad CLI | `mcp/mcp-kicad-cli/server.py` | `python server.py` |
| SKiDL | `mcp/mcp-skidl/server.py` | `python server.py` |
| FreeRouting | `mcp/mcp-freerouting/server.py` | `python server.py` |
| Nexar | `mcp/mcp-nexar/server.py` | `python server.py` |
| iBOM | `mcp/mcp-ibom/server.py` | `python server.py` |
| KiKit | `mcp/mcp-kikit/server.py` | `python server.py` |
| KiBot | `mcp/mcp-kibot/server.py` | `python server.py` |
| LCSC | `mcp/mcp-lcsc/server.py` | `python server.py` |

**Setup:** Add to `claude_desktop_config.json` (absolute paths + env vars)

---

**Last updated:** Oct 23, 2025
**Status:** MCP servers ready for integration
