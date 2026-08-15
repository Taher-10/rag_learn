from pathlib import Path
from .processing import normalize_text
import json

def load_file(path: str | Path) -> dict:
    """Load movie data from a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_stopwords(path: str | Path) -> list[str]:
    """Load and normalize stopwords from a file."""
    with open(path, "r", encoding="utf-8") as file:
        return [normalize_text(word) for word in file if word.strip()]
