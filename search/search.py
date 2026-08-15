from .processing import process_tokens
from .index import InvertedIndex




def search(
    data: dict,
    query: str,
    stopwords: list[str],
    index:InvertedIndex
) -> list[str]:
    """Search movie titles containing the given query and return up to 5 results."""

    query_tokens = process_tokens(query, stopwords)

    if not query_tokens:
        return []
    
    results=[]
    seen=set()

    for token in query_tokens:
        ids=index.get_documents(token)
        for id in ids:
            if id in seen:
                continue
            seen.add(id)
            movie=index.docmap[id]
            results.append(f"{movie['title']} ({id})")


    return results[:10]