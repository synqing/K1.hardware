# K1 Lightwave MCP Setup & Configuration

## Complete Setup Guide

After the initial project scaffold was deployed, we've now added:

1. **9 MCP Servers** (all 10 including official servers)
2. **Configuration Helper Script** (auto-generates claude_desktop_config.json)
3. **Deployment & Troubleshooting Guides**
4. **Fabops Composite Tools** (one-command fab packs + vendor sync)

---

## What's New (Phase 2 Deployment)

### **New MCP Servers**

- ✅ **mcp-fabops** — Composite tools:
  - `make_fab_pack()` — One command: panelize → JLC fab pack → iBOM → STEP/GLB
  - `vendor_sync()` — Fill missing LCSC C-numbers from LCSC OpenAPI + Nexar

### **Configuration Tools**

- ✅ **mcp/configure_claude.py** — Auto-generates your claude_desktop_config.json
- ✅ **mcp/DEPLOYMENT.md** — Detailed setup guide for all OSes

### **New Capabilities**

| Tool | What It Does |
|------|-------------|
| **make_fab_pack** | 1) DRC check → 2) Panelize (4×8 grid, V-cuts) → 3) JLC fab pack → 4) iBOM HTML → 5) STEP/GLB 3D |
| **vendor_sync** | 1) Export BOM → 2) Search LCSC for missing C-numbers → 3) Write back to schematic → 4) (Optional) Run fab |
| **sch_erc / pcb_drc** | Electrical & design rules checks (validation gates) |
| **parts_search / best_datasheet_url** | Nexar component lookup + datasheets |
| **lcsc_search / lcsc_item_info** | LCSC C-number lookup (stock, price, datasheet) |
| **panelize_grid / fab_jlcpcb** | KiKit panelization + JLC-ready fab pack |
| **ibom_generate** | Interactive HTML BOM for assembly |
| **kicad_pcb_export_step / glb** | 3D exports (CAD + rendering) |

---

## Quick Start (3 Steps)

### **Step 1: Run Configuration Script**

```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp
python3 configure_claude.py
```

**What it does:**
- Auto-detects KiCad CLI path
- Finds Java (for FreeRouting)
- Prompts for optional Nexar + LCSC credentials
- Generates `~/.config/Claude/claude_desktop_config.json`
- Backs up existing config

**You'll be prompted for (all optional initially):**
```
Nexar Client ID:      [leave blank or paste your ID]
Nexar Client Secret:  [leave blank or paste your secret]
LCSC API Key:         [leave blank or paste your key]
LCSC API Secret:      [leave blank or paste your secret]
```

### **Step 2: Reload Claude Code**

Close and reopen Claude Code to load the new MCP servers.

### **Step 3: Verify & Get Datasheets**

Test a simple command in Claude:

```python
# This should work immediately
result = parts_search("ESP32-S3-WROOM-1U", limit=1)
print(f"✅ Nexar working: {result.get('data')}")
```

---

## File Locations

| File | Purpose |
|------|---------|
| **mcp/DEPLOYMENT.md** | Full setup guide (OS-specific paths, troubleshooting) |
| **mcp/configure_claude.py** | Auto-generates config (run this first) |
| **mcp/mcp-*/server.py** | 9 individual MCP servers (1 server = 1-3 tools) |
| **~/.config/Claude/claude_desktop_config.json** | Generated config (points to all servers) |

---

## MCP Servers Deployed

| Server | Provided Tools | Status |
|--------|----------------|--------|
| **Official: filesystem** | read_file, write_file, list_directory | ✅ (via npx) |
| **Official: git** | clone, commit, push, diff | ✅ (via npx) |
| **Official: fetch** | web fetch + HTML→markdown conversion | ✅ (via npx) |
| **mcp-kicad-cli** | sch_erc, pcb_drc, export bom/netlist/gerbers/step/glb/ipc-2581 | ✅ Created |
| **mcp-skidl** | skidl_gen_netlist (Python schematic synthesis) | ✅ Created |
| **mcp-freerouting** | route (DSN→SES batch autorouting) | ✅ Created |
| **mcp-nexar** | parts_search, part_by_mpn, best_datasheet_url | ✅ Created |
| **mcp-ibom** | generate (interactive HTML BOM) | ✅ Created |
| **mcp-kikit** | panelize_grid, fab_jlcpcb | ✅ Created |
| **mcp-kibot** | kibot_run (CI automation) | ✅ Created |
| **mcp-lcsc** | lcsc_search, lcsc_item_info | ✅ Created |
| **mcp-fabops** | make_fab_pack, vendor_sync (composites) | ✅ Created |

---

## Typical Workflows

### **Workflow 1: Full Fabrication Pack (One Command)**

```python
# When schematic & PCB are ready:
result = make_fab_pack(
    board_kicad_pcb="hardware/k1-lightwave/kicad/board.kicad_pcb",
    schematic_kicad_sch="hardware/k1-lightwave/kicad/project.kicad_sch",
    out_root="fab/out",
    rows=4, cols=8,  # 4×8 panel grid
    tabs="full",
    cuts="vcuts; clearance: 0.4mm",  # JLC-friendly
    gen_step=True, gen_glb=True, gen_ibom=True
)

# Returns paths to:
# - fab/out/jlc/gerbers.zip          ← Upload to JLC
# - fab/out/jlc/bom.csv              ← JLC assembly BOM
# - fab/out/jlc/pos.csv              ← Pick-and-place
# - docs/ibom/ibom.html              ← Assembly guide
# - fab/out/mechanical/board.step    ← CAD data
# - fab/out/mechanical/board.glb     ← 3D rendering
```

### **Workflow 2: Sync LCSC C-Numbers & Fab**

```python
# Fill missing C-numbers from LCSC, write back to schematic, then fab:
result = vendor_sync(
    schematic_kicad_sch="hardware/k1-lightwave/kicad/project.kicad_sch",
    board_kicad_pcb="hardware/k1-lightwave/kicad/board.kicad_pcb",
    lcsc_field="LCSC",
    apply_changes=True,  # Write C-numbers to schematic
    run_fab=True,        # Then run kikit fab jlcpcb
    jlc_out_dir="fab/jlc"
)

# Returns manifest JSON showing:
# - resolved: [{"ref": "R1", "mpn": "10k", "lcsc": "C25741"}, ...]
# - skipped: [{"ref": "U2", "reason": "No MPN found"}]
# - fab: KiKit fab pack results
```

### **Workflow 3: Component Research**

```python
# Find components + datasheets:
esp32_search = parts_search("ESP32-S3-WROOM-1U", limit=3)
# → MPN, manufacturer, best_datasheet URL

ds_url = best_datasheet_url("WS2812B")
# → Download via fetch()

lcsc_item = lcsc_search("C2653")
# → LCSC pricing, stock, datasheet
```

### **Workflow 4: Validation Gates**

```python
# Before committing any design changes:
erc = sch_erc("hardware/k1-lightwave/kicad/project.kicad_sch", out="erc.json")
assert erc["summary"]["errors"] == 0, "ERC failed"

drc = pcb_drc("hardware/k1-lightwave/kicad/board.kicad_pcb", out="drc.json")
assert drc["summary"]["violations"] == 0, "DRC failed"

bom = sch_export_bom("hardware/k1-lightwave/kicad/project.kicad_sch", out_csv="bom.csv")
# Check all parts are available on LCSC

print("✅ All gates passed")
```

---

## Credentials (Optional but Recommended)

### **Why Add Credentials?**

- **Nexar (Octopart):** Find component datasheets, alternates, stock
- **LCSC:** Resolve MPN → C-number for JLC assembly

### **Getting Credentials**

**Nexar:**
1. Go to [https://nexar.com/](https://nexar.com/)
2. Create developer account
3. Generate OAuth2 Client (scope: `supply.domain`)
4. Copy Client ID & Secret

**LCSC:**
1. Go to [https://www.lcsc.com/](https://www.lcsc.com/)
2. Sign in → Account Settings → API
3. Generate API Key & Secret

### **Adding Later**

If you skipped credentials during setup, you can:
1. Edit `~/.config/Claude/claude_desktop_config.json`
2. Update the `NEXAR_CLIENT_ID` / `LCSC_API_KEY` values
3. Save and reload Claude Code

---

## Troubleshooting

### **"kicad-cli: command not found"**

Verify KiCad is installed:
```bash
which kicad-cli
# or for full path:
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli --version
```

Update the `KICAD_CLI` env var in `configure_claude.py` or manually in the config.

### **"python: command not found" in MCP server**

Use full path to Python:
```bash
which python3
# Usually: /usr/bin/python3 or /opt/homebrew/bin/python3
```

Update the `command` field in claude_desktop_config.json to the full path.

### **Nexar / LCSC not responding**

Check credentials are set. If you see `"•••"` in the config, those are placeholders.

Get real credentials from [https://nexar.com/](https://nexar.com/) and [https://www.lcsc.com/](https://www.lcsc.com/).

### **MCP server won't start**

Check Claude's MCP logs:
- **macOS:** `~/Library/Logs/Claude/mcp.log`
- **Linux:** `~/.local/share/Claude/logs/mcp.log`

---

## What's Next?

1. ✅ **Run configure_claude.py** (auto-generates config)
2. ✅ **Reload Claude Code** (load new MCP servers)
3. ✅ **Verify servers work** (test parts_search or sch_erc)
4. 📝 **Begin schematic entry** (create K1_Lightwave.kicad_sch)
5. 🎯 **Use validation gates** (ERC/DRC per governance)
6. 🏭 **Generate fab pack** (make_fab_pack when layout is done)
7. 🚀 **Submit to JLC** (upload gerbers.zip + bom.csv)

---

## References

- **MCP Setup:** `/mcp/DEPLOYMENT.md`
- **Governance:** `/.claude/GOVERNANCE.md`
- **Hardware PRD:** `/docs/prd/02-hardware-prd.md`
- **Tooling Guide:** `/docs/TOOLING.md`
- **Hardware README:** `/hardware/k1-lightwave/README.md`

---

## Summary

✅ **9 MCP servers** deployed (all Python, documented CLIs/APIs)
✅ **Configuration script** (auto-generates config, handles all OSes)
✅ **Fabops composite tools** (one-command fab pack + vendor sync)
✅ **Governance protocol** (3-phase design validation)
✅ **Documentation complete** (PRDs, tooling, deployment guides)

**Ready to begin hardware design. Start with: `python3 /mcp/configure_claude.py`**

---

**Last updated:** Oct 23, 2025
**Status:** MCP setup complete; configuration ready
