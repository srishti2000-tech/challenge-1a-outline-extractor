import fitz  # PyMuPDF
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
import torch

def extract_outline(pdf_path, model):
    doc = fitz.open(pdf_path)
    all_spans = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if line_text:
                    all_spans.append((line_text, page_num))

    if not all_spans:
        return []

    texts = [t[0] for t in all_spans]
    embeddings = model.encode(texts, convert_to_tensor=True)

    # Dynamically determine number of clusters based on total lines
    num_clusters = min(5, max(1, len(texts) // 10))
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    labels = kmeans.fit_predict(embeddings.cpu().numpy())

    clustered = [[] for _ in range(num_clusters)]
    for (text, page_num), label in zip(all_spans, labels):
        clustered[label].append((text, page_num))

    # For simplicity, treat all clustered headings as H1
    outline = []
    for cluster in clustered:
        for text, page in cluster:
            outline.append({
                "level": "H1",
                "text": text.strip(),
                "page": page
            })

    return outline

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🚀 Starting semantic outline extraction")
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    for pdf_file in input_dir.glob("*.pdf"):
        print(f"📄 Processing {pdf_file.name}")
        outline = extract_outline(str(pdf_file), model)
        result = {
            "title": outline[0]["text"] if outline else "",
            "outline": outline[1:] if outline else []
        }

        output_path = output_dir / f"{pdf_file.stem}.json"
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

if __name__ == "__main__":
    process_pdfs()
