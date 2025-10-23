# K1 Lightwave Hardware Design — Claude Code Agent Guide

## READ THIS FIRST

This directory contains **critical context** for hardware PCB design using Claude Code + MCP servers. All design changes must follow the governance protocol before committing.

---

## The K1 Lightwave Hardware Project

**Dual-ESP32-S3 music visualizer** with real-time audio capture and addressable LED output.

- **MCU**: 2× ESP32-S3-WROOM-1/1U (I/O mapping in progress)
- **Audio input**: SPH0645 + IM69D130 digital MEMS microphones
- **LED output**: WS2812B/SK6812 addressable LEDs with SN74AHCT125 level shifter
- **Power**: 5V input, 3.3V logic rails, per-rail current limits TBD
- **PCB**: 4-layer, JLC/PCBWay vendor manufacturing rules

---

## The Problem We're Solving

Hardware design changes can fail catastrophically if not validated:
- **Power delivery issues** → MCU brown-out, LED dropout under full load
- **Signal integrity failures** → audio noise, I2S frame loss, BLE dropout
- **Manufacturing rejections** → DRC violations, unroutable areas, $$$$ delays
- **Thermal runaway** → LED driver overheating, logic failures
- **Assembly disasters** → panelization conflicts, missing test points, prototype dead on arrival

---

## How This System Works

### **Step 1: Understand Design Governance** (5 minutes)
Read: `GOVERNANCE.md` - Explains the hardware design change protocol

### **Step 2: Before Making ANY Design Change** (Depends on risk)
Follow the three-phase process in `GOVERNANCE.md`:
- **Phase 1:** Assess risk level (component changes, routing, power, thermal)
- **Phase 2:** Analyze dependencies (datasheets, thermal, manufacturing)
- **Phase 3:** Validate changes (ERC/DRC, BOM, vendor rules)

### **Step 3: Use MCP Tools to Validate** (5-10 minutes)
- `sch_erc()` — Verify schematic electrical rules
- `pcb_drc()` — Verify PCB design rules (JLC 4-layer)
- `parts_search()` — Verify component availability via Nexar
- `best_datasheet_url()` — Verify datasheets available

### **Step 4: Document and Commit** (5 minutes)
Document reasoning in commit message; reference GOVERNANCE.md phase checklist

---

## Files in This Directory

### `GOVERNANCE.md` (MANDATORY - Read First)
- Hardware design change protocol
- Risk level assessment (Level 1/2/3)
- Mandatory pre/post change checklists
- Decision tree for design changes
- Template for pre-change documentation
- Critical files requiring absolute respect

### `README.md` (You are here)
- Quick start guide for hardware design agents
- Project specs and component list
- MCP tool reference
- Escalation path for questions

---

## Quick Decision Tree

```
"I want to make a K1 Lightwave hardware design change"
    ↓
"What type of change?"
    ├─ Comments, docs, silkscreen → Proceed (Level 1)
    ├─ Component values, decoupling → Read GOVERNANCE.md Phase 2 (Level 2)
    └─ Pinouts, routing, power, thermal → Read GOVERNANCE.md Phase 2+3 (Level 3)
    ↓
"Have you completed GOVERNANCE.md Phases 2 & 3?"
    ├─ NO → STOP. Follow the protocol first
    └─ YES → Continue
    ↓
"Do ERC and DRC pass?"
    ├─ NO → STOP. Debug and revert
    └─ YES → Commit with documentation
```

---

## Critical Files That Require Absolute Care

| File | Why | Cost of Failure |
|------|-----|-----------------|
| `kicad/K1_Lightwave.kicad_sch` | Master schematic | Full re-spin required |
| `kicad/K1_Lightwave.kicad_pcb` | PCB layout + stackup | Manufacturability fail |
| `kicad/symbols/esp32-s3-wroom-1.kicad_sym` | MCU pinout (immutable) | PCB rework impossible |
| `kicad/design_rules.kicad_dru` | DRC/vendor rules | Fab rejection |

**Before modifying these:**
1. Read commit history
2. Check datasheets in `/docs/datasheets/`
3. Run ERC/DRC immediately after
4. Verify against JLC/PCBWay rules
5. Document reasoning in commit
6. Flag for review if unsure

---

## MCP Tools Available (Code-Driven)

All these are wired as Claude Code MCP servers:

- `sch_erc(schematic, out, format="json")` — Electrical rules check
- `pcb_drc(board, out, format="json")` — Design rules check (JLC 4-layer)
- `sch_export_bom(schematic, out_csv)` — Bill of materials
- `sch_export_netlist(schematic, out_net)` — Netlist for routing
- `pcb_export_gerbers(board, out_dir)` — Gerber files
- `pcb_export_drill(board, out_dir)` — Drill files
- `pcb_export_step(board, out_file)` — 3D STEP model
- `pcb_export_ipc2581(board, out_file)` — IPC-2581 (manufacturing data)
- `skidl_gen_netlist(script_path, out_net)` — Generate netlist from Python
- `route(dsn, ses_out)` — FreeRouting autorouter
- `parts_search(q, limit)` — Nexar component lookup
- `best_datasheet_url(mpn)` — Fetch datasheets
- `lcsc_search(keyword)` — LCSC part lookup (JLC assembly)
- `kikit_panelize_grid(...)` — Panelization preview
- `kibot_run(project_dir, config_yaml)` — CI fab packs
- `generate_ibom(board)` — Interactive assembly BOM (HTML)

See `docs/TOOLING.md` for usage examples.

---

## Project Structure

```
k1-lightwave/
├── .claude/                 ← You are here
│   ├── GOVERNANCE.md
│   ├── README.md
│   └── skills/
├── hardware/
│   └── k1-lightwave/
│       ├── kicad/           ← Schematics, PCB, symbols, footprints
│       ├── skidl/           ← Python schematic generation
│       └── README.md
├── docs/
│   ├── datasheets/          ← Component PDFs
│   ├── prd/                 ← Product requirements docs
│   └── TOOLING.md           ← MCP examples
├── .github/
│   └── workflows/           ← GitHub Actions CI (KiBot)
└── mcp/
    ├── mcp-kicad-cli/       ← ERC/DRC server
    ├── mcp-skidl/
    ├── mcp-freerouting/
    ├── mcp-nexar/
    ├── mcp-ibom/
    ├── mcp-kikit/
    ├── mcp-kibot/
    └── mcp-lcsc/
```

---

## Right Now

**If you're here to make design changes:**

1. ✅ Read `GOVERNANCE.md` — Understand the protocol
2. ✅ Assess risk level (Phases 1–3)
3. ✅ Use MCP tools to validate (ERC, DRC, BOM)
4. ✅ Document reasoning in commit
5. ✅ Never skip validation steps

**If you have questions:**
- Check `/docs/datasheets/` — Datasheet answers
- Run `sch_erc()` or `pcb_drc()` — Instant validation
- See `GOVERNANCE.md` escalation path — When in doubt, ask

---

## Component References

**Datasheets in `/docs/datasheets/`:**
- ESP32-S3 SoC and module datasheets
- SPH0645 digital MEMS microphone
- IM69D130 digital MEMS microphone
- WS2812B/SK6812 addressable LEDs
- SN74AHCT125 logic level shifter
- JLC/PCBWay 4-layer stackup and DRC rules

**Key Links:**
- [KiCad CLI Docs](https://docs.kicad.org/cli/)
- [ESP32-S3 Datasheet](https://www.espressif.com/)
- [Nexar API](https://docs.nexar.com/)
- [KiBot Docs](https://kibot.readthedocs.io/)
- [JLC PCB Rules](https://jlcpcb.com/)

---

## Remember

**This system exists because hardware failures are expensive.** Follow the protocol to prevent spinning bad PCBs.

**The goal:** Make hardware design confident, not terrifying.

---

**Next Steps:**
1. Read `GOVERNANCE.md`
2. Set up MCP servers (see DEPLOYMENT.md)
3. Download datasheets via Nexar
4. Start design work with validation gates

**Questions?** All answers are in `GOVERNANCE.md` and the datasheets.

**Last updated:** Oct 23, 2025
