import os
from pathlib import Path
import tqdm
from unstructured.partition.auto import partition
from src.custom_types import PATHLIKE
from src.config import RAW_DIR, INGESTED_DIR
from src.helper import _convert_to_path


class UnstructuredConverter:
    def __init__(
        self, input_dir: PATHLIKE = RAW_DIR, output_dir: PATHLIKE = INGESTED_DIR
    ):
        self.input_dir = _convert_to_path(input_dir)
        self.output_dir = _convert_to_path(output_dir)

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
        """Convert entire input directory but only pdfs for now until i
        understand how to use glob correctly
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        input_files_glob = list(self.input_dir.glob("*.pdf"))
        for file in tqdm.tqdm(
            input_files_glob, desc="Processing files using unstructured"
        ):
            if file.is_file():
                self.convert_file_to_txt(file, self.output_dir)


if __name__ == "__main__":
    converter = UnstructuredConverter()
    converter.convert_files_in_input_dir()
