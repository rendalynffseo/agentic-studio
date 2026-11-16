import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {loadTemplateLibrary,recommendTemplate,selectForJob,prepareSelectedTemplate,workspaceRoot} from './lib/template-selection.mjs';

test('all 13 source templates and every imported file match the downloaded bundle',()=>{
 const {library}=loadTemplateLibrary();assert.equal(library.templates.length,13);
 const extraction=JSON.parse(fs.readFileSync(path.join(workspaceRoot,'vendor/templates/library-extraction.json'),'utf8'));
 assert.equal(extraction.files.length,277);
 for(const file of extraction.files){const bytes=fs.readFileSync(path.join(workspaceRoot,extraction.directory,file.path));assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),file.sha256,file.path);}
 assert.equal(library.templates.find(t=>t.id==='t12').source_kind,'node-static');
});
test('layout and palette examples can select every template, without defaulting everything to App Guide',()=>{
 const cases=[['t1','A red gold one-page campaign landing page'],['t2','Android app guide explaining permissions'],['t3','A navy sidebar catalog with portrait cards'],['t4','An orange portal with category pages'],['t5','Teal gold gradients and carousel section chips'],['t6','A green yellow directory'],['t7','An analytics dashboard with a three-column search workspace'],['t8','A royal purple and white catalog'],['t9','Charcoal and yellow tables for comparison'],['t10','A cream rose and maroon magazine'],['t11','A neon teal navy comparison grid'],['t12','A red black educational searchable blog with articles'],['t13','A sky blue glossary and knowledge base']];
 for(const [id,request] of cases){const choice=recommendTemplate({request,design_template_id:'auto'});assert.equal(choice.template_id,id,request);assert.equal(choice.ranking.length,13);assert.equal(choice.mode,'automatic');assert.ok(choice.reason);}
});
test('explicit choices win, valid agent overrides are explained, and ambiguity is recorded',()=>{
 const explicit=recommendTemplate({request:'A green analytics dashboard',design_template_id:'t8'});assert.equal(explicit.template_id,'t8');assert.equal(explicit.mode,'explicit');
 assert.throws(()=>recommendTemplate({design_template_id:'t99'}),/Unknown requested/);
 assert.throws(()=>recommendTemplate({design_template_id:'t8'},{overrideId:'t7',overrideReason:'different'}),/explicit user/);
 assert.throws(()=>recommendTemplate({design_template_id:'auto'},{overrideId:'t7'}),/reason/);
 const override=recommendTemplate({request:'A documentation guide'},{overrideId:'t13',overrideReason:'The approved architecture is a glossary.'});assert.equal(override.template_id,'t13');assert.equal(override.mode,'agent_override');
 const fallback=recommendTemplate({request:'Create a useful website designed for organic search visibility, qualified clicks, and conversions.'});assert.equal(fallback.template_id,'t2');assert.equal(fallback.provisional,true);assert.equal(fallback.confidence,'low');
 assert.equal(recommendTemplate({design_preferences:{site_type:'dashboard',palette:['green'],layout:'three column'}}).template_id,'t7');
});
test('new jobs select automatically, prepare real source, and prevent changing reviewed work',()=>{
 const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'template-job-'));const briefFile=path.join(temporary,'brief.json'),job=path.join(temporary,'job');
 fs.writeFileSync(briefFile,JSON.stringify({project_name:'Analytics workspace',request:'Create an analytics dashboard with search',business:'Reporting workspace'}));
 const result=spawnSync(process.execPath,[path.join(workspaceRoot,'workflow.mjs'),'init','--brief',briefFile,'--job',job],{encoding:'utf8'});assert.equal(result.status,0,result.stderr);
 const brief=JSON.parse(fs.readFileSync(path.join(job,'brief.json'),'utf8'));assert.equal(brief.design_template_id,'auto');assert.equal(brief.design_selected_template_id,'t7');assert.equal(brief.design_selection_required,true);
 const state=JSON.parse(fs.readFileSync(path.join(job,'state.json'),'utf8'));assert.equal(state.design_selection.template_id,'t7');assert.ok(state.events.some(e=>e.action==='template_selected'));
 const selected=selectForJob(job,{overrideId:'t13',overrideReason:'Owner prefers a glossary architecture.'});assert.equal(selected.template_id,'t13');
 const provenance=prepareSelectedTemplate(job);assert.equal(provenance.template_id,'t13');assert.ok(fs.existsSync(path.join(job,provenance.source_evidence)));assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(job,provenance.source_evidence))).digest('hex'),provenance.stylesheet_sha256);
 const current=JSON.parse(fs.readFileSync(path.join(job,'state.json'),'utf8'));current.tasks[6].status='done';fs.writeFileSync(path.join(job,'state.json'),JSON.stringify(current));assert.throws(()=>selectForJob(job),/Reopen design/);assert.throws(()=>prepareSelectedTemplate(job),/Reopen design/);
});
