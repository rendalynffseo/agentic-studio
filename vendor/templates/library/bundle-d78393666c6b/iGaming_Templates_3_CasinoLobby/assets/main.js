// Sidebar drawer (mobile) + game-row arrow scrolling.
(function () {
  var body = document.body;
  function setNav(open) {
    body.classList.toggle('nav-open', open);
    document.querySelectorAll('[data-nav]').forEach(function (b) { b.setAttribute('aria-expanded', open); });
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-nav], .scrim, .side-close, .sidebar a, [data-scroll]');
    if (!t) return;
    if (t.matches('[data-nav]')) return setNav(!body.classList.contains('nav-open'));
    if (t.matches('[data-scroll]')) {
      var track = t.closest('.row').querySelector('.row-track');
      track.scrollBy({ left: track.clientWidth * 0.9 * (+t.dataset.scroll), behavior: 'smooth' });
      return;
    }
    setNav(false);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
})();

// Popup: show shortly after load, then again 30 s after every close.
(function () {
  var popup = document.getElementById('promo-popup');
  if (!popup) return;
  var REOPEN_MS = 30000, timer;
  function open() { popup.classList.add('open'); }
  function close() {
    if (!popup.classList.contains('open')) return;
    popup.classList.remove('open');
    clearTimeout(timer);
    timer = setTimeout(open, REOPEN_MS);
  }
  timer = setTimeout(open, 1500);
  popup.addEventListener('click', function (e) { if (e.target === popup) close(); });
  popup.querySelector('.popup-close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
