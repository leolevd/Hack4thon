# Project: spam detector

## Goal

Being able to detect spam in most situations.

**Main file:** `spam_filter.py`
**Usage:**
Mainly intended for `import` — when imported, it automatically runs a few tests to make sure all filters work properly.

---

## Example

```python
from spam_filter import (
    zero_width_cleaner,
    collection_filter,
    susWords_filter,
    CAPS_check,
    zero_width_analyser,
    spam_filter
)

zero_width_cleaner("Hel\u00a3lo")
# Output: 'Hello'
# Cleans zero-width or invisible characters from the message.

collection_filter("You won a free car!")
# Output: 'SPAM'
# Uses word frequency dictionaries to detect spam.

susWords_filter("You won $100!")
# Output: 'SPAM'
# Simple keyword-based filter for very suspicious words.

CAPS_check("WOW!!!! YOU WON A CAR!")
# Output: 'SPAM'
# Detects messages with excessive uppercase usage.

zero_width_analyser("Hel\u00a3lo")
# Output: 'SPAM'
# Flags messages containing zero-width characters.

spam_filter("You won a car! Call us: +74 5389 45983")
# Output: 'SPAM'
# Combines all four filters for final classification.
```
