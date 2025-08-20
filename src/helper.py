from pathlib import Path
from src.custom_types import PATHLIKE

def _convert_to_path(fp: PATHLIKE):
    """
    safely convert a file path to a pathlib.Path
    """
    if not isinstance(fp, Path):
        fp = Path(fp)
    return fp

