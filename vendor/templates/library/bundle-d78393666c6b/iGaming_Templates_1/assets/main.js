(function () {
  var root = document.documentElement;

  // Language: Bahasa Melayu by default, English when chosen (?lang=en or toggle)
  function getStored() { try { return localStorage.getItem('lang'); } catch (e) { return null; } }
  function setStored(v) { try { localStorage.setItem('lang', v); } catch (e) {} }
  function applyLang(lang) {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang === 'en' ? 'en' : 'ms');
  }
  var q = new URLSearchParams(location.search).get('lang');
  applyLang(q === 'en' || q === 'ms' ? q : (getStored() || 'ms'));
  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () {
      var l = b.getAttribute('data-set-lang');
      applyLang(l); setStored(l);
    });
  });

  // Popup banner: show shortly after load, then again 30s after each close
  var popup = document.getElementById('promo-popup');
  if (popup) {
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
  }
})();
