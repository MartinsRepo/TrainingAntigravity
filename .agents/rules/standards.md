---
trigger: always_on
description: Mandatory repository coding standards and testing conventions
---

# Repository Coding Standards

1. **Strict Type Hints**: Every function parameter and return type must have explicit Python type annotations.
2. **Google-Style Docstrings**: Every public function and class must include a comprehensive Google-style docstring (`Args:`, `Returns:`, `Raises:`).
3. **No Mutable Defaults**: Never use mutable default arguments (e.g. `def f(items=[])`).
4. **Automated Test Requirement**: Whenever a new module or utility is implemented, an accompanying `test_<module>.py` must be created and verified using `unittest`.
