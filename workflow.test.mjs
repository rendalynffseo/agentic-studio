import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import crypto from 'node:crypto';

const root = path.dirname(fileURLToPath(import.meta.url));
test('sequential handoffs, evidence gates, retry, reopen, and full completion', () => {
  const job = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'seo-workflow-')), 'job');
  function cli(command, options = [], ok = true) {
    const result = spawnSync(process.execPath, [path.join(root, 'workflow.mjs'), command, '--job', job, ...options], {encoding: 'utf8'});
    assert.equal(result.status, ok ? 0 : 1, result.stderr);
    return result.stdout;
  }
  const state = () => JSON.parse(fs.readFileSync(path.join(job, 'state.json'), 'utf8'));
  const classicBrief=path.join(path.dirname(job),'classic-brief.json');
  fs.writeFileSync(classicBrief,JSON.stringify({...JSON.parse(fs.readFileSync(path.join(root,'templates/brief.json'),'utf8')),workflow_team:'classic'}));
  cli('init', ['--brief', classicBrief]);
  cli('init', ['--brief', path.join(root, 'templates/brief.json')], false);
  cli('claim', ['--agent', 'planning-agent'], false);
  cli('complete', ['--agent', 'queue-agent'], false);
  cli('claim', ['--agent', 'queue-agent']);
  cli('claim', ['--agent', 'queue-agent'], false);
  cli('complete', ['--agent', 'queue-agent'], false);
  cli('fail', ['--agent', 'queue-agent', '--reason', 'Need brief']);
  cli('claim', ['--agent', 'queue-agent'], false);
  cli('retry');
  for (const task of state().tasks) {
    cli('claim', ['--agent', task.agent]);
    const report = `artifacts/${task.id}-report.md`;
    fs.writeFileSync(path.join(job, report), 'Saved work and validation evidence');
    const artifact = {...JSON.parse(fs.readFileSync(path.join(root, 'templates/deliverable.json'), 'utf8')), stage_id: task.id, agent: task.agent, outputs: [report], checks: [{name: 'Role acceptance', passed: true, evidence: report}]};
    if (task.id === '07') {
      fs.writeFileSync(path.join(job, task.artifact), JSON.stringify(artifact));
      cli('complete', ['--agent', task.agent], false);
      const library = JSON.parse(fs.readFileSync(path.join(root, 'vendor/templates/library-manifest.json'), 'utf8'));
      const source = fs.readFileSync(path.join(root, library.templates.find(template => template.id === 't2').stylesheet_path));
      fs.writeFileSync(path.join(job, 'artifacts/template-source.txt'), source);
      artifact.design = {catalog_url: 'https://igaming-templates.vercel.app', template_id: 't2', download_url: 'https://igaming-templates.vercel.app/downloads/iGaming_Templates_2_AppGuide.zip', source_evidence: 'artifacts/template-source.txt', stylesheet_sha256: crypto.createHash('sha256').update(source).digest('hex'), adaptation_evidence: report, library_version: library.version, selection_evidence: 'artifacts/template-selection.json'};
      fs.writeFileSync(path.join(job, task.artifact), JSON.stringify({...artifact, design: {...artifact.design, stylesheet_sha256: 'wrong'}}));
      cli('complete', ['--agent', task.agent], false);
      fs.writeFileSync(path.join(job, task.artifact), JSON.stringify({...artifact, design: {...artifact.design, template_id: 'missing'}}));
      cli('complete', ['--agent', task.agent], false);
      const fabricated = '/* An unrelated stylesheet with a matching self-declared hash. */';
      fs.writeFileSync(path.join(job, 'artifacts/template-source.txt'), fabricated);
      fs.writeFileSync(path.join(job, task.artifact), JSON.stringify({...artifact, design: {...artifact.design, stylesheet_sha256: crypto.createHash('sha256').update(fabricated).digest('hex')}}));
      cli('complete', ['--agent', task.agent], false);
      fs.writeFileSync(path.join(job, 'artifacts/template-source.txt'), source);
    }
    fs.writeFileSync(path.join(job, task.artifact), JSON.stringify({...artifact, checks: [{name: 'Failed check', passed: false, evidence: report}]}));
    cli('complete', ['--agent', task.agent], false);
    fs.writeFileSync(path.join(job, task.artifact), JSON.stringify({...artifact, outputs: ['../outside.md']}));
    cli('complete', ['--agent', task.agent], false);
    fs.writeFileSync(path.join(job, task.artifact), JSON.stringify(artifact));
    cli('complete', ['--agent', task.agent]);
  }
  assert.equal(JSON.parse(cli('next')).status, 'complete');
  cli('reopen', ['--stage', '06', '--reason', 'Content correction']);
  assert.ok(state().tasks.slice(0, 5).every(t => t.status === 'done'));
  assert.ok(state().tasks.slice(5).every(t => t.status === 'pending'));
  assert.equal(JSON.parse(cli('next')).agent, 'content-agent');
});
