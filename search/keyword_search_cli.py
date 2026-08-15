import argparse

from .config import MOVIES_PATH,STOPWORDS_PATH,INDEX_PATH,DOCMAP_PATH
from .data_loader import load_file,load_stopwords
from .search import search
from .index import build_command,InvertedIndex


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search Command Parser
    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    # Build Command Parser
    subparsers.add_parser("build", help="Create and build an inverted index")

    args = parser.parse_args()

    match args.command:
        case "search":
            movies = load_file(MOVIES_PATH)
            stopwords = load_stopwords(STOPWORDS_PATH)

            index=InvertedIndex(stopwords,INDEX_PATH,DOCMAP_PATH)
            index.load()


            results = search(movies, args.query, stopwords)

            print(f"Searching for: {args.query}")
            for i, movie in enumerate(results, start=1):
                print(f"{i}. {movie}")

        case "build":
            """"""
            build_command(MOVIES_PATH, STOPWORDS_PATH)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()