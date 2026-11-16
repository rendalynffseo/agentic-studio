// Mobile menu toggle.
(function () {
  var menu = document.getElementById('menu'), btn = document.querySelector('.menu-toggle');
  if (!menu || !btn) return;
  btn.addEventListener('click', function () { btn.setAttribute('aria-expanded', menu.classList.toggle('open')); });
})();

// Popup (9:16): first opens 1.2 s after the visitor's first interaction (or after 20 s), then 30 s after every close.
// The image is requested only when the popup opens, so it never competes with LCP and causes no layout shift.
(function () {
  var popup = document.getElementById('promo-popup');
  if (!popup) return;
  var REOPEN_MS = 30000, timer, started = false, evs = ['scroll', 'pointerdown', 'keydown', 'touchstart'];
  function open() {
    var im = popup.querySelector('img[data-src]');
    if (im) { im.src = im.getAttribute('data-src'); im.removeAttribute('data-src'); }
    popup.classList.add('open');
  }
  function close() {
    if (!popup.classList.contains('open')) return;
    popup.classList.remove('open');
    clearTimeout(timer);
    timer = setTimeout(open, REOPEN_MS);
  }
  function start() {
    if (started) return;
    started = true;
    evs.forEach(function (x) { removeEventListener(x, start, { passive: true }); });
    clearTimeout(timer);
    timer = setTimeout(open, 1200);
  }
  evs.forEach(function (x) { addEventListener(x, start, { passive: true }); });
  timer = setTimeout(function () { started = true; open(); }, 20000);
  popup.addEventListener('click', function (e) { if (e.target === popup) close(); });
  popup.querySelector('.popup-close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
