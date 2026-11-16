// Local static server for dist/ (or preview/ with --preview). Returns real 404s.
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const dir = path.resolve(process.argv.includes('--preview') ? 'preview' : 'dist');
const port = Number(process.env.PORT || 4173);
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8' };

export function createServer(root = dir) {
  return http.createServer(async (req, res) => {
    const url = new URL(req.url, 'http://x');
    let p = path.normalize(decodeURIComponent(url.pathname));
    if (p.includes('..')) { res.writeHead(400).end(); return; }
    // Directory without trailing slash → 301 to canonical form
    const file = path.join(root, p);
    try {
      const st = await fs.stat(file);
      if (st.isDirectory()) {
        if (!p.endsWith('/')) { res.writeHead(301, { Location: p + '/' }).end(); return; }
        p = path.join(p, 'index.html');
      }
      const body = await fs.readFile(path.join(root, p));
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }).end(body);
    } catch {
      const body = await fs.readFile(path.join(root, '404.html')).catch(() => 'Not found');
      res.writeHead(404, { 'Content-Type': TYPES['.html'] }).end(body);
    }
  });
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  createServer().listen(port, () => console.log(`Serving ${dir} on http://localhost:${port}`));
}
