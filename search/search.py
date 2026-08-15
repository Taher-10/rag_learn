from .processing import process_tokens

def _token_matches(query_tokens: list[str], title: str,stopwords: list[str],) -> bool:
    """Check whether any query token matches a token in the movie title."""
    title_tokens = process_tokens(title, stopwords)

    return any(
        query_token in title_token
        for query_token in query_tokens
        for title_token in title_tokens
    )


def search(
    data: dict,
    query: str,
    stopwords: list[str],
) -> list[str]:
    """Search movie titles containing the given query and return up to 5 results."""

    query_tokens = process_tokens(query, stopwords)

    if not query_tokens:
        return []

    results = [
        movie["title"]
        for movie in data["movies"]
        if _token_matches(query_tokens, movie["title"],stopwords)
    ]

    return results[:5]