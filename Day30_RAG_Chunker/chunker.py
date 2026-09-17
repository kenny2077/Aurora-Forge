"""RAG text chunker with overlap and dedup.

Before embedding a document for retrieval we split it into overlapping word-windows (overlap keeps
context across boundaries) and drop exact-duplicate chunks (boilerplate repeats waste the vector DB
and skew retrieval). Implement `chunk_text` to pass test_chunker.py.

Contract:
    chunk_text(text: str, size: int, overlap: int) -> list[str]
    - Tokenize on whitespace (words = text.split()).
    - Produce windows of `size` words, advancing by (size - overlap) words each step.
    - The final window may be shorter than `size`.
    - Each chunk is its words joined by single spaces.
    - Drop exact-duplicate chunk strings, keeping the FIRST occurrence (preserve order).
    - Empty text -> [].
    - size <= 0 raises ValueError; overlap outside [0, size) raises ValueError.
"""


def chunk_text(text, size, overlap):
    raise NotImplementedError("Window by size, step by size-overlap, then dedup preserving order.")
