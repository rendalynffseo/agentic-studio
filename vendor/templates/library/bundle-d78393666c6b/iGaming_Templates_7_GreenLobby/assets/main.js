// Mobile menu toggle + app strip close.
(function () {
  var menu = document.getElementById('menu'), btn = document.querySelector('.menu-toggle');
  if (menu && btn) btn.addEventListener('click', function () { btn.setAttribute('aria-expanded', menu.classList.toggle('open')); });
  var strip = document.getElementById('app-strip');
  if (strip) strip.querySelector('.app-x').addEventListener('click', function () { strip.classList.add('hide'); });
})();

// Game board: category tabs (Hot = badge "hot"), search, lucky pick. Without JS every tile stays visible.
(function () {
  document.querySelectorAll('.board').forEach(function (board) {
    var tiles = [].slice.call(board.querySelectorAll('.tile')), filter = 'all', q = '';
    var empty = board.querySelector('.no-match'), input = board.querySelector('[data-search]');
    function apply() {
      var shown = 0;
      tiles.forEach(function (t) {
        var okTab = filter === 'all' || (filter === 'hot' ? t.dataset.hot === '1' : t.dataset.tab === filter);
        var ok = okTab && (!q || t.dataset.name.indexOf(q) > -1);
        t.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    }
    board.querySelectorAll('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        board.querySelectorAll('[data-filter]').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on'); filter = b.dataset.filter; apply();
      });
    });
    if (input) input.addEventListener('input', function () { q = input.value.trim().toLowerCase(); apply(); });
  });
  var lucky = document.querySelector('[data-lucky]');
  if (lucky) lucky.addEventListener('click', function () {
    var tiles = document.querySelectorAll('#lobby .tile'), out = document.querySelector('.lucky-out');
    if (!tiles.length || !out) return;
    var pick = tiles[Math.floor(Math.random() * tiles.length)];
    out.textContent = pick.querySelector('.meta b').textContent;
    pick.scrollIntoView({ behavior: 'smooth', block: 'center' });
    pick.classList.add('flash'); setTimeout(function () { pick.classList.remove('flash'); }, 1600);
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
