"""Text manipulation utilities adhering to repository coding standards."""

import re
import unicodedata


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncates a text string to a maximum length and appends a suffix.

    If the text length is less than or equal to max_length, the original text
    is returned unaltered. If truncation occurs, the returned string (including
    suffix) will not exceed max_length.

    Args:
        text: The input string to truncate.
        max_length: The maximum allowable length of the returned string.
        suffix: The string appended when truncation occurs. Defaults to '...'.

    Returns:
        The truncated string ending with the suffix, or original text if short enough.

    Raises:
        ValueError: If max_length is less than or equal to 0, or if the suffix
            length exceeds max_length.
    """
    if max_length <= 0:
        raise ValueError(f"max_length must be greater than 0, got {max_length}.")

    if len(suffix) > max_length:
        raise ValueError(
            f"Suffix length ({len(suffix)}) cannot exceed max_length ({max_length})."
        )

    if len(text) <= max_length:
        return text

    cutoff = max_length - len(suffix)
    return text[:cutoff] + suffix


def slugify(title: str, separator: str = "-", allow_unicode: bool = False) -> str:
    """Converts a title string into a clean, URL-safe slug.

    Normalizes characters, converts whitespace to separators, removes special
    characters and punctuation, and collapses duplicate separators.

    Args:
        title: The input string to convert into a URL slug.
        separator: The string used to join words. Defaults to '-'.
        allow_unicode: Whether to preserve Unicode characters. If False,
            converts characters to standard ASCII equivalents. Defaults to False.

    Returns:
        A lowercased, URL-safe slug string.

    Raises:
        ValueError: If separator is empty or contains whitespace characters.
    """
    if not separator or separator.isspace():
        raise ValueError("Separator must be a non-empty, non-whitespace string.")

    # Normalize Unicode characters
    if allow_unicode:
        cleaned = unicodedata.normalize("NFKC", title)
    else:
        cleaned = (
            unicodedata.normalize("NFKD", title)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    cleaned = cleaned.lower()

    # Replace all non-alphanumeric characters with the separator
    if allow_unicode:
        cleaned = re.sub(r"[^\w\s-]", "", cleaned, flags=re.UNICODE)
    else:
        cleaned = re.sub(r"[^a-z0-9\s-]", "", cleaned)

    # Collapse consecutive whitespace and separators
    escaped_sep = re.escape(separator)
    cleaned = re.sub(r"[\s" + escaped_sep + r"]+", separator, cleaned)

    # Strip leading/trailing separators
    return cleaned.strip(separator)
