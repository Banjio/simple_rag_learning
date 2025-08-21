import faiss
import pickle
from sentence_transformers import SentenceTransformer
from src.config import INDEX_DIR

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def search(query, top_k=3):
    # Load FAISS index + metadata
    index = faiss.read_index(f"{INDEX_DIR}/faiss_index.bin")
    with open(f"{INDEX_DIR}/metadata.pkl", "rb") as f:
        chunks = pickle.load(f)

    # Embed query
    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([query], convert_to_numpy=True)

    # Search
    distances, indices = index.search(query_vec, top_k)

    # Return results
    results = [chunks[i] for i in indices[0]]
    return results

if __name__ == "__main__":
    query = "Give me the most recent insurance documents?"
    results = search(query, top_k=3)

    print("\n🔎 Search Results:")
    for r in results:
        print(f"- {r['source']} [chunk {r['pk_chunk']}]: {r['text'][:200]}...")
