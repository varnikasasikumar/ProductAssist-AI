import re
from typing import List, Dict, Any

def detect_section_header(text: str) -> str:
    """
    Detect section titles, error code headers, or major sub-headings at the start of or within a chunk.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines:
        if line.startswith("Error Code E") or line.startswith("WARNING") or re.match(r"^\d+\.\s+", line):
            return line[:100]
    return base_document_section(lines)

def base_document_section(lines: List[str]) -> str:
    if lines:
        return lines[0][:80]
    return ""

def _split_text_recursively(text: str, separators: List[str], chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Pure Python recursive text splitter.
    Splits text by separators in order of semantic preference:
    headings -> double line breaks -> single line breaks -> sentences -> spaces.
    """
    text = text.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    # Find the first separator present in text
    separator = None
    for s in separators:
        if s in text:
            separator = s
            break

    if not separator:
        return [text[i:i + chunk_size] for i in range(0, len(text), max(1, chunk_size - chunk_overlap))]

    parts = text.split(separator)
    final_chunks = []
    current_chunk = []
    current_len = 0

    for part in parts:
        part_str = part.strip()
        if not part_str:
            continue
        part_len = len(part_str)

        if current_len + part_len <= chunk_size:
            current_chunk.append(part_str)
            current_len += part_len + len(separator)
        else:
            if current_chunk:
                joined = f" {separator.strip()} ".join(current_chunk).strip()
                if joined:
                    final_chunks.append(joined)
            
            if len(part_str) > chunk_size:
                sub_separators = separators[separators.index(separator) + 1:]
                if sub_separators:
                    sub_chunks = _split_text_recursively(part_str, sub_separators, chunk_size, chunk_overlap)
                    final_chunks.extend(sub_chunks)
                else:
                    final_chunks.append(part_str[:chunk_size])
                current_chunk = []
                current_len = 0
            else:
                current_chunk = [part_str]
                current_len = part_len

    if current_chunk:
        joined = f" {separator.strip()} ".join(current_chunk).strip()
        if joined:
            final_chunks.append(joined)

    return final_chunks

def chunk_documents(documents: List[Dict[str, Any]], chunk_size: int = 850, chunk_overlap: int = 120) -> List[Dict[str, Any]]:
    """
    Structure-aware recursive chunker to split document page texts into semantically coherent blocks.
    
    Prefers section headers, paragraphs, and complete sentences as boundaries so that related items
    (such as Error Code E105 descriptions, diagnostics, actions, safety precautions) stay together.
    """
    separators = [
        "\n\nError Code ",
        "\n\n1. ", "\n\n2. ", "\n\n3. ", "\n\n4. ", "\n\n5. ", "\n\n6. ", "\n\n7. ",
        "\n\nWARNING",
        "\n\n",
        "\n",
        ". ",
        " "
    ]

    chunks = []

    for doc in documents:
        page_text = doc["text"]
        base_metadata = doc["metadata"]

        raw_chunks = _split_text_recursively(page_text, separators, chunk_size, chunk_overlap)

        for chunk_idx, chunk_text in enumerate(raw_chunks):
            chunk_text_clean = chunk_text.strip()
            if not chunk_text_clean:
                continue

            section = detect_section_header(chunk_text_clean)

            chunk_metadata = dict(base_metadata)
            chunk_metadata["chunk_index"] = chunk_idx
            chunk_metadata["section"] = section

            chunks.append({
                "text": chunk_text_clean,
                "metadata": chunk_metadata
            })

    return chunks
