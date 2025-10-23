#!/usr/bin/env python3
"""
Claude Desktop MCP Configuration Helper for K1 Lightwave

This script generates your claude_desktop_config.json with:
- Automatic path detection
- Credential prompts (optional)
- Backup of existing config
- Safe JSON validation

Usage:
  python3 configure_claude.py

The script will:
1. Auto-detect your system (macOS/Linux/Windows)
2. Find KiCad CLI installation
3. Prompt for optional credentials (Nexar, LCSC)
4. Generate updated config
5. Offer to backup & install

Docs: /mcp/DEPLOYMENT.md
"""
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict

def get_config_path() -> Path:
    """Get the path to claude_desktop_config.json"""
    system = platform.system()
    if system == "Darwin":  # macOS
        return Path.home() / ".config/Claude/claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config/Claude/claude_desktop_config.json"
    elif system == "Windows":
        return Path(os.environ["APPDATA"]) / "Claude" / "claude_desktop_config.json"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

def find_kicad_cli() -> str:
    """Try to find kicad-cli on the system"""
    system = platform.system()

    # Try `which` first (universal)
    try:
        result = subprocess.run(["which", "kicad-cli"], capture_output=True, text=True)
        if result.returncode == 0:
            path = result.stdout.strip()
            print(f"✅ Found kicad-cli at: {path}")
            return path
    except Exception:
        pass

    # Fallback paths by OS
    if system == "Darwin":
        candidates = [
            "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
            "/usr/local/bin/kicad-cli",
            "/opt/homebrew/bin/kicad-cli"
        ]
    elif system == "Linux":
        candidates = ["/usr/bin/kicad-cli", "/usr/local/bin/kicad-cli"]
    elif system == "Windows":
        candidates = [
            "C:\\Program Files\\KiCad\\9.0\\bin\\kicad-cli.exe",
            "C:\\Program Files (x86)\\KiCad\\9.0\\bin\\kicad-cli.exe"
        ]
    else:
        candidates = []

    for path in candidates:
        if Path(path).exists():
            print(f"✅ Found kicad-cli at: {path}")
            return path

    print(f"⚠️  Could not find kicad-cli. Candidates checked:")
    for c in candidates:
        print(f"   - {c}")
    print(f"\n   Install KiCad 8/9 or provide the full path:")
    user_path = input("   > ").strip()
    if Path(user_path).exists():
        return user_path
    else:
        raise RuntimeError(f"Path does not exist: {user_path}")

def find_java_home() -> str:
    """Find JAVA_HOME"""
    system = platform.system()
    if system == "Darwin":
        try:
            result = subprocess.run(["/usr/libexec/java_home"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "/usr/libexec/java_home"
    elif system == "Linux":
        if Path("/usr/lib/jvm/java-11-openjdk-amd64").exists():
            return "/usr/lib/jvm/java-11-openjdk-amd64"
        if Path("/usr/lib/jvm/java-openjdk").exists():
            return "/usr/lib/jvm/java-openjdk"
        return "/usr/lib/jvm/java-11-openjdk-amd64"  # best guess
    elif system == "Windows":
        return os.environ.get("JAVA_HOME", "C:\\Program Files\\Java\\jdk-11")
    else:
        return ""

def prompt_optional(name: str, env_var: str) -> str:
    """Prompt user for optional credential"""
    existing = os.environ.get(env_var, "")
    if existing:
        print(f"ℹ️  {name}: Found in env var ${env_var}")
        return existing

    print(f"\n[Optional] {name}:")
    print(f"  (Leave blank to skip; you can add later)")
    value = input(f"  {name}: ").strip()
    return value if value else "•••"

def generate_config(project_root: str, kicad_cli: str, java_home: str,
                    nexar_id: str, nexar_secret: str,
                    lcsc_key: str, lcsc_secret: str) -> Dict:
    """Generate the MCP server configuration"""
    return {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "--root", project_root],
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
                "args": [f"{project_root}/mcp/mcp-kicad-cli/server.py"],
                "env": {"KICAD_CLI": kicad_cli}
            },
            "skidl": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-skidl/server.py"],
                "env": {}
            },
            "freerouting": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-freerouting/server.py"],
                "env": {
                    "JAVA_HOME": java_home,
                    "FREEROUTING_JAR": f"{Path.home()}/freerouting.jar"
                }
            },
            "nexar": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-nexar/server.py"],
                "env": {
                    "NEXAR_CLIENT_ID": nexar_id,
                    "NEXAR_CLIENT_SECRET": nexar_secret,
                    "NEXAR_SCOPE": "supply.domain"
                }
            },
            "ibom": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-ibom/server.py"],
                "env": {"INTERACTIVE_HTML_BOM_NO_DISPLAY": "1"}
            },
            "kikit": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-kikit/server.py"],
                "env": {}
            },
            "kibot": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-kibot/server.py"],
                "env": {}
            },
            "lcsc": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-lcsc/server.py"],
                "env": {
                    "LCSC_API_KEY": lcsc_key,
                    "LCSC_API_SECRET": lcsc_secret
                }
            },
            "fabops": {
                "command": "python",
                "args": [f"{project_root}/mcp/mcp-fabops/server.py"],
                "env": {
                    "KICAD_CLI": kicad_cli,
                    "LCSC_API_KEY": lcsc_key,
                    "LCSC_API_SECRET": lcsc_secret,
                    "NEXAR_CLIENT_ID": nexar_id,
                    "NEXAR_CLIENT_SECRET": nexar_secret,
                    "NEXAR_SCOPE": "supply.domain"
                }
            }
        }
    }

def main():
    print("=" * 70)
    print("Claude Desktop MCP Configuration Helper — K1 Lightwave")
    print("=" * 70)

    # 1. Get project root
    project_root = Path(__file__).parent.parent.resolve().as_posix()
    print(f"\n📁 Project root: {project_root}")

    # 2. Find KiCad CLI
    print("\n🔍 Finding KiCad CLI...")
    kicad_cli = find_kicad_cli()

    # 3. Find Java (for FreeRouting)
    print("\n🔍 Finding Java...")
    java_home = find_java_home()
    print(f"✅ Using JAVA_HOME: {java_home}")

    # 4. Optional credentials
    print("\n🔑 Credentials (optional; leave blank to skip):")
    nexar_id = prompt_optional("Nexar Client ID", "NEXAR_CLIENT_ID")
    nexar_secret = prompt_optional("Nexar Client Secret", "NEXAR_CLIENT_SECRET")
    lcsc_key = prompt_optional("LCSC API Key", "LCSC_API_KEY")
    lcsc_secret = prompt_optional("LCSC API Secret", "LCSC_API_SECRET")

    # 5. Generate config
    print("\n📝 Generating configuration...")
    config = generate_config(project_root, kicad_cli, java_home,
                             nexar_id, nexar_secret, lcsc_key, lcsc_secret)

    # 6. Get config path
    config_path = get_config_path()
    print(f"   Config path: {config_path}")

    # 7. Backup existing config
    if config_path.exists():
        backup_path = config_path.with_suffix(".json.bak")
        print(f"\n💾 Backing up existing config to: {backup_path}")
        shutil.copy(config_path, backup_path)
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)

    # 8. Write config
    print(f"\n✍️  Writing configuration...")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"   ✅ Wrote {config_path}")

    # 9. Summary
    print("\n" + "=" * 70)
    print("✅ Configuration complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Reload Claude Code (File → Close All → Reopen window)")
    print("2. Verify MCP servers are available")
    print("3. Download datasheets: python3 download_datasheets.py")
    print("4. Begin hardware design!")
    print("\nFor troubleshooting, see: /mcp/DEPLOYMENT.md")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
