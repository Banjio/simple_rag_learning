import os
from pathlib import Path
from unstructured.partition.auto import partition


# Input and Output folder
PROJECT_PATH = os.environ.get("PROJECT_PATH") or "~/ws/simple_rag_system" 
PATHLIKE = str | Path

INPUT_DIR = "../documents_db/raw"
OUTPUT_DIR="../documents_db/ingested"


class UnstructuredConverter:

    def __init__(self, input_dir:PATHLIKE = INPUT_DIR, output_dir:PATHLIKE = OUTPUT_DIR):
        self.input_dir = self._convert_to_path(input_dir)
        self.output_dir = self._convert_to_path(output_dir)

    @staticmethod
    def convert_file_to_txt(file_path: Path, output_dir: Path):
        """
        Extract all texdt from a file and save it to text
        """
        
        try:
            elements = partition(filename=str(file_path))
            content = "\n".join([el.text for el in elements if el.text])

            output_fn = output_dir / (file_path.stem + ".txt")
            output_fn.write_text(content, encoding="utf-8")

            print(f"✅ Converted: {file_path} → {output_fn}")
        except Exception as e:
            print(f"❌ Failed to process {file_path}: {e}")            


    def convert_files_in_input_dir(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for file in self.input_dir.glob("*.pdf|*.docx"):
            if file.is_file():
                self.convert_file_to_txt(file, self.output_dir)


    @staticmethod
    def _convert_to_path(fp: PATHLIKE):
        """
        safely convert a file path to a pathlib.Path
        """
        if not isinstance(fp, Path):
            fp = Path(fp)
        return fp
