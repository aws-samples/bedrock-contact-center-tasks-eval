from typing import cast
from pathlib import Path
from tokenizers import Tokenizer

_tokenizer: Tokenizer = None

# file location for tokenizer.json
TOKENIZER_PATH = Path("./tokenizer.json")

def count_tokens(text: str) -> int:
    """Return the number of tokens in the input text.

    Args:
        text (str): The input text.

    Returns:
        count (int): The number of tokens in the input text
    """
    global _tokenizer

    if _tokenizer is None:
        tokenizer_path = TOKENIZER_PATH
        tokenizer_text = tokenizer_path.read_text(encoding="utf-8")
        _tokenizer = cast(Tokenizer, Tokenizer.from_str(tokenizer_text))

    encoded_text = _tokenizer.encode(text)
    count = len(encoded_text.ids)
    return count

