import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawn,spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {agentPrompt} from './agent-team.mjs';
import {validate} from '../workflow.mjs';

export const workspace=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=file=>JSON.parse(fs.readFileSync(file,'utf8').replace(/^\uFEFF/,''));
const alive=pid=>{try{process.kill(pid,0);return true;}catch(error){return error.code==='EPERM';}};
export function redact(text){return String(text).replace(/\b(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{25,})\b/g,'[redacted]').replace(/(authorization\s*[:=]\s*)(?:bearer\s+)?[^\s",]+/gi,'$1[redacted]');}
export function findEngine(root=workspace){
 const settings=path.join(root,'desktop/worker-settings.json');
 if(fs.existsSync(settings)){const selected=read(settings).engine_path;if(selected){if(!fs.existsSync(selected))throw new Error('The saved Codex engine path no longer exists. Choose it again in AI worker settings.');return selected;}}
 const binary=process.platform==='win32'?'codex.exe':'codex';
 for(const directory of (process.env.PATH||'').split(path.delimiter)){const file=path.join(directory.replace(/^"|"$/g,''),binary);if(fs.existsSync(file)&&fs.statSync(file).isFile())return file;}
 if(process.platform==='win32'){
  const extensions=path.join(os.homedir(),'.vscode/extensions');
  if(fs.existsSync(extensions))for(const entry of fs.readdirSync(extensions).filter(n=>n.startsWith('openai.chatgpt-')).sort().reverse()){const file=path.join(extensions,entry,'bin/windows-x86_64/codex.exe');if(fs.existsSync(file))return file;}
  const npm=path.join(process.env.APPDATA||'', 'npm/node_modules/@openai');
  for(const file of [path.join(npm,'codex/vendor/x86_64-pc-windows-msvc/codex/codex.exe'),path.join(npm,'codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/codex/codex.exe')])if(fs.existsSync(file))return file;
 }
 throw new Error('Codex engine not found. Install the Codex CLI or choose codex.exe in AI worker settings. VS Code does not need to be open.');
}
export function doctor(root=workspace){
 const engine=findEngine(root);
 const version=spawnSync(engine,['--version'],{encoding:'utf8',timeout:15000,windowsHide:true});
 if(version.error||version.status!==0)throw new Error('The Codex engine could not start. Check its path and Windows permissions.');
 const login=spawnSync(engine,['login','status'],{encoding:'utf8',timeout:15000,windowsHide:true});
 return {engine,version:(version.stdout||'').trim(),signed_in:login.status===0,message:login.status===0?'Signed in. Ready to run without VS Code.':'Sign in to Codex in this window before starting a task.'};
}
export function acquireLock(root,job){
 const file=path.join(root,'desktop/worker-runtime.lock');fs.mkdirSync(path.dirname(file),{recursive:true});
 const owner={pid:process.pid,job,started_at:new Date().toISOString(),nonce:Math.random().toString(36).slice(2)};
 for(let attempt=0;attempt<2;attempt++){
  try{fs.writeFileSync(file,JSON.stringify(owner),{flag:'wx'});const release=()=>{try{if(read(file).nonce===owner.nonce)fs.unlinkSync(file);}catch{}};release.owner=owner;return release;}
  catch(error){if(error.code!=='EEXIST')throw error;let previous;try{previous=read(file);}catch{throw new Error('Worker lock is unreadable. Inspect desktop/worker-runtime.lock before starting another worker.');}if(Number.isInteger(previous.pid)&&alive(previous.pid))throw new Error('A desktop worker is already running. Use its window to pause or stop it.');fs.unlinkSync(file);}
 }
 throw new Error('Another worker acquired the workspace.');
}
export function engineArgs(root){return ['--search','exec','--json','--sandbox','workspace-write','--skip-git-repo-check','--ephemeral','--color','never','--cd',root,'-'];}
function queue(root,job,args){const result=spawnSync(process.execPath,[path.join(root,'workflow.mjs'),...args,'--job',job],{encoding:'utf8',windowsHide:true});if(result.status!==0)throw new Error((result.stderr||result.stdout||'Queue operation failed').trim());return result.stdout;}
function cleanJob(root,input){const job=fs.realpathSync(path.resolve(input));const base=fs.realpathSync(path.join(root,'jobs'));if(path.dirname(job)!==base)throw new Error('Select a task directly inside this workspace jobs folder.');read(path.join(job,'brief.json'));read(path.join(job,'state.json'));return job;}
export function controlWorker(root,input,command){
 if(!['pause','stop'].includes(command))throw new Error('Unknown worker control');const job=cleanJob(root,input),owner=read(path.join(root,'desktop/worker-runtime.lock'));
 if(owner.job!==job||!alive(owner.pid))throw new Error('No active desktop worker owns this task.');
 const file=path.join(root,'desktop/worker-control.json'),temporary=file+'.'+process.pid+'.tmp';fs.writeFileSync(temporary,JSON.stringify({nonce:owner.nonce,command}));fs.renameSync(temporary,file);
}
export function recoverWorker(root,input){const job=cleanJob(root,input),release=acquireLock(root,job);try{const task=read(path.join(job,'state.json')).tasks.find(t=>t.status!=='done');if(task?.status!=='running')throw new Error('No interrupted running stage to recover.');queue(root,job,['fail','--agent',task.agent,'--reason','User recovered an interrupted stage after confirming no other agent is working. Partial work is preserved; review it before retrying.']);}finally{release();}}
export async function runWorker({job:input,root=workspace,engine,emit=()=>{},control,checkLogin=true,launch=spawn}){
 const job=cleanJob(root,input),release=acquireLock(root,job);let child=null,stop=false,pause=false,ownedTask=null,activeAgent='';
 const statusFile=path.join(job,'worker-status.json'),logFile=path.join(job,'worker-events.jsonl');
 const notify=(type,message,extra={})=>{const event={at:new Date().toISOString(),type,message:redact(message),...extra};fs.appendFileSync(logFile,JSON.stringify(event)+'\n');emit(event);};
 const status=(value,message)=>{const data={status:value,message:redact(message),pid:process.pid,agent:activeAgent,updated_at:new Date().toISOString()};fs.writeFileSync(statusFile+'.tmp',JSON.stringify(data,null,2));fs.renameSync(statusFile+'.tmp',statusFile);notify('status',message,{status:value,agent:activeAgent});};
 const failOwned=reason=>{const task=read(path.join(job,'state.json')).tasks.find(t=>t.id===ownedTask);if(task?.status==='running')queue(root,job,['fail','--agent',task.agent,'--reason',reason]);};
 const onControl=command=>{if(command==='pause'){pause=true;notify('control','Pause requested. The active agent will finish; no next agent will start.');}if(command==='stop'){stop=true;notify('control','Stopping the active worker. Partial files will be preserved.');if(child?.pid){if(process.platform==='win32')spawn('taskkill.exe',['/PID',String(child.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});else child.kill('SIGTERM');}}};
 control?.on('command',onControl);
 const controlFile=path.join(root,'desktop/worker-control.json');
 const poll=setInterval(()=>{try{if(fs.existsSync(controlFile)){const request=read(controlFile);if(request.nonce===release.owner.nonce){fs.unlinkSync(controlFile);onControl(request.command);}}}catch{}},250);poll.unref();
 try{
  if(checkLogin){status('checking','Checking Codex engine and sign-in.');const result=doctor(root);engine=engine||result.engine;if(!result.signed_in)throw new Error('Sign in using AI worker > Sign in before starting.');}
  engine=engine||findEngine(root);
  for(;;){
   if(stop){status('stopped','Worker stopped. Continue the task when ready.');return;}
   if(pause){status('paused','Paused between agents. Start to continue.');return;}
   const state=read(path.join(job,'state.json')),task=state.tasks.find(t=>t.status!=='done');
   if(!task){activeAgent='';status('complete','All assigned agents completed their verified handoffs.');return;}
   if(task.status==='running')throw new Error('This task is already marked running. Inspect its existing worker or resolve the interrupted stage before resuming; a duplicate worker was not launched.');
   if(task.status==='failed')throw new Error('The next agent needs attention: '+(task.failure||'Review its last failure, then retry the stage.'));
   activeAgent=task.agent;ownedTask=task.id;
   queue(root,job,['claim','--agent',task.agent]);status('running','Working: '+task.agent);
   const claimed=read(path.join(job,'state.json'));
   const prompt=agentPrompt(job,claimed,task.agent)+'\n\nDESKTOP EXECUTION: The desktop runner has already claimed this role. Do not claim it again. You are the actual worker for ONLY this assigned role; do not spawn other workers or execute the next role. Perform real work, save evidence and the required handoff, then run the normal workflow complete command. The desktop starts the next separate worker only after this stage is done. If blocked, use workflow fail with a precise reason. Never edit state.json directly or create fake passing evidence. Read the brief authorization; do not deploy, publish, push hosted source, or change audience unless the current brief explicitly authorizes that action.\n';
   let lastError='',buffer='';
   const result=await new Promise(resolve=>{
    try{child=launch(engine,engineArgs(root),{cwd:root,windowsHide:true,stdio:['pipe','pipe','pipe']});}catch(error){resolve({code:1,error:error.message});return;}
    const line=text=>{if(!text.trim())return;try{const event=JSON.parse(text);if(event.type==='error'||event.type==='turn.failed'){lastError=event.message||event.error?.message||'Engine reported a failure';notify('error',lastError);}else if(event.item?.type==='agent_message')notify('message',event.item.text||'');else if(event.item?.type==='command_execution')notify('command',String(event.item.command||'Command')+' ['+(event.item.status||event.type)+']');else if(event.type==='thread.started'||event.type==='turn.completed')notify('engine',event.type);else if(event.item?.type)notify('activity',event.item.type+' / '+event.type);}catch{notify('engine',text);}};
    child.stdout.on('data',data=>{buffer+=data.toString();let index;while((index=buffer.indexOf('\n'))>=0){line(buffer.slice(0,index));buffer=buffer.slice(index+1);}});
    child.stderr.on('data',data=>notify('engine',data.toString().trim()));
    child.once('error',error=>resolve({code:1,error:error.message}));
    child.once('close',code=>{if(buffer)line(buffer);resolve({code,error:lastError});});
    child.stdin.on('error',()=>{});child.stdin.end(prompt);
   });child=null;
   const current=read(path.join(job,'state.json')).tasks.find(t=>t.id===ownedTask);
   if(stop){failOwned('Desktop worker stopped by the user. Partial work was preserved; inspect it before retrying.');status('stopped','Stopped. Review partial work, then retry the stage to continue.');return;}
   if(result.code!==0){failOwned('Codex worker failed: '+redact(result.error||'Engine exited with code '+result.code));throw new Error(result.error||'Codex worker exited with code '+result.code);}
   if(current?.status!=='done'){failOwned('The engine ended without a verified completed handoff. Review the worker log and partial files.');throw new Error(current?.failure||'The agent did not complete its validated handoff.');}
   try{validate(job,{...task,status:current.status});}catch(error){
    queue(root,job,['reopen','--stage',task.id,'--reason','Desktop independently rejected the agent handoff: '+redact(error.message)]);
    queue(root,job,['claim','--agent',task.agent]);
    failOwned('Desktop validation failed: '+redact(error.message));throw error;
   }
   notify('handoff',task.agent+' completed. Passing saved outputs to the next agent.');ownedTask=null;
  }
 }catch(error){try{if(ownedTask)failOwned(redact(error.message));}catch{}status('blocked',error.message);throw error;}
 finally{clearInterval(poll);control?.off('command',onControl);try{if(fs.existsSync(controlFile)&&read(controlFile).nonce===release.owner.nonce)fs.unlinkSync(controlFile);}catch{}release();}
}
