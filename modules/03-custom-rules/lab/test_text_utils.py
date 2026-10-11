"""Unit tests for text_utils adhering to repository coding standards."""

import unittest
from pathlib import Path
import sys

# Ensure module is loadable
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from text_utils import truncate, slugify


class TestTruncate(unittest.TestCase):
    """Test suite for truncate function."""

    def test_short_string_unaltered(self) -> None:
        """Verify that strings within max_length are untouched."""
        result = truncate("Hello", 10)
        self.assertEqual(result, "Hello")

    def test_exact_length(self) -> None:
        """Verify behavior when text length exactly equals max_length."""
        result = truncate("Hello", 5)
        self.assertEqual(result, "Hello")

    def test_truncation_with_suffix(self) -> None:
        """Verify truncation respects max_length including suffix."""
        result = truncate("Hello World!", 8, suffix="...")
        self.assertEqual(result, "Hello...")
        self.assertEqual(len(result), 8)

    def test_custom_suffix(self) -> None:
        """Verify custom suffix truncation."""
        result = truncate("Long description here", 10, suffix="~")
        self.assertEqual(result, "Long desc~")
        self.assertEqual(len(result), 10)

    def test_invalid_max_length(self) -> None:
        """Verify ValueError when max_length is <= 0."""
        with self.assertRaises(ValueError):
            truncate("Hello", 0)

    def test_suffix_longer_than_max_length(self) -> None:
        """Verify ValueError when suffix length exceeds max_length."""
        with self.assertRaises(ValueError):
            truncate("Hello", 2, suffix="...")


class TestSlugify(unittest.TestCase):
    """Test suite for slugify function."""

    def test_basic_slug(self) -> None:
        """Verify basic title conversion to slug."""
        result = slugify("Antigravity Agent Mastery")
        self.assertEqual(result, "antigravity-agent-mastery")

    def test_special_characters_and_whitespace(self) -> None:
        """Verify punctuation removal and whitespace collapsing."""
        result = slugify("Hello, World! -- Welcome 2026")
        self.assertEqual(result, "hello-world-welcome-2026")

    def test_custom_separator(self) -> None:
        """Verify custom separator."""
        result = slugify("Custom Separator Test", separator="_")
        self.assertEqual(result, "custom_separator_test")

    def test_accented_characters_ascii(self) -> None:
        """Verify ASCII conversion for accented letters."""
        result = slugify("Café & Crème Brûlée")
        self.assertEqual(result, "cafe-creme-brulee")

    def test_invalid_separator(self) -> None:
        """Verify ValueError when separator is invalid."""
        with self.assertRaises(ValueError):
            slugify("Title", separator="")
        with self.assertRaises(ValueError):
            slugify("Title", separator="   ")


if __name__ == "__main__":
    unittest.main()
