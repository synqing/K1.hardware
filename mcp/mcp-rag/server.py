#!/usr/bin/env python3
"""
mcp-rag: a minimal, local Retrieval-Augmented MCP server.

- Exposes three tools:
  * rag_add(paths_or_globs, tag=""): index local PDFs/MD/TXT/HTML
  * rag_query(query, top_k=8, tag=None): return top chunks with citations
  * rag_explain(ids): return full chunk text for audit

Design choices:
- FastMCP from the official MCP Python SDK (stdio).
- pypdf for PDF text with page numbers.
- BeautifulSoup for HTML -> text; MD/TXT read as text.
- rank_bm25 BM25Okapi retrieval; token cache persisted.

Citations:
- MCP SDK & FastMCP: https://github.com/modelcontextprotocol/python-sdk
- KiCad CLI + iBOM + KiKit etc. referenced by the seed documents we ingest.
"""

from __future__ import annotations
import os, re, json, glob, pickle, uuid, chardet
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple

from mcp.server.fastmcp import FastMCP
from rank_bm25 import BM25Okapi
from bs4 import BeautifulSoup

# Optional import: pypdf for PDFs
try:
    from pypdf import PdfReader
except Exception as e:
    PdfReader = None

# ---- Config ----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
DOCS_JSONL = INDEX_DIR / "docs.jsonl"
TOKENS_PKL = INDEX_DIR / "tokens.pkl"

SUPPORTED = {".pdf", ".md", ".txt", ".html", ".htm"}
CHUNK_CHARS = 1200           # ~800-900 tokens depending on text
CHUNK_OVERLAP = 200
NORMALIZE_RX = re.compile(r"[^\w]+", re.UNICODE)

mcp = FastMCP("mcp-rag")

# ---- Data model -------------------------------------------------------------
@dataclass
class Chunk:
    id: str
    path: str
    tag: str
    page_start: int
    page_end: int
    text: str

# ---- Utilities --------------------------------------------------------------
def _ensure_dirs():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    if not DOCS_JSONL.exists():
        DOCS_JSONL.write_text("", encoding="utf-8")

def _read_file_text(path: Path) -> str:
    # Detect encoding for text/markdown/html
    raw = path.read_bytes()
    enc = chardet.detect(raw).get("encoding") or "utf-8"
    return raw.decode(enc, errors="ignore")

def _load_pdf(path: Path) -> List[Tuple[int, str]]:
    if PdfReader is None:
        raise RuntimeError("pypdf not installed")
    r = PdfReader(str(path))
    pages = []
    for i, p in enumerate(r.pages, start=1):
        try:
            t = p.extract_text() or ""
        except Exception:
            t = ""
        pages.append((i, t))
    return pages

def _html_to_text(s: str) -> str:
    soup = BeautifulSoup(s, "html.parser")
    # Drop scripts/styles
    for bad in soup(["script","style","noscript"]):
        bad.extract()
    return soup.get_text(separator="\n")

def _chunk_text(text: str, page: int|None=None) -> List[Tuple[int,int,str]]:
    # Simple fixed-size chunking with overlap; page numbers carried in metadata.
    chunks = []
    i = 0
    L = len(text)
    while i < L:
        j = min(L, i + CHUNK_CHARS)
        window = text[i:j]
        chunks.append((page or 1, page or 1, window))
        i = j - CHUNK_OVERLAP if j < L else L
        if i < 0: i = 0
    return chunks or [(page or 1, page or 1, text)]

def _tokenize(s: str) -> List[str]:
    return [w for w in NORMALIZE_RX.split(s.lower()) if w]

def _load_all_chunks() -> List[Chunk]:
    _ensure_dirs()
    out: List[Chunk] = []
    with DOCS_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                out.append(Chunk(**d))
            except Exception:
                continue
    return out

def _save_chunks(chunks: List[Chunk]) -> None:
    _ensure_dirs()
    with DOCS_JSONL.open("a", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")

def _rebuild_tokens_cache() -> None:
    chunks = _load_all_chunks()
    corpus = [c.text for c in chunks]
    tokens = [ _tokenize(t) for t in corpus ]
    with TOKENS_PKL.open("wb") as fp:
        pickle.dump({"ids":[c.id for c in chunks], "tokens":tokens}, fp)

def _ensure_tokens_cache() -> Dict[str, Any]:
    if not TOKENS_PKL.exists():
        _rebuild_tokens_cache()
    try:
        return pickle.loads(TOKENS_PKL.read_bytes())
    except Exception:
        _rebuild_tokens_cache()
        return pickle.loads(TOKENS_PKL.read_bytes())

def _index_one_file(path: Path, tag: str) -> List[Chunk]:
    ext = path.suffix.lower()
    chunks: List[Chunk] = []

    if ext not in SUPPORTED:
        return []

    if ext == ".pdf":
        pages = _load_pdf(path)
        for (pg, txt) in pages:
            for (p0, p1, piece) in _chunk_text(txt, page=pg):
                cid = str(uuid.uuid4())
                chunks.append(Chunk(id=cid, path=str(path), tag=tag, page_start=p0, page_end=p1, text=piece))
    else:
        s = _read_file_text(path)
        if ext in (".html", ".htm"):
            s = _html_to_text(s)
        # treat MD/TXT as plain text
        for (p0,p1,piece) in _chunk_text(s, page=None):
            cid = str(uuid.uuid4())
            chunks.append(Chunk(id=cid, path=str(path), tag=tag, page_start=p0, page_end=p1, text=piece))

    return chunks

# ---- MCP Tools --------------------------------------------------------------
@mcp.tool()
def rag_add(paths_or_globs: List[str], tag: str = "") -> Dict[str, Any]:
    """
    Index local files matching the given globs. Supported: .pdf, .md, .txt, .html.
    Returns counts and a sample of added chunk IDs.
    """
    _ensure_dirs()
    added: List[Chunk] = []
    seen: set[str] = set()
    for pattern in paths_or_globs:
        for p in glob.glob(pattern, recursive=True):
            path = Path(p).resolve()
            if not path.exists() or path.suffix.lower() not in SUPPORTED:
                continue
            if str(path) in seen:
                continue
            seen.add(str(path))
            added.extend(_index_one_file(path, tag=tag))

    if added:
        _save_chunks(added)
        _rebuild_tokens_cache()

    return {
        "files": len(seen),
        "chunks": len(added),
        "sample_ids": [c.id for c in added[:5]]
    }

@mcp.tool()
def rag_query(query: str, top_k: int = 8, tag: Optional[str] = None) -> Dict[str, Any]:
    """
    Query BM25 over the indexed chunks. Optionally filter by tag.
    Returns: [{id, score, source, page_start, page_end, snippet}]
    """
    chunks = _load_all_chunks()
    if tag:
        chunks = [c for c in chunks if c.tag == tag]
    if not chunks:
        return {"results": [], "note": "No chunks available. Run rag_add() first."}

    cache = _ensure_tokens_cache()
    ids = cache["ids"]
    tokens = cache["tokens"]

    # Align ids/tokens to filtered set if tag is used
    if tag:
        # rebuild quick view for filtered subset
        filt_ids = set(c.id for c in chunks)
        toks = [tok for (tok_id, tok) in zip(ids, tokens) if tok_id in filt_ids]
        bm25 = BM25Okapi(toks)
        idx_map = [tok_id for tok_id in ids if tok_id in filt_ids]
        scores = bm25.get_scores(_tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda t: t[1], reverse=True)
        results = []
        by_id = {c.id: c for c in chunks}
        for (i, s) in ranked[:top_k]:
            if i >= len(idx_map):
                continue
            cid = idx_map[i]
            c = by_id.get(cid)
            if not c: continue
            results.append({
                "id": c.id,
                "score": float(s),
                "source": f"file://{c.path}" + (f"#page={c.page_start}" if c.page_start else ""),
                "page_start": c.page_start,
                "page_end": c.page_end,
                "snippet": c.text[:600]
            })
        return {"results": results, "count": len(results)}
    else:
        bm25 = BM25Okapi(tokens)
        scores = bm25.get_scores(_tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda t: t[1], reverse=True)
        # Build id->chunk
        by_id = {c.id: c for c in chunks}
        results = []
        for (i, s) in ranked[:top_k]:
            cid = ids[i]
            c = by_id.get(cid)
            if not c: continue
            results.append({
                "id": c.id,
                "score": float(s),
                "source": f"file://{c.path}" + (f"#page={c.page_start}" if c.page_start else ""),
                "page_start": c.page_start,
                "page_end": c.page_end,
                "snippet": c.text[:600]
            })
        return {"results": results, "count": len(results)}

@mcp.tool()
def rag_explain(ids: List[str]) -> Dict[str, Any]:
    """Return full chunk text + metadata for the given IDs."""
    chunks = _load_all_chunks()
    by_id = {c.id: c for c in chunks}
    out = []
    for cid in ids:
        c = by_id.get(cid)
        if not c: continue
        out.append(asdict(c))
    return {"chunks": out, "count": len(out)}

if __name__ == "__main__":
    _ensure_dirs()
    mcp.run()
