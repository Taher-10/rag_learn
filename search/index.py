import os
import pickle
import math
from pathlib import Path
from collections import Counter

from .search import  process_tokens
from .data_loader import load_file, load_stopwords


class InvertedIndex:
    """Inverted Index mapping preprocessed tokens to sets of document IDs.\n
        - dindex mapp term to set of doc ids that term occur in exp : star [20, 5,200]
        - docmap maps id to doc related to it(movie corres pondin exp : 5 -> star wars)\n
        - term frequincy map id to a counter special duntionarry
    
    """
    def __init__(self, stopwords: list[str],index_path:str ,docmap_path:str,term_frequencies_path=str):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, dict] = {}
        self.term_frequencies:dict[int,Counter]={}

        self.stopwords: list[str] = stopwords or []
        self.index_path:str=index_path
        self.docmap_path:str=docmap_path
        self.term_frequencies_path:str=term_frequencies_path

    def _add_document(self, doc_id: int, text: str) -> None:
        """Tokenize input text and map tokens to the document ID."""
        tokens = process_tokens(text, self.stopwords)

        #create a counter for this document
        self.term_frequencies[doc_id]=Counter(tokens)

        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list[int]:
        """Return doc IDs for a preprocessed term as a sorted list."""
        return sorted(list(self.index.get(term, set())))
    
    def get_tf(self,doc_id:int,term:str):
        """return how many times the token appears in the document with the given ID. If the term doesn't appear in that document, return 0. 
        Assume term is a single token"""
        counter=self.term_frequencies.get(doc_id,Counter())
        #searsh for the term in counter
        return counter.get(term,0)
    
    def get_df(self,term:str):
        """return how many documents contain the given term. If the term doesn't appear in any document, return 0. 
        Assume term is a single token"""
        return len(self.index.get(term,set()))
    
    def get_idf(self,term:str):
        """return the inverse document frequency (IDF) of the given term.
        this score stand for how rare term is in the hole corpus. 
        If the term doesn't appear in any document, return 0."""
        total_doc_count=len(self.docmap)
        if term =="":
            print(0)

        idf=math.log((total_doc_count+1)/(self.get_df(term)+1))
        return idf
    
    def get_tf_idf(self,doc_id:int,term:str):
        """"""
        tf=self.get_tf(doc_id,term)
        idf=self.get_idf(term)
        return tf*idf

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

        with open(self.term_frequencies_path,"wb") as frequencies_file:
            pickle.dump(self.term_frequencies,frequencies_file)


    def load(self) -> None:
        """Load index and docmap dictionaries from disk."""
        with open(self.index_path, "rb") as index_file:
            self.index = pickle.load(index_file)

        with open(self.docmap_path, "rb") as docmap_file:
            self.docmap = pickle.load(docmap_file)

        with open(self.term_frequencies_path,"rb") as frequencies_file:
            self.term_frequencies=pickle.load(frequencies_file)


def build_command(
    data_path: str,
    stopwords_path: str,
    index_path: str,
    docmap_path: str,
    term_frequencies_path: str,
) -> None:
    """Build and save the inverted index."""

    stopwords = load_stopwords(stopwords_path)

    index = InvertedIndex(
        stopwords,
        index_path,
        docmap_path,
        term_frequencies_path,
    )

    index.build(data_path, stopwords_path)
    index.save()