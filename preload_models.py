from sentence_transformers import SentenceTransformer

print("✅ Starting model preload...")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("✅ Model preload complete.")
