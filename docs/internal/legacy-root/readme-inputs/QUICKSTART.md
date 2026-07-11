# K1 Lightwave: Quick Start Guide

**TL;DR:** 5-minute setup + ask an agent to design your board.

---

## 1. Prerequisites (5 min)

Install if you don't have:
- **KiCad 8 or 9** (https://kicad.org/download/)
- **Python 3.9+** (`python3 --version`)
- **Claude Code** (https://claude.com/claude-code)

Verify:
```bash
kicad-cli --version
python3 --version
```

---

## 2. Setup MCP Servers (10 min)

```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware

# Run the configuration script
python3 mcp/configure_claude.py

# When prompted for credentials:
#   - Leave blank if you don't have Nexar/LCSC credentials
#   - Or paste your credentials if you do
#   - (See SETUP_CREDENTIALS.md for details)
```

Expected output:
```
✅ Configuration complete!
   Next steps:
   1. Reload Claude Code
   2. Verify MCP servers are available
```

---

## 3. Reload Claude Code (2 min)

- Close all Claude Code windows
- Reopen Claude Code
- MCP servers should now be available

---

## 4. Verify Setup (Optional, 3 min)

```bash
python3 mcp/verify-servers.py
```

Or test in Claude Code directly:
> "Can you query the RAG system? Search for 'antenna design ESP32-S3'."

Expected: Returns relevant documentation chunks ✅

---

## 5. Start Designing (Now!)

### Option A: Let an Agent Lead

Ask in Claude Code:

> "I need a compact PCB for K1 Lightwave: dual ESP32-S3 MCUs, digital I2S microphone, WS2812B addressable LEDs with 3.3V→5V level shifter, 5V input power, 100×80mm form factor. Target JLCPCB standard class manufacturing. Design the board."

The **PCB Hardware Designer** agent will:
1. ✅ Extract design specification
2. ✅ Generate schematic (SKiDL + ERC)
3. ✅ Select components (parts search + BOM)
4. ✅ Commit to Git

Then ask:

> "Layout the PCB and route it."

The **PCB Layout Specialist** will:
1. ✅ Create board file (pcbnew API)
2. ✅ Place components (heuristic)
3. ✅ Route with FreeRouting
4. ✅ Commit routed design

Finally:

> "Validate the design and generate manufacturing files for JLCPCB."

The **Hardware Validation Specialist** will:
1. ✅ Run DRC + DFM checks
2. ✅ Generate Gerbers + IPC-2581 + STEP
3. ✅ Create fab package
4. ✅ Provide cost estimate

**Total time: 4-6 hours (first design).**

### Option B: Manual Step-by-Step

If you prefer to drive it yourself:

1. **Design Spec** → Read `.claude/K1_PCB_PIPELINE_ARCHITECTURE.md` → "Phase 1: Specification"
2. **Schematic** → Use kicad-schematic-synthesizer skill
3. **Parts** → Use kicad-part-picker skill
4. **Layout** → Use kicad-pcb-synthesizer skill
5. **Routing** → Use kicad-router-orchestrator skill
6. **Validation** → Use kicad-verification-drf skill
7. **Manufacturing** → Use kicad-publisher-fabpack skill

---

## 6. Next: Order PCBs

Once manufacturing files are generated:

1. Go to https://jlcpcb.com
2. Click "Add Gerber File"
3. Upload `fab/k1_lightwave_fab_package.zip`
4. JLC auto-detects specs + component assembly
5. Review BOM (pre-populated from design)
6. Select assembly options
7. Place order

**Lead time:** 2-4 weeks
**Cost:** ~$100/unit for small volumes

---

## 7. During PCB Manufacturing: Start Firmware

While PCBs are being made (2-4 week wait):

```bash
cd firmware/
# Follow firmware setup guide
```

Available skills:
- **ESP-IDF** — ESP32-S3 development framework
- **PlatformIO** — Firmware build system
- **FastLED** — LED control library
- **freertos-synchronization** — Real-time task coordination

---

## Files You'll Need

| File | Purpose |
|------|---------|
| `.claude/K1_PCB_PIPELINE_ARCHITECTURE.md` | Full design pipeline docs |
| `SETUP_CREDENTIALS.md` | Credential setup guide |
| `docs/prd/01-product-brief.md` | K1 product requirements |
| `docs/knowledge/` | Indexed design guidelines (RAG) |

---

## Troubleshooting

### "MCP servers not found"
- Did you run `configure_claude.py`? ✓
- Did you reload Claude Code after setup? ✓
- Check `~/.config/Claude/claude_desktop_config.json` exists

### "KiCad CLI not found"
- Install KiCad 8/9: https://kicad.org/download/
- Or provide full path when configure script asks

### "RAG system returns no results"
- Run: `python3 mcp/ingest_new_sources.py`
- Verify: `python3 mcp/test_rag.py`

### "Nexar/LCSC queries fail"
- Credentials may be wrong
- Re-run: `python3 mcp/configure_claude.py` with correct credentials
- Or skip credentials; manually search on websites

### "Can't find a skill"
- Make sure you're asking for the right action
- Skills auto-activate on **keywords**
- Example: Say "schematic" → kicad-schematic-synthesizer activates

---

## Quick Command Reference

```bash
# Setup
python3 mcp/configure_claude.py          # Initial setup
python3 mcp/verify-servers.py            # Check MCP servers

# Testing
python3 mcp/test_rag.py                  # Test RAG system
python3 mcp/ingest_new_sources.py        # Re-index documentation

# Check status
ls hardware/k1-lightwave/                # Design files
git log --oneline -10                    # Recent commits
```

---

## Example Workflow

```
Day 1 (Morning):
  1. Run configure_claude.py
  2. Reload Claude Code
  3. Test RAG system

Day 1 (Afternoon):
  1. Ask PCB Hardware Designer: "Design K1 spec, schematic, parts"
  2. Review generated files
  3. Commit to Git

Day 2 (Morning):
  1. Ask Layout Specialist: "Layout and route the PCB"
  2. Review routing results
  3. Commit to Git

Day 2 (Afternoon):
  1. Ask Validation Specialist: "Verify design and generate fab package"
  2. Download fab package
  3. Upload to JLCPCB.com

Day 3+:
  1. Order PCBs (2-4 week wait)
  2. Start firmware development in parallel
  3. When PCBs arrive: assemble + test
```

---

## What Happens Next

### Manufacturing (2-4 weeks)
- JLCPCB manufactures PCBs
- Parts are ordered
- SMD assembly + hand-soldering

### Assembly (1 week after PCBs arrive)
- Inspect + test for defects
- Flash firmware
- Verify I2S audio + LED output

### Integration & Tuning (2-4 weeks)
- Optimize audio DSP (FFT, beat detection)
- Fine-tune LED color mapping
- Wi-Fi + BLE testing
- Performance profiling

---

## You're Ready

The infrastructure is **locked in** and **fully functional**.

**Next action:** Ask the PCB Hardware Designer agent to start the design.

> "Design K1 Lightwave: dual ESP32-S3, I2S microphone, WS2812B LEDs, compact 100×80mm form factor, JLCPCB standard class."

**Go.**
