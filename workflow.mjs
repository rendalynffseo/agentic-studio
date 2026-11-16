// Sequential queue for a single orchestrator. Node.js 18+, no dependencies.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import crypto from 'node:crypto';
import {recommendTemplate,applySelectionToBrief,loadTemplateLibrary} from './lib/template-selection.mjs';
import {normalizeUserContent,activeUserContent,prepareUserContent,validatePlacementMap,verifyUserContent,saveUserContent} from './lib/user-content.mjs';

const roles = ['queue', 'planning', 'setup', 'research', 'architecture', 'content', 'development', 'technical-seo', 'qa', 'release', 'measurement'];
const now = () => new Date().toISOString();
const read = file => JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
function save(file, value) {
  fs.writeFileSync(file + '.tmp', JSON.stringify(value, null, 2) + '\n');
  fs.renameSync(file + '.tmp', file);
}
function requireThat(condition, message) { if (!condition) throw new Error(message); }
function evidence(job, value) {
  requireThat(typeof value === 'string' && value.trim(), 'Evidence needs a file path');
  const file = fs.realpathSync(path.resolve(job, value));
  const relative = path.relative(fs.realpathSync(job), file);
  requireThat(relative && relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative), 'Evidence must stay inside the job directory');
  const stat = fs.statSync(file);
  requireThat(stat.isFile() && stat.size > 0, `Missing or empty evidence: ${value}`);
  return file;
}
function validate(job, task) {
  const file = evidence(job, task.artifact);
  const data = read(file);
  requireThat(data && typeof data === 'object' && !Array.isArray(data), 'Deliverable must be an object');
  requireThat(data.stage_id === task.id && data.agent === task.agent, 'Deliverable stage_id/agent mismatch');
  for (const key of ['summary', 'handoff']) requireThat(typeof data[key] === 'string' && data[key].trim(), `Missing ${key}`);
  for (const key of ['decisions', 'assumptions', 'sources', 'outputs', 'checks', 'limitations']) requireThat(Array.isArray(data[key]), `Missing ${key} list`);
  requireThat(data.outputs.length && data.checks.length, 'Substantive outputs and checks are required');
  for (const output of data.outputs) requireThat(evidence(job, output) !== file, 'Deliverable cannot be its own substantive output');
  for (const check of data.checks) {
    requireThat(check && typeof check.name === 'string' && check.name.trim(), 'Check needs a name');
    requireThat(check.passed === true, `Check has not passed: ${check.name}`);
    requireThat(evidence(job, check.evidence) !== file, 'Checks need substantive saved evidence');
  }
  const brief = read(path.join(job, 'brief.json'));
  if (['06','07','09'].includes(task.id) && activeUserContent(brief).length) {
    requireThat(data.user_content, 'Supplied content needs source and placement evidence');
    const snapshot = read(evidence(job, data.user_content.source_evidence));
    const placement = read(evidence(job, data.user_content.placement_evidence));
    validatePlacementMap(brief, snapshot, placement);
    if (task.id !== '06') {
      requireThat(typeof brief.project_path === 'string' && brief.project_path.trim(), 'Set project_path before verifying supplied copy in the built site');
      const project = fs.realpathSync(path.resolve(fileURLToPath(new URL('.', import.meta.url)), brief.project_path));
      requireThat(typeof data.user_content.output_directory === 'string', 'Record the built output directory relative to the project');
      const output = fs.realpathSync(path.resolve(project, data.user_content.output_directory));
      const relative = path.relative(project, output);
      requireThat(relative !== '..' && !relative.startsWith('..'+path.sep) && !path.isAbsolute(relative), 'Content output must stay inside the website project');
      const verified = verifyUserContent(brief, snapshot, placement, output);
      requireThat(verified.passed, 'Built pages do not contain every supplied block exactly: '+verified.blocks.filter(b=>!b.passed).map(b=>b.block_id).join(', '));
      const report = read(evidence(job, data.user_content.verification_evidence));
      requireThat(report.passed === true && report.source_sha256 === verified.source_sha256 && report.output_directory === output, 'Save the current exact-content verification report');
    }
  }
  if (task.id === '07' && brief.design_catalog_url) {
    const catalog = read(fileURLToPath(new URL('./config/template-catalog.json', import.meta.url)));
    const design = data.design;
    requireThat(design && design.catalog_url === brief.design_catalog_url && design.catalog_url === catalog.catalog_url, 'Design must identify the required template catalog');
    const selected = catalog.templates.find(template => template.id === design.template_id);
    requireThat(selected, 'Design must select a template from the catalog');
    requireThat(!brief.design_template_id || brief.design_template_id === 'auto' || brief.design_template_id === selected.id, 'Design template does not match the brief');
    requireThat(design.download_url === catalog.catalog_url + '/downloads/' + selected.download, 'Design must record the selected source download URL');
    const source = evidence(job, design.source_evidence);
    const hash = crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex');
    requireThat(design.stylesheet_sha256 === hash, 'Template source stylesheet checksum does not match saved evidence');
    evidence(job, design.adaptation_evidence);
    if (brief.design_selection_required) {
      const {library} = loadTemplateLibrary();
      const installed = library.templates.find(template => template.id === selected.id);
      requireThat(brief.design_selected_template_id === selected.id, 'Design does not match the task’s selected template');
      requireThat(design.stylesheet_sha256 === installed.stylesheet_sha256, 'Source evidence is not the installed template stylesheet');
      requireThat(brief.design_library_version === library.version && design.library_version === library.version, 'Template library selection is stale; review it again');
      const choice = read(evidence(job, design.selection_evidence));
      requireThat(choice.template_id === selected.id && choice.library_version === library.version && typeof choice.reason === 'string' && choice.reason.trim(), 'Template selection evidence is missing or inconsistent');
    }
  }
}

export function run(argv) {
  const [command, ...rest] = argv;
  const allowed = {init: ['brief'], status: [], next: [], claim: ['agent'], complete: ['agent'], fail: ['agent', 'reason'], retry: [], reopen: ['stage', 'reason'], 'set-content':['input']};
  if (!command || command === '--help') {
    console.log('node workflow.mjs <init|status|next|claim|complete|fail|retry|reopen|set-content> --job <directory>\ninit: --brief <json>\nclaim/complete/fail: --agent <name>\nfail/reopen: --reason <text>\nreopen: --stage <01..11>\nset-content: --input <content JSON>');
    return;
  }
  requireThat(Object.hasOwn(allowed, command), 'Unknown command');
  const args = {};
  for (let i = 0; i < rest.length; i += 2) {
    requireThat(rest[i].startsWith('--') && rest[i + 1] && !rest[i + 1].startsWith('--'), 'Options require values');
    const key = rest[i].slice(2);
    requireThat(['job', ...allowed[command]].includes(key) && !Object.hasOwn(args, key), `Unknown or repeated option: ${key}`);
    args[key] = rest[i + 1];
  }
  for (const key of ['job', ...allowed[command]]) requireThat(args[key]?.trim(), `Missing --${key}`);
  const job = path.resolve(args.job);
  const stateFile = path.join(job, 'state.json');
  if (command === 'init') {
    const brief = read(args.brief);
    requireThat(brief && typeof brief.project_name === 'string' && brief.project_name.trim() && typeof brief.request === 'string' && brief.request.trim(), 'Brief needs project_name and request');
    requireThat(!fs.existsSync(job) || fs.readdirSync(job).length === 0, 'Use a new or empty job directory');
    const selection = recommendTemplate(brief);
    const selectedBrief = {...applySelectionToBrief(brief, selection),...normalizeUserContent(brief)};
    fs.mkdirSync(path.join(job, 'artifacts'), {recursive: true});
    save(path.join(job, 'brief.json'), selectedBrief);
    save(path.join(job, 'artifacts/template-selection.json'), selection);
    prepareUserContent(job, selectedBrief);
    save(stateFile, {version: 1, project_name: brief.project_name, created_at: now(), tasks: roles.map((role, i) => {
      const id = String(i + 1).padStart(2, '0');
      return {id, agent: role + '-agent', status: 'pending', attempts: 0, artifact: `artifacts/${id}-${role}.json`};
    }), design_selection: {template_id:selection.template_id,name:selection.template_name,mode:selection.mode,reason:selection.reason,artifact:'artifacts/template-selection.json'}, events: [{at:now(),action:'template_selected',stage:'02',reason:`${selection.template_id} — ${selection.template_name}: ${selection.reason}`} ]});
    console.log(`Created ${job}; read ORCHESTRATOR.md before executing tasks.`);
    return;
  }
  if (command === 'set-content') { console.log(JSON.stringify(saveUserContent(job, read(args.input)),null,2)); return; }
  const state = read(stateFile);
  let task = state.tasks.find(t => t.status !== 'done');
  if (command === 'status') {
    console.log(`Project: ${state.project_name}`);
    for (const item of state.tasks) console.log(`${item.id}  ${item.status.padEnd(7)}  ${item.agent}  attempts=${item.attempts}`);
    return;
  }
  if (command === 'next') { console.log(JSON.stringify(task ?? {status: 'complete'}, null, 2)); return; }
  if (command === 'reopen') {
    task = state.tasks.find(t => t.id === args.stage);
    requireThat(task, 'Unknown stage; use 01 through 11');
    for (const item of state.tasks.filter(t => Number(t.id) >= Number(args.stage))) {
      item.status = 'pending';
      for (const key of ['started_at', 'completed_at', 'failure']) delete item[key];
    }
  } else {
    requireThat(task, 'All tasks are complete; reopen a stage or create a new job');
    if (['claim', 'complete', 'fail'].includes(command)) requireThat(args.agent === task.agent, `Next task belongs to ${task.agent}`);
    if (command === 'claim') {
      requireThat(task.status === 'pending', 'Only pending tasks can be claimed');
      Object.assign(task, {status: 'running', started_at: now(), attempts: task.attempts + 1});
    } else if (command === 'complete') {
      requireThat(task.status === 'running', 'Claim the task before completing it');
      validate(job, task);
      Object.assign(task, {status: 'done', completed_at: now()});
    } else if (command === 'fail') {
      requireThat(task.status === 'running', 'Only running tasks can fail');
      Object.assign(task, {status: 'failed', failure: args.reason});
    } else if (command === 'retry') {
      requireThat(task.status === 'failed', 'Only failed tasks can be retried');
      task.status = 'pending';
      delete task.failure;
    }
  }
  state.events.push({at: now(), action: command, stage: task.id, ...(args.reason ? {reason: args.reason} : {})});
  save(stateFile, state);
  console.log(JSON.stringify(task, null, 2));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { run(process.argv.slice(2)); } catch (error) { console.error(`Error: ${error.message}`); process.exitCode = 1; }
}
