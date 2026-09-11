import os
import json
from pathlib import Path
import pypdf

# Mapping document filename keywords to standard DocumentType values
DOC_TYPE_MAP = {
    "operation-manual": "OPERATION_MANUAL",
    "installation-guide": "INSTALLATION_GUIDE",
    "troubleshooting-guide": "TROUBLESHOOTING",
    "maintenance-manual": "MAINTENANCE_MANUAL",
    "safety-guide": "SAFETY",
    "technical-specifications": "TECHNICAL_SPECIFICATION",
    "service-manual": "SERVICE_MANUAL",
    "specifications": "STRUCTURED_SPECIFICATION",
}

PRODUCT_NAME_MAP = {
    "CNC-X100": "CNC Machine",
    "Printer-A200": "Industrial 3D Printer",
    "HVAC-C500": "Commercial HVAC System",
}

def derive_document_type(filename: str) -> str:
    """Derive standardized document type enum string from file name."""
    clean_name = filename.lower().replace(".pdf", "").replace(".json", "").replace(".csv", "")
    for key, doc_type in DOC_TYPE_MAP.items():
        if key in clean_name:
            return doc_type
    return "GENERAL_DOCUMENT"

def find_knowledge_base_dir() -> Path:
    """Locate the root knowledge base directory containing product subdirectories."""
    possible_paths = [
        Path(__file__).resolve().parent.parent.parent / "knowledge-base",
        Path(__file__).resolve().parent.parent / "knowledge-base",
        Path("knowledge-base").resolve(),
        Path("../knowledge-base").resolve(),
    ]
    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path
    raise FileNotFoundError("Could not locate knowledge-base directory.")

def extract_docx_text(file_path: Path) -> str:
    """Extract clean text content from Word .docx file using stdlib zipfile & ElementTree."""
    import zipfile
    import xml.etree.ElementTree as ET
    try:
        with zipfile.ZipFile(file_path) as z:
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            texts = [node.text for node in tree.findall(".//w:t", namespaces) if node.text]
            return "\n".join(texts).strip()
    except Exception as err:
        print(f"Warning: Could not parse DOCX {file_path}: {err}")
        return ""

def extract_html_text(file_path: Path) -> str:
    """Extract clean text content from HTML document using stdlib HTMLParser."""
    from html.parser import HTMLParser
    class HTMLTextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.chunks = []
        def handle_data(self, data):
            text = data.strip()
            if text:
                self.chunks.append(text)
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        parser = HTMLTextExtractor()
        parser.feed(content)
        return "\n".join(parser.chunks).strip()
    except Exception as err:
        print(f"Warning: Could not parse HTML {file_path}: {err}")
        return ""

def extract_csv_text(file_path: Path) -> str:
    """Extract tabular row data from CSV file."""
    import csv
    lines = []
    try:
        with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    lines.append(" | ".join(row))
        return "\n".join(lines).strip()
    except Exception as err:
        print(f"Warning: Could not parse CSV {file_path}: {err}")
        return ""

def load_pdf_documents(kb_dir: Path = None):
    """
    Multi-format document & structured knowledge extractor across all product model subdirectories.
    Supports PDF, Word (DOCX), HTML, CSV, JSON, and Image visual metadata assets.
    
    Returns:
        List of dicts: each containing 'text' and 'metadata' for a specific document page or chunk.
    """
    if kb_dir is None:
        kb_dir = find_knowledge_base_dir()

    pdf_files = sorted(list(kb_dir.rglob("*.pdf")))
    json_files = sorted(list(kb_dir.rglob("*.json")))
    docx_files = sorted(list(kb_dir.rglob("*.docx")))
    html_files = sorted(list(kb_dir.rglob("*.html")))
    csv_files = sorted(list(kb_dir.rglob("*.csv")))
    img_files = sorted([f for f in kb_dir.rglob("*") if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".svg"]])

    if not any([pdf_files, json_files, docx_files, html_files, csv_files, img_files]):
        raise FileNotFoundError(f"No valid knowledge document files found in {kb_dir}")

    documents = []

    # Process PDF files
    for file_path in pdf_files:
        doc_name = file_path.name
        doc_type = derive_document_type(doc_name)
        model = file_path.parent.name if file_path.parent != kb_dir else "CNC-X100"
        product = PRODUCT_NAME_MAP.get(model, "Industrial Equipment")

        try:
            reader = pypdf.PdfReader(str(file_path))
            num_pages = len(reader.pages)

            for page_idx in range(num_pages):
                page_obj = reader.pages[page_idx]
                page_text = page_obj.extract_text() or ""
                page_number = page_idx + 1

                if page_text.strip():
                    documents.append({
                        "text": page_text.strip(),
                        "metadata": {
                            "product": product,
                            "model": model,
                            "document_name": doc_name,
                            "document_type": doc_type,
                            "file_format": "PDF",
                            "page_number": page_number,
                            "source_file": str(file_path),
                        }
                    })
        except Exception as err:
            print(f"Warning: Could not parse PDF {file_path}: {err}")

    # Process Word documents
    for file_path in docx_files:
        doc_name = file_path.name
        doc_type = derive_document_type(doc_name)
        model = file_path.parent.name if file_path.parent != kb_dir else "CNC-X100"
        product = PRODUCT_NAME_MAP.get(model, "Industrial Equipment")

        text = extract_docx_text(file_path)
        if text:
            documents.append({
                "text": f"DOCUMENT: {doc_name} ({product} - {model})\n{text}",
                "metadata": {
                    "product": product,
                    "model": model,
                    "document_name": doc_name,
                    "document_type": doc_type,
                    "file_format": "DOCX",
                    "page_number": 1,
                    "source_file": str(file_path),
                }
            })

    # Process HTML documents
    for file_path in html_files:
        doc_name = file_path.name
        doc_type = derive_document_type(doc_name)
        model = file_path.parent.name if file_path.parent != kb_dir else "CNC-X100"
        product = PRODUCT_NAME_MAP.get(model, "Industrial Equipment")

        text = extract_html_text(file_path)
        if text:
            documents.append({
                "text": f"HTML KNOWLEDGE GUIDE: {doc_name} ({product} - {model})\n{text}",
                "metadata": {
                    "product": product,
                    "model": model,
                    "document_name": doc_name,
                    "document_type": doc_type,
                    "file_format": "HTML",
                    "page_number": 1,
                    "source_file": str(file_path),
                }
            })

    # Process CSV files
    for file_path in csv_files:
        doc_name = file_path.name
        doc_type = derive_document_type(doc_name)
        model = file_path.parent.name if file_path.parent != kb_dir else "CNC-X100"
        product = PRODUCT_NAME_MAP.get(model, "Industrial Equipment")

        text = extract_csv_text(file_path)
        if text:
            documents.append({
                "text": f"STRUCTURED CSV DATASET: {doc_name} ({product} - {model})\n{text}",
                "metadata": {
                    "product": product,
                    "model": model,
                    "document_name": doc_name,
                    "document_type": doc_type,
                    "file_format": "CSV",
                    "page_number": 1,
                    "source_file": str(file_path),
                }
            })

    # Process JSON files
    for file_path in json_files:
        doc_name = file_path.name
        doc_type = derive_document_type(doc_name)
        model = file_path.parent.name if file_path.parent != kb_dir else "CNC-X100"
        product = PRODUCT_NAME_MAP.get(model, "Industrial Equipment")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            formatted_json_text = (
                f"AUTHORIZED STRUCTURED SPECIFICATIONS FOR {product} ({model}):\n"
                f"{json.dumps(data, indent=2)}"
            )

            documents.append({
                "text": formatted_json_text,
                "metadata": {
                    "product": product,
                    "model": model,
                    "document_name": doc_name,
                    "document_type": doc_type,
                    "file_format": "JSON",
                    "page_number": 1,
                    "source_file": str(file_path),
                }
            })
        except Exception as err:
            print(f"Warning: Could not parse JSON {file_path}: {err}")

    # Process image asset metadata
    for file_path in img_files:
        doc_name = file_path.name
        doc_type = derive_document_type(doc_name)
        model = file_path.parent.name if file_path.parent != kb_dir else "CNC-X100"
        product = PRODUCT_NAME_MAP.get(model, "Industrial Equipment")

        image_desc = (
            f"VISUAL KNOWLEDGE ASSET & DIAGRAM: {doc_name} ({product} - {model}).\n"
            f"File: {doc_name}, Location Path: /assets/{doc_name}.\n"
            f"Contains technical visual schematic for model {model}."
        )

        documents.append({
            "text": image_desc,
            "metadata": {
                "product": product,
                "model": model,
                "document_name": doc_name,
                "document_type": doc_type,
                "file_format": "IMAGE",
                "page_number": 1,
                "source_file": str(file_path),
            }
        })

    return documents

