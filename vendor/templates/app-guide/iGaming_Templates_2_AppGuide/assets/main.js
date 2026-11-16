// Mobile menu toggle; closes when a link is tapped.
(function () {
  var menu = document.getElementById('menu'), btn = document.querySelector('.menu-toggle');
  if (!menu || !btn) return;
  btn.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
  menu.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') { menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  });
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
