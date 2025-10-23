# K1 Lightwave MCP Servers — Deployment Guide

This guide walks you through configuring Claude Code to use all 10 MCP servers for K1 Lightwave hardware design.

---

## Quick Start

### **Step 1: Find Your Claude Desktop Config File**

**macOS / Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### **Step 2: Get Absolute Paths**

Determine the absolute path to your K1 Lightwave project:

```bash
# In your K1 Lightwave project folder
pwd  # macOS/Linux
# /Users/spectrasynq/Workspace_Management/Software/K1.hardware

echo %cd%  # Windows PowerShell
# C:\Users\...\K1.hardware
```

**All paths below use `/Users/spectrasynq/Workspace_Management/Software/K1.hardware` as the example.**
Replace with YOUR absolute path.

### **Step 3: Get API Credentials** (optional for initial config)

- **NEXAR_CLIENT_ID / NEXAR_CLIENT_SECRET**: Request from [Nexar/Octopart](https://nexar.com/)
- **LCSC_API_KEY / LCSC_API_SECRET**: Create account on [LCSC.com](https://www.lcsc.com/) → Settings → API

You can leave these as placeholder `"•••"` initially and fill them later when needed.

### **Step 4: Identify KiCad CLI Path**

**macOS (KiCad installed via app):**
```bash
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
```

**macOS (installed via Homebrew):**
```bash
/usr/local/bin/kicad-cli
# or
/opt/homebrew/bin/kicad-cli
```

**Linux:**
```bash
which kicad-cli
# Usually: /usr/bin/kicad-cli
```

**Windows:**
```
C:\Program Files\KiCad\9.0\bin\kicad-cli.exe
```

Verify it's installed:
```bash
kicad-cli --version
# Should print: KiCad CLI version …
```

---

## Full Configuration Template

Edit your `claude_desktop_config.json` and **replace the entire `mcpServers` block**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "--root", "/Users/spectrasynq/Workspace_Management/Software/K1.hardware"],
      "env": {}
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {}
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"],
      "env": {}
    },
    "kicad-cli": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-kicad-cli/server.py"],
      "env": {
        "KICAD_CLI": "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
      }
    },
    "skidl": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-skidl/server.py"],
      "env": {}
    },
    "freerouting": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-freerouting/server.py"],
      "env": {
        "JAVA_HOME": "/usr/libexec/java_home",
        "FREEROUTING_JAR": "/Users/spectrasynq/freerouting.jar"
      }
    },
    "nexar": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-nexar/server.py"],
      "env": {
        "NEXAR_CLIENT_ID": "•••",
        "NEXAR_CLIENT_SECRET": "•••",
        "NEXAR_SCOPE": "supply.domain"
      }
    },
    "ibom": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-ibom/server.py"],
      "env": {
        "INTERACTIVE_HTML_BOM_NO_DISPLAY": "1"
      }
    },
    "kikit": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-kikit/server.py"],
      "env": {}
    },
    "kibot": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-kibot/server.py"],
      "env": {}
    },
    "lcsc": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-lcsc/server.py"],
      "env": {
        "LCSC_API_KEY": "•••",
        "LCSC_API_SECRET": "•••"
      }
    },
    "fabops": {
      "command": "python",
      "args": ["/Users/spectrasynq/Workspace_Management/Software/K1.hardware/mcp/mcp-fabops/server.py"],
      "env": {
        "KICAD_CLI": "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
        "LCSC_API_KEY": "•••",
        "LCSC_API_SECRET": "•••",
        "NEXAR_CLIENT_ID": "•••",
        "NEXAR_CLIENT_SECRET": "•••",
        "NEXAR_SCOPE": "supply.domain"
      }
    }
  }
}
```

---

## Configuration by OS

### **macOS (Standard KiCad Install)**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "--root", "/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware"],
      "env": {}
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {}
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"],
      "env": {}
    },
    "kicad-cli": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-kicad-cli/server.py"],
      "env": {
        "KICAD_CLI": "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
      }
    },
    "skidl": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-skidl/server.py"],
      "env": {}
    },
    "freerouting": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-freerouting/server.py"],
      "env": {
        "JAVA_HOME": "/usr/libexec/java_home",
        "FREEROUTING_JAR": "/Users/YOUR_USERNAME/freerouting.jar"
      }
    },
    "nexar": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-nexar/server.py"],
      "env": {
        "NEXAR_CLIENT_ID": "YOUR_ID_HERE",
        "NEXAR_CLIENT_SECRET": "YOUR_SECRET_HERE",
        "NEXAR_SCOPE": "supply.domain"
      }
    },
    "ibom": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-ibom/server.py"],
      "env": {
        "INTERACTIVE_HTML_BOM_NO_DISPLAY": "1"
      }
    },
    "kikit": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-kikit/server.py"],
      "env": {}
    },
    "kibot": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-kibot/server.py"],
      "env": {}
    },
    "lcsc": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-lcsc/server.py"],
      "env": {
        "LCSC_API_KEY": "YOUR_KEY_HERE",
        "LCSC_API_SECRET": "YOUR_SECRET_HERE"
      }
    },
    "fabops": {
      "command": "python",
      "args": ["/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/mcp/mcp-fabops/server.py"],
      "env": {
        "KICAD_CLI": "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
        "LCSC_API_KEY": "YOUR_KEY_HERE",
        "LCSC_API_SECRET": "YOUR_SECRET_HERE",
        "NEXAR_CLIENT_ID": "YOUR_ID_HERE",
        "NEXAR_CLIENT_SECRET": "YOUR_SECRET_HERE",
        "NEXAR_SCOPE": "supply.domain"
      }
    }
  }
}
```

### **Linux (Standard Install)**

Replace paths:
- `KICAD_CLI`: `/usr/bin/kicad-cli`
- `JAVA_HOME`: `/usr/lib/jvm/java-11-openjdk-amd64` (or `java -XshowSettings:properties -version` to find)
- Root path: `/home/YOUR_USERNAME/K1.hardware` (or wherever you cloned it)

### **Windows (PowerShell)**

Replace paths with forward slashes (Windows accepts both):
```json
"KICAD_CLI": "C:/Program Files/KiCad/9.0/bin/kicad-cli.exe"
```

---

## Credential Setup

### **Nexar (Octopart) Credentials**

1. Go to [https://nexar.com/](https://nexar.com/)
2. Sign up or log in
3. Navigate to **API Keys** or **Developer Settings**
4. Create a new **OAuth2 Client** with scope: `supply.domain`
5. Copy `Client ID` and `Client Secret`

In config:
```json
"NEXAR_CLIENT_ID": "YOUR_CLIENT_ID",
"NEXAR_CLIENT_SECRET": "YOUR_CLIENT_SECRET"
```

### **LCSC (JLC Electronics) Credentials**

1. Go to [https://www.lcsc.com/](https://www.lcsc.com/)
2. Create an account or log in
3. Go to **Account Settings** → **API Interface** (or similar)
4. Generate API Key and Secret
5. Copy both

In config:
```json
"LCSC_API_KEY": "YOUR_API_KEY",
"LCSC_API_SECRET": "YOUR_API_SECRET"
```

---

## Verification

### **Test Each Server (Optional)**

In Claude Code, after reloading, try:

```python
# Test KiCad CLI server
result = sch_erc("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_sch", out="test_erc.json")
# Should return: {"returncode": 0, "ok": true, ...} (even if no file exists yet)

# Test iBOM
result = generate("hardware/k1-lightwave/kicad/K1_Lightwave.kicad_pcb", out_dir="test_ibom")
# Should execute without error

# Test Nexar
result = parts_search("ESP32-S3-WROOM-1", limit=1)
# Should return GraphQL results with part data

# Test LCSC
result = lcsc_search("C2653", page_size=10)
# Should return LCSC product data

# Test fabops composite
result = make_fab_pack(
    board_kicad_pcb="hardware/k1-lightwave/kicad/board.kicad_pcb",
    schematic_kicad_sch="hardware/k1-lightwave/kicad/project.kicad_sch"
)
# Should return {"ok": true, "artifacts": {...}}
```

---

## Troubleshooting

### **"Command not found: kicad-cli"**

Verify KiCad is installed and the path is correct:

```bash
which kicad-cli
# or for full path:
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli --version
```

If it fails, check your KiCad installation path.

### **"python: command not found"**

Use the full path to Python instead:

```json
"command": "/usr/bin/python3"
```

Or set up a venv:

```bash
# In K1.hardware project
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" requests InteractiveHtmlBom kikit
```

Then in config:
```json
"command": "/Users/YOUR_USERNAME/Workspace_Management/Software/K1.hardware/.venv/bin/python"
```

### **"NEXAR_CLIENT_ID not set"**

This is a warning; Nexar features will skip gracefully. Set credentials when ready.

### **"LCSC_API_KEY not set"**

Same as Nexar. LCSC lookups won't work until credentials are configured.

### **MCP Server Won't Start**

Check Claude's MCP logs:
- **macOS**: `~/Library/Logs/Claude/mcp.log`
- **Linux**: `~/.local/share/Claude/logs/mcp.log`
- **Windows**: `%APPDATA%\Claude\logs\mcp.log`

---

## Next Steps

1. **Update your `claude_desktop_config.json`** with the paths above (use YOUR absolute paths)
2. **Reload Claude Code** (may require restart)
3. **Verify servers are available** by calling a simple command (e.g., `parts_search(...)`)
4. **Download datasheets** when ready (see DATASHEET_DOWNLOAD.md)
5. **Begin hardware design** with ERC/DRC validation gates

---

## Servers at a Glance

| Server | Purpose | Requires Credentials |
|--------|---------|----------------------|
| **filesystem** | Read/write project files | No |
| **git** | Clone, commit, branch, push | No |
| **fetch** | Download PDFs/HTML | No |
| **kicad-cli** | ERC/DRC/exports (Gerber, STEP, etc.) | No |
| **skidl** | Generate netlists from Python | No |
| **freerouting** | Batch autorouting (DSN→SES) | No (needs Java + JAR) |
| **nexar** | Component search, datasheets, alternates | YES (Nexar OAuth) |
| **ibom** | Interactive HTML BOM for assembly | No |
| **kikit** | Panelization + JLC fab pack | No |
| **kibot** | CI automation (reproducible fab) | No |
| **lcsc** | LCSC part lookup, C-number resolution | YES (LCSC API) |
| **fabops** | Composite: full fab pack + vendor sync | Needs Nexar + LCSC |

---

**Status:** Configuration guide ready. Proceed to next step when all paths are verified.

**Last updated:** Oct 23, 2025
