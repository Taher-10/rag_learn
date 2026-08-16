import argparse

from .config import MOVIES_PATH,STOPWORDS_PATH,INDEX_PATH,DOCMAP_PATH,TF_PATH
from .data_loader import load_file,load_stopwords
from .search import search
from .index import build_command,InvertedIndex
from .processing import tokenize_term
import math


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search Command Parser
    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    # Build Command Parser
    subparsers.add_parser("build", help="Create and build an inverted index")

    # Term frequincy Parser
    tf_parser=subparsers.add_parser("tf",help="Searsh how frequent a term is in a document(movie)")
    tf_parser.add_argument("doc_id", type=int, help="docment id of the movie")
    tf_parser.add_argument("term", type=str, help="term to se how frequent it is")
    
    # Inversed document frequincy Parser
    idf_parser=subparsers.add_parser("idf",help="Searsh how rare a term is the corpus of documents")
    idf_parser.add_argument("term", type=str, help="term to se how frequent it is")

    # TF-IDF Parser
    tf_idf_parser=subparsers.add_parser("tf-idf",help="give a score of how important a term is in a document(movie) in the corpus")
    tf_idf_parser.add_argument("doc_id", type=int, help="docment id of the movie")
    tf_idf_parser.add_argument("term", type=str, help="term to se how frequent it is")
    

    args = parser.parse_args()

    match args.command:
        case "search":
            movies = load_file(MOVIES_PATH)
            stopwords = load_stopwords(STOPWORDS_PATH)

            index=InvertedIndex(stopwords,INDEX_PATH,DOCMAP_PATH,TF_PATH)
            index.load()


            results = search(movies, args.query, stopwords,index)

            print(f"Searching for: {args.query}")
            for i, movie in enumerate(results, start=1):
                print(f"{i}. {movie}")

        case "build":
            """"""
            build_command(
                MOVIES_PATH,
                STOPWORDS_PATH,
                INDEX_PATH,
                DOCMAP_PATH,
                TF_PATH,
            )

        case "tf":
            """"""
            stopwords = load_stopwords(STOPWORDS_PATH)

            index=InvertedIndex(stopwords,INDEX_PATH,DOCMAP_PATH,TF_PATH)
            index.load()

            term=tokenize_term(args.term,stopwords)
            if term =="":
                print(0)
            print(index.get_tf(args.doc_id,term))

        case "idf":
            """"""
            stopwords = load_stopwords(STOPWORDS_PATH)

            index=InvertedIndex(stopwords,INDEX_PATH,DOCMAP_PATH,TF_PATH)
            index.load()
            term=tokenize_term(args.term,stopwords)
            idf=index.get_idf(term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")

        case "tf-idf":
            """"""
            stopwords = load_stopwords(STOPWORDS_PATH)

            index=InvertedIndex(stopwords,INDEX_PATH,DOCMAP_PATH,TF_PATH)
            index.load()

            term=tokenize_term(args.term,stopwords)
            if term =="":
                print(0)
            tf_idf=index.get_tf_idf(args.doc_id,term)
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}")




        case _:
            parser.print_help()


if __name__ == "__main__":
    main()