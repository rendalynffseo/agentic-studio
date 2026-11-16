import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';

export const workspaceRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=file=>JSON.parse(fs.readFileSync(file,'utf8').replace(/^\uFEFF/,''));
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const normalize=value=>String(value??'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
function includes(text,phrase){const needle=normalize(phrase);return (' '+text+' ').includes(' '+needle+' ')||(' '+text+' ').includes(' '+needle+'s ');}
function checkedPath(root,relative){
 const file=fs.realpathSync(path.resolve(root,relative));const rel=path.relative(fs.realpathSync(root),file);
 if(!rel||rel==='..'||rel.startsWith('..'+path.sep)||path.isAbsolute(rel))throw new Error('Template path escaped the workspace');
 return file;
}
export function loadTemplateLibrary(root=workspaceRoot){
 const library=read(path.join(root,'vendor/templates/library-manifest.json'));
 const catalog=read(path.join(root,'config/template-catalog.json'));
 const profiles=read(path.join(root,'config/template-profiles.json'));
 if(library.catalog_url!==catalog.catalog_url||library.templates.length!==catalog.templates.length||new Set(library.templates.map(t=>t.id)).size!==catalog.templates.length)throw new Error('The installed library does not match the catalog');
 for(const template of library.templates){
  if(!catalog.templates.some(t=>t.id===template.id)||!profiles.profiles.some(t=>t.id===template.id))throw new Error('Missing catalog or selection profile');
  if(!template.ready||hash(checkedPath(root,template.stylesheet_path))!==template.stylesheet_sha256)throw new Error(`Template ${template.id} is missing or its source was changed; verify the library before selecting`);
 }
 return {library,catalog,profiles,root};
}
export function verifyTemplateSources(root=workspaceRoot){
 const {library}=loadTemplateLibrary(root);
 if(hash(checkedPath(root,library.archive_path))!==library.archive_sha256)throw new Error('The complete source archive checksum changed');
 const extraction=read(path.join(root,'vendor/templates/library-extraction.json'));
 if(extraction.archive_sha256!==library.version)throw new Error('Source extraction and library versions differ');
 for(const entry of extraction.files){const file=checkedPath(root,extraction.directory+'/'+entry.path);if(fs.statSync(file).size!==entry.length||hash(file)!==entry.sha256)throw new Error(`Template source mismatch: ${entry.path}`);}
 return {templates:library.templates.length,verified_source_files:extraction.files.length,version:library.version};
}
export function recommendTemplate(brief,{root=workspaceRoot,overrideId,overrideReason}={}){
 const {library,catalog,profiles}=loadTemplateLibrary(root);
 const requested=brief.design_template_id||'auto';
 if(brief.design_catalog_url&&brief.design_catalog_url!==catalog.catalog_url)throw new Error('Brief requests a different catalog');
 if(requested!=='auto'&&!library.templates.some(t=>t.id===requested))throw new Error(`Unknown requested template: ${requested}`);
 if(overrideId&&requested!=='auto'&&overrideId!==requested)throw new Error('An agent override cannot replace an explicit user template choice');
 if(overrideId&&(!overrideReason?.trim()||!library.templates.some(t=>t.id===overrideId)))throw new Error('An agent override needs a valid template ID and a reason');
 const prefs=brief.design_preferences||{};
 const fields=['business','audience','offer','additional_instructions','website_type','site_type'];
 const generic='Create a useful website designed for organic search visibility, qualified clicks, and conversions.';
 const request=brief.request===generic?'':brief.request;
 const text=normalize([...fields.map(key=>brief[key]),request,Array.isArray(prefs.palette)?prefs.palette.join(' '):prefs.palette,prefs.layout,prefs.site_type].filter(Boolean).join(' '));
 const siteType=normalize(prefs.site_type||brief.website_type||brief.site_type);
 const palette=normalize(Array.isArray(prefs.palette)?prefs.palette.join(' '):prefs.palette);
 const layout=normalize(prefs.layout);
 const ranking=library.templates.map(template=>{
  const profile=profiles.profiles.find(p=>p.id===template.id);let score=0;const reasons=[];
  for(const [signal,weight] of Object.entries(profile.signals))if(includes(text,signal)){score+=weight;reasons.push({signal,points:weight});}
  if(siteType&&siteType!=='auto'&&profile.site_types.some(type=>includes(siteType,type))){score+=25;reasons.push({signal:'Requested site type: '+siteType,points:25});}
  for(const color of profile.palette)if(palette&&includes(palette,color)){score+=12;reasons.push({signal:'Preferred palette: '+color,points:12});}
  for(const feature of profile.layout)if(layout&&layout!=='auto'&&includes(layout,feature)){score+=10;reasons.push({signal:'Preferred layout: '+feature,points:10});}
  return {id:template.id,name:template.name,score,reasons,style:template.style};
 }).sort((a,b)=>b.score-a.score||Number(a.id.slice(1))-Number(b.id.slice(1)));
 const noSignals=ranking[0].score===0;
 const id=overrideId||(requested!=='auto'?requested:noSignals?profiles.fallback_template_id:ranking[0].id);
 const chosen=library.templates.find(template=>template.id===id);
 const mode=overrideId?'agent_override':requested!=='auto'?'explicit':noSignals?'fallback':'automatic';
 const selectedRank=ranking.find(template=>template.id===id);
 const reason=overrideReason?.trim()||(mode==='explicit'?'Honor the explicit template choice in the user brief.':mode==='fallback'?`The brief has no useful layout or palette signals yet. Use the configurable ${chosen.name} fallback provisionally and review it during planning.`:`Best visual/layout fit among ${ranking.length} installed templates: ${selectedRank.reasons.map(r=>r.signal).join(', ')}.`);
 return {schema_version:1,selected_at:new Date().toISOString(),catalog_url:catalog.catalog_url,library_version:library.version,template_id:chosen.id,template_name:chosen.name,mode,reason,provisional:mode==='fallback',confidence:mode==='explicit'?'user_choice':mode==='agent_override'?'agent_review':noSignals?'low':ranking[0].score-ranking[1].score<8?'close_match':'clear_match',demo_url:chosen.demo_url,download_url:chosen.download_url,source_directory:chosen.source_directory,stylesheet_path:chosen.stylesheet_path,stylesheet_sha256:chosen.stylesheet_sha256,obtained_from:library.obtained_from,archive_path:library.archive_path,archive_sha256:library.archive_sha256,source_kind:chosen.source_kind,ranking,limitations:['Visual-fit heuristic, not a ranking/CTR/performance or compliance score.','Inspect the chosen demo/source and adapt it to the approved scope. No downloaded script was executed.']};
}
export function applySelectionToBrief(brief,selection){
 return {...brief,design_catalog_url:selection.catalog_url,design_template_id:brief.design_template_id||'auto',design_selected_template_id:selection.template_id,design_template_name:selection.template_name,design_demo_url:selection.demo_url,design_library_version:selection.library_version,design_selection_required:true};
}
function save(file,value){fs.writeFileSync(file+'.tmp',JSON.stringify(value,null,2)+'\n');fs.renameSync(file+'.tmp',file);}
export function selectForJob(job,options={}){
 const directory=path.resolve(job);const statePath=path.join(directory,'state.json');const state=read(statePath);
 if(state.tasks.slice(state.tasks.findIndex(task=>task.id==='07')).some(task=>['running','done'].includes(task.status)))throw new Error('Reopen design stage 07 before changing a reviewed or active template');
 const brief=read(path.join(directory,'brief.json'));const selection=recommendTemplate(brief,options);
 save(path.join(directory,'artifacts/template-selection.json'),selection);save(path.join(directory,'brief.json'),applySelectionToBrief(brief,selection));
 state.design_selection={template_id:selection.template_id,name:selection.template_name,mode:selection.mode,reason:selection.reason,artifact:'artifacts/template-selection.json'};
 state.events.push({at:new Date().toISOString(),action:'template_selected',stage:'02',reason:`${selection.template_id} — ${selection.template_name}: ${selection.reason}`});save(statePath,state);
 return selection;
}
export function prepareSelectedTemplate(job,options={}){
 const directory=path.resolve(job);let brief=read(path.join(directory,'brief.json'));const state=read(path.join(directory,'state.json'));
 if(state.tasks.slice(state.tasks.findIndex(task=>task.id==='07')).some(task=>task.status==='done'))throw new Error('Reopen design stage 07 before replacing template source evidence');
 const selectionFile=path.join(directory,'artifacts/template-selection.json');
 if(!fs.existsSync(selectionFile))selectForJob(directory,options);
 const selection=read(selectionFile);brief=read(path.join(directory,'brief.json'));
 const {library,root}=loadTemplateLibrary(options.root||workspaceRoot);
 const selected=library.templates.find(t=>t.id===selection.template_id);
 if(!selected||selection.library_version!==library.version||brief.design_selected_template_id!==selected.id)throw new Error('Selection is stale; review and choose the template again');
 const evidenceFile=path.join(directory,'artifacts/template-source.css.txt');
 if(fs.existsSync(evidenceFile)&&hash(evidenceFile)!==selected.stylesheet_sha256)fs.copyFileSync(evidenceFile,evidenceFile+'.previous-'+hash(evidenceFile).slice(0,12));
 fs.copyFileSync(checkedPath(root,selected.stylesheet_path),evidenceFile);
 const provenance={catalog_url:library.catalog_url,template_id:selected.id,name:selected.name,demo_url:selected.demo_url,download_url:selected.download_url,obtained_from:library.obtained_from,archive_path:library.archive_path,archive_sha256:library.archive_sha256,library_version:library.version,stylesheet_path:selected.stylesheet_path,stylesheet_sha256:selected.stylesheet_sha256,source_evidence:'artifacts/template-source.css.txt',selection_evidence:'artifacts/template-selection.json',adaptation_evidence:'artifacts/template-adaptation.md'};
 save(path.join(directory,'artifacts/template-provenance.json'),provenance);
 return provenance;
}
