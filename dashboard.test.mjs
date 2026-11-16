import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {createServer} from './dashboard-server.mjs';

test('dashboard serves actual queue and restricts mutations and file access', async () => {
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), 'dashboard-test-'));
  const jobDirectory = path.join(workspace, 'jobs', 'first-site');
  const init = spawnSync(process.execPath, ['workflow.mjs', 'init', '--brief', 'templates/brief.json', '--job', jobDirectory], {encoding: 'utf8'});
  assert.equal(init.status, 0, init.stderr);
  const stateFile = path.join(jobDirectory, 'state.json');
  const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  state.events.push({action: 'fail', reason: 'Fixture intake needs details'});
  fs.writeFileSync(stateFile, JSON.stringify(state));
  fs.writeFileSync(path.join(jobDirectory, 'artifacts', 'intake-notes.md'), 'awaiting essential user information');
  const server = createServer({workspace});
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  try {
    assert.equal((await fetch(origin)).status, 200);
    const jobs = await (await fetch(origin + '/api/jobs')).json();
    assert.ok(Array.isArray(jobs.jobs));
    const job = jobs.jobs.find(j => j.id === 'first-site');
    assert.ok(job);
    assert.equal(job.tasks.length, 11);
    assert.ok(job.events.some(event => event.action === 'fail'));
    assert.equal((await fetch(origin + '/api/jobs/first-site/retry', {method: 'POST', body: '{}'})).status, 403);
    const {token} = await (await fetch(origin + '/api/session')).json();
    const invalidBrief = await fetch(origin + '/api/jobs/first-site/brief', {method: 'POST', headers: {'Origin': origin, 'X-Dashboard-Token': token}, body: '{}'});
    const expectedBriefStatus = job.tasks.some(task => task.status === 'running' || task.status === 'done') ? 409 : 400;
    assert.equal(invalidBrief.status, expectedBriefStatus);
    assert.equal((await fetch(origin + '/api/jobs/first-site/artifact?name=..%2Fbrief.json')).status, 400);
    const report = await (await fetch(origin + '/api/jobs/first-site/artifact?name=intake-notes.md')).json();
    assert.match(report.content, /awaiting essential user information/);
    assert.equal((await fetch(origin + '/state.json')).status, 404);
    const hostStatus = await new Promise((resolve, reject) => {
      const request = http.get(origin, {headers: {Host: 'untrusted.example:4311'}}, response => {response.resume(); resolve(response.statusCode);});
      request.on('error', reject);
    });
    assert.equal(hostStatus, 403);
  } finally { await new Promise(resolve => server.close(resolve)); fs.rmSync(workspace, {recursive: true, force: true}); }
});
