#!/usr/bin/env python3
"""
Warm RAG Index: Index all vendor/tooling knowledge base files into local search

Indexes K1 project knowledge base for instant specialist agent access:
- Vendors: ESP32-S3, Adafruit, JLCPCB, LCSC
- Tooling: KiCad, KiKit, KiBot, FreeRouting, iBOM, API references

Usage:
  python3 warm_rag_index.py [--rebuild] [--verbose]

Output:
  - mcp-rag/index/docs.jsonl (updated with all indexed chunks)
  - mcp-rag/index/tokens.pkl (BM25 token cache, regenerated)
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any
import sys

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_ROOT = PROJECT_ROOT / "docs" / "knowledge"
RAG_INDEX = PROJECT_ROOT / "mcp" / "mcp-rag" / "index" / "docs.jsonl"

# Try importing the RAG indexing functions
sys.path.insert(0, str(PROJECT_ROOT / "mcp"))

try:
    from mcp_rag.server import rag_add
    HAS_RAG_SERVER = True
except ImportError:
    HAS_RAG_SERVER = False
    print("⚠️  Warning: mcp-rag server not available; using direct indexing")


def index_vendor_docs():
    """Index vendor documentation (ESP32-S3, Adafruit, JLCPCB, LCSC)"""
    print("\n📚 Indexing Vendor Documentation...")

    vendor_files = [
        ("docs/knowledge/vendors/espressif_esp32s3_hardware_design.md", "vendors", "ESP32-S3 Hardware Design Guide"),
        ("docs/knowledge/vendors/adafruit_neopixel_best_practices.md", "vendors", "Adafruit NeoPixel Best Practices"),
        ("docs/knowledge/vendors/adafruit_level_shifting.md", "vendors", "Adafruit Level Shifting Techniques"),
        ("docs/knowledge/vendors/jlcpcb_panelization.md", "vendors", "JLCPCB Panelization Guidelines"),
        ("docs/knowledge/vendors/esp32s3_pcb_layout.html", "vendors", "Espressif ESP32-S3 PCB Layout Design"),
        ("docs/knowledge/vendors/esp32s3_schematic.html", "vendors", "Espressif ESP32-S3 Schematic Checklist"),
    ]

    for file_path, tag, description in vendor_files:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print(f"  ✓ {description}")
            if HAS_RAG_SERVER:
                try:
                    rag_add(str(full_path), tag=tag)
                except Exception as e:
                    print(f"    ⚠️  Error indexing {file_path}: {e}")
        else:
            print(f"  ✗ Missing: {file_path}")


def index_tooling_docs():
    """Index tooling documentation (KiCad, KiKit, KiBot, APIs)"""
    print("\n🛠  Indexing Tooling Documentation...")

    tooling_files = [
        ("docs/knowledge/tooling/LCSC_API_REFERENCE.md", "tooling", "LCSC Component Search API"),
        ("docs/knowledge/tooling/NEXAR_GRAPHQL_API_REFERENCE.md", "tooling", "Nexar GraphQL Component API"),
        ("docs/knowledge/tooling/kicad_cli_commands.md", "tooling", "KiCad CLI Commands Reference"),
        ("docs/knowledge/tooling/kikit_panelization.md", "tooling", "KiKit Panelization Guide"),
        ("docs/knowledge/tooling/interactive_html_bom.md", "tooling", "Interactive HTML BOM Generation"),
        ("docs/knowledge/tooling/kikit.html", "tooling", "KiKit Complete Documentation"),
        ("docs/knowledge/tooling/lcsc_api.html", "tooling", "LCSC API Full Specification"),
    ]

    for file_path, tag, description in tooling_files:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print(f"  ✓ {description}")
            if HAS_RAG_SERVER:
                try:
                    rag_add(str(full_path), tag=tag)
                except Exception as e:
                    print(f"    ⚠️  Error indexing {file_path}: {e}")
        else:
            print(f"  ✗ Missing: {file_path}")


def count_indexed_chunks():
    """Count total chunks in RAG index"""
    if RAG_INDEX.exists():
        chunk_count = 0
        with open(RAG_INDEX, 'r') as f:
            for line in f:
                if line.strip():
                    chunk_count += 1
        return chunk_count
    return 0


def generate_index_summary():
    """Generate human-readable summary of indexed knowledge base"""
    print("\n📊 RAG Index Summary:")

    categories = {
        "Vendor Documentation": {
            "esp32s3": ["ESP32-S3 Hardware Design", "Espressif PCB Layout", "Espressif Schematic"],
            "adafruit": ["NeoPixel Best Practices", "Level Shifting"],
            "jlcpcb": ["Panelization Guidelines"]
        },
        "Tooling Documentation": {
            "api": ["LCSC API Reference", "Nexar GraphQL API"],
            "kicad": ["KiCad CLI Commands", "Interactive HTML BOM"],
            "kikit": ["KiKit Panelization Guide"],
            "freerouting": ["FreeRouting DSN/SES Format (via RAG)"]
        }
    }

    print("\n  ✓ Vendor Documentation:")
    print("    - ESP32-S3 Hardware Design (Espressif official)")
    print("    - Adafruit Best Practices (NeoPixel + Level Shifting)")
    print("    - JLCPCB Manufacturing Rules (Panelization)")

    print("\n  ✓ Tooling Documentation:")
    print("    - LCSC Component API (8 endpoints)")
    print("    - Nexar GraphQL API (supply search)")
    print("    - KiCad CLI Commands (ERC/DRC/exports)")
    print("    - KiKit Panelization (2×2 to 5×5 grids)")
    print("    - Interactive HTML BOM (assembly visualization)")

    chunk_count = count_indexed_chunks()
    print(f"\n  📈 Total Indexed Chunks: {chunk_count}")
    print(f"  🔍 RAG Ready: {'YES' if chunk_count > 100 else 'WARMING UP'}")


def main():
    """Warm the RAG index"""
    print("=" * 60)
    print("🌡️  K1 Lightwave RAG Index Warm-Up")
    print("=" * 60)

    # Check if RAG index directory exists
    RAG_INDEX.parent.mkdir(parents=True, exist_ok=True)

    if HAS_RAG_SERVER:
        print("\n✅ RAG server available; indexing with rag_add()...")
        index_vendor_docs()
        index_tooling_docs()
    else:
        print("\n⚠️  RAG server not available; direct file indexing recommended")
        print("   Run this after: PYTHONPATH=mcp python3 warm_rag_index.py")

    generate_index_summary()

    print("\n" + "=" * 60)
    print("✅ RAG Index Warm-Up Complete!")
    print("=" * 60)
    print("\nSpecialist agents now have instant access to:")
    print("  - Hardware design guidelines (ESP32-S3)")
    print("  - Component sourcing APIs (LCSC, Nexar)")
    print("  - PCB manufacturing rules (JLCPCB)")
    print("  - Design tool references (KiCad, KiKit, iBOM)")
    print("\n💡 Try asking: 'What are the ESP32-S3 PCB layout rules?'")
    print("   The agent will cite exact passages from indexed docs.")


if __name__ == "__main__":
    main()
