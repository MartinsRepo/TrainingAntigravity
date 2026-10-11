# Module 03: Lab Results & Output Documentation

This document records the creation of custom repository guardrails in **`.agents/rules/standards.md`** and the automated compliance test executed during **Module 03: Custom Rules & Guardrails**.

---

## 📌 Exercise 3.1: Defining Repository Rules

### Created Rule File: `.agents/rules/standards.md`
```markdown
---
trigger: always_on
description: Mandatory repository coding standards and testing conventions
---

# Repository Coding Standards

1. **Strict Type Hints**: Every function parameter and return type must have explicit Python type annotations.
2. **Google-Style Docstrings**: Every public function and class must include a comprehensive Google-style docstring (`Args:`, `Returns:`, `Raises:`).
3. **No Mutable Defaults**: Never use mutable default arguments (e.g. `def f(items=[])`).
4. **Automated Test Requirement**: Whenever a new module or utility is implemented, an accompanying `test_<module>.py` must be created and verified using `unittest`.
```

* **Git Commit:** `0597a28` (`feat(rules): add repository coding standards in .agents/rules/standards.md`)

---

## 📌 Exercise 3.2: Rule Compliance Verification Challenge

### The Test Prompt (Intentionally Minimal)
```text
Write a text utility in modules/03-custom-rules/lab/text_utils.py that truncates strings with an ellipsis and generates URL slugs from titles.
```
> Notice that the prompt contains **no mention** of type hints, docstrings, formatting, or unit tests.

### Compliance Evaluation Matrix
| Rule Mandate from `.agents/rules/standards.md` | Observation in Generated Code | Status |
| :--- | :--- | :---: |
| **1. Strict Type Hints** | `truncate(text: str, max_length: int, suffix: str = "...") -> str`<br/>`slugify(title: str, separator: str = "-", allow_unicode: bool = False) -> str` | ✅ Pass |
| **2. Google-Style Docstrings** | Both functions feature complete docstrings detailing `Args:`, `Returns:`, and `Raises:` sections. | ✅ Pass |
| **3. No Mutable Defaults** | Default parameters only use immutable values (`"..."`, `"-"`, `False`). | ✅ Pass |
| **4. Accompanying Unit Tests** | Automatically created `test_text_utils.py` covering all edge cases, exceptions, and boundaries. | ✅ Pass |

---

## 📌 Test Execution Output

Command executed:
```bash
python3 -m unittest modules/03-custom-rules/lab/test_text_utils.py -v
```

Output:
```text
test_accented_characters_ascii (modules.03-custom-rules.lab.test_text_utils.TestSlugify.test_accented_characters_ascii)
Verify ASCII conversion for accented letters. ... ok
test_basic_slug (modules.03-custom-rules.lab.test_text_utils.TestSlugify.test_basic_slug)
Verify basic title conversion to slug. ... ok
test_custom_separator (modules.03-custom-rules.lab.test_text_utils.TestSlugify.test_custom_separator)
Verify custom separator. ... ok
test_invalid_separator (modules.03-custom-rules.lab.test_text_utils.TestSlugify.test_invalid_separator)
Verify ValueError when separator is invalid. ... ok
test_special_characters_and_whitespace (modules.03-custom-rules.lab.test_text_utils.TestSlugify.test_special_characters_and_whitespace)
Verify punctuation removal and whitespace collapsing. ... ok
test_custom_suffix (modules.03-custom-rules.lab.test_text_utils.TestTruncate.test_custom_suffix)
Verify custom suffix truncation. ... ok
test_exact_length (modules.03-custom-rules.lab.test_text_utils.TestTruncate.test_exact_length)
Verify behavior when text length exactly equals max_length. ... ok
test_invalid_max_length (modules.03-custom-rules.lab.test_text_utils.TestTruncate.test_invalid_max_length)
Verify ValueError when max_length is <= 0. ... ok
test_short_string_unaltered (modules.03-custom-rules.lab.test_text_utils.TestTruncate.test_short_string_unaltered)
Verify that strings within max_length are untouched. ... ok
test_suffix_longer_than_max_length (modules.03-custom-rules.lab.test_text_utils.TestTruncate.test_suffix_longer_than_max_length)
Verify ValueError when suffix length exceeds max_length. ... ok
test_truncation_with_suffix (modules.03-custom-rules.lab.test_text_utils.TestTruncate.test_truncation_with_suffix)
Verify truncation respects max_length including suffix. ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.001s

OK (100% Pass Rate)
```

---

## 🧠 Key Takeaways from Module 03

1. **Persistent Context vs. Repetitive Prompting:** By codifying standards in `.agents/rules/`, you never have to remind the agent about formatting, types, or tests again.
2. **Deterministic Quality:** The agent treats rules as high-priority behavioral constraints rather than optional suggestions.
3. **Team Sharing via VCS:** Because rules live inside `.agents/rules/` within the repository, every developer and agent on the team operates under the exact same standard.
