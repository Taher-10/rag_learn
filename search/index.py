import os
import pickle
from pathlib import Path

from .search import  process_tokens
from .data_loader import load_file, load_stopwords


class InvertedIndex:
    """Inverted Index mapping preprocessed tokens to sets of document IDs."""
    def __init__(self, stopwords: list[str],index_path:str ,docmap_path:str):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, dict] = {}
        self.stopwords: list[str] = stopwords or []
        self.index_path:str=index_path
        self.docmap_path:str=docmap_path

    def _add_document(self, doc_id: int, text: str) -> None:
        """Tokenize input text and map tokens to the document ID."""
        tokens = process_tokens(text, self.stopwords)

        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list[int]:
        """Return doc IDs for a preprocessed term as a sorted list."""
        return sorted(list(self.index.get(term, set())))

    def build(self, data_path: str | Path, stopwords_path: str | Path) -> None:
        """Build index and docmap from raw movie dataset and stopwords file."""
        self.stopwords = load_stopwords(stopwords_path)
        movies_data = load_file(data_path)

        for movie in movies_data["movies"]:
            doc_id = movie["id"]
            self.docmap[doc_id] = movie

            text = f"{movie['title']} {movie['description']}"
            self._add_document(doc_id, text)

    def save(self, cache_dir: str = "cache") -> None:
        """Save index and docmap dictionaries to disk using pickle."""
        os.makedirs(cache_dir, exist_ok=True)

        with open(self.index_path, "wb") as index_file:
            pickle.dump(self.index, index_file)

        with open(self.docmap_path, "wb") as docmap_file:
            pickle.dump(self.docmap, docmap_file)

    def load(self)-> None:
        """"""
        with open(self.index_path, "r") as index_file:
            self.index=pickle.load(index_file)

        with open(self.docmap_path, "r") as docmap_file:
            self.docmap=pickle.load(docmap_file)


def build_command(data_path: str, stopwords_path: str) -> None:
    """CLI Handler to build, pickle index, and display test lookups."""
    index = InvertedIndex()
    index.build(data_path, stopwords_path)
    index.save()