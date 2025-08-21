import json
from pathlib import Path
from typing import List
from tqdm import tqdm
from src.custom_types import PATHLIKE
from src.helper import _convert_to_path, str_to_uuid
from src.config import INDEX_DIR, CHUNKED_DIR, VECTORIZATION_MODEL_NAME
import hashlib as hash
import pickle
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

class Vectorizer:

    def __init__(self, input_dir: PATHLIKE = CHUNKED_DIR, output_dir: PATHLIKE = INDEX_DIR) -> None:
        self.chunk_dir = _convert_to_path(input_dir)
        self.indexed_dir = _convert_to_path(output_dir)

    
    def load_chunks(self):
        all_chunks = []
        for file in tqdm(self.chunk_dir.glob("*.json"), desc="Reading all chunkgs into ram."):
            with open(file, "r") as f:
                all_chunks.extend(json.load(f))
        
        return all_chunks
        
    def build_index(self, chunks: List[dict]):
        """
        Build a faiss index from text chunks https://faiss.ai/
        Arguments: 
            chunks List[dict] -- Alls chunks in an array
        """
        model = SentenceTransformer(VECTORIZATION_MODEL_NAME)
        texts= [d["text"] for d in chunks]
        
        print(f"🔍 Encoding {len(texts)} chunks...")
        embs = model.encode(texts, convert_to_numpy=True, show_progress_bar=True).astype("float32")

        # CREATE the FAISS index
        embs = np.asarray(embs, dtype=np.float32)
        embs = np.ascontiguousarray(embs)
        assert embs.ndim == 2, f"Embeddings must be (n, d), got {embs.shape}"

        d = embs.shape[1]
        index = faiss.IndexFlatL2(d)

        # Support both FAISS Python API variants
        try:
            index.add(embs)  # newer binding
        except TypeError:
            index.add(embs.shape[0], embs)  # older/SWIG binding
            # Save index + metadata
        faiss.write_index(index, str(self.indexed_dir / "faiss_index.bin"))
        with open(self.indexed_dir / "metadata.pkl", "wb") as f:
            pickle.dump(chunks, f)

        print(f"✅ Saved FAISS index with {index.ntotal} vectors.")

    def index_all_chunks(self):
        self.indexed_dir.mkdir(parents=True, exist_ok=True)
        chunks = self.load_chunks()
        self.build_index(chunks)


if __name__ == '__main__':
    vec = Vectorizer()
    vec.index_all_chunks()