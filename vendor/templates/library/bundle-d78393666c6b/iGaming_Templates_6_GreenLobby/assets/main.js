// Mobile menu, game tabs, GMT+8 clock, dismissible app strip.
(function () {
  var menu = document.getElementById('menu'), btn = document.querySelector('.menu-toggle');
  if (menu && btn) btn.addEventListener('click', function () { btn.setAttribute('aria-expanded', menu.classList.toggle('open')); });

  document.querySelectorAll('.tab').forEach(function (t) {
    t.addEventListener('click', function () {
      var box = t.closest('.tabs-box');
      box.querySelectorAll('.tab').forEach(function (x) { x.classList.toggle('on', x === t); x.setAttribute('aria-selected', x === t); });
      box.querySelectorAll('.panel').forEach(function (p) { p.classList.toggle('on', p.dataset.panel === t.dataset.tab); });
    });
  });

  var clock = document.querySelector('[data-clock]');
  function tick() {
    var d = new Date(Date.now() + 8 * 3600e3), p = function (n) { return ('0' + n).slice(-2); };
    clock.textContent = p(d.getUTCDate()) + '/' + p(d.getUTCMonth() + 1) + '/' + d.getUTCFullYear() + ' ' + p(d.getUTCHours()) + ':' + p(d.getUTCMinutes()) + ':' + p(d.getUTCSeconds()) + ' (GMT+8)';
  }
  if (clock) { tick(); setInterval(tick, 1000); }

  var strip = document.getElementById('app-strip');
  try { if (strip && sessionStorage.getItem('appStrip') === '0') strip.remove(); } catch (e) {}
  var x = document.querySelector('.app-strip-x');
  if (x) x.addEventListener('click', function () { strip.remove(); try { sessionStorage.setItem('appStrip', '0'); } catch (e) {} });
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
