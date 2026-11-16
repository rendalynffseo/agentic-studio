import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export const contentModes=['agent','provided','hybrid'];
const read=file=>JSON.parse(fs.readFileSync(file,'utf8').replace(/^\uFEFF/,''));
const nl=value=>value.replace(/\r\n?/g,'\n');
const digest=value=>crypto.createHash('sha256').update(value).digest('hex');
const save=(file,value)=>{fs.writeFileSync(file+'.tmp',JSON.stringify(value,null,2)+'\n');fs.renameSync(file+'.tmp',file);};
const requireThat=(ok,message)=>{if(!ok)throw new Error(message);};
export function validPage(page){
 if(typeof page!=='string'||!page.startsWith('/')||page.startsWith('//')||/[?#\\]/.test(page))return false;
 try{return !decodeURIComponent(page).split('/').some(part=>part==='..'||part==='.')&&!/[\0<>:"|*]/.test(decodeURIComponent(page));}catch{return false;}
}
export function normalizeUserContent(input={}){
 const mode=input.content_mode??'agent';requireThat(contentModes.includes(mode),'Choose agent, provided, or hybrid content mode');
 const blocks=input.content_blocks??[];requireThat(Array.isArray(blocks)&&blocks.length<=20,'Provide at most 20 content blocks');
 const seen=new Set();let characters=0;
 const normalized=blocks.map((block,index)=>{
  requireThat(block&&typeof block==='object'&&!Array.isArray(block),'Content block must be an object');
  const id=block.id||`block-${index+1}`;requireThat(typeof id==='string'&&/^[a-zA-Z0-9_-]{1,80}$/.test(id)&&!seen.has(id),'Content block IDs must be unique letters, numbers, hyphens, or underscores');seen.add(id);
  requireThat(typeof block.text==='string'&&block.text.length<=200000,'Each content block must contain text of at most 200,000 characters');characters+=block.text.length;
  requireThat(block.text.trim(),'Content blocks cannot be empty');
  requireThat(block.preserve_exact!==false,'User content is preserved exactly; use agent mode for generated copy');
  const label=block.label??`Content block ${index+1}`;requireThat(typeof label==='string'&&label.length<=300,'Content label is too long');
  const placement=block.placement??{};const page=placement.page||'auto',section=placement.section||'auto';
  requireThat(page==='auto'||validPage(page),'Target page must be auto or a local path such as /about/');requireThat(typeof section==='string'&&section.length<=300,'Target section must be a short label or auto');
  return{id,label,text:block.text,preserve_exact:true,placement:{page,section}};
 });
 requireThat(characters<=500000,'Total supplied content exceeds 500,000 characters');
 requireThat(mode==='agent'||normalized.length>0,'Paste at least one content block for this content mode');
 return{content_mode:mode,content_blocks:normalized};
}
export function activeUserContent(brief){const spec=normalizeUserContent(brief);return spec.content_mode==='agent'?[]:spec.content_blocks;}
export function contentFingerprint(brief){const spec=normalizeUserContent(brief);return digest(JSON.stringify({mode:spec.content_mode,blocks:spec.content_blocks.map(b=>({...b,text:nl(b.text)}))}));}
export function prepareUserContent(job,brief=read(path.join(job,'brief.json'))){
 const spec=normalizeUserContent(brief);if(spec.content_mode==='agent')return null;
 const snapshot={schema_version:1,source_sha256:contentFingerprint(brief),mode:spec.content_mode,blocks:spec.content_blocks,normalization:'Line endings may use LF or CRLF. No wording, punctuation, spacing, or Unicode normalization is allowed.'};
 const file=path.join(job,'artifacts/user-content-source.json');
 if(fs.existsSync(file)){const old=read(file);if(old.source_sha256!==snapshot.source_sha256)fs.copyFileSync(file,path.join(job,`artifacts/user-content-source.previous-${old.source_sha256.slice(0,12)}.json`));}
 save(file,snapshot);return snapshot;
}
export function validatePlacementMap(brief,snapshot,map){
 const blocks=activeUserContent(brief);const fingerprint=contentFingerprint(brief);
 requireThat(snapshot?.source_sha256===fingerprint&&contentFingerprint({content_mode:snapshot.mode,content_blocks:snapshot.blocks})===fingerprint,'The supplied-content snapshot is stale or changed');
 requireThat(map&&map.schema_version===1&&map.source_sha256===fingerprint,'Content placement map must reference the current content snapshot');
 requireThat(Array.isArray(map.placements)&&map.placements.length===blocks.length,'Every supplied content block needs exactly one placement');
 const seen=new Set();
 for(const placement of map.placements){
  const block=blocks.find(b=>b.id===placement.block_id);requireThat(block&&!seen.has(block.id),'Placement contains an unknown or duplicate content block');seen.add(block.id);
  requireThat(validPage(placement.page),'Choose a real local page path for each block');
  requireThat(typeof placement.section==='string'&&placement.section.trim()&&placement.section.toLowerCase()!=='auto','Choose a section for each block');
  requireThat(typeof placement.reason==='string'&&placement.reason.trim(),'Explain why each content block belongs in its section');
  requireThat(placement.preserve_exact===true,'Placement must preserve the supplied wording exactly');
  requireThat(block.placement.page==='auto'||block.placement.page===placement.page,'Placement must honor the user’s requested page');
  requireThat(block.placement.section==='auto'||block.placement.section.trim().toLowerCase()===placement.section.trim().toLowerCase(),'Placement must honor the user’s requested section');
 }
 return true;
}
export function renderUserContent(block,placement,{tag='div'}={}){
 requireThat(['div','p','h1','h2','h3','span','blockquote'].includes(tag),'Unsupported content element');
 requireThat(placement.block_id===block.id&&placement.preserve_exact===true,'Render the matching exact-content placement');
 const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;');
 return `<${tag} class="user-supplied-copy" data-content-block="${escape(block.id)}" data-content-section="${escape(placement.section)}">${escape(block.text)}</${tag}>`;
}
function decode(text){return text.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi,(_,entity)=>entity[0]==='#'?String.fromCodePoint(entity[1].toLowerCase()==='x'?parseInt(entity.slice(2),16):parseInt(entity.slice(1),10)):({amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:'\u00a0'}[entity.toLowerCase()]));}
export function verifyUserContent(brief,snapshot,map,outputDirectory){
 validatePlacementMap(brief,snapshot,map);const directory=fs.realpathSync(outputDirectory);const results=[];
 for(const block of activeUserContent(brief)){
  const placement=map.placements.find(p=>p.block_id===block.id);
  try{
   const relative=placement.page.slice(1)+(placement.page.endsWith('/')?'index.html':'');
   const file=fs.realpathSync(path.resolve(directory,relative));const contained=path.relative(directory,file);
   requireThat(contained&&contained!=='..'&&!contained.startsWith('..'+path.sep)&&!path.isAbsolute(contained),'Content output path escaped the built site');
   const html=fs.readFileSync(file,'utf8').replace(/<!--[\s\S]*?-->/g,'');
   const matches=[...html.matchAll(/<([a-z][a-z0-9]*)\b([^>]*\bdata-content-block="([a-zA-Z0-9_-]+)"[^>]*)>([\s\S]*?)<\/\1\s*>/gi)].filter(m=>m[3]===block.id);
   requireThat(matches.length===1,'Content marker is missing or duplicated on the planned page');
   requireThat(!matches[0][4].includes('<'),'Use a plain escaped-text content element for exact copy');
   const actual=decode(matches[0][4]);requireThat(nl(actual)===nl(block.text),'Supplied wording was changed, omitted, or reformatted');
   const section=matches[0][2].match(/data-content-section="([^"]*)"/);requireThat(section&&decode(section[1])===placement.section,'Content section marker does not match the placement map');
   results.push({block_id:block.id,page:placement.page,section:placement.section,passed:true,exact:true,text_sha256:digest(nl(actual))});
  }catch(error){results.push({block_id:block.id,page:placement.page,section:placement.section,passed:false,error:error.message});}
 }
 return{schema_version:1,checked_at:new Date().toISOString(),source_sha256:contentFingerprint(brief),output_directory:directory,passed:results.every(r=>r.passed),blocks:results,limitations:['Static HTML verification. Browser QA must check visible placement and surrounding context.']};
}
export function saveUserContent(job,input){
 const directory=path.resolve(job);const state=read(path.join(directory,'state.json'));
 requireThat(!state.tasks.some(t=>t.status==='running'),'Wait for the active agent to finish before updating supplied content');
 const spec=normalizeUserContent(input);const current=read(path.join(directory,'brief.json'));
 if(contentFingerprint(current)===contentFingerprint(spec))return{changed:false,message:'Content is unchanged; the queue was not reopened.'};
 const updated={...current,...spec};save(path.join(directory,'brief.json'),updated);prepareUserContent(directory,updated);
 for(const task of state.tasks.filter(t=>Number(t.id)>=6)){task.status='pending';for(const key of ['started_at','completed_at','failure'])delete task[key];}
 state.user_content={mode:spec.content_mode,blocks:spec.content_blocks.length,source_sha256:contentFingerprint(spec)};
 state.events.push({at:new Date().toISOString(),action:'content_updated',stage:'06',reason:`Content writer updated: ${spec.content_mode}, ${spec.content_blocks.length} exact content blocks. Content and downstream stages require review.`});save(path.join(directory,'state.json'),state);
 return{changed:true,mode:spec.content_mode,blocks:spec.content_blocks.length,message:'Content saved. Stage 06 and later stages are queued for review; no worker or deployment was started.'};
}
