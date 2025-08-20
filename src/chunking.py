import json
from pathlib import Path
from typing import List
from tqdm import tqdm
from src.custom_types import PATHLIKE
from src.helper import _convert_to_path
from src.config import INGESTED_DIR, CHUNKED_DIR

CHUNK_SIZE = 1000   # characters per chunk
CHUNK_OVERLAP = 200 # overlap between chunks

class Chunker:

    def __init__(self, input_dir:PATHLIKE = INGESTED_DIR, output_dir:PATHLIKE = CHUNKED_DIR, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.input_dir = _convert_to_path(input_dir)
        self.output_dir = _convert_to_path(output_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    @staticmethod
    def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Splits text into overlapping chunks.
        """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunks.append(text[start:end])
            start += chunk_size - overlap

        return chunks

    def process_file(self, file_path: Path):
        """
        Reads a .txt file, chunks it, and saves chunks as JSON.
        """
        text = file_path.read_text(encoding="utf-8")
        chunks = self.chunk_text(text, self.chunk_size, self.chunk_overlap)

        # Prepare structured data
        data = [
            {
                "source": file_path.name,
                "chunk_id": i,
                "text": chunk
            }
            for i, chunk in enumerate(chunks)
        ]

        # Save JSON
        output_file = self.output_dir / (file_path.stem + ".json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Chunked: {file_path} → {output_file} ({len(chunks)} chunks)")

    def process_files_in_input_dir(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        input_files_glob = list(self.input_dir.glob("*.txt"))
        for file in tqdm(
            input_files_glob, desc="Chunking files into jsons"
        ):
            if file.is_file():
                self.process_file(file)

if __name__ == "__main__":
    chunker = Chunker()
    chunker.process_files_in_input_dir()
