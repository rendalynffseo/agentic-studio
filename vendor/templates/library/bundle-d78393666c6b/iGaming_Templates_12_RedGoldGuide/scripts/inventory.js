// Writes CONTENT-INVENTORY.md and content-inventory.csv from src/inventory.js.
import fs from 'node:fs/promises';
import { ARTICLES, CLUSTERS, HUBS, SOURCES } from '../src/inventory.js';

const urlOf = (a) => `${HUBS[CLUSTERS[a.cluster].hub].path}${a.slug}/`;
const role = (a) => (CLUSTERS[a.cluster].pillar === a.n ? 'Pillar' : `Supports ${CLUSTERS[a.cluster].pillar}`);
const src = (a) => a.sources.map((k) => SOURCES[k].label.split(' — ').pop()).join('; ') || '—';

let md = '# Content inventory\n\nGenerated from `src/inventory.js` by `node scripts/inventory.js`. Keyword targets are planning hypotheses, not measured data.\n\n';
for (const [k, c] of Object.entries(CLUSTERS)) {
  md += `## Cluster ${k} — ${c.name} (hub: ${HUBS[c.hub].path})\n\n| # | Title | URL | Primary keyword | Role | Status | Sources | Missing before publishing |\n|---|---|---|---|---|---|---|---|\n`;
  for (const a of ARTICLES.filter((x) => x.cluster === k))
    md += `| ${a.n} | ${a.title} | \`${urlOf(a)}\` | ${a.kw} | ${role(a)} | ${a.status === 'published' ? 'Published' : '**Draft**'} | ${src(a)} | ${(a.missing || []).join('; ') || '—'} |\n`;
  md += '\n';
}
const q = (s) => `"${String(s).replace(/"/g, '""')}"`;
const csv = ['n,cluster,title,slug,url,primary_keyword,role,status,sources,missing',
  ...ARTICLES.map((a) => [a.n, a.cluster, q(a.title), a.slug, urlOf(a), q(a.kw), q(role(a)), a.status, q(src(a)), q((a.missing || []).join('; '))].join(','))].join('\n');
await fs.writeFile('CONTENT-INVENTORY.md', md);
await fs.writeFile('content-inventory.csv', csv + '\n');
console.log('Wrote CONTENT-INVENTORY.md and content-inventory.csv');
