// Static site generator for eu9slots.com.
//   dist/     published pages only. Indexable only when SITE_ENV=production.
//   preview/  published + draft articles, always noindex. Never deploy to production.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import config from '../src/config.js';
import { RELATIONSHIP } from '../src/relationship.js';
import { ARTICLES, CLUSTERS, HUBS, SOURCES } from '../src/inventory.js';
import { PAGES } from '../src/pages.js';
import { existsSync } from 'node:fs';
import { GAME_GROUPS, GAME_SHOTS_DATE } from '../src/games.js';
import { GALLERY } from '../src/gallery.js';

const ROOT = path.resolve('.');
const hasImg = (f) => existsSync(path.join(ROOT, 'src/img', f));
const LOGO = hasImg('logo.png');
const HERO_BANNER = hasImg('hero-banner-1526.webp');
const galleryLink = (html) => (GALLERY.length ? html : '');
const PROD = process.env.SITE_ENV === 'production';
const REL = RELATIONSHIP[config.relationship];
if (!REL) throw new Error(`Unknown relationship "${config.relationship}"`);

const NAV = [
  { href: '/', label: 'Utama' },
  { href: '/panduan/', label: 'Panduan' },
  { href: '/permainan-slot/', label: 'Permainan Slot' },
  { href: '/bonus-syarat-cuci/', label: 'Bonus & Syarat Cuci' },
  { href: '/bantuan/', label: 'Bantuan' },
  { href: '/blog/', label: 'Blog' },
];

const MONTHS = ['Januari', 'Februari', 'Mac', 'April', 'Mei', 'Jun', 'Julai', 'Ogos', 'September', 'Oktober', 'November', 'Disember'];
const fmtDate = (iso) => { const [y, m, d] = iso.split('-').map(Number); return `${d} ${MONTHS[m - 1]} ${y}`; };
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const abs = (p) => config.domain + p;
const urlOf = (a) => `${HUBS[CLUSTERS[a.cluster].hub].path}${a.slug}/`;
const byN = new Map(ARTICLES.map((a) => [a.n, a]));
const slugify = (s) => s.toLowerCase().replace(/<[^>]+>/g, '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .replace(/&[a-z]+;/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

for (const a of ARTICLES) {
  a.published = a.published || config.launchDate;
  a.updated = a.updated || a.published;
}

// ---------------------------------------------------------------- build state
function makeSite(includeDrafts) {
  const isLive = (a) => a.status === 'published' || includeDrafts;
  const pagePaths = new Set(['/', '/blog/', ...Object.values(HUBS).map((h) => h.path), ...PAGES.map((p) => p.path)]);
  for (const a of ARTICLES) if (isLive(a)) pagePaths.add(urlOf(a));
  return { includeDrafts, isLive, pagePaths, warnings: [], files: new Map() };
}

// Resolve [[N|text]] and [[/path/|text]] tokens.
function resolveLinks(html, site, from) {
  return html.replace(/\[\[([^|\]]+)\|([^\]]+)\]\]/g, (_, target, text) => {
    if (/^\d+$/.test(target)) {
      const a = byN.get(Number(target));
      if (!a) { site.warnings.push(`${from}: unknown article ${target}`); return text; }
      if (!site.isLive(a)) return text; // never link to unpublished drafts
      const cls = a.status === 'draft' ? ' class="draft-link"' : '';
      return `<a href="${urlOf(a)}"${cls}>${text}</a>`;
    }
    const [p, hash] = target.split('#');
    if (!site.pagePaths.has(p)) site.warnings.push(`${from}: unknown page ${target}`);
    return `<a href="${p}${hash ? '#' + hash : ''}">${text}</a>`;
  });
}

function addHeadingIds(html) {
  const toc = []; const used = new Set();
  const out = html.replace(/<h([23])>([\s\S]*?)<\/h\1>/g, (_, lvl, inner) => {
    let id = slugify(inner) || 'bahagian'; let i = 2;
    while (used.has(id)) id = `${slugify(inner)}-${i++}`;
    used.add(id);
    if (lvl === '2') toc.push({ id, text: inner.replace(/<[^>]+>/g, '') });
    return `<h${lvl} id="${id}">${inner}</h${lvl}>`;
  });
  return { html: out, toc };
}

// ---------------------------------------------------------------- components
const img = ({ base, alt, w = 1200, h = 675, sizes = '(min-width: 960px) 360px, 100vw', eager = false }) =>
  `<img src="/img/${base}-1200.webp" srcset="/img/${base}-640.webp 640w, /img/${base}-1200.webp 1200w" sizes="${sizes}" width="${w}" height="${h}" alt="${esc(alt)}"${eager ? ' fetchpriority="high"' : ' loading="lazy" decoding="async"'}>`;

const thumbAlt = (a) => `Grafik abstrak merah dan emas untuk artikel ${a.card.toLowerCase()}`;

function card(a, { compact = false } = {}) {
  const c = CLUSTERS[a.cluster];
  const search = esc(`${a.title} ${a.desc} ${a.kw} ${c.name}`.toLowerCase());
  return `<article class="card${compact ? ' card--compact' : ''}" data-cluster="${a.cluster}" data-search="${search}">
  <a class="card__link" href="${urlOf(a)}">
    ${compact ? '' : `<div class="card__media">${img({ base: `artikel/${a.slug}`, alt: '' })}</div>`}
    <div class="card__body">
      <p class="kicker">${esc(c.name)}${a.status === 'draft' ? ' · <span class="badge-draft">DRAF</span>' : ''}</p>
      <h3 class="card__title">${esc(a.title)}</h3>
      ${compact ? '' : `<p class="card__desc">${esc(a.desc)}</p>`}
    </div>
  </a>
</article>`;
}

const cards = (list, opts) => `<div class="grid${opts?.compact ? ' grid--compact' : ''}">${list.map((a) => card(a, opts)).join('\n')}</div>`;

function breadcrumbs(items) {
  const html = `<nav class="breadcrumbs" aria-label="Laluan halaman"><ol>${items.map((it, i) =>
    i === items.length - 1 ? `<li><span aria-current="page">${esc(it.name)}</span></li>` : `<li><a href="${it.path}">${esc(it.name)}</a></li>`).join('')}</ol></nav>`;
  const ld = { '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({ '@type': 'ListItem', position: i + 1, name: it.name, item: abs(it.path) })) };
  return { html, ld };
}

// Referral CTA: label always names the real destination and marks it as a referral link.
const ctaButton = (extra = '') => config.cta
  ? `<a class="btn btn--primary btn--cta${extra}" href="${esc(config.cta.url)}" rel="sponsored nofollow noopener" target="_blank">Ke ${esc(config.cta.brand)} <span class="sr-note">(laman luar, pautan rujukan)</span></a>`
  : '';

const platformButton = () => config.platformUrl
  ? `<a class="btn btn--ghost" href="${esc(config.platformUrl)}" rel="nofollow noopener${config.relationship === 'affiliate' ? ' sponsored' : ''}" target="_blank">Ke platform EU9 <span class="sr-note">(laman luar: ${esc(new URL(config.platformUrl).hostname)})</span></a>`
  : '';

const ORG = {
  '@type': 'Organization', '@id': `${config.domain}/#organization`, name: config.publisherLegalName || config.name,
  url: config.domain + '/', email: config.email, logo: { '@type': 'ImageObject', url: abs('/img/apple-touch-icon.png'), width: 180, height: 180 },
};

function gameTiles(games) {
  return `<ul class="games">${games.map((g) => `<li><figure class="game"><img src="/img/permainan/${g.file}.webp" width="400" height="300" alt="Seni muka depan permainan ${esc(g.title)}" loading="lazy" decoding="async"><figcaption>${esc(g.title)}</figcaption></figure></li>`).join('')}</ul>`;
}

const GAME_NOTE = `<p class="games-note">Seni permainan dibekalkan oleh pemilik laman ini daripada tangkapan skrin lobi platform EU9 pada ${fmtDate(GAME_SHOTS_DATE)}. Senarai permainan boleh berubah. Seni permainan ialah hak cipta pembekal masing-masing. Ini bukan permainan yang boleh dimainkan.</p>`;

function gameGallery() {
  return `<section class="section" id="senarai-permainan" aria-labelledby="h-senarai">
  <div class="wrap">
    <div class="section__head">
      <p class="kicker">Lobi EU9</p>
      <h2 id="h-senarai">Permainan slot yang dipaparkan di EU9</h2>
      ${GAME_NOTE}
    </div>
    ${GAME_GROUPS.map((g) => `<div class="games-group"><h3>${esc(g.name)}</h3>${gameTiles(g.games)}</div>`).join('\n')}
    <p class="more">Sebelum mencuba mana-mana permainan, semak skrin maklumatnya: <a href="${urlOf(byN.get(5))}">cara membaca maklumat permainan</a>.</p>
    ${galleryLink('<p><a href="/galeri/">Lihat tangkapan skrin penuh lobi EU9, termasuk promosi</a></p>')}
  </div>
</section>`;
}

// Floating Login/Register bar + once-per-session pop-up. Without a URL the buttons are inert.
function accessUi() {
  if (!config.access?.show) return '';
  const u = config.access.url;
  const btn = (cls, ms, en) => u
    ? `<a class="btn ${cls}" href="${esc(u)}" rel="nofollow noopener" target="_blank">${ms} <span class="btn__en">${en}</span></a>`
    : `<span class="btn ${cls}" aria-disabled="true">${ms} <span class="btn__en">${en}</span></span>`;
  const pair = `${btn('btn--secondary', 'Log Masuk', 'Login')}${btn('btn--primary', 'Daftar', 'Register')}`;
  return `<div class="float-bar" role="region" aria-label="Log masuk dan daftar">${pair}</div>
<div class="popup" data-popup data-repeat="${config.access.repeatSeconds || 0}" hidden>
  <div class="popup__backdrop" data-popup-close></div>
  <div class="popup__card" role="dialog" aria-modal="true" aria-labelledby="popup-title">
    <button type="button" class="popup__close" data-popup-close aria-label="Tutup / Close">×</button>
    <h2 id="popup-title" class="sr-only">Promosi EU9</h2>
    <img src="/img/popup-banner.webp" width="584" height="778" alt="${esc(config.access.popupAlt || config.name)}" decoding="async">
    <div class="popup__actions">${pair}</div>
    <p class="popup__note"><span class="age">18+</span> Tertakluk pada terma EU9. <a href="${urlOf(byN.get(16))}">Baca terma bonus</a> sebelum menerima.</p>
  </div>
</div>`;
}

// ---------------------------------------------------------------- layout
let ASSET_V = '';
function layout(site, { path: p, title, desc, body, ld = [], ogImage = '/img/og/default.jpg', ogType = 'website', noindex = false, preload = '' }) {
  const robots = !PROD || site.includeDrafts || noindex ? 'noindex, nofollow' : 'index, follow, max-image-preview:large';
  const nav = NAV.map((n) => {
    const current = n.href === '/' ? p === '/' : p.startsWith(n.href);
    return `<li><a href="${n.href}"${current ? ' aria-current="page"' : ''}>${esc(n.label)}</a></li>`;
  }).join('');
  const ldTags = ld.map((x) => `<script type="application/ld+json">${JSON.stringify(x).replace(/</g, '\\u003c')}</script>`).join('\n');
  return `<!doctype html>
<html lang="${config.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="${robots}">
<link rel="canonical" href="${abs(p)}">
${config.gscVerification ? `<meta name="google-site-verification" content="${esc(config.gscVerification)}">\n` : ''}
<meta name="theme-color" content="#0C0C0C">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="${ogType}">
<meta property="og:site_name" content="${esc(config.name)}">
<meta property="og:locale" content="${config.locale}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${abs(p)}">
<meta property="og:image" content="${abs(ogImage)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
${preload}<link rel="stylesheet" href="/assets/site.css?v=${ASSET_V}">
<script src="/assets/site.js?v=${ASSET_V}"></script>
${ldTags}
</head>
<body>
<a class="skip" href="#kandungan">Langkau ke kandungan</a>
${site.includeDrafts ? '<div class="preview-bar" role="note">PRATONTON DALAMAN — termasuk draf yang belum diterbitkan. Jangan diterbitkan.</div>' : ''}
<header class="site-header">
  <div class="wrap header__inner">
    <a class="wordmark" href="/" aria-label="${esc(config.name)} — Utama">${LOGO ? `<img class="wordmark__logo" src="/img/logo.png" width="276" height="110" alt=""><span class="wordmark__text"><b>Slots</b> Malaysia</span>` : `<span class="wordmark__mark" aria-hidden="true">E9</span><span>EU9 <b>Slots</b> Malaysia</span>`}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu-utama"><span class="nav-toggle__bars" aria-hidden="true"></span><span class="nav-toggle__label">Menu</span></button>
    <nav id="menu-utama" class="site-nav" aria-label="Menu utama"><ul>${nav}</ul></nav>
    ${ctaButton(' btn--header')}
  </div>
</header>
<main id="kandungan">
${body}
</main>
${accessUi()}
<footer class="site-footer">
  <div class="wrap footer__grid">
    <div>
      <p class="wordmark wordmark--footer">${LOGO ? `<img class="wordmark__logo" src="/img/logo.png" width="276" height="110" alt="EU9" loading="lazy"><span class="wordmark__text"><b>Slots</b> Malaysia</span>` : `<span class="wordmark__mark" aria-hidden="true">E9</span><span>EU9 <b>Slots</b> Malaysia</span>`}</p>
      <p>${esc(REL.short)}</p>
      <p>Hubungi laman ini: <a href="mailto:${config.email}">${config.email}</a></p>
    </div>
    <nav aria-label="Panduan">
      <h2 class="footer__h">Panduan</h2>
      <ul>${NAV.slice(1).map((n) => `<li><a href="${n.href}">${esc(n.label)}</a></li>`).join('')}</ul>
    </nav>
    <nav aria-label="Maklumat laman">
      <h2 class="footer__h">Maklumat laman</h2>
      <ul>${PAGES.map((pg) => `<li><a href="${pg.path}">${esc(pg.nav)}</a></li>`).join('')}</ul>
    </nav>
  </div>
  <div class="wrap footer__legal">
    <p><span class="age">18+</span> Kandungan ini untuk pembaca dewasa sahaja. Perjudian melibatkan risiko kehilangan wang dan tertakluk kepada undang-undang di tempat anda. <a href="/permainan-bertanggungjawab/">Permainan bertanggungjawab</a>.</p>
    <p>© ${config.launchDate.slice(0, 4)} ${esc(config.name)}. Nama EU9 serta nama permainan dan pembekal ialah milik pemilik masing-masing.</p>
  </div>
</footer>
</body>
</html>
`;
}

// ---------------------------------------------------------------- pages
const live = (site, list) => list.filter(site.isLive);
const inCluster = (site, k) => live(site, ARTICLES.filter((a) => a.cluster === k));

function homePage(site) {
  const q = [
    [12, 'Apa maksud RTP 96% dalam ringgit?'],
    [7, 'Bagaimana membaca jadual bayaran?'],
    [17, 'Bagaimana syarat cuci dikira?'],
    [20, 'Kenapa bonus belum boleh dikeluarkan?'],
    [22, 'Tidak boleh login — apa yang perlu disemak?'],
    [24, 'Deposit belum masuk — rekod apa yang perlu disimpan?'],
    [27, 'Bagaimana mengenal laman tiruan?'],
    [29, 'Bagaimana menetapkan had wang dan masa?'],
  ].filter(([n]) => site.isLive(byN.get(n)));
  const latest = live(site, ARTICLES).slice().sort((a, b) => b.updated.localeCompare(a.updated) || b.n - a.n).slice(0, 6);
  const helpList = [...inCluster(site, 'E'), ...inCluster(site, 'F')];
  const section = (id, kicker, title, intro, inner, more) => `
<section class="section" aria-labelledby="${id}">
  <div class="wrap">
    <div class="section__head">
      <p class="kicker">${kicker}</p>
      <h2 id="${id}">${title}</h2>
      ${intro ? `<p class="lead">${intro}</p>` : ''}
    </div>
    ${inner}
    ${more ? `<p class="more"><a href="${more[0]}">${more[1]} <span aria-hidden="true">→</span></a></p>` : ''}
  </div>
</section>`;

  const body = `
<section class="hero${HERO_BANNER ? '' : ' hero--art'}" aria-labelledby="h1">
  ${HERO_BANNER ? `  <figure class="wrap hero__banner">
    <img src="/img/hero-banner-1526.webp" srcset="/img/hero-banner-800.webp 800w, /img/hero-banner-1526.webp 1526w" sizes="(min-width: 1200px) 1150px, 100vw" width="1526" height="610" alt="Sepanduk EU9 bersama LiveScore dan Sofascore, menampilkan duta jenama EU9 serta pemain bola sepak Cristiano Ronaldo dan Luka Modrić" fetchpriority="high">
    <figcaption>Sepanduk promosi EU9. Dakwaan dalam sepanduk ialah dakwaan EU9 sendiri. ${galleryLink('<a href="/galeri/">Lihat galeri lobi EU9</a>.')}</figcaption>
  </figure>` : `<picture class="hero__art">
    <source media="(max-width: 699px)" srcset="/img/hero-mobile-800.webp" width="800" height="900">
    <source media="(min-width: 700px)" srcset="/img/hero-1000.webp 1000w, /img/hero-1600.webp 1600w" sizes="100vw" width="1600" height="700">
    <img src="/img/hero-1600.webp" width="1600" height="700" alt="" fetchpriority="high">
  </picture>`}
  <div class="wrap hero__content">
    <p class="kicker">Panduan dalam Bahasa Melayu</p>
    <h1 id="h1">EU9 Slots Malaysia: Panduan Permainan dan Pengguna</h1>
    <p class="hero__lead">Terokai panduan slot EU9 dalam Bahasa Melayu, daripada peraturan permainan dan ciri bonus hingga syarat cuci serta bantuan akaun. Fahami maklumat penting sebelum membuat keputusan.</p>
    <div class="btn-row">
      <a class="btn btn--primary" href="/permainan-slot/">Terokai Panduan Slot</a>
      <a class="btn btn--secondary" href="/bantuan/">Cari Bantuan</a>
      ${platformButton()}
    </div>
${config.cta ? `<div class="cta-box"><p>${ctaButton()}</p><p class="cta-box__note">${esc(config.cta.brand)} ialah platform berasingan daripada EU9. Pautan rujukan — kami mungkin menerima komisen. 18+ sahaja. Tetapkan <a href="/permainan-bertanggungjawab/">had wang dan masa</a> sebelum bermain.</p></div>` : ''}
    <p class="hero__note">${esc(REL.short)} <a href="/pendedahan-afiliasi/">Baca pendedahan</a>.</p>
  </div>
</section>

${section('soalan', 'Soalan lazim pembaca', 'Mulakan dengan soalan anda', '', `<ul class="quick">${q.map(([n, t]) => `<li><a href="${urlOf(byN.get(n))}">${esc(t)}</a></li>`).join('')}</ul>`)}

${section('pemula', 'Pengenalan EU9', 'Panduan untuk pemula', CLUSTERS.A.blurb, cards(inCluster(site, 'A')), ['/panduan/', 'Semua panduan pemula'])}

${section('ciri', 'Peraturan dan ciri slot', 'Permainan dan ciri slot', 'Antara permainan yang dipaparkan di lobi EU9, dan panduan untuk memahami peraturan serta ciri yang biasa ditemui di dalamnya.', `${GAME_GROUPS.length ? `<div class="games-group"><h3>${esc(GAME_GROUPS[0].name)}</h3>${gameTiles(GAME_GROUPS[0].games.slice(0, 12))}${GAME_NOTE}<p class="more"><a href="/permainan-slot/#senarai-permainan">Lihat semua ${GAME_GROUPS.reduce((n, g) => n + g.games.length, 0)} permainan <span aria-hidden="true">→</span></a> · ${galleryLink('<a href="/galeri/">Galeri tangkapan skrin lobi EU9</a>')}</p></div>` : ''}<h3 class="subhead">Panduan peraturan dan ciri</h3>${cards(inCluster(site, 'B'))}`, ['/permainan-slot/', 'Semua panduan permainan slot'])}

${section('rtp', 'RTP, volatiliti dan keputusan', 'Memahami risiko sebelum bermain', CLUSTERS.C.blurb, cards(inCluster(site, 'C'), { compact: true }), ['/permainan-slot/#kelompok-c', 'Lihat semua penerangan RTP dan volatiliti'])}

${section('bonus', 'Bonus dan syarat cuci', 'Baca terma sebelum menerima bonus', 'Laman ini tidak menyenaraikan tawaran semasa. Artikel di bawah menerangkan cara membaca terma mana-mana promosi.', cards(inCluster(site, 'D'), { compact: true }), ['/bonus-syarat-cuci/', 'Semua panduan bonus'])}

${section('bantuan-akaun', 'Akaun, transaksi dan keselamatan', 'Bantuan dan penyelesaian masalah', 'Semakan umum yang boleh dibuat sendiri. Laman ini tidak boleh mengakses akaun EU9 anda.', cards(helpList, { compact: true }), ['/bantuan/', 'Pusat bantuan'])}

${section('terkini', 'Terbitan terkini', 'Artikel terkini', '', cards(latest), ['/blog/', 'Cari semua artikel'])}

<section class="section section--panel" aria-labelledby="penerbit">
  <div class="wrap split">
    <div>
      <p class="kicker">Siapa kami</p>
      <h2 id="penerbit">Penerbit dan kaedah editorial</h2>
      ${REL.full}
    </div>
    <div>
      <h3>Cara kami menulis</h3>
      <ul class="ticks">
        <li>Setiap artikel menjawab satu soalan utama di bahagian awal.</li>
        <li>Contoh dalam RM dilabel sebagai hipotetikal.</li>
        <li>Maklumat khusus platform hanya diterbitkan selepas disahkan; selainnya kekal sebagai draf.</li>
        <li>Setiap artikel menyenaraikan sumber dan tarikh kemas kini.</li>
      </ul>
      <p><a href="/dasar-editorial/">Dasar editorial</a> · <a href="/tentang-kami/">Tentang kami</a> · <a href="/penulis/">Profil penulis</a></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="hubungi">
  <div class="wrap split">
    <div>
      <p class="kicker">Hubungi</p>
      <h2 id="hubungi">Pembetulan, cadangan dan pertanyaan</h2>
      <p>Jumpa kesilapan atau mahu mencadangkan topik? E-mel <a href="mailto:${config.email}">${config.email}</a>. Alamat ini untuk laman panduan ini sahaja — kami tidak boleh mengakses atau mengubah akaun EU9.</p>
    </div>
    <div class="rg">
      <h3><span class="age">18+</span> Bermain secara bertanggungjawab</h3>
      <p>Tetapkan bajet dan had masa sebelum bermain, dan berhenti jika ia tidak lagi menyeronokkan. Jika anda memerlukan seseorang untuk bercakap, Befrienders KL boleh dihubungi di <a href="tel:+60376272929">03-7627 2929</a>.</p>
      <p><a href="/permainan-bertanggungjawab/">Maklumat permainan bertanggungjawab</a></p>
    </div>
  </div>
</section>`;

  return layout(site, {
    path: '/', title: 'EU9 Slots Malaysia — Panduan Permainan, Bonus & Bantuan',
    desc: 'Panduan EU9 Slots Malaysia dalam Bahasa Melayu: peraturan slot, RTP dan volatiliti, syarat bonus dan syarat cuci, serta bantuan akaun dan keselamatan.',
    body,
    preload: HERO_BANNER
      ? '<link rel="preload" as="image" imagesrcset="/img/hero-banner-800.webp 800w, /img/hero-banner-1526.webp 1526w" imagesizes="(min-width: 1200px) 1150px, 100vw" fetchpriority="high">\n'
      : '<link rel="preload" as="image" href="/img/hero-mobile-800.webp" media="(max-width: 699px)" fetchpriority="high">\n<link rel="preload" as="image" imagesrcset="/img/hero-1000.webp 1000w, /img/hero-1600.webp 1600w" imagesizes="100vw" media="(min-width: 700px)" fetchpriority="high">\n',
    ld: [
      { '@context': 'https://schema.org', ...ORG },
      { '@context': 'https://schema.org', '@type': 'WebSite', '@id': `${config.domain}/#website`, name: config.name, url: config.domain + '/', inLanguage: config.lang, publisher: { '@id': ORG['@id'] } },
    ],
  });
}

const HUB_INTRO = {
  panduan: { h1: 'Panduan EU9 untuk Pengguna Baharu', title: 'Panduan EU9 untuk Pemula — EU9 Slots Malaysia', desc: 'Panduan pemula EU9: istilah slot, cara membaca maklumat permainan dan perkara penting sebelum memulakan sesi.', clusters: ['A'],
    intro: 'Mulakan di sini jika anda baru mengenali slot dalam talian. Panduan ini menerangkan istilah asas dan maklumat yang perlu dibaca sebelum bermain.' },
  'permainan-slot': { h1: 'Permainan Slot: Peraturan, RTP dan Volatiliti', title: 'Permainan Slot EU9 — Peraturan, RTP & Volatiliti', desc: 'Panduan permainan slot: cara membaca paytable, paylines, wild dan scatter, free spins, RTP, volatiliti dan kelebihan rumah.', clusters: ['B', 'C'],
    intro: 'Panduan pendidikan tentang cara slot berfungsi. Peraturan setiap permainan boleh berbeza mengikut pembekal dan versi, jadi rujuk sentiasa skrin maklumat dalam permainan berkenaan.' },
  'bonus-syarat-cuci': { h1: 'Bonus dan Syarat Cuci', title: 'Bonus & Syarat Cuci EU9 — Cara Membaca Terma', desc: 'Cara membaca terma bonus: syarat cuci (turnover), sumbangan permainan, had pertaruhan, had pengeluaran dan tarikh luput, dengan contoh RM.', clusters: ['D'],
    intro: 'Laman ini tidak menyenaraikan tawaran bonus semasa. Panduan di sini membantu anda membaca dan mengira terma mana-mana promosi sebelum menerimanya.' },
  bantuan: { h1: 'Bantuan Akaun, Transaksi dan Keselamatan', title: 'Bantuan EU9 — Akaun, Transaksi & Keselamatan', desc: 'Bantuan EU9: semakan apabila tidak boleh login atau deposit belum masuk, cara mengenal laman tiruan dan cara menetapkan had wang serta masa.', clusters: ['E', 'F'],
    intro: 'Semakan umum yang boleh anda lakukan sendiri. Laman ini bukan saluran sokongan EU9 dan tidak boleh mengakses akaun anda; untuk masalah akaun, gunakan saluran sokongan dalam platform.' },
};

function hubPage(site, key) {
  const hub = HUBS[key], meta = HUB_INTRO[key];
  const bc = breadcrumbs([{ name: 'Utama', path: '/' }, { name: hub.name, path: hub.path }]);
  const blocks = meta.clusters.map((k) => {
    const c = CLUSTERS[k], list = inCluster(site, k), pillar = byN.get(c.pillar);
    const pending = ARTICLES.filter((a) => a.cluster === k && !site.isLive(a)).length;
    const pillarLive = site.isLive(pillar);
    return `<section class="cluster" id="kelompok-${k.toLowerCase()}" aria-labelledby="h-${k}">
  <div class="cluster__head">
    <div class="cluster__media">${img({ base: `cluster/${k.toLowerCase()}`, alt: '', sizes: '(min-width: 960px) 420px, 100vw' })}</div>
    <div>
      <h2 id="h-${k}">${esc(c.name)}</h2>
      <p>${esc(c.blurb)}</p>
      ${pillarLive ? `<p><a class="btn btn--secondary" href="${urlOf(pillar)}">Mula dengan panduan utama</a></p>` : ''}
    </div>
  </div>
  ${cards(list)}
  ${pending ? `<p class="muted small">${pending} panduan lagi dalam kelompok ini sedang menunggu pengesahan maklumat platform dan belum diterbitkan.</p>` : ''}
</section>`;
  }).join('\n');
  const body = `<div class="wrap page-head">${bc.html}<h1>${esc(meta.h1)}</h1><p class="lead">${esc(meta.intro)}</p></div>
<div class="wrap">${blocks}</div>${key === 'permainan-slot' && GAME_GROUPS.length ? gameGallery() : ''}`;
  return layout(site, { path: hub.path, title: meta.title, desc: meta.desc, body, ld: [bc.ld] });
}

function blogPage(site) {
  const list = live(site, ARTICLES);
  const bc = breadcrumbs([{ name: 'Utama', path: '/' }, { name: 'Blog', path: '/blog/' }]);
  const chips = Object.entries(CLUSTERS).filter(([k]) => inCluster(site, k).length)
    .map(([k, c]) => `<button type="button" class="chip" data-filter="${k}" aria-pressed="false">${esc(c.name)}</button>`).join('');
  const body = `<div class="wrap page-head">${bc.html}<h1>Semua Artikel</h1><p class="lead">${list.length} artikel tentang permainan slot, bonus, akaun dan keselamatan. Taip kata kunci atau pilih kelompok untuk menapis.</p></div>
<div class="wrap">
  <div class="filters" data-filters hidden>
    <label class="search"><span class="sr-only">Cari artikel</span><input type="search" id="cari" placeholder="Cari: RTP, syarat cuci, login…" autocomplete="off"></label>
    <div class="chips" role="group" aria-label="Tapis mengikut kelompok"><button type="button" class="chip" data-filter="" aria-pressed="true">Semua</button>${chips}</div>
    <p class="muted small" aria-live="polite" data-count></p>
  </div>
  ${cards(list)}
  <p class="empty" data-empty hidden>Tiada artikel sepadan. Cuba kata kunci lain atau <a href="/bantuan/">lihat pusat bantuan</a>.</p>
</div>`;
  return layout(site, { path: '/blog/', title: 'Blog EU9 Slots Malaysia — Semua Artikel Panduan', desc: 'Senarai semua artikel EU9 Slots Malaysia: panduan permainan slot, RTP dan volatiliti, syarat cuci bonus, bantuan akaun dan keselamatan.', body, ld: [bc.ld] });
}

async function articlePage(site, a) {
  const c = CLUSTERS[a.cluster], hub = HUBS[c.hub], p = urlOf(a);
  const raw = await fs.readFile(path.join(ROOT, 'src/articles', `${String(a.n).padStart(2, '0')}.html`), 'utf8');
  const { html, toc } = addHeadingIds(resolveLinks(raw, site, `artikel ${a.n}`));
  const bc = breadcrumbs([{ name: 'Utama', path: '/' }, { name: hub.name, path: hub.path }, { name: a.card, path: p }]);
  const pillar = byN.get(c.pillar);
  const isPillar = a.n === c.pillar;

  const relatedNs = [...new Set([...(isPillar ? [] : [c.pillar]), ...a.related,
    ...ARTICLES.filter((x) => x.cluster === a.cluster).map((x) => x.n)])].filter((n) => n !== a.n);
  const related = relatedNs.map((n) => byN.get(n)).filter(site.isLive).slice(0, 6);

  const sources = a.sources.map((k) => SOURCES[k]).map((s) => `<li>${s.url ? `<a href="${s.url}" rel="noopener" hreflang="en">${esc(s.label)}</a>` : esc(s.label)}</li>`).join('');
  const reviewer = config.reviewer ? ` · Disemak oleh ${esc(config.reviewer.name)}${config.reviewer.role ? `, ${esc(config.reviewer.role)}` : ''}` : '';
  const draftBanner = a.status === 'draft' ? `<div class="draft-banner" role="note"><p><strong>DRAF — belum diterbitkan.</strong> Maklumat yang diperlukan sebelum penerbitan:</p><ul>${a.missing.map((m) => `<li>${esc(m)}</li>`).join('')}</ul></div>` : '';
  const pillarBox = !isPillar && site.isLive(pillar)
    ? `<aside class="pillar-box"><p class="kicker">Sebahagian daripada</p><p><a href="${urlOf(pillar)}">${esc(pillar.title)}</a></p></aside>`
    : (!isPillar ? `<aside class="pillar-box"><p class="kicker">Kelompok</p><p><a href="${hub.path}#kelompok-${a.cluster.toLowerCase()}">${esc(c.name)}</a></p></aside>` : '');

  const body = `<article class="article">
  <div class="wrap wrap--read">
    ${bc.html}
    ${draftBanner}
    <p class="kicker"><a href="${hub.path}#kelompok-${a.cluster.toLowerCase()}">${esc(c.name)}</a></p>
    <h1>${esc(a.title)}</h1>
    <p class="byline">Oleh <a href="${config.author.url}">${esc(config.author.name)}</a>${reviewer} · Diterbitkan <time datetime="${a.published}">${fmtDate(a.published)}</time>${a.updated !== a.published ? ` · Dikemas kini <time datetime="${a.updated}">${fmtDate(a.updated)}</time>` : ''}</p>
  </div>
  <div class="wrap wrap--wide article__media">${img({ base: `artikel/${a.slug}`, alt: thumbAlt(a), sizes: '(min-width: 1000px) 960px, 100vw', eager: true })}</div>
  <div class="wrap wrap--read">
    ${toc.length > 2 ? `<details class="toc" open><summary>Kandungan artikel</summary><ol>${toc.map((t) => `<li><a href="#${t.id}">${esc(t.text)}</a></li>`).join('')}</ol></details>` : ''}
    <div class="prose">
${html}
    </div>
    ${pillarBox}
    <section class="sources" aria-labelledby="sumber">
      <h2 id="sumber">Sumber dan rujukan</h2>
      ${sources ? `<ul>${sources}</ul>` : '<p class="muted">Sumber khusus platform belum disahkan.</p>'}
      <p class="muted small">Contoh dalam RM ialah ilustrasi hipotetikal, bukan ramalan hasil. Peraturan, RTP dan terma boleh berbeza mengikut permainan, versi dan promosi.</p>
    </section>
    <aside class="about-box">
      <h2 class="about-box__h">Tentang artikel ini</h2>
      <p>${esc(REL.short)} Artikel ini mengikut <a href="/dasar-editorial/">dasar editorial</a> kami. Jumpa kesilapan? E-mel <a href="mailto:${config.email}?subject=${encodeURIComponent('Pembetulan: ' + a.title)}">${config.email}</a>.</p>
      <p class="small"><span class="age">18+</span> Bermain melibatkan risiko kehilangan wang. <a href="/permainan-bertanggungjawab/">Permainan bertanggungjawab</a>.</p>
    </aside>
  </div>
  ${related.length ? `<section class="section related" aria-labelledby="berkaitan"><div class="wrap"><h2 id="berkaitan">Artikel berkaitan</h2>${cards(related)}</div></section>` : ''}
</article>`;

  const ld = [{
    '@context': 'https://schema.org', '@type': 'BlogPosting', headline: a.title, description: a.desc,
    image: [abs(`/img/og/${a.slug}.jpg`), abs(`/img/artikel/${a.slug}-1200.webp`)],
    datePublished: a.published, dateModified: a.updated, inLanguage: config.lang,
    author: { '@type': 'Organization', name: config.author.name, url: abs(config.author.url) },
    publisher: { '@id': ORG['@id'], ...ORG },
    mainEntityOfPage: abs(p), articleSection: c.name,
  }, bc.ld];
  return layout(site, { path: p, title: `${a.title} | ${config.name}`, desc: a.desc, body, ld, ogImage: `/img/og/${a.slug}.jpg`, ogType: 'article', noindex: a.status === 'draft' });
}

function staticPage(site, pg) {
  const bc = breadcrumbs([{ name: 'Utama', path: '/' }, { name: pg.nav, path: pg.path }]);
  const w = pg.wide ? 'wrap' : 'wrap wrap--read';
  const body = `<div class="${w} page-head">${bc.html}<h1>${esc(pg.h1)}</h1>${pg.updated ? `<p class="byline">Dikemas kini <time datetime="${pg.updated}">${fmtDate(pg.updated)}</time></p>` : ''}</div>
<div class="${w} prose">${resolveLinks(pg.body(), site, pg.path)}</div>`;
  return layout(site, { path: pg.path, title: pg.title, desc: pg.desc, body, ld: [bc.ld] });
}

function notFoundPage(site) {
  const body = `<div class="wrap wrap--read page-head"><p class="kicker">Ralat 404</p><h1>Halaman tidak dijumpai</h1>
<p class="lead">Alamat ini tidak wujud atau telah dialihkan.</p>
<div class="btn-row"><a class="btn btn--primary" href="/">Ke halaman utama</a><a class="btn btn--secondary" href="/blog/">Cari artikel</a></div></div>`;
  return layout(site, { path: '/404', title: 'Halaman tidak dijumpai — EU9 Slots Malaysia', desc: 'Halaman yang anda cari tidak wujud.', body, noindex: true });
}

// ---------------------------------------------------------------- write
async function write(dir, rel, content) {
  const file = path.join(dir, rel);
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, content);
}

async function copyDir(from, to) {
  await fs.cp(from, to, { recursive: true });
}

async function buildSite(outDir, includeDrafts) {
  const site = makeSite(includeDrafts);
  await fs.rm(outDir, { recursive: true, force: true });
  await copyDir(path.join(ROOT, 'static'), outDir);
  await copyDir(path.join(ROOT, 'src/img'), path.join(outDir, 'img'));

  const pages = [['/', homePage(site)], ['/blog/', blogPage(site)]];
  for (const key of Object.keys(HUBS)) pages.push([HUBS[key].path, hubPage(site, key)]);
  for (const a of ARTICLES) if (site.isLive(a)) pages.push([urlOf(a), await articlePage(site, a)]);
  for (const pg of PAGES) pages.push([pg.path, staticPage(site, pg)]);
  for (const [p, html] of pages) await write(outDir, path.join(p, 'index.html'), html);
  await write(outDir, '404.html', notFoundPage(site));

  const indexable = PROD && !includeDrafts;
  await write(outDir, 'robots.txt', indexable
    ? `User-agent: *\nAllow: /\n\nSitemap: ${config.domain}/sitemap.xml\n`
    : 'User-agent: *\nDisallow: /\n');
  if (indexable) {
    const latest = ARTICLES.filter((a) => a.status === 'published').map((a) => a.updated).sort().pop();
    const entries = [
      ['/', latest], ['/blog/', latest],
      ...Object.values(HUBS).map((h) => [h.path, latest]),
      ...ARTICLES.filter((a) => a.status === 'published').map((a) => [urlOf(a), a.updated]),
      ...PAGES.map((pg) => [pg.path, pg.updated || config.launchDate]),
    ];
    await write(outDir, 'sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries.map(([p, d]) => `  <url><loc>${abs(p)}</loc><lastmod>${d}</lastmod></url>`).join('\n')}\n</urlset>\n`);
  } else {
    await fs.rm(path.join(outDir, '_redirects'), { force: true });
  }
  if (includeDrafts) {
    const drafts = ARTICLES.filter((a) => a.status === 'draft');
    await write(outDir, '_drafts.txt', drafts.map((a) => `${a.n}\t${urlOf(a)}\t${a.missing.join('; ')}`).join('\n') + '\n');
  }
  return site;
}

const css = await fs.readFile(path.join(ROOT, 'static/assets/site.css'));
const js = await fs.readFile(path.join(ROOT, 'static/assets/site.js'));
ASSET_V = crypto.createHash('sha1').update(css).update(js).digest('hex').slice(0, 10);

const dist = await buildSite(path.join(ROOT, 'dist'), false);
const preview = await buildSite(path.join(ROOT, 'preview'), true);
const warnings = [...new Set([...dist.warnings, ...preview.warnings])];
const pub = ARTICLES.filter((a) => a.status === 'published').length;
console.log(`Built dist/ (${PROD ? 'PRODUCTION — indexable' : 'non-production — noindex'}): ${pub} published articles, ${ARTICLES.length - pub} drafts kept in preview/ only.`);
if (warnings.length) { console.warn('Warnings:\n  ' + warnings.join('\n  ')); process.exitCode = 1; }
