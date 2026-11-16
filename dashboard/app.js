const $ = id => document.getElementById(id);
const descriptions = [
  ['Queue & intake', 'Understand the request and gather the essentials.'],
  ['Planning', 'Define scope, priorities, and acceptance checks.'],
  ['Project setup', 'Prepare the stack, workspace, and preview.'],
  ['SERP research', 'Research search intent and useful opportunities.'],
  ['Site architecture', 'Map pages, queries, and internal links.'],
  ['Content & snippets', 'Write useful copy and accurate search previews.'],
  ['Design & development', 'Build a responsive, accessible website.'],
  ['Technical SEO', 'Check crawlability, metadata, and search appearance.'],
  ['Quality review', 'Verify the site and its supporting evidence.'],
  ['Release', 'Prepare or verify the production launch.'],
  ['Measurement', 'Track real search data and plan improvements.']
];
let selected = '', current = null, token = '', dirty = false, busy = false, lastBrief = '';
function node(tag, className, text) { const element = document.createElement(tag); if (className) element.className = className; if (text !== undefined) element.textContent = text; return element; }
function notice(message, error = false) { $('notice').hidden = false; $('notice').className = 'notice' + (error ? ' error' : ''); $('notice').textContent = message; }
async function api(url, options = {}) { const response = await fetch(url, {...options, headers: {'Content-Type': 'application/json', 'X-Dashboard-Token': token, ...options.headers}}); const data = await response.json(); if (!response.ok) throw new Error(data.error || 'Request failed'); return data; }
function render(job) {
  current = job;
  const tasks = job.tasks, next = tasks.find(t => t.status !== 'done');
  const done = tasks.filter(t => t.status === 'done').length;
  $('project-name').textContent = job.project_name === 'Replace with your website name' ? 'Your first website' : job.project_name;
  $('project-status').textContent = !next ? 'Completed' : next.status === 'failed' ? 'Needs your input' : next.status === 'running' ? 'Agent working' : 'Ready for agent';
  $('progress').textContent = `${Math.round(done / tasks.length * 100)}%`;
  $('progress-bar').style.width = `${done / tasks.length * 100}%`;
  $('progress-caption').textContent = `${done} of ${tasks.length} stages completed`;
  $('running').textContent = tasks.filter(t => t.status === 'running').length;
  $('blocked').textContent = tasks.filter(t => t.status === 'failed').length;
  $('file-count').textContent = job.files.length;
  $('attention-title').textContent = next?.status === 'failed' ? 'A little context will get things moving.' : next?.status === 'running' ? 'An agent has claimed the current task.' : next ? 'Ready for the next handoff.' : 'Every workflow stage is complete.';
  $('attention-text').textContent = next?.failure || (next?.status === 'running' ? 'Progress updates will appear as the agent saves its work and completes the stage.' : next ? 'The queue is ready. Ask your coding agent to continue this job using ORCHESTRATOR.md.' : 'Review the release status and measurement plan in your deliverables.');
  $('attention-action').textContent = next?.id === '01' ? 'Complete brief ↗' : 'View pipeline ↗';
  $('attention-action').href = next?.id === '01' ? '#brief' : '#pipeline';
  $('next-title').textContent = next ? descriptions[Number(next.id) - 1][0] : 'Review your results';
  $('next-description').textContent = next ? `${next.agent} · ${next.status === 'failed' ? 'Waiting for required information or a fix.' : next.status === 'running' ? 'Task is claimed in the queue.' : 'Waiting to be claimed by the agent runner.'}` : 'Check the saved evidence and plan your next improvement cycle.';
  $('retry').disabled = busy || next?.status !== 'failed';
  const stages = $('stages'); stages.replaceChildren();
  for (const task of tasks) {
    const [title, description] = descriptions[Number(task.id) - 1];
    const row = node('div', `stage ${task.status}`), text = node('div');
    text.append(node('h3', '', title), node('p', '', description));
    row.append(node('span', 'stage-icon', task.status === 'done' ? '✓' : task.status === 'failed' ? '!' : task.id), text, node('span', 'stage-status', {pending: 'Queued', failed: 'Needs input', running: 'Running', done: 'Complete'}[task.status]));
    stages.append(row);
  }
  const files = $('files'); files.replaceChildren();
  if (!job.files.length) files.append(node('p', 'empty', 'Agent outputs will appear here when saved.'));
  for (const name of job.files) { const button = node('button', 'file', `▤  ${name}  ↗`); button.addEventListener('click', () => openArtifact(job.id, name)); files.append(button); }
  const events = $('events'); events.replaceChildren();
  const history = [{at: job.created_at, action: 'created'}, ...job.events].reverse();
  const labels = {created: 'Workflow created', claim: 'Agent claimed task', fail: 'Task needs attention', complete: 'Stage completed', retry: 'Task returned to queue', reopen: 'Stage reopened', brief_updated: 'Website brief updated'};
  for (const event of history) {
    const item = node('div', 'event');
    item.append(node('strong', '', labels[event.action] || event.action));
    if (event.stage) item.append(node('p', '', `Stage ${event.stage} · ${descriptions[Number(event.stage) - 1]?.[0] || ''}`));
    if (event.reason) item.append(node('p', '', event.reason));
    const time = node('time', '', new Date(event.at).toLocaleString([], {month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'})); time.dateTime = event.at; item.append(time); events.append(item);
  }
  const serialized = JSON.stringify(job.brief);
  if (!dirty && serialized !== lastBrief) {
    for (const [key, value] of Object.entries(job.brief)) { const input = $('brief-form').elements.namedItem(key); if (input) input.value = key === 'project_name' && value === 'Replace with your website name' ? '' : value; }
    lastBrief = serialized;
  }
  const editable = !tasks.some(t => t.status === 'running' || t.status === 'done');
  for (const input of $('brief-form').elements) input.disabled = busy || !editable;
  if (!editable) $('save-brief').textContent = 'Brief locked during execution';
  else $('save-brief').textContent = 'Save website brief ↗';
}
async function refresh() {
  try {
    const data = await api('/api/jobs');
    const select = $('project-select'); select.replaceChildren();
    if (!data.jobs.some(j => j.id === selected)) selected = data.jobs[0]?.id || '';
    for (const job of data.jobs) { const option = node('option', '', job.project_name === 'Replace with your website name' ? 'Your first website' : job.project_name); option.value = job.id; select.append(option); }
    select.value = selected;
    const job = data.jobs.find(j => j.id === selected);
    if (job) render(job); else { current = null; $('project-name').textContent = 'No jobs found'; notice('Initialize a workflow job to show its progress here.'); }
    $('connection').textContent = 'Live queue · 3s sync'; $('connection').className = 'connection';
    $('updated').textContent = `Last synced ${new Date(data.refreshed_at).toLocaleTimeString()}`;
  } catch (error) { $('connection').textContent = 'Disconnected'; $('connection').className = 'connection offline'; notice('Cannot reach the local queue. ' + error.message, true); }
}
async function openArtifact(job, name) {
  try { const data = await api(`/api/jobs/${job}/artifact?name=${encodeURIComponent(name)}`); $('artifact-name').textContent = data.name; $('artifact-content').textContent = data.content; $('artifact-dialog').showModal(); } catch (error) { notice(error.message, true); }
}
$('brief-form').addEventListener('input', () => {dirty = true;});
$('brief-form').addEventListener('submit', async event => {
  event.preventDefault(); if (!current || busy) return;
  const values = Object.fromEntries(new FormData(event.target)); busy = true; $('save-brief').disabled = true;
  try { const data = await api(`/api/jobs/${selected}/brief`, {method: 'POST', body: JSON.stringify(values)}); dirty = false; lastBrief = ''; notice(data.message); } catch (error) { notice(error.message, true); }
  finally { busy = false; await refresh(); }
});
$('retry').addEventListener('click', async () => {
  if (!current || busy) return; busy = true; $('retry').disabled = true;
  try { const data = await api(`/api/jobs/${selected}/retry`, {method: 'POST', body: '{}'}); notice(data.message); } catch (error) { notice(error.message, true); }
  finally { busy = false; await refresh(); }
});
$('project-select').addEventListener('change', event => { if (dirty && !confirm('Switch projects and discard unsaved brief edits?')) {event.target.value = selected; return;} selected = event.target.value; dirty = false; lastBrief = ''; refresh(); });
$('refresh').addEventListener('click', refresh);
$('close-dialog').addEventListener('click', () => $('artifact-dialog').close());
async function start() { try { token = (await api('/api/session')).token; await refresh(); setInterval(refresh, 3000); } catch (error) { notice(error.message, true); } }
start();
