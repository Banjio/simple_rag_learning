import hashlib
import uuid
from pathlib import Path
from src.custom_types import PATHLIKE

def _convert_to_path(fp: PATHLIKE):
    """
    safely convert a file path to a pathlib.Path
    """
    if not isinstance(fp, Path):
        fp = Path(fp)
    return fp


def str_to_uuid(s: str) -> str:
    sha256_hash = hashlib.sha256(s.encode('utf-8')).hexdigest()
    hashed_uuid = uuid.UUID(hex=sha256_hash[:32], version=5)
    return str(hashed_uuid)