# 🧠 Semantic PDF Outline Extractor – Adobe India Hackathon Round 1A

Extract a structured outline (Title, H1, H2, H3) from PDF files using a lightweight, semantic-aware model. Designed for fast, offline, CPU-only execution under strict resource constraints.

---

## 📌 Problem Statement

Design a tool that extracts semantic document outlines from PDFs while satisfying:

- ≤ 200MB total model size
- ≤ 10s runtime for a 50-page PDF
- Must run offline, CPU-only
- Bonus: Support for multilingual documents

---

## 🚀 Approach

We replaced traditional font-size-based heuristics with semantic reasoning using a transformer model.

### Key Steps:

1. Extract all text blocks via PyMuPDF
2. Generate sentence embeddings using MiniLM (multilingual)
3. Cluster similar sentences using KMeans
4. Infer heading levels via relative position & cluster properties
5. Output structured JSON with title and heading hierarchy

---

## ⚙️ Tech Stack

| Component             | Tool/Library                             |
|----------------------|-------------------------------------------|
| Programming Language  | Python 3.9                                |
| PDF Parsing           | PyMuPDF (fitz)                            |
| Semantic Embeddings   | sentence-transformers                    |
| Clustering            | scikit-learn KMeans                       |
| Environment           | Docker (python:3.9-slim, linux/amd64)     |

---

## 🧠 Model Info

- Model: paraphrase-multilingual-MiniLM-L12-v2
- Framework: SentenceTransformers
- Size: ~120MB
- Offline Support: Model preloaded and cached during build

---

## 📦 Folder Structure

```bash
challenge_1A/
├── Dockerfile
├── preload_models.py
├── extractor.py
├── requirements.txt
├── input/
│   └── file01.pdf
├── output/
│   └── file01.json
