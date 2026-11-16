"""Developer-added home page sections (the 'more added by new developer' slot).

Everything here is optional. Leave the strings empty to keep the standard layout.
Write plain HTML. For bilingual text use:
    <span class="ms">Teks BM</span><span class="en">English text</span>
Tokens __BRAND__, __SLUG__, __MIN_DEPOSIT__, __MIN_WITHDRAW__ are replaced at build time.
Link CTAs to the register URL with rel="nofollow sponsored". Give every <img> an alt and width/height.
"""

# Inserted right after the hero section (above the slot showcase).
AFTER_HERO = ""

# Inserted just before the home FAQ section.
BEFORE_FAQ = ""

# Extra CSS appended after the main stylesheet (inlined, so keep it small).
EXTRA_CSS = ""

# Example (copy into AFTER_HERO to try it):
# AFTER_HERO = '''
# <section id="promo"><div class="wrap">
# <h2><span class="ms">Promosi Minggu Ini</span><span class="en">This Week's Promotion</span></h2>
# <div class="showcase single"><img src="/images/promo-1.webp" alt="Promosi __BRAND__ / __BRAND__ promotion" width="800" height="300" loading="lazy"></div>
# </div></section>
# '''
