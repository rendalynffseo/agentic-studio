// Explicit integration check: starts a real signed-in model for one isolated intake role.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {runWorker,workspace} from '../lib/desktop-worker.mjs';
if(process.argv[2]!=='--run')throw new Error('This calls the signed-in model. Run explicitly with --run; it is not part of npm test.');
const name='.desktop-worker-smoke-'+crypto.randomBytes(6).toString('hex'),job=path.join(workspace,'jobs',name),briefFile=path.join(workspace,'desktop','worker-smoke-brief.json');
let passed=false,error='';
try{
 fs.writeFileSync(briefFile,JSON.stringify({project_name:'Desktop engine integration check',business:'Agentic Studio runtime verification',audience:'Application maintainer',offer:'Verify local engine and handoff execution',request:'This is an isolated desktop engine health check, not a website creation task. Read this temporary task and save artifacts/engine-check.md confirming real execution and ability to save artifacts. Save the normal queue-agent deliverable with actual evidence and complete this single role. Do not browse, research, build a website, modify application or website source, publish, deploy, push, or change files outside this temporary job.',workflow_team:'classic',deployment_authorized:false}));
 const init=spawnSync(process.execPath,[path.join(workspace,'workflow.mjs'),'init','--brief',briefFile,'--job',job],{cwd:workspace,encoding:'utf8'});if(init.status!==0)throw new Error(init.stderr);
 const stateFile=path.join(job,'state.json'),state=JSON.parse(fs.readFileSync(stateFile,'utf8'));state.tasks=state.tasks.slice(0,1);fs.writeFileSync(stateFile,JSON.stringify(state,null,2));
 await runWorker({job,emit:event=>{if(['status','handoff','error'].includes(event.type))console.log(JSON.stringify(event));}});
 const final=JSON.parse(fs.readFileSync(stateFile,'utf8'));passed=final.tasks[0].status==='done'&&fs.existsSync(path.join(job,'artifacts/engine-check.md'));if(!passed)throw new Error('The real worker did not save its requested artifact and complete the intake role.');
}catch(exception){error=exception.message;process.exitCode=1;}
finally{
 const result={checked_at:new Date().toISOString(),passed,real_model_execution:true,error};fs.writeFileSync(path.join(workspace,'desktop/worker-live-result.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
 if(fs.existsSync(briefFile))fs.unlinkSync(briefFile);
 if(fs.existsSync(job)&&path.dirname(fs.realpathSync(job))===fs.realpathSync(path.join(workspace,'jobs'))&&path.basename(job)===name)fs.rmSync(job,{recursive:true,force:true});
}
