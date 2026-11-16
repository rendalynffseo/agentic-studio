import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const team=JSON.parse(fs.readFileSync(path.join(root,'config/agent-team.json'),'utf8'));
const classic=['queue','planning','setup','research','architecture','content','development','technical-seo','qa','release','measurement'].map(role=>role+'-agent');
export function teamTasks(brief){
 const specialist=brief.workflow_team==='specialist';
 return team.agents.filter(a=>specialist?(a.condition==='always'||a.condition==='blog'&&brief.blog_enabled===true||a.condition==='content'&&['provided','hybrid'].includes(brief.content_mode)&&brief.content_blocks?.length||a.condition==='affiliate'&&(brief.affiliate_links?.some(l=>l.url)||brief.affiliate_url)):classic.includes(a.agent)).map(a=>({id:a.id,agent:a.agent,title:a.title,station:a.station,responsibility:a.responsibility,instruction_file:a.instruction_file,required_outputs:specialist?a.required_outputs:[],status:'pending',attempts:0,artifact:`artifacts/${a.id}-${a.agent.replace(/-agent$/,'')}.json`}));
}
export function agentPrompt(job,state,agent){
 const task=state.tasks.find(t=>t.status!=='done');
 if(!task||task.agent!==agent)throw new Error('Only the next queued agent can receive an execution handoff');
 const profile=team.agents.find(a=>a.agent===agent);
 const index=state.tasks.indexOf(task),previous=state.tasks.slice(0,index).map(t=>t.artifact);
 const next=state.tasks[index+1];
 return [`Workspace: ${root}`,`Job directory: ${path.resolve(job)}`,`Assigned agent: ${agent}`,`Responsibility: ${profile?.responsibility||agent}`,`Read: ORCHESTRATOR.md, brief.json, state.json, ${profile?.instruction_file||'agents/roles.md'}`,`Prior handoffs: ${previous.join(', ')||'none; intake begins the workflow'}`,`Current status: ${task.status}. Inspect active work before resuming; never start a duplicate worker. Resolve a failed task before retrying.`,`When pending, claim: node workflow.mjs claim --job "${path.resolve(job)}" --agent ${agent}`,`Save handoff to ${task.artifact} using stage_id ${task.id} and agent ${agent}.`,`Required outputs: ${(task.required_outputs||[]).join(', ')||'Substantive role output and verification evidence'}`,`Complete verified work: node workflow.mjs complete --job "${path.resolve(job)}" --agent ${agent}`,`Pass to: ${next?.agent||'user; workflow complete'}. Execute only your assigned role, then report the handoff.`,`Do not deploy unless the brief authorizes it. Never invent checks, metrics, or completed work.`].join('\n');
}
