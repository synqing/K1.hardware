# K1 Lightwave: Credentials Setup Guide

## Overview

The MCP pipeline requires API credentials for:
1. **Nexar** (Octopart) — Component search, datasheets, pricing
2. **LCSC** — JLC Assembly pricing, stock checks, component API

Both are **optional** for basic design. If not provided, you can:
- Manually search components on Octopart/LCSC
- Use cached/example data from RAG system

## Step 1: Get Nexar Credentials (Optional)

### Option A: Free Tier (Recommended)
1. Go to https://nexar.com/
2. Click "Sign Up" → Create account
3. Dashboard → API Credentials → Create App
4. Copy **Client ID** and **Client Secret**
5. Save these for Step 3 below

### Option B: Skip Nexar
- Leave credentials blank
- Manual component search via browser works fine
- RAG system has fallback component data

---

## Step 2: Get LCSC Credentials (Optional)

### Option A: LCSC API Key
1. Go to https://www.lcsc.com/
2. Account → API Settings
3. Generate API Key + Secret
4. Save for Step 3 below

### Option B: Skip LCSC
- Manually check LCSC pricing on website
- JLC cost estimates will use defaults
- Still works fine

---

## Step 3: Configure MCP Servers

### Automated Setup (Recommended)

Run the configuration script:

```bash
cd /Users/spectrasynq/Workspace_Management/Software/K1.hardware
python3 mcp/configure_claude.py
```

The script will:
1. ✅ Auto-detect KiCad CLI path
2. ✅ Auto-detect Java installation
3. ❓ Prompt for Nexar credentials (paste from Step 1)
4. ❓ Prompt for LCSC credentials (paste from Step 2)
5. ✅ Generate `~/.config/Claude/claude_desktop_config.json`
6. ✅ Backup existing config if it exists

**If you don't have credentials yet:** Just press Enter (skip) when prompted. You can add them later.

### Manual Setup (If Script Fails)

Edit `~/.config/Claude/claude_desktop_config.json` and add your credentials to the `mcpServers` section:

```json
"nexar": {
  "env": {
    "NEXAR_CLIENT_ID": "YOUR_ID_HERE",
    "NEXAR_CLIENT_SECRET": "YOUR_SECRET_HERE"
  }
},
"lcsc": {
  "env": {
    "LCSC_API_KEY": "YOUR_KEY_HERE",
    "LCSC_API_SECRET": "YOUR_SECRET_HERE"
  }
}
```

---

## Step 4: Verify Setup

After running the configuration script:

### Test MCP Servers

```bash
python3 mcp/verify-servers.py
```

Expected output:
```
✅ mcp-kicad-cli: READY
✅ mcp-nexar: READY (with credentials)
✅ mcp-lcsc: READY (with credentials)
✅ mcp-freerouting: READY
✅ mcp-rag: READY
(etc.)
```

### Reload Claude Code

1. Close all Claude Code windows
2. Reopen Claude Code
3. MCP servers should now be available to agents

---

## Step 5: Test RAG System

Once Claude Code is reloaded, test the RAG system:

```python
# In Claude Code terminal:
python3 mcp/test_rag.py
```

Expected output:
```
✅ RAG System Smoke Tests Complete
  - Query 1: antenna design → 3 results found
  - Query 2: panelization → 3 results found
  - Query 3: power delivery → 3 results found
```

---

## Step 6: Test Specialist Agents

### Test PCB Hardware Designer Agent

In Claude Code, ask:
> "I need to design a simple board: dual ESP32-S3, I2S microphone, 5V→3.3V power. Target JLCPCB. Design spec please."

Expected: Agent uses **kicad-spec-extractor** skill to generate `design-spec.yaml`

### Test Part Picker Agent

Ask:
> "Search for resistors and capacitors for the design-spec.yaml. Generate BOM."

Expected: Agent queries Nexar/LCSC and creates `k1_lightwave_bom.csv`

### Test RAG System

Ask:
> "What are the antenna design guidelines for ESP32-S3?"

Expected: RAG returns relevant snippets from indexed documentation

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **"kicad-cli not found"** | Install KiCad 8 or 9; or provide full path when prompted |
| **"ModuleNotFoundError: typing"** | Python 3.6+ should have typing built-in; check `python3 --version` |
| **MCP servers not appearing in Claude Code** | Reload Claude Code (File → Close All → Reopen); check `~/.config/Claude/claude_desktop_config.json` exists |
| **Nexar/LCSC queries fail** | Credentials may be wrong; re-run `configure_claude.py` with correct credentials |
| **RAG system empty** | Run `python3 mcp/ingest_new_sources.py` to index documentation |

---

## Environment Variables (Alternative)

Instead of interactive prompts, you can set environment variables:

```bash
export NEXAR_CLIENT_ID="your_id"
export NEXAR_CLIENT_SECRET="your_secret"
export LCSC_API_KEY="your_key"
export LCSC_API_SECRET="your_secret"

python3 mcp/configure_claude.py
```

The script will use env vars if available.

---

## What's Working Without Credentials

Even without API credentials, you can:

✅ Use RAG system (search 309 indexed documentation chunks)
✅ Run ERC/DRC checks (local KiCad CLI)
✅ Generate schematics (SKiDL)
✅ Route PCBs (FreeRouting)
✅ Export Gerbers (KiCad CLI)
✅ Manually search components (via browser)

What requires credentials:
❓ Automatic component pricing (Nexar/LCSC APIs)
❓ Real-time stock checks (LCSC API)
❓ Automated datasheet fetching (Nexar API)

---

## Next: Start Hardware Design

Once setup is complete, go to `.claude/K1_PCB_PIPELINE_ARCHITECTURE.md` and follow the "Workflow Example" section.

Or ask the PCB Hardware Designer agent directly:
> "Design K1 Lightwave: dual ESP32-S3, I2S audio, WS2812B LEDs, 100×80mm form factor, JLCPCB standard class."

**Ready to design.** 🚀
