# mcp-rag — Local Retrieval-Augmented MCP Server

**Purpose:** Offline, cite-aware retrieval over indexed local files (PDFs, Markdown, HTML, TXT).

## Tools

### `rag_add(paths_or_globs: list[str], tag: str = "")`

Index local files matching glob patterns. Supported formats: `.pdf`, `.md`, `.txt`, `.html`, `.htm`.

**Parameters:**
- `paths_or_globs` — List of glob patterns (e.g., `["docs/knowledge/**/*.pdf"]`)
- `tag` — Optional label for grouping (e.g., `"vendors"`, `"tooling"`)

**Returns:**
```json
{
  "files": 5,
  "chunks": 42,
  "sample_ids": ["uuid-1", "uuid-2", ...]
}
```

**Example:**
```python
result = rag_add(["docs/knowledge/vendors/**/*"], tag="vendors")
```

---

### `rag_query(query: str, top_k: int = 8, tag: str | None = None)`

BM25 semantic retrieval over indexed chunks. Returns results with citations.

**Parameters:**
- `query` — Natural language question
- `top_k` — Number of results (default: 8)
- `tag` — Optional filter by tag (e.g., `"vendors"` to search only vendor docs)

**Returns:**
```json
{
  "results": [
    {
      "id": "chunk-uuid",
      "score": 12.34,
      "source": "file:///path/to/doc.pdf#page=5",
      "page_start": 5,
      "page_end": 5,
      "snippet": "text excerpt (600 chars)"
    }
  ],
  "count": 3
}
```

**Examples:**
```python
# Query all indexed sources
result = rag_query("ESP32-S3 antenna keep-out zone", top_k=5)

# Query only vendor documents
result = rag_query("V-cuts vs mouse-bites panel requirements", top_k=5, tag="vendors")

# Query only tooling/automation docs
result = rag_query("KiCad CLI export STEP and GLB commands", top_k=5, tag="tooling")
```

---

### `rag_explain(ids: list[str])`

Return full chunk text for inspection/audit.

**Parameters:**
- `ids` — List of chunk UUIDs (from rag_query results)

**Returns:**
```json
{
  "chunks": [
    {
      "id": "chunk-uuid",
      "path": "/path/to/source.pdf",
      "tag": "vendors",
      "page_start": 5,
      "page_end": 5,
      "text": "full chunk text (1200 chars)"
    }
  ],
  "count": 1
}
```

**Example:**
```python
# Get full text for a chunk
result = rag_explain(["chunk-uuid-from-query"])
```

---

## Implementation

- **MCP SDK:** Official `mcp` Python package (FastMCP server, stdio).
- **PDF extraction:** `pypdf` with page-number awareness.
- **HTML parsing:** BeautifulSoup4 (strips scripts/styles).
- **Retrieval:** BM25Okapi (rank-bm25) over tokenized chunks.
- **Storage:** Chunks persisted as JSONL; token cache pickled for speed.
- **Citations:** Every result includes source path + page numbers.

---

## Index Structure

```
mcp/mcp-rag/
├── index/
│   ├── docs.jsonl           (chunked documents + metadata)
│   └── tokens.pkl           (BM25 token cache, auto-rebuilt)
├── server.py
├── requirements.txt
└── README.md
```

- **docs.jsonl:** One JSON object per line. Schema: `{id, path, tag, page_start, page_end, text}`
- **tokens.pkl:** Cached BM25 corpus for fast retrieval; auto-generated on first query.

---

## Chunking Strategy

- **Fixed-size chunks:** 1200 characters (~800–900 tokens) per chunk.
- **Overlap:** 200 characters between chunks (context preservation).
- **PDF pages:** Page numbers tracked and included in citations.
- **Markdown/HTML/TXT:** Treated as single-page documents; page_start/end = 1.

---

## Seed Knowledge

Populate the index with vendor datasheets + tooling guides:

```bash
# Create knowledge folders
mkdir -p docs/knowledge/{vendors,tooling}

# Download sources (using fetch MCP or manual):
# - Espressif ESP32-S3 Hardware Design Guidelines
# - Adafruit NeoPixel Best Practices + Level Shifting
# - JLCPCB Panelization Help Pages
# - KiCad CLI Manual (v8)
# - Interactive HTML BOM Usage
# - KiKit Panelization Examples
# - Nexar/LCSC API Overviews

# Index them:
rag_add(["docs/knowledge/vendors/**/*"], tag="vendors")
rag_add(["docs/knowledge/tooling/**/*"], tag="tooling")
```

---

## Usage in Claude Code

Once configured in `~/.config/Claude/claude_desktop_config.json`, agents can query the RAG:

```python
# Schematic Sage queries vendor docs
result = rag_query("ESP32-S3 power supply decoupling requirements", tag="vendors")
for r in result["results"]:
    print(f"✓ {r['source']}: {r['snippet']}")

# Layout Coach queries tooling docs
result = rag_query("KiCad DRC JSON format and violations", tag="tooling")
```

---

## Offline-First Design

**mcp-rag never calls the web.** All sources are pre-downloaded locally:

1. Use the `fetch` MCP to download PDFs/HTML to `/docs/knowledge/`.
2. Call `rag_add()` to index.
3. Call `rag_query()` for retrieval (no external calls).

---

## Performance Notes

- **Index time:** ~100–200ms per document (depends on size).
- **Query time:** ~50–100ms (BM25 is fast; no embeddings).
- **Storage:** ~1–2 KB per 1200-char chunk (JSON + metadata).

---

**Status:** Offline, local, cite-aware RAG for hardware design knowledge.

**Last updated:** Oct 23, 2025
