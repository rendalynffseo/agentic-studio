// Generates original abstract red-and-gold editorial graphics (no brand assets,
// no game artwork, no interface imitations). Output: src/img/ (WebP + JPEG).
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import config from '../src/config.js';
import { ARTICLES, CLUSTERS } from '../src/inventory.js';
import { GAME_GROUPS, GRIDS } from '../src/games.js';
import { GALLERY } from '../src/gallery.js';

const OUT = path.resolve('src/img');
const C = { bg: '#0C0C0C', surface: '#1C1917', raised: '#282421', red: '#C8262F', dark: '#9E0B0F', gold: '#F0C94B', text: '#F7F5F2', muted: '#BDB5AE' };
const FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";

function rng(seed) {
  let s = seed * 9301 + 49297;
  return () => ((s = (s * 9301 + 49297) % 233280) / 233280);
}

const defs = (id) => `<defs>
  <radialGradient id="glow${id}" cx="70%" cy="40%" r="70%"><stop offset="0" stop-color="${C.red}" stop-opacity=".6"/><stop offset=".55" stop-color="${C.dark}" stop-opacity=".18"/><stop offset="1" stop-color="${C.bg}" stop-opacity="0"/></radialGradient>
  <linearGradient id="gold${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF6D8"/><stop offset=".5" stop-color="#F2D06B"/><stop offset="1" stop-color="#D9A433"/></linearGradient>
  <linearGradient id="red${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C.red}"/><stop offset="1" stop-color="${C.dark}"/></linearGradient>
</defs>`;

// Cluster motifs, drawn inside a w×h box. r() gives per-image variation.
const MOTIFS = {
  // A: Pengenalan — open path / signpost of stepping stones
  A: (w, h, r, id) => {
    let s = '';
    for (let i = 0; i < 7; i++) {
      const x = w * (0.18 + i * 0.11), y = h * (0.78 - i * 0.075 - r() * 0.04);
      s += `<rect x="${x}" y="${y}" width="${w * 0.08}" height="${h * 0.035}" rx="${h * 0.017}" fill="url(#gold${id})" opacity="${0.35 + i * 0.09}"/>`;
    }
    s += `<circle cx="${w * 0.84}" cy="${h * 0.24}" r="${h * 0.11}" fill="none" stroke="url(#gold${id})" stroke-width="${h * 0.012}"/>`;
    s += `<path d="M${w * 0.84} ${h * 0.15} L${w * 0.87} ${h * 0.24} L${w * 0.84} ${h * 0.33} L${w * 0.81} ${h * 0.24}Z" fill="${C.red}"/>`;
    return s;
  },
  // B: Peraturan & ciri — abstract reel grid with geometric symbols
  B: (w, h, r, id) => {
    let s = '';
    const cols = 5, rows = 3, cw = w * 0.11, ch = h * 0.2, x0 = w * 0.5 - (cols * cw) / 2 + w * 0.12, y0 = h * 0.2;
    for (let c = 0; c < cols; c++) {
      s += `<rect x="${x0 + c * cw + 4}" y="${y0 - 10}" width="${cw - 8}" height="${rows * ch + 20}" rx="14" fill="${C.raised}" stroke="${C.red}" stroke-opacity=".35"/>`;
      for (let rI = 0; rI < rows; rI++) {
        const cx = x0 + c * cw + cw / 2, cy = y0 + rI * ch + ch / 2, k = Math.floor(r() * 4), sz = Math.min(cw, ch) * 0.28;
        const fill = rI === 1 ? `url(#gold${id})` : (k % 2 ? C.red : C.muted);
        const op = rI === 1 ? 1 : 0.55;
        if (k === 0) s += `<circle cx="${cx}" cy="${cy}" r="${sz}" fill="${fill}" opacity="${op}"/>`;
        else if (k === 1) s += `<rect x="${cx - sz}" y="${cy - sz}" width="${sz * 2}" height="${sz * 2}" rx="6" fill="${fill}" opacity="${op}"/>`;
        else if (k === 2) s += `<path d="M${cx} ${cy - sz * 1.1} L${cx + sz} ${cy + sz * 0.8} L${cx - sz} ${cy + sz * 0.8}Z" fill="${fill}" opacity="${op}"/>`;
        else s += `<path d="M${cx} ${cy - sz * 1.1} L${cx + sz} ${cy} L${cx} ${cy + sz * 1.1} L${cx - sz} ${cy}Z" fill="${fill}" opacity="${op}"/>`;
      }
    }
    s += `<line x1="${x0 - 20}" y1="${y0 + ch * 1.5}" x2="${x0 + cols * cw + 20}" y2="${y0 + ch * 1.5}" stroke="${C.gold}" stroke-width="3" stroke-dasharray="10 8" opacity=".8"/>`;
    return s;
  },
  // C: RTP & volatiliti — bell curves and a long-run line
  C: (w, h, r, id) => {
    const base = h * 0.8, x0 = w * 0.3, x1 = w * 0.95;
    const curve = (spread, amp, col, op) => {
      let d = `M${x0} ${base}`;
      for (let i = 0; i <= 60; i++) {
        const t = i / 60, x = x0 + (x1 - x0) * t, z = (t - 0.55) / spread;
        d += ` L${x.toFixed(1)} ${(base - amp * Math.exp(-z * z / 2)).toFixed(1)}`;
      }
      return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${h * 0.012}" stroke-linecap="round" opacity="${op}"/>`;
    };
    let s = `<line x1="${x0}" y1="${base}" x2="${x1}" y2="${base}" stroke="${C.muted}" stroke-opacity=".4" stroke-width="2"/>`;
    s += curve(0.07 + r() * 0.03, h * 0.55, `url(#gold${id})`, 1);
    s += curve(0.2 + r() * 0.05, h * 0.25, C.red, 0.9);
    for (let i = 0; i < 18; i++) s += `<circle cx="${x0 + (x1 - x0) * r()}" cy="${base - h * 0.62 * r()}" r="${3 + r() * 4}" fill="${C.text}" opacity=".18"/>`;
    return s;
  },
  // D: Bonus & syarat cuci — progress rings
  D: (w, h, r, id) => {
    let s = '';
    const cx = w * 0.72, cy = h * 0.5;
    [0.34, 0.25, 0.16].forEach((rad, i) => {
      const R = h * rad, circ = 2 * Math.PI * R, p = 0.35 + r() * 0.55;
      s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${C.raised}" stroke-width="${h * 0.05}"/>`;
      s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${i === 1 ? C.red : `url(#gold${id})`}" stroke-width="${h * 0.05}" stroke-linecap="round" stroke-dasharray="${(circ * p).toFixed(1)} ${circ.toFixed(1)}" transform="rotate(-90 ${cx} ${cy})"/>`;
    });
    return s;
  },
  // E: Akaun & transaksi — key and ledger lines
  E: (w, h, r, id) => {
    let s = '';
    for (let i = 0; i < 5; i++) {
      const y = h * (0.25 + i * 0.12), len = w * (0.22 + r() * 0.2);
      s += `<rect x="${w * 0.42}" y="${y}" width="${len}" height="${h * 0.045}" rx="${h * 0.022}" fill="${i === 2 ? C.red : C.raised}"/>`;
      s += `<circle cx="${w * 0.42 + len + h * 0.06}" cy="${y + h * 0.022}" r="${h * 0.022}" fill="url(#gold${id})" opacity="${i === 2 ? 1 : 0.5}"/>`;
    }
    const kx = w * 0.86, ky = h * 0.36;
    s += `<circle cx="${kx}" cy="${ky}" r="${h * 0.08}" fill="none" stroke="url(#gold${id})" stroke-width="${h * 0.025}"/>`;
    s += `<path d="M${kx} ${ky + h * 0.08} V${ky + h * 0.38} M${kx} ${ky + h * 0.28} h${h * 0.06} M${kx} ${ky + h * 0.34} h${h * 0.045}" stroke="url(#gold${id})" stroke-width="${h * 0.025}" stroke-linecap="round" fill="none"/>`;
    return s;
  },
  // F: Sokongan & had — shield and clock
  F: (w, h, r, id) => {
    const sx = w * 0.62, sy = h * 0.2, sw = h * 0.42;
    let s = `<path d="M${sx} ${sy} L${sx + sw / 2} ${sy + sw * 0.15} V${sy + sw * 0.6} Q${sx + sw / 2} ${sy + sw * 1.15} ${sx} ${sy + sw * 1.4} Q${sx - sw / 2} ${sy + sw * 1.15} ${sx - sw / 2} ${sy + sw * 0.6} V${sy + sw * 0.15}Z" fill="url(#red${id})" opacity=".9"/>`;
    s += `<path d="M${sx - sw * 0.2} ${sy + sw * 0.7} L${sx - sw * 0.03} ${sy + sw * 0.87} L${sx + sw * 0.24} ${sy + sw * 0.52}" stroke="${C.text}" stroke-width="${h * 0.022}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
    const cx = w * 0.86, cy = h * 0.62, R = h * 0.16, a = r() * Math.PI * 2;
    s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold${id})" stroke-width="${h * 0.02}"/>`;
    s += `<path d="M${cx} ${cy} L${cx} ${cy - R * 0.65} M${cx} ${cy} L${cx + Math.cos(a) * R * 0.5} ${cy + Math.sin(a) * R * 0.5}" stroke="${C.gold}" stroke-width="${h * 0.018}" stroke-linecap="round"/>`;
    return s;
  },
};

function background(w, h, r, id) {
  let s = `<rect width="${w}" height="${h}" fill="${C.bg}"/><rect width="${w}" height="${h}" fill="url(#glow${id})"/>`;
  // Diagonal light bands for depth
  for (let i = 0; i < 4; i++) {
    const x = w * (0.1 + r() * 0.8);
    s += `<path d="M${x} 0 L${x + w * 0.08} 0 L${x - w * 0.2} ${h} L${x - w * 0.28} ${h}Z" fill="${C.text}" opacity="${0.015 + r() * 0.02}"/>`;
  }
  return s;
}

function svg(w, h, body, id = 'x') {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${defs(id)}${body}</svg>`;
}

function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

function wrap(text, max) {
  const words = text.split(' '); const lines = []; let line = '';
  for (const w of words) {
    if ((line + ' ' + w).trim().length > max) { lines.push(line.trim()); line = w; } else line += ' ' + w;
  }
  if (line.trim()) lines.push(line.trim());
  return lines;
}

function heroSvg(w, h, mobile) {
  const r = rng(mobile ? 7 : 3), id = 'h';
  let s = background(w, h, r, id);
  // Large gold arc + stacked "reel" pillars, anchored to the right (desktop) or bottom (mobile)
  const cx = mobile ? w * 0.55 : w * 0.74, cy = mobile ? h * 0.72 : h * 0.55, R = mobile ? w * 0.46 : h * 0.44;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 1.25}" fill="none" stroke="${C.red}" stroke-opacity=".25" stroke-width="2"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="url(#gold${id})" stroke-width="${R * 0.05}" stroke-dasharray="${R * 0.9} ${R * 0.25}"/>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${R * 0.72}" fill="url(#red${id})" opacity=".85"/>`;
  for (let i = 0; i < 3; i++) {
    const pw = R * 0.26, px = cx - pw * 1.6 + i * pw * 1.1, ph = R * 0.95;
    s += `<rect x="${px}" y="${cy - ph / 2}" width="${pw}" height="${ph}" rx="${pw * 0.25}" fill="${C.bg}" opacity=".88"/>`;
    s += `<circle cx="${px + pw / 2}" cy="${cy}" r="${pw * 0.28}" fill="url(#gold${id})"/>`;
    s += `<rect x="${px + pw * 0.25}" y="${cy - ph * 0.33}" width="${pw * 0.5}" height="${pw * 0.12}" rx="3" fill="${C.muted}" opacity=".35"/>`;
    s += `<rect x="${px + pw * 0.25}" y="${cy + ph * 0.28}" width="${pw * 0.5}" height="${pw * 0.12}" rx="3" fill="${C.muted}" opacity=".35"/>`;
  }
  for (let i = 0; i < 26; i++) s += `<circle cx="${w * r()}" cy="${h * r()}" r="${1 + r() * 3}" fill="${C.gold}" opacity="${0.15 + r() * 0.35}"/>`;
  // Fade the text side so overlaid HTML text keeps contrast
  s += mobile
    ? `<rect width="${w}" height="${h * 0.5}" fill="url(#fadeV)"/>`
    : `<rect width="${w * 0.6}" height="${h}" fill="url(#fadeH)"/>`;
  const fades = `<linearGradient id="fadeH" x1="0" x2="1"><stop offset="0" stop-color="${C.bg}" stop-opacity=".95"/><stop offset="1" stop-color="${C.bg}" stop-opacity="0"/></linearGradient><linearGradient id="fadeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C.bg}" stop-opacity=".95"/><stop offset="1" stop-color="${C.bg}" stop-opacity="0"/></linearGradient>`;
  return svg(w, h, `<defs>${fades}</defs>${s}`, id);
}

function coverSvg(key, w, h, seed, label) {
  const r = rng(seed), id = `c${seed}`;
  // Per-image variation: glow position, motif scale/offset and mirroring
  const flip = seed % 2 === 1, k = 0.78 + r() * 0.3, dx = (r() - 0.5) * w * 0.16, dy = (r() - 0.5) * h * 0.12;
  const tf = `translate(${w / 2 + dx} ${h / 2 + dy}) scale(${flip ? -k : k} ${k}) translate(${-w / 2} ${-h / 2})`;
  let s = background(w, h, r, id);
  s += `<circle cx="${w * (0.2 + r() * 0.6)}" cy="${h * r()}" r="${h * (0.3 + r() * 0.3)}" fill="${r() > 0.5 ? C.gold : C.red}" opacity=".07"/>`;
  s += `<g transform="${tf}">${MOTIFS[key](w, h, r, id)}</g>`;
  if (label) s += `<text x="${w * 0.06}" y="${h * 0.86}" font-family="${FONT}" font-weight="800" font-size="${h * 0.28}" fill="${C.text}" opacity=".08">${esc(label)}</text>`;
  s += `<rect x="${w * 0.06}" y="${h * 0.12}" width="${w * 0.07}" height="${h * 0.012}" fill="${C.red}"/>`;
  return svg(w, h, s, id);
}

function ogSvg(title, kicker, seed, key) {
  const w = 1200, h = 630, r = rng(seed), id = `o${seed}`;
  let s = background(w, h, r, id);
  if (key) s += `<g opacity=".55">${MOTIFS[key](w, h, r, id)}</g>`;
  s += `<rect width="${w * 0.72}" height="${h}" fill="${C.bg}" opacity=".72"/>`;
  s += `<text x="64" y="92" font-family="${FONT}" font-weight="800" font-size="34" fill="${C.text}">EU9 <tspan fill="${C.gold}">Slots</tspan> Malaysia</text>`;
  s += `<rect x="64" y="122" width="80" height="6" fill="${C.red}"/>`;
  if (kicker) s += `<text x="64" y="186" font-family="${FONT}" font-weight="700" font-size="26" fill="${C.gold}" letter-spacing="1">${esc(kicker.toUpperCase())}</text>`;
  const lines = wrap(title, 30).slice(0, 4);
  lines.forEach((l, i) => { s += `<text x="64" y="${262 + i * 66}" font-family="${FONT}" font-weight="800" font-size="54" fill="${C.text}">${esc(l)}</text>`; });
  s += `<text x="64" y="${h - 48}" font-family="${FONT}" font-size="24" fill="${C.muted}">eu9slots.com · Panduan dalam Bahasa Melayu</text>`;
  return svg(w, h, s, id);
}

async function out(svgText, file, w, h, fmt = 'webp') {
  const p = path.join(OUT, file);
  await fs.mkdir(path.dirname(p), { recursive: true });
  let img = sharp(Buffer.from(svgText)).resize(w, h);
  img = fmt === 'jpg' ? img.jpeg({ quality: 82, mozjpeg: true }) : img.webp({ quality: 80 });
  await img.toFile(p);
}

await fs.rm(OUT, { recursive: true, force: true });

await out(heroSvg(1600, 700, false), 'hero-1600.webp', 1600, 700);
await out(heroSvg(1600, 700, false), 'hero-1000.webp', 1000, 438);
await out(heroSvg(800, 900, true), 'hero-mobile-800.webp', 800, 900);

for (const [key] of Object.entries(CLUSTERS)) {
  const seed = key.charCodeAt(0);
  const s = coverSvg(key, 1200, 675, seed, key);
  await out(s, `cluster/${key.toLowerCase()}-1200.webp`, 1200, 675);
  await out(s, `cluster/${key.toLowerCase()}-640.webp`, 640, 360);
}

for (const a of ARTICLES) {
  const s = coverSvg(a.cluster, 1200, 675, a.n * 31 + 5, String(a.n).padStart(2, '0'));
  await out(s, `artikel/${a.slug}-1200.webp`, 1200, 675);
  await out(s, `artikel/${a.slug}-640.webp`, 640, 360);
  await out(ogSvg(a.title, CLUSTERS[a.cluster].name, a.n * 31 + 5, a.cluster), `og/${a.slug}.jpg`, 1200, 630, 'jpg');
}

await out(ogSvg('Panduan Permainan, Bonus & Bantuan', 'Panduan slot EU9', 11, 'B'), 'og/default.jpg', 1200, 630, 'jpg');

const favicon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="${C.red}"/><text x="32" y="43" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="28" fill="#fff">E9</text></svg>`;
await fs.writeFile(path.join(OUT, 'favicon.svg'), favicon);
await sharp(Buffer.from(favicon)).resize(180, 180).png().toFile(path.join(OUT, 'apple-touch-icon.png'));
await sharp(Buffer.from(favicon)).resize(32, 32).png().toFile(path.join(OUT, 'favicon-32.png'));

// Owner-supplied assets (all optional) from assets-src/owner/:
//   logo.png, hero-banner.png (wide banner shown whole above the hero), popup.png (9:16),
//   <shot>.png lobby screenshots for src/games.js and <n>.png screenshots for src/gallery.js.
const OWNER = path.resolve('assets-src/owner');
const has = async (f) => fs.stat(path.join(OWNER, f)).then(() => true, () => false);
if (await has('logo.png')) await sharp(path.join(OWNER, 'logo.png')).png().toFile(path.join(OUT, 'logo.png'));
if (await has('hero-banner.png'))
  for (const w of [1526, 800]) await sharp(path.join(OWNER, 'hero-banner.png')).resize({ width: w, withoutEnlargement: true }).webp({ quality: 84 }).toFile(path.join(OUT, `hero-banner-${w}.webp`));
if (await has('popup.png')) {
  await sharp(path.join(OWNER, 'popup.png')).resize(584, 778, { fit: 'cover' }).webp({ quality: 84 }).toFile(path.join(OUT, 'popup-banner.webp'));
} else {
  // Generated 9:16-ish fallback popup art (no text claims, no offers)
  const w = 584, h = 778, r = rng(99), id = 'p';
  let body = background(w, h, r, id) + `<g transform="translate(${-w * 0.22} ${h * 0.14})">${MOTIFS.D(w, h * 0.7, r, id)}</g>`;
  body += `<text x="${w / 2}" y="${h * 0.16}" text-anchor="middle" font-family="${FONT}" font-weight="800" font-size="54" fill="url(#gold${id})">${esc(config.name)}</text>`;
  await out(svg(w, h, body, id), 'popup-banner.webp', w, h);
}

if (GAME_GROUPS.length) await fs.mkdir(path.join(OUT, 'permainan'), { recursive: true });
for (const g of GAME_GROUPS) {
  for (const game of g.games) {
    const grid = GRIDS[game.shot], [x0, x1] = grid.cols[game.col], [y0, y1] = grid.rows[game.row], inset = 4;
    await sharp(path.join(OWNER, `${game.shot}.png`))
      .extract({ left: x0 + inset, top: y0 + inset, width: x1 - x0 - inset * 2, height: y1 - y0 - inset * 2 })
      .resize(400, 300, { fit: 'contain', background: '#141011' })
      .webp({ quality: 82 }).toFile(path.join(OUT, 'permainan', `${game.file}.webp`));
  }
}

if (GALLERY.length) {
  await fs.mkdir(path.join(OUT, 'galeri'), { recursive: true });
  const manifest = {};
  for (const shot of GALLERY.flatMap((g) => g.shots)) {
    const src = path.join(OWNER, `${shot.n}.png`), { width, height } = await sharp(src).metadata();
    const big = Math.min(width, 1600), small = Math.min(width, 800);
    for (const w of new Set([big, small])) await sharp(src).resize(w).webp({ quality: 82 }).toFile(path.join(OUT, 'galeri', `${shot.n}-${w}.webp`));
    manifest[shot.n] = { big, small, width: big, height: Math.round(height * big / width) };
  }
  await fs.writeFile(path.join(OUT, 'galeri', 'manifest.json'), JSON.stringify(manifest, null, 2));
}

console.log('Images written to', OUT);
