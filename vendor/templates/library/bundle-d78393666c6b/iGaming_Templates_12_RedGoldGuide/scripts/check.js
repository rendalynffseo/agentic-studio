// Launch checks for dist/. Run after `npm run build:prod`.
//   node scripts/check.js             internal checks + local HTTP status checks
//   node scripts/check.js --external  also requests every external source URL
import fs from 'node:fs/promises';
import path from 'node:path';
import config from '../src/config.js';
import { ARTICLES, CLUSTERS, HUBS } from '../src/inventory.js';
import { createServer } from './serve.js';

const DIST = path.resolve('dist');
const errors = []; const notes = [];
const fail = (m) => errors.push(m);

async function walk(dir) {
  const out = [];
  for (const e of await fs.readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...await walk(p)); else out.push(p);
  }
  return out;
}

const files = await walk(DIST);
const htmlFiles = files.filter((f) => f.endsWith('.html'));
const rel = (f) => '/' + path.relative(DIST, f).replace(/index\.html$/, '').replace(/\\/g, '/');
const pages = new Map();
for (const f of htmlFiles) pages.set(rel(f), await fs.readFile(f, 'utf8'));

const exists = async (p) => fs.stat(path.join(DIST, p)).then(() => true, () => false);
const urlOf = (a) => `${HUBS[CLUSTERS[a.cluster].hub].path}${a.slug}/`;
const draftUrls = new Set(ARTICLES.filter((a) => a.status === 'draft').map(urlOf));
const pubArticles = ARTICLES.filter((a) => a.status === 'published');

// --- per-page checks
const titles = new Map(); const descs = new Map(); const inbound = new Map();
const extLinks = new Set();
for (const [p, html] of pages) {
  const isErr = p === '/404.html';
  const title = html.match(/<title>([^<]*)<\/title>/)?.[1];
  const desc = html.match(/<meta name="description" content="([^"]*)"/)?.[1];
  const canon = html.match(/<link rel="canonical" href="([^"]*)"/)?.[1];
  const robots = html.match(/<meta name="robots" content="([^"]*)"/)?.[1];
  if (!title) fail(`${p}: missing <title>`);
  if (!desc) fail(`${p}: missing description`);
  if (!isErr) {
    titles.set(title, [...(titles.get(title) || []), p]);
    descs.set(desc, [...(descs.get(desc) || []), p]);
    if (canon !== config.domain + p) fail(`${p}: canonical ${canon} is not self-referencing`);
    if (!robots?.startsWith('index')) fail(`${p}: robots meta is "${robots}" (build with SITE_ENV=production)`);
  } else if (!robots?.startsWith('noindex')) fail('404 page must be noindex');
  if ((html.match(/<h1[\s>]/g) || []).length !== 1) fail(`${p}: expected exactly one <h1>`);
  if (!/<html lang="ms-MY">/.test(html)) fail(`${p}: html lang is not ms-MY`);
  if (/\[\[|PERLU DISAHKAN|class="todo"/.test(html)) fail(`${p}: unresolved token or draft placeholder`);

  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try {
      const d = JSON.parse(m[1]);
      if (/Rating|Review|FAQPage/.test(JSON.stringify(d))) fail(`${p}: unsupported rating/review/FAQ schema`);
    } catch { fail(`${p}: invalid JSON-LD`); }
  }

  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    const tag = m[0];
    if (!/\swidth="\d+"/.test(tag) || !/\sheight="\d+"/.test(tag)) fail(`${p}: img without width/height`);
    if (!/\salt="/.test(tag)) fail(`${p}: img without alt`);
    const src = tag.match(/\ssrc="([^"]+)"/)?.[1];
    if (src && !(await exists(src))) fail(`${p}: missing image ${src}`);
    for (const s of (tag.match(/srcset="([^"]+)"/)?.[1] || '').split(',').map((x) => x.trim().split(' ')[0]).filter(Boolean))
      if (!(await exists(s))) fail(`${p}: missing srcset image ${s}`);
  }
  for (const m of html.matchAll(/(?:srcset|imagesrcset)="([^"]+)"/g))
    for (const s of m[1].split(',').map((x) => x.trim().split(' ')[0])) if (!(await exists(s))) fail(`${p}: missing ${s}`);
  const og = html.match(/property="og:image" content="([^"]+)"/)?.[1];
  if (og && !(await exists(og.replace(config.domain, '')))) fail(`${p}: missing og:image ${og}`);

  // Internal links
  for (const m of html.matchAll(/<a\b[^>]*href="([^"]+)"/g)) {
    const href = m[1];
    if (/^(mailto:|tel:)/.test(href)) continue;
    if (/^https?:/.test(href)) { if (!href.startsWith(config.domain)) extLinks.add(href); continue; }
    const [hp, hash] = href.split('#');
    const target = hp || p;
    if (draftUrls.has(target)) fail(`${p}: links to draft ${target}`);
    if (target.startsWith('/assets/') || target.startsWith('/img/')) { if (!(await exists(target.split('?')[0]))) fail(`${p}: missing asset ${target}`); continue; }
    if (!pages.has(target)) { fail(`${p}: broken link ${href}`); continue; }
    if (hash && !new RegExp(`id="${hash}"`).test(pages.get(target))) fail(`${p}: missing anchor ${href}`);
    if (target !== p) {
      if (!inbound.has(target)) inbound.set(target, new Set());
      inbound.get(target).add(p);
    }
  }
}
for (const [t, ps] of titles) if (ps.length > 1) fail(`duplicate title "${t}": ${ps.join(', ')}`);
for (const [d, ps] of descs) if (ps.length > 1) fail(`duplicate description: ${ps.join(', ')}`);

// --- cluster linking rules (body links only, so nav/related cards don't mask gaps)
const bodyOf = (html) => html.split('<div class="prose">')[1]?.split('<section class="sources"')[0] || '';
for (const a of pubArticles) {
  const c = CLUSTERS[a.cluster], pillar = ARTICLES.find((x) => x.n === c.pillar);
  const body = bodyOf(pages.get(urlOf(a)));
  if (a.n === c.pillar) {
    for (const s of pubArticles.filter((x) => x.cluster === a.cluster && x.n !== a.n))
      if (!body.includes(`href="${urlOf(s)}"`)) fail(`pillar ${a.n} does not link to supporting ${s.n}`);
  } else if (pillar.status === 'published' && !body.includes(`href="${urlOf(pillar)}"`)) {
    fail(`article ${a.n} does not link back to pillar ${pillar.n}`);
  } else if (pillar.status === 'draft') {
    notes.push(`article ${a.n}: pillar ${pillar.n} is a draft; article links to the cluster hub instead`);
  }
  const fromArticles = [...(inbound.get(urlOf(a)) || [])].filter((p) => pubArticles.some((x) => urlOf(x) === p));
  if (!fromArticles.length) fail(`article ${a.n} has no inbound links from other articles (orphan)`);
}

// --- sitemap and robots
const sitemap = await fs.readFile(path.join(DIST, 'sitemap.xml'), 'utf8').catch(() => '');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(config.domain, ''));
if (!locs.length) fail('sitemap.xml missing or empty');
for (const l of locs) if (!pages.has(l)) fail(`sitemap lists missing page ${l}`);
for (const l of locs) if (draftUrls.has(l)) fail(`sitemap lists draft ${l}`);
for (const p of pages.keys()) if (p !== '/404.html' && !locs.includes(p)) fail(`indexable page missing from sitemap: ${p}`);
const robots = await fs.readFile(path.join(DIST, 'robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${config.domain}/sitemap.xml`) || /Disallow: \/\s/.test(robots)) fail('robots.txt not production-ready');
for (const d of draftUrls) if (await exists(d)) fail(`draft present in dist: ${d}`);

// --- HTTP status codes from a local server
const server = createServer(DIST).listen(0);
const port = server.address().port;
const status = async (p) => (await fetch(`http://localhost:${port}${p}`, { redirect: 'manual' })).status;
for (const l of locs) if ((await status(l)) !== 200) fail(`HTTP ${await status(l)} for ${l}`);
for (const p of ['/tiada-halaman/', '/panduan/artikel-tidak-wujud/', ...draftUrls]) {
  const s = await status(p); if (s !== 404) fail(`expected 404 for ${p}, got ${s}`);
}
server.close();

// --- external sources (optional)
if (process.argv.includes('--external')) {
  for (const u of extLinks) {
    try {
      const r = await fetch(u, { redirect: 'follow', headers: { 'User-Agent': 'Mozilla/5.0 (link check)' }, signal: AbortSignal.timeout(20000) });
      if (r.status >= 400) fail(`external ${r.status}: ${u}`);
    } catch (e) { fail(`external error: ${u} (${e.message})`); }
  }
}

console.log(`Checked ${pages.size} HTML files, ${locs.length} sitemap URLs, ${extLinks.size} external links${process.argv.includes('--external') ? ' (fetched)' : ' (not fetched)'}.`);
for (const n of [...new Set(notes)]) console.log('note:', n);
if (errors.length) { console.error(`\n${errors.length} problem(s):\n  ` + errors.join('\n  ')); process.exit(1); }
console.log('All checks passed.');
