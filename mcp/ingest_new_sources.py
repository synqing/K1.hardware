#!/usr/bin/env python3
"""
Ingest newly downloaded documentation sources into the RAG system.
This script adds the HTML pages and PDFs that were downloaded.
"""

import sys
from pathlib import Path

# Add mcp-rag to path for direct import
RAG_DIR = Path(__file__).parent / "mcp-rag"
sys.path.insert(0, str(RAG_DIR))

from server import rag_add

def main():
    print("=" * 70)
    print("K1 Lightwave: Ingesting New Documentation Sources")
    print("=" * 70)

    # Project root
    project_root = Path(__file__).parent.parent.resolve()
    knowledge_dir = project_root / "docs" / "knowledge"
    datasheets_dir = project_root / "docs" / "datasheets"

    # Step 1: Index new vendor HTML documentation
    print("\n" + "=" * 70)
    print("STEP 1: Indexing new vendor HTML documentation...")
    print("=" * 70)

    vendor_html_patterns = [
        str(knowledge_dir / "vendors" / "esp32s3_*.html"),
    ]

    for pattern in vendor_html_patterns:
        result = rag_add([pattern], tag="vendors")
        print(f"✓ Indexed {result['chunks']} chunks from {result['files']} files")
        if result['sample_ids']:
            print(f"  Sample IDs: {result['sample_ids'][:3]}")

    # Step 2: Index new tooling HTML documentation
    print("\n" + "=" * 70)
    print("STEP 2: Indexing new tooling HTML documentation...")
    print("=" * 70)

    tooling_html_patterns = [
        str(knowledge_dir / "tooling" / "interactive_html_bom.html"),
        str(knowledge_dir / "tooling" / "lcsc_api.html"),
        str(knowledge_dir / "tooling" / "kikit.html"),
    ]

    for pattern in tooling_html_patterns:
        result = rag_add([pattern], tag="tooling")
        print(f"✓ Indexed {result['chunks']} chunks from {result['files']} files")
        if result['sample_ids']:
            print(f"  Sample IDs: {result['sample_ids'][:3]}")

    # Step 3: Index local PDF datasheets
    print("\n" + "=" * 70)
    print("STEP 3: Indexing local PDF datasheets...")
    print("=" * 70)

    pdf_patterns = [
        str(datasheets_dir / "esp32-s3_datasheet_en.pdf"),
        str(datasheets_dir / "esp-hardware-design-guidelines-en-master-esp32s3.pdf"),
    ]

    for pattern in pdf_patterns:
        result = rag_add([pattern], tag="datasheets")
        print(f"✓ Indexed {result['chunks']} chunks from {result['files']} files")
        if result['sample_ids']:
            print(f"  Sample IDs: {result['sample_ids'][:3]}")

    # Summary
    print("\n" + "=" * 70)
    print("✅ New Sources Ingested Successfully")
    print("=" * 70)
    print("\nAll documentation sources have been indexed:")
    print("  • ESP32-S3 PCB Layout Design (HTML)")
    print("  • ESP32-S3 Schematic Checklist (HTML)")
    print("  • Interactive HTML BOM Wiki (HTML)")
    print("  • LCSC API Documentation (HTML)")
    print("  • KiKit Documentation (HTML)")
    print("  • ESP32-S3 Datasheet (PDF)")
    print("  • ESP32-S3 Hardware Design Guidelines (PDF)")

if __name__ == "__main__":
    main()
