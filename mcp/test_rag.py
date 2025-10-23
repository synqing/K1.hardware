#!/usr/bin/env python3
"""
Test script for mcp-rag server indexing and retrieval.
This tests the RAG system with smoke tests to verify functionality.
"""

import subprocess
import json
import sys
from pathlib import Path

# Add mcp-rag to path for direct import
RAG_DIR = Path(__file__).parent / "mcp-rag"
sys.path.insert(0, str(RAG_DIR))

from server import rag_add, rag_query, rag_explain

def main():
    print("=" * 70)
    print("K1 Lightwave RAG System Smoke Tests")
    print("=" * 70)

    # Project root
    project_root = Path(__file__).parent.parent.resolve()
    knowledge_dir = project_root / "docs" / "knowledge"

    print(f"\nKnowledge base directory: {knowledge_dir}")
    print(f"Vendor docs: {list((knowledge_dir / 'vendors').glob('*.md'))}")
    print(f"Tooling docs: {list((knowledge_dir / 'tooling').glob('*.md'))}")

    # Step 1: Index vendor documentation
    print("\n" + "=" * 70)
    print("STEP 1: Indexing vendor documentation...")
    print("=" * 70)

    vendor_pattern = str(knowledge_dir / "vendors" / "*.md")
    result = rag_add([vendor_pattern], tag="vendors")
    print(f"✓ Indexed {result['chunks']} vendor chunks from {result['files']} files")
    print(f"  Sample IDs: {result['sample_ids'][:3]}")

    # Step 2: Index tooling documentation
    print("\n" + "=" * 70)
    print("STEP 2: Indexing tooling documentation...")
    print("=" * 70)

    tooling_pattern = str(knowledge_dir / "tooling" / "*.md")
    result = rag_add([tooling_pattern], tag="tooling")
    print(f"✓ Indexed {result['chunks']} tooling chunks from {result['files']} files")
    print(f"  Sample IDs: {result['sample_ids'][:3]}")

    # Step 3: Query vendor documentation
    print("\n" + "=" * 70)
    print("STEP 3: Query 1 - Antenna & stackup guidance")
    print("=" * 70)

    query1 = "For ESP32-S3 module antenna, what is the keep-out guidance and preferred PCB layer count?"
    result = rag_query(query1, top_k=3, tag="vendors")
    print(f"Query: {query1}")
    print(f"Results found: {result['count']}")
    for i, res in enumerate(result['results'], 1):
        print(f"\n  [{i}] Score: {res['score']:.3f}")
        print(f"      Source: {res['source']}")
        print(f"      Pages: {res['page_start']}-{res['page_end']}")
        print(f"      Snippet: {res['snippet'][:150]}...")

    # Step 4: Query for panelization
    print("\n" + "=" * 70)
    print("STEP 4: Query 2 - JLC panelization (V-cuts vs mouse-bites)")
    print("=" * 70)

    query2 = "What are the differences between V-cuts and mouse-bites for panel separation?"
    result = rag_query(query2, top_k=3, tag="vendors")
    print(f"Query: {query2}")
    print(f"Results found: {result['count']}")
    for i, res in enumerate(result['results'], 1):
        print(f"\n  [{i}] Score: {res['score']:.3f}")
        print(f"      Source: {res['source']}")
        print(f"      Pages: {res['page_start']}-{res['page_end']}")
        print(f"      Snippet: {res['snippet'][:150]}...")

    # Step 5: Query tooling documentation
    print("\n" + "=" * 70)
    print("STEP 5: Query 3 - KiCad CLI export commands")
    print("=" * 70)

    query3 = "What are the exact KiCad CLI commands to export ERC/DRC reports in JSON and 3D STEP/GLB files?"
    result = rag_query(query3, top_k=3, tag="tooling")
    print(f"Query: {query3}")
    print(f"Results found: {result['count']}")
    for i, res in enumerate(result['results'], 1):
        print(f"\n  [{i}] Score: {res['score']:.3f}")
        print(f"      Source: {res['source']}")
        print(f"      Pages: {res['page_start']}-{res['page_end']}")
        print(f"      Snippet: {res['snippet'][:150]}...")

    # Step 6: Explain (audit) a result
    if result['results']:
        print("\n" + "=" * 70)
        print("STEP 6: Audit full chunk text via rag_explain()")
        print("=" * 70)

        chunk_id = result['results'][0]['id']
        explain_result = rag_explain([chunk_id])
        print(f"Chunk ID: {chunk_id}")
        print(f"Chunks returned: {explain_result['count']}")

        if explain_result['chunks']:
            chunk = explain_result['chunks'][0]
            print(f"\nFull Chunk Text:")
            print(f"  Path: {chunk['path']}")
            print(f"  Tag: {chunk['tag']}")
            print(f"  Pages: {chunk['page_start']}-{chunk['page_end']}")
            print(f"  Text length: {len(chunk['text'])} chars")
            print(f"  Text preview: {chunk['text'][:300]}...\n")

    # Summary
    print("\n" + "=" * 70)
    print("✅ RAG System Smoke Tests Complete")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Reload Claude Code (File → Close All → Reopen)")
    print("2. Verify MCP servers are available")
    print("3. Begin hardware design with RAG-powered specialist agents")
    print("\nFor more information, see: /mcp/DEPLOYMENT.md")

if __name__ == "__main__":
    main()
