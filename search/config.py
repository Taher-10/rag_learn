from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"

MOVIES_PATH = DATA_DIR / "movies.json"
STOPWORDS_PATH = DATA_DIR / "stopwords.txt"

INDEX_PATH =CACHE_DIR / "index.pkl"
DOCMAP_PATH =CACHE_DIR / "docmap.pkl"
TF_PATH =CACHE_DIR / "term_frequencies.pkl"