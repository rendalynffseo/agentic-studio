// Mobile menu toggle.
(function () {
  var menu = document.getElementById('menu'), btn = document.querySelector('.menu-toggle');
  if (!menu || !btn) return;
  btn.addEventListener('click', function () { btn.setAttribute('aria-expanded', menu.classList.toggle('open')); });
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

// Promo carousel: arrows, dots, auto-advance every 5 s (paused on hover / reduced motion).
(function () {
  document.querySelectorAll('[data-carousel]').forEach(function (c) {
    var track = c.querySelector('.slides'), dots = c.querySelectorAll('.dots button'), n = dots.length, i = 0, t;
    if (!n) return;
    function go(k) { i = (k + n) % n; track.scrollTo({ left: track.clientWidth * i, behavior: 'smooth' }); mark(); }
    function mark() { dots.forEach(function (d, j) { d.classList.toggle('on', j === i); }); }
    function auto() { clearInterval(t); if (!matchMedia('(prefers-reduced-motion: reduce)').matches) t = setInterval(function () { go(i + 1); }, 5000); }
    c.querySelector('.prev').addEventListener('click', function () { go(i - 1); auto(); });
    c.querySelector('.next').addEventListener('click', function () { go(i + 1); auto(); });
    dots.forEach(function (d, j) { d.addEventListener('click', function () { go(j); auto(); }); });
    track.addEventListener('scroll', function () { var k = Math.round(track.scrollLeft / track.clientWidth); if (k !== i) { i = k; mark(); } }, { passive: true });
    c.addEventListener('mouseenter', function () { clearInterval(t); });
    c.addEventListener('mouseleave', auto);
    mark(); auto();
  });
})();
