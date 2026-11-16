"""Developer-added home page blocks (the per-site "extra content" slot).

Everything here is optional. Leave a value "" to keep the standard layout.
Each value is either one HTML string (used for every language) or a dict per language:
    AFTER_HERO = {"en": "<section>...</section>", "ms": "...", "zh": "..."}
Tokens __BRAND__, __SITE__, __SLUG__ are replaced at build time.
Link CTAs to the register URL with rel="nofollow sponsored noopener". Give every <img> alt, width, height, loading="lazy".
Reuse existing classes: .section .kicker .cards .card .callout .tbl .widget .btn .btn-gold
"""

# Full-width block between the hero and the main content (e.g. a promo strip).
AFTER_HERO = ""

# Block inside the main column, just before the FAQ (wrap it in <section class="section">).
BEFORE_FAQ = ""

# Extra sidebar widget(s), above the 18+ widget (wrap each in <div class="widget">).
SIDEBAR = ""

# Extra CSS appended to the inlined stylesheet (keep it small).
EXTRA_CSS = ""

# Example:
# BEFORE_FAQ = {
#     "en": '<section id="promo" class="section"><span class="kicker">Promotion</span><h2>This week at __BRAND__</h2>'
#           '<div class="callout"><h3>Check the terms</h3><p>Always read wagering rules on the official page.</p></div></section>',
# }
