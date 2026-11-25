from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
METADATA_DIR = DATA_DIR / "metadata"
METADATA_FILE = METADATA_DIR / "documents.json"





