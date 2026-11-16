// Progressive enhancement only: every page works without this file.
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('menu-utama');
  if (toggle && nav) {
    const set = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    };
    toggle.addEventListener('click', () => set(toggle.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { set(false); toggle.focus(); }
    });
  }

  // Pop-up banner: shown once per browser session, after a short delay.
  const popup = document.querySelector('[data-popup]');
  if (popup) {
    let seen = false;
    try { seen = sessionStorage.getItem('eu9-popup') === '1'; } catch { /* storage blocked */ }
    let last = null;
    const repeat = Number(popup.dataset.repeat) || 0;
    const show = () => {
      last = document.activeElement;
      popup.hidden = false;
      popup.querySelector('.popup__close').focus();
      document.addEventListener('keydown', onKey);
      try { sessionStorage.setItem('eu9-popup', '1'); } catch { /* storage blocked */ }
    };
    const close = () => {
      popup.hidden = true;
      document.removeEventListener('keydown', onKey);
      if (last) last.focus();
      if (repeat) setTimeout(show, repeat * 1000);
    };
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    popup.querySelectorAll('[data-popup-close]').forEach((el) => el.addEventListener('click', close));
    if (!seen || repeat) setTimeout(show, 2500);
  }

  // Blog search and cluster filter. Filtering happens in the page; no search URLs are created.
  const filters = document.querySelector('[data-filters]');
  if (filters) {
    filters.hidden = false;
    const input = filters.querySelector('#cari');
    const chips = [...filters.querySelectorAll('.chip')];
    const cards = [...document.querySelectorAll('.card[data-search]')];
    const count = filters.querySelector('[data-count]');
    const empty = document.querySelector('[data-empty]');
    let cluster = '';
    const apply = () => {
      const terms = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let shown = 0;
      for (const c of cards) {
        const ok = (!cluster || c.dataset.cluster === cluster) && terms.every((t) => c.dataset.search.includes(t));
        c.hidden = !ok;
        if (ok) shown++;
      }
      count.textContent = `${shown} daripada ${cards.length} artikel dipaparkan`;
      empty.hidden = shown > 0;
    };
    input.addEventListener('input', apply);
    chips.forEach((chip) => chip.addEventListener('click', () => {
      cluster = chip.dataset.filter;
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
      apply();
    }));
    apply();
  }
});
