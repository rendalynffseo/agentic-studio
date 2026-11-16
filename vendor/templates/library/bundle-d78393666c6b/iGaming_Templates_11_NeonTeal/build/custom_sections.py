"""Developer-added home page blocks (optional). "" keeps the standard layout.
Each value is one HTML string (all languages) or a dict per language: {"ms": "...", "en": "..."}.
Tokens __BRAND__ __SLUG__ are replaced at build time. Register CTAs need rel="nofollow sponsored noopener".
Reuse classes: .block .head .game-grid .promos .promo .tbl .btn .btn-fill .btn-line. Images must be square.
"""

# Below the 4 feature cards, above the "about" split section.
AFTER_HERO = ""

# Above the home FAQ.
BEFORE_FAQ = ""

# Extra CSS appended to the inlined stylesheet (keep it small).
EXTRA_CSS = ""


def per_lang(value, lang):
    return value.get(lang, "") if isinstance(value, dict) else value
