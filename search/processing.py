from nltk.stem import PorterStemmer
import string
STEMMER = PorterStemmer()

########
#    query text ->normalize(strip lower punuctuation) -> tokenize -(list)-> removestopwords -> stem
# #

def normalize_text(text: str) -> str:
    """Remove punctuation, whitespace, and lower-case the text."""
    translation_table = str.maketrans("", "", string.punctuation)
    text = text.strip().lower()
    return text.translate(translation_table)


def _tokenize(text: str) -> list[str]:
    """Normalize text and split it into tokens."""
    return text.split()



def remove_stopwords(
    tokens: list[str],
    stopwords: list[str],
) -> list[str]:
    """Remove stopwords from a list of tokens."""
    return [token for token in tokens if token not in stopwords]


def _stem_tokens(tokens: list[str]) -> list[str]:
    """Stem a list of tokens using the Porter stemmer."""
    return [STEMMER.stem(token) for token in tokens]


def process_tokens(text: str, stopwords: list[str]) -> list[str]:
    """Tokenize, clean, drop stopwords, and stem text."""
    query_tokens = _tokenize(normalize_text(text))
    query_tokens = remove_stopwords(query_tokens, stopwords)
    return _stem_tokens(query_tokens)


def tokenize_term(text: str, stopwords: list[str]) -> str:
    """Tokenize a term and require exactly one resulting token."""
    tokens = process_tokens(text, stopwords)

    if len(tokens) != 1:
        raise ValueError("Term must tokenize to exactly one token")

    return tokens[0]
