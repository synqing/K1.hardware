#!/usr/bin/env python3
"""
Verify MCP Server Functionality

Tests all MCP servers to ensure they're working correctly.
Run this after configure_claude.py to validate setup.
"""

import sys
import subprocess
from pathlib import Path

def test_kicad_cli():
    """Test KiCad CLI availability"""
    try:
        result = subprocess.run(["kicad-cli", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ kicad-cli: {result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"❌ kicad-cli: {e}")
        return False

def test_python_imports():
    """Test required Python libraries"""
    libraries = [
        "skidl",
        "pcbnew",
        "rank_bm25",
        "bs4",
        "pypdf",
        "requests",
        "pyyaml"
    ]

    all_ok = True
    for lib in libraries:
        try:
            __import__(lib)
            print(f"✅ {lib}: installed")
        except ImportError:
            print(f"⚠️  {lib}: NOT INSTALLED (run: pip install {lib})")
            all_ok = False

    return all_ok

def test_rag_system():
    """Test RAG system"""
    try:
        # Add mcp-rag to path
        rag_dir = Path(__file__).parent / "mcp-rag"
        sys.path.insert(0, str(rag_dir))

        from server import rag_query, _load_all_chunks

        chunks = _load_all_chunks()
        if len(chunks) > 0:
            print(f"✅ RAG system: {len(chunks)} chunks indexed")

            # Try a sample query
            result = rag_query("antenna design", top_k=3)
            if result['count'] > 0:
                print(f"   └─ Sample query returned {result['count']} results")
                return True
        else:
            print(f"⚠️  RAG system: No chunks indexed (run: python3 ingest_new_sources.py)")
            return True  # Not a hard failure
    except Exception as e:
        print(f"⚠️  RAG system: {e}")
        return False

def test_freerouting():
    """Test FreeRouting availability"""
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=5)
        if "java version" in result.stderr or "openjdk" in result.stderr:
            print(f"✅ Java: available for FreeRouting")
            return True
    except Exception as e:
        print(f"⚠️  Java: NOT FOUND (FreeRouting requires Java)")
        return False

def test_nodejs():
    """Test Node.js for MCP filesystem server"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"⚠️  Node.js: NOT FOUND (required for MCP filesystem server)")
        return False

def test_config_exists():
    """Test Claude Desktop config exists"""
    from pathlib import Path
    import platform

    system = platform.system()
    if system == "Darwin":  # macOS
        config_path = Path.home() / ".config/Claude/claude_desktop_config.json"
    elif system == "Linux":
        config_path = Path.home() / ".config/Claude/claude_desktop_config.json"
    elif system == "Windows":
        config_path = Path(os.environ["APPDATA"]) / "Claude" / "claude_desktop_config.json"
    else:
        config_path = None

    if config_path and config_path.exists():
        print(f"✅ Claude config: {config_path}")
        return True
    else:
        print(f"❌ Claude config: NOT FOUND at {config_path}")
        print(f"   Run: python3 configure_claude.py")
        return False

def main():
    print("=" * 70)
    print("K1 Lightwave MCP Server Verification")
    print("=" * 70)

    results = {}

    print("\n🔍 Checking dependencies...")
    print("-" * 70)

    results["kicad-cli"] = test_kicad_cli()
    results["python-libs"] = test_python_imports()
    results["java"] = test_freerouting()
    results["nodejs"] = test_nodejs()
    results["config"] = test_config_exists()

    print("\n🔍 Testing MCP servers...")
    print("-" * 70)

    results["rag"] = test_rag_system()

    # Summary
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\n✅ Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All systems ready! You can start hardware design.")
        print("\nNext steps:")
        print("1. Ask PCB Hardware Designer agent:")
        print("   'Design K1 Lightwave: dual ESP32-S3, I2S audio, WS2812B LEDs'")
        print("\n2. See QUICKSTART.md for workflow example")
        return 0
    else:
        print(f"\n⚠️  {total - passed} system(s) need attention. See above for details.")
        print("\nCommon fixes:")
        print("- Missing kicad-cli: Install KiCad 8/9 from kicad.org")
        print("- Missing Python libs: pip install skidl pcbnew rank-bm25 beautifulsoup4 pypdf requests pyyaml")
        print("- Missing Java: Install OpenJDK 11+ (for FreeRouting)")
        print("- Missing Node.js: Install from nodejs.org (for MCP filesystem)")
        print("- Missing Claude config: Run python3 configure_claude.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
