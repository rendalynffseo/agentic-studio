import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

const root = path.dirname(fileURLToPath(import.meta.url));
const token = crypto.randomBytes(24).toString('hex');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const save = (file, value) => { fs.writeFileSync(file + '.tmp', JSON.stringify(value, null, 2) + '\n'); fs.renameSync(file + '.tmp', file); };
const fields = ['project_name', 'business', 'audience', 'offer', 'conversion_goal', 'target_country', 'language', 'domain', 'additional_instructions'];
function jobPath(id, workspace = root) {
  if (!/^[a-zA-Z0-9_-]+$/.test(id)) throw new Error('Invalid job ID');
  const base = path.resolve(workspace, 'jobs');
  const directory = path.join(base, id);
  const actual = fs.realpathSync(directory);
  if (path.dirname(actual) !== fs.realpathSync(base)) throw new Error('Invalid job path');
  return directory;
}
function detail(id, workspace = root) {
  const directory = jobPath(id, workspace);
  const state = read(path.join(directory, 'state.json'));
  return {...state, id, brief: read(path.join(directory, 'brief.json')), tasks: state.tasks.map(task => ({...task, artifact_available: fs.existsSync(path.join(directory, task.artifact))})), files: fs.readdirSync(path.join(directory, 'artifacts')).filter(name => /\.(json|md|txt|csv|html)$/.test(name))};
}
async function body(req) {
  let value = '';
  for await (const chunk of req) { value += chunk; if (Buffer.byteLength(value) > 64000) throw new Error('Request too large'); }
  return JSON.parse(value);
}
export function createServer({workspace = root} = {}) {
  return http.createServer(async (req, res) => {
    const json = (status, value) => {res.writeHead(status, {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store'}); res.end(JSON.stringify(value));};
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'no-referrer');
    res.setHeader('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'");
    try {
      const host = req.headers.host || '';
      if (!/^(127\.0\.0\.1|localhost):\d+$/.test(host)) return json(403, {error: 'Local access only'});
      const url = new URL(req.url, `http://${host}`);
      if (req.method === 'GET' && url.pathname === '/api/session') return json(200, {token});
      if (req.method === 'GET' && url.pathname === '/api/jobs') {
        const directory = path.join(workspace, 'jobs');
        const jobs = fs.existsSync(directory) ? fs.readdirSync(directory, {withFileTypes: true}).filter(item => item.isDirectory() && /^[a-zA-Z0-9_-]+$/.test(item.name)).map(item => {try {return detail(item.name, workspace);} catch {return null;}}).filter(Boolean) : [];
        return json(200, {jobs, refreshed_at: new Date().toISOString()});
      }
      const match = url.pathname.match(/^\/api\/jobs\/([a-zA-Z0-9_-]+)\/(brief|retry|artifact)$/);
      if (match) {
        const directory = jobPath(match[1], workspace);
        const action = match[2];
        if (req.method === 'GET' && action === 'artifact') {
          const name = url.searchParams.get('name') || '';
          if (!/^[a-zA-Z0-9_.-]+\.(md|json|txt|csv|html)$/.test(name)) return json(400, {error: 'Invalid artifact name'});
          const file = fs.realpathSync(path.join(directory, 'artifacts', name));
          if (path.dirname(file) !== fs.realpathSync(path.join(directory, 'artifacts'))) return json(403, {error: 'Invalid artifact path'});
          return json(200, {name, content: fs.readFileSync(file, 'utf8').slice(0, 200000)});
        }
        if (req.method !== 'POST') return json(405, {error: 'Method not allowed'});
        if (req.headers.origin !== `http://${host}` || req.headers['x-dashboard-token'] !== token) return json(403, {error: 'Invalid dashboard session; refresh and try again'});
        if (action === 'brief') {
          const input = await body(req);
          const brief = read(path.join(directory, 'brief.json'));
          const state = read(path.join(directory, 'state.json'));
          if (state.tasks.some(t => t.status === 'running' || t.status === 'done')) return json(409, {error: 'Brief editing is available before agent execution. Reopen intake with the orchestrator to revise active work.'});
          for (const field of fields) {
            if (typeof input[field] !== 'string' || input[field].length > 8000) return json(400, {error: `Invalid ${field}`});
            brief[field] = input[field].trim();
          }
          if (!brief.project_name || !brief.business || !brief.offer) return json(400, {error: 'Enter a project name, business/topic, and offer.'});
          save(path.join(directory, 'brief.json'), brief);
          state.project_name = brief.project_name;
          state.events.push({at: new Date().toISOString(), action: 'brief_updated', stage: '01', reason: 'Website brief saved from dashboard'});
          save(path.join(directory, 'state.json'), state);
          return json(200, {message: 'Brief saved. Retry intake to make it ready for the agent runner.'});
        }
        if (action === 'retry') {
          const brief = read(path.join(directory, 'brief.json'));
          if (!brief.business?.trim() || !brief.offer?.trim() || !brief.project_name?.trim() || brief.project_name === 'Replace with your website name') return json(400, {error: 'Save your website name, business/topic, and offer before retrying.'});
          const result = spawnSync(process.execPath, [path.join(root, 'workflow.mjs'), 'retry', '--job', directory], {encoding: 'utf8', timeout: 10000});
          if (result.status !== 0) return json(409, {error: result.stderr.trim() || 'Retry failed'});
          return json(200, {message: 'Intake is queued. The agent runner must claim it; this dashboard does not launch AI workers.'});
        }
      }
      if (req.method === 'GET') {
        const assets = {'/': ['index.html', 'text/html'], '/app.js': ['app.js', 'text/javascript'], '/styles.css': ['styles.css', 'text/css']};
        const asset = assets[url.pathname];
        if (asset) {res.writeHead(200, {'Content-Type': asset[1] + '; charset=utf-8', 'Cache-Control': 'no-cache'}); return res.end(fs.readFileSync(path.join(root, 'dashboard', asset[0])));}
      }
      return json(404, {error: 'Not found'});
    } catch (error) { return json(400, {error: error.code === 'ENOENT' ? 'Job or artifact not found' : error.message}); }
  });
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT || 4311);
  const server = createServer();
  server.on('error', error => {console.error(error.message); process.exitCode = 1;});
  server.listen(port, '127.0.0.1', () => console.log(`Agentic dashboard: http://127.0.0.1:${port}`));
}
