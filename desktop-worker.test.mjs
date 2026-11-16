import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {EventEmitter} from 'node:events';
import {PassThrough} from 'node:stream';
import {spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {runWorker,acquireLock,engineArgs,redact,workspace,controlWorker,recoverWorker} from './lib/desktop-worker.mjs';

function fixture(){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'desktop-worker-')),job=path.join(root,'jobs','test');fs.mkdirSync(path.join(root,'desktop'),{recursive:true});
 const brief=path.join(root,'brief.json');fs.writeFileSync(brief,JSON.stringify({project_name:'Worker fixture',request:'A neutral test of role handoffs',workflow_team:'classic'}));
 const result=spawnSync(process.execPath,[path.join(workspace,'workflow.mjs'),'init','--brief',brief,'--job',job],{encoding:'utf8'});assert.equal(result.status,0,result.stderr);
 fs.writeFileSync(path.join(root,'workflow.mjs'),`import {run} from ${JSON.stringify(pathToFileURL(path.join(workspace,'workflow.mjs')).href)};try{run(process.argv.slice(2));}catch(e){console.error(e.message);process.exitCode=1;}`);
 const state=JSON.parse(fs.readFileSync(path.join(job,'state.json'),'utf8'));state.tasks=state.tasks.slice(0,2);fs.writeFileSync(path.join(job,'state.json'),JSON.stringify(state));
 return {root,job,state:()=>JSON.parse(fs.readFileSync(path.join(job,'state.json'),'utf8')),cleanup:()=>fs.rmSync(root,{recursive:true,force:true})};
}
function fakeEngine(fixture,{complete=true,forge=false,onStarted}={}){
 return (engine,args)=>{
  assert.ok(args.includes('workspace-write'));assert.ok(!args.some(a=>a.includes('dangerously')));
  const child=new EventEmitter();child.stdout=new PassThrough();child.stderr=new PassThrough();child.stdin=new PassThrough();let prompt='';child.stdin.on('data',data=>prompt+=data);
  child.stdin.on('finish',()=>setImmediate(()=>{
   const task=fixture.state().tasks.find(t=>t.status==='running');assert.ok(task,'Desktop claims the assigned role before launch');assert.ok(prompt.includes(task.agent));assert.ok(prompt.includes('already claimed'));
   onStarted?.();
   if(complete){const evidence='artifacts/'+task.id+'-actual-output.md';fs.writeFileSync(path.join(fixture.job,evidence),'Output created by the simulated engine process.');fs.writeFileSync(path.join(fixture.job,task.artifact),JSON.stringify({stage_id:task.id,agent:task.agent,summary:'Fixture work',handoff:'Next queued role',decisions:[],assumptions:[],sources:[],outputs:[evidence],checks:[{name:'Fixture output',passed:true,evidence}],limitations:[]}));
    const result=spawnSync(process.execPath,[path.join(fixture.root,'workflow.mjs'),'complete','--job',fixture.job,'--agent',task.agent],{encoding:'utf8'});assert.equal(result.status,0,result.stderr);
    if(forge)fs.unlinkSync(path.join(fixture.job,evidence));
   }
   child.stdout.write(JSON.stringify({type:'item.completed',item:{type:'agent_message',text:'Role done'}})+'\n');child.emit('close',0);
  }));return child;
 };
}

test('desktop starts separate role processes and advances only verified completed tasks',async()=>{
 const f=fixture(),events=[];let calls=0;try{await runWorker({root:f.root,job:f.job,engine:'mock',checkLogin:false,emit:e=>events.push(e),launch:fakeEngine(f,{onStarted:()=>calls++})});assert.equal(calls,2);assert.ok(f.state().tasks.every(t=>t.status==='done'));assert.equal(events.at(-1).status,'complete');assert.ok(!fs.existsSync(path.join(f.root,'desktop/worker-runtime.lock')));}finally{f.cleanup();}
});
test('a successful engine exit without evidence never completes a role',async()=>{
 const f=fixture();try{await assert.rejects(runWorker({root:f.root,job:f.job,engine:'mock',checkLogin:false,launch:fakeEngine(f,{complete:false})}),/validated handoff/);assert.equal(f.state().tasks[0].status,'failed');assert.equal(f.state().tasks[1].status,'pending');}finally{f.cleanup();}
});
test('desktop independently rejects a completed role whose evidence was removed',async()=>{
 const f=fixture();try{await assert.rejects(runWorker({root:f.root,job:f.job,engine:'mock',checkLogin:false,launch:fakeEngine(f,{forge:true})}));assert.equal(f.state().tasks[0].status,'failed');assert.equal(f.state().tasks[1].status,'pending');}finally{f.cleanup();}
});
test('pause waits for the active role and does not launch the next worker',async()=>{
 const f=fixture(),control=new EventEmitter();let calls=0;try{await runWorker({root:f.root,job:f.job,engine:'mock',checkLogin:false,control,launch:fakeEngine(f,{onStarted:()=>{calls++;control.emit('command','pause');}})});assert.equal(calls,1);assert.equal(f.state().tasks[0].status,'done');assert.equal(f.state().tasks[1].status,'pending');assert.equal(JSON.parse(fs.readFileSync(path.join(f.job,'worker-status.json'),'utf8')).status,'paused');}finally{f.cleanup();}
});
test('stop preserves partial work and leaves the role failed, not completed',async()=>{
 const f=fixture(),control=new EventEmitter();try{await runWorker({root:f.root,job:f.job,engine:'mock',checkLogin:false,control,launch:fakeEngine(f,{complete:false,onStarted:()=>{fs.writeFileSync(path.join(f.job,'artifacts/partial.md'),'Partial work');control.emit('command','stop');}})});assert.equal(f.state().tasks[0].status,'failed');assert.ok(fs.existsSync(path.join(f.job,'artifacts/partial.md')));assert.equal(f.state().tasks[1].status,'pending');}finally{f.cleanup();}
});
test('global lock prevents duplicate workers and active external tasks are not taken over',async()=>{
 const f=fixture();try{const release=acquireLock(f.root,f.job);assert.throws(()=>acquireLock(f.root,f.job),/already running/);release();const state=f.state();state.tasks[0].status='running';fs.writeFileSync(path.join(f.job,'state.json'),JSON.stringify(state));await assert.rejects(runWorker({root:f.root,job:f.job,engine:'mock',checkLogin:false,launch:()=>{throw new Error('Must not launch');}}),/already marked running/);assert.equal(f.state().tasks[0].status,'running');assert.ok(!fs.existsSync(path.join(f.root,'desktop/worker-runtime.lock')));}finally{f.cleanup();}
});
test('worker keeps normal sandbox settings and masks credential-shaped log values',()=>{
 assert.ok(engineArgs(workspace).includes('--search'));assert.ok(!engineArgs(workspace).some(a=>a.includes('dangerously')));
 const secret='sk-proj-'+ 'A'.repeat(32);assert.ok(!redact('Authorization: Bearer '+secret+' key='+secret).includes(secret));
});
test('another desktop window addresses controls to the current lock owner',()=>{
 const f=fixture();try{const release=acquireLock(f.root,f.job);controlWorker(f.root,f.job,'pause');const request=JSON.parse(fs.readFileSync(path.join(f.root,'desktop/worker-control.json'),'utf8'));assert.equal(request.nonce,release.owner.nonce);assert.equal(request.command,'pause');assert.throws(()=>controlWorker(f.root,f.job,'unknown'));release();}finally{f.cleanup();}
});
test('recovery refuses a live owner and marks interrupted work for review without losing files',()=>{
 const f=fixture();try{const state=f.state();state.tasks[0].status='running';fs.writeFileSync(path.join(f.job,'state.json'),JSON.stringify(state));fs.writeFileSync(path.join(f.job,'artifacts/partial.md'),'Keep this');const release=acquireLock(f.root,f.job);assert.throws(()=>recoverWorker(f.root,f.job),/already running/);release();recoverWorker(f.root,f.job);assert.equal(f.state().tasks[0].status,'failed');assert.ok(fs.existsSync(path.join(f.job,'artifacts/partial.md')));assert.equal(f.state().tasks[1].status,'pending');}finally{f.cleanup();}
});
