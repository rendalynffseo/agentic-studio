import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {team,teamTasks} from './lib/agent-team.mjs';
import {saveUserContent} from './lib/user-content.mjs';

test('each specialist has one role and instructions; task scope selects only needed agents',()=>{
 assert.equal(team.agents.length,18);
 assert.equal(new Set(team.agents.map(a=>a.agent)).size,18);
 assert.equal(new Set(team.agents.map(a=>a.id)).size,18);
 for(const agent of team.agents)assert.ok(fs.readFileSync(agent.instruction_file,'utf8').includes(agent.agent));
 assert.equal(teamTasks({workflow_team:'classic'}).length,11);
 assert.equal(teamTasks({workflow_team:'specialist'}).length,14);
 const tasks=teamTasks({workflow_team:'specialist',blog_enabled:true,affiliate_links:[{url:'https://example.org/'}],content_mode:'provided',content_blocks:[{id:'copy'}]});
 assert.equal(tasks.length,18);
 assert.ok(tasks.findIndex(t=>t.agent==='template-selection-agent')<tasks.findIndex(t=>t.agent==='setup-agent'));
 assert.ok(tasks.findIndex(t=>t.agent==='blog-writing-agent')<tasks.findIndex(t=>t.agent==='development-agent'));
});

test('specialist handoffs, evidence requirements, nonnumeric order, and safe legacy upgrade',()=>{
 const directory=fs.mkdtempSync(path.join(os.tmpdir(),'agent-team-')),job=path.join(directory,'job'),briefFile=path.join(directory,'brief.json');
 function cli(command,args=[],status=0){const result=spawnSync(process.execPath,['workflow.mjs',command,'--job',job,...args],{encoding:'utf8'});assert.equal(result.status,status,result.stderr);return result.stdout;}
 const state=()=>JSON.parse(fs.readFileSync(path.join(job,'state.json'),'utf8'));
 try{
  fs.writeFileSync(briefFile,JSON.stringify({project_name:'Specialist fixture',request:'A neutral guide',workflow_team:'classic'}));cli('init',['--brief',briefFile]);
  cli('claim',['--agent','queue-agent']);cli('fail',['--agent','queue-agent','--reason','Intake clarification']);cli('upgrade-team');
  assert.equal(state().tasks.length,14);assert.equal(state().tasks[0].failure,'Intake clarification');cli('retry');
  const prompt=cli('agent-prompt',['--agent','queue-agent']);assert.match(prompt,/agents\/instructions\/queue-agent.md/);assert.match(prompt,/Pass to: planning-agent/);
  cli('agent-prompt',['--agent','development-agent'],1);cli('claim',['--agent','planning-agent'],1);
  function finish(task,outputs=['artifacts/evidence.md']){fs.writeFileSync(path.join(job,task.artifact),JSON.stringify({stage_id:task.id,agent:task.agent,summary:'Fixture output',handoff:'Next assigned role',decisions:[],assumptions:[],sources:[],outputs,checks:[{name:'Fixture evidence',passed:true,evidence:'artifacts/evidence.md'}],limitations:[]}));}
  fs.writeFileSync(path.join(job,'artifacts/evidence.md'),'Saved fixture output');
  for(const task of state().tasks.slice(0,2)){cli('claim',['--agent',task.agent]);finish(task);cli('complete',['--agent',task.agent]);}
  const selection=state().tasks[2];assert.equal(selection.agent,'template-selection-agent');cli('claim',['--agent',selection.agent]);finish(selection);cli('complete',['--agent',selection.agent],1);
  fs.writeFileSync(path.join(job,'artifacts/template-review.md'),'Reviewed actual selection and brief');finish(selection,['artifacts/evidence.md','artifacts/template-review.md']);cli('complete',['--agent',selection.agent]);
  assert.equal(JSON.parse(cli('next')).agent,'setup-agent');cli('upgrade-team',[],1);
  const completed=state();completed.tasks.forEach(t=>t.status='done');fs.writeFileSync(path.join(job,'state.json'),JSON.stringify(completed));
  cli('reopen',['--stage','17','--reason','UI revision']);const reopened=state(),boundary=reopened.tasks.findIndex(t=>t.id==='17');
  assert.ok(reopened.tasks.slice(0,boundary).every(t=>t.status==='done'));
  assert.ok(reopened.tasks.slice(boundary).every(t=>t.status==='pending'));
  assert.equal(JSON.parse(cli('next')).agent,'design-agent');
  saveUserContent(job,{content_mode:'provided',content_blocks:[{id:'copy',text:'Exact source copy',placement:{page:'auto',section:'auto'}}]});
  const updated=state();assert.equal(updated.tasks.find(t=>t.status!=='done').agent,'content-placement-agent');
  assert.ok(updated.tasks.slice(updated.tasks.findIndex(t=>t.agent==='content-placement-agent')).every(t=>t.status==='pending'));
 }finally{fs.rmSync(directory,{recursive:true,force:true});}
});
