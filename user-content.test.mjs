import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {normalizeUserContent,prepareUserContent,contentFingerprint,validatePlacementMap,renderUserContent,verifyUserContent,saveUserContent} from './lib/user-content.mjs';
import {workspaceRoot} from './lib/template-selection.mjs';
const example=()=>({content_mode:'hybrid',content_blocks:[{id:'hero-copy',label:'Hero heading',text:'  Your “exact” words & <tags> stay.\r\nSecond line — café 🎉\t',preserve_exact:true,placement:{page:'/',section:'hero'}}]});
function fixture(){const directory=fs.mkdtempSync(path.join(os.tmpdir(),'user-content-'));fs.mkdirSync(path.join(directory,'artifacts'));const brief=example();fs.writeFileSync(path.join(directory,'brief.json'),JSON.stringify(brief));const snapshot=prepareUserContent(directory,brief);const map={schema_version:1,source_sha256:snapshot.source_sha256,placements:[{block_id:'hero-copy',page:'/',section:'hero',reason:'This is the user-provided hero heading.',preserve_exact:true}]};return{directory,brief,snapshot,map};}
test('raw copy is retained, with only line-ending equivalence permitted',()=>{
 const input=example(),spec=normalizeUserContent(input);assert.equal(spec.content_blocks[0].text,input.content_blocks[0].text);
 assert.equal(contentFingerprint(input),contentFingerprint({...input,content_blocks:input.content_blocks.map(b=>({...b,text:b.text.replaceAll('\r\n','\n')}))}));
 assert.notEqual(contentFingerprint(input),contentFingerprint({...input,content_blocks:input.content_blocks.map(b=>({...b,text:b.text.trim()}))}));
 assert.throws(()=>normalizeUserContent({content_mode:'provided',content_blocks:[]}),/at least one/);
 assert.throws(()=>normalizeUserContent({...input,content_blocks:[{...input.content_blocks[0],preserve_exact:false}]}),/preserved exactly/);
 assert.throws(()=>normalizeUserContent({...input,content_blocks:[input.content_blocks[0],input.content_blocks[0]]}),/unique/);
 assert.throws(()=>normalizeUserContent({...input,content_blocks:[{...input.content_blocks[0],placement:{page:'/../private'}}]}),/Target page/);
});
test('every block gets a specific placement that honors explicit user choices',()=>{
 const {brief,snapshot,map}=fixture();assert.equal(validatePlacementMap(brief,snapshot,map),true);
 assert.throws(()=>validatePlacementMap(brief,snapshot,{...map,placements:[]}),/Every supplied/);
 assert.throws(()=>validatePlacementMap(brief,snapshot,{...map,placements:[{...map.placements[0],page:'/about/'}]}),/requested page/);
 assert.throws(()=>validatePlacementMap(brief,snapshot,{...map,placements:[{...map.placements[0],section:'footer'}]}),/requested section/);
 assert.throws(()=>validatePlacementMap(brief,snapshot,{...map,source_sha256:'stale'}),/current content/);
 assert.throws(()=>validatePlacementMap(brief,{...snapshot,blocks:[{...snapshot.blocks[0],text:'Changed'}]},map),/stale or changed/);
});
test('escaped exact copy passes output verification; omission, rewriting, comments, and duplicates fail',()=>{
 const {directory,brief,snapshot,map}=fixture(),site=path.join(directory,'site');fs.mkdirSync(site);
 const html=renderUserContent(brief.content_blocks[0],map.placements[0]);assert.ok(html.includes('&lt;tags&gt;'));assert.ok(!html.includes('<tags>'));
 const file=path.join(site,'index.html');fs.writeFileSync(file,`<!doctype html><html><body>${html}</body></html>`);
 assert.equal(verifyUserContent(brief,snapshot,map,site).passed,true);
 for(const changed of [html.replace('Your','Our'),'',`<!--${html}-->`,html+html,html.replace('data-content-section="hero"','data-content-section="footer"')]){fs.writeFileSync(file,changed);assert.equal(verifyUserContent(brief,snapshot,map,site).passed,false);}
 assert.throws(()=>renderUserContent(brief.content_blocks[0],map.placements[0],{tag:'script'}),/Unsupported/);
});
test('content changes reopen stage 06 onward, keep the live deployment record, and block concurrent editing',()=>{
 const {directory}=fixture();const state={tasks:Array.from({length:11},(_,i)=>({id:String(i+1).padStart(2,'0'),status:'done',completed_at:'old'})),events:[],deployment:{status:'succeeded',url:'https://example.test'}};fs.writeFileSync(path.join(directory,'state.json'),JSON.stringify(state));
 const changed=example();changed.content_blocks[0].text='A new exact paragraph.\nWith a second line.';const saved=saveUserContent(directory,changed);assert.equal(saved.changed,true);
 const next=JSON.parse(fs.readFileSync(path.join(directory,'state.json'),'utf8'));assert.ok(next.tasks.slice(0,5).every(t=>t.status==='done'));assert.ok(next.tasks.slice(5).every(t=>t.status==='pending'));assert.equal(next.deployment.status,'succeeded');assert.equal(saveUserContent(directory,changed).changed,false);
 next.tasks[5].status='running';fs.writeFileSync(path.join(directory,'state.json'),JSON.stringify(next));assert.throws(()=>saveUserContent(directory,example()),/active agent/);
});
test('writer stage cannot complete without the complete, current placement map',()=>{
 const directory=fs.mkdtempSync(path.join(os.tmpdir(),'content-queue-')),job=path.join(directory,'job'),briefFile=path.join(directory,'brief.json');fs.writeFileSync(briefFile,JSON.stringify({...example(),project_name:'Content fixture',request:'A neutral informational guide'}));
 function cli(command,options=[],expected=0){const result=spawnSync(process.execPath,[path.join(workspaceRoot,'workflow.mjs'),command,'--job',job,...options],{encoding:'utf8'});assert.equal(result.status,expected,result.stderr);}
 cli('init',['--brief',briefFile]);const state=JSON.parse(fs.readFileSync(path.join(job,'state.json'),'utf8'));fs.writeFileSync(path.join(job,'artifacts/report.md'),'Test fixture evidence.');
 for(const task of state.tasks.slice(0,6)){
  cli('claim',['--agent',task.agent]);const artifact={stage_id:task.id,agent:task.agent,summary:'Test fixture stage',handoff:'Next test fixture stage',decisions:[],assumptions:[],sources:[],outputs:['artifacts/report.md'],checks:[{name:'Fixture check',passed:true,evidence:'artifacts/report.md'}],limitations:[]};const file=path.join(job,task.artifact);
  if(task.id==='06'){
   fs.writeFileSync(file,JSON.stringify(artifact));cli('complete',['--agent',task.agent],1);
   const snapshot=JSON.parse(fs.readFileSync(path.join(job,'artifacts/user-content-source.json'),'utf8'));const map={schema_version:1,source_sha256:snapshot.source_sha256,placements:[]};fs.writeFileSync(path.join(job,'artifacts/content-placement.json'),JSON.stringify(map));artifact.user_content={source_evidence:'artifacts/user-content-source.json',placement_evidence:'artifacts/content-placement.json'};fs.writeFileSync(file,JSON.stringify(artifact));cli('complete',['--agent',task.agent],1);
   map.placements=[{block_id:'hero-copy',page:'/',section:'hero',reason:'Hero copy belongs in the hero.',preserve_exact:true}];fs.writeFileSync(path.join(job,'artifacts/content-placement.json'),JSON.stringify(map));
  }
  fs.writeFileSync(file,JSON.stringify(artifact));cli('complete',['--agent',task.agent]);
 }
 const brief=JSON.parse(fs.readFileSync(path.join(job,'brief.json'),'utf8'));const snapshot=JSON.parse(fs.readFileSync(path.join(job,'artifacts/user-content-source.json'),'utf8'));const map=JSON.parse(fs.readFileSync(path.join(job,'artifacts/content-placement.json'),'utf8'));
 const site=path.join(directory,'website'),output=path.join(site,'dist');fs.mkdirSync(output,{recursive:true});brief.project_path=site;fs.writeFileSync(path.join(job,'brief.json'),JSON.stringify(brief));const html=renderUserContent(brief.content_blocks[0],map.placements[0]);fs.writeFileSync(path.join(output,'index.html'),html);
 const verified=verifyUserContent(brief,snapshot,map,output);fs.writeFileSync(path.join(job,'artifacts/content-verification.json'),JSON.stringify(verified));
 const library=JSON.parse(fs.readFileSync(path.join(workspaceRoot,'vendor/templates/library-manifest.json'),'utf8'));const selected=library.templates.find(t=>t.id===brief.design_selected_template_id);fs.copyFileSync(path.join(workspaceRoot,selected.stylesheet_path),path.join(job,'artifacts/template-source.txt'));
 const task=state.tasks[6];cli('claim',['--agent',task.agent]);const artifact={stage_id:task.id,agent:task.agent,summary:'Static content-verification fixture',handoff:'Next fixture',decisions:[],assumptions:[],sources:[],outputs:['artifacts/report.md'],checks:[{name:'Fixture evidence',passed:true,evidence:'artifacts/report.md'}],limitations:[],design:{catalog_url:library.catalog_url,template_id:selected.id,download_url:selected.download_url,stylesheet_sha256:selected.stylesheet_sha256,source_evidence:'artifacts/template-source.txt',adaptation_evidence:'artifacts/report.md',library_version:library.version,selection_evidence:'artifacts/template-selection.json'},user_content:{source_evidence:'artifacts/user-content-source.json',placement_evidence:'artifacts/content-placement.json',verification_evidence:'artifacts/content-verification.json',output_directory:'dist'}};
 fs.writeFileSync(path.join(job,task.artifact),JSON.stringify(artifact));fs.writeFileSync(path.join(output,'index.html'),html.replace('Your','Our'));cli('complete',['--agent',task.agent],1);
 fs.writeFileSync(path.join(output,'index.html'),html);cli('complete',['--agent',task.agent]);
});
