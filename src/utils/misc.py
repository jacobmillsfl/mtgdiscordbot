import re
from .emojis import Emojis


def card_match(content: str) -> list:
    card_search_pattern = r"\[\[(.*?)\]\]"
    return re.findall(card_search_pattern, content)
