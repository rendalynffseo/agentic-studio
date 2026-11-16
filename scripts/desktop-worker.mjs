import {EventEmitter} from 'node:events';
import readline from 'node:readline';
import {spawn} from 'node:child_process';
import {doctor,findEngine,runWorker,redact,controlWorker,recoverWorker,workspace} from '../lib/desktop-worker.mjs';
const [command,...args]=process.argv.slice(2);
const emit=event=>process.stdout.write(JSON.stringify(event)+'\n');
try{
 if(command==='doctor')console.log(JSON.stringify(doctor()));
 else if(command==='control'){if(args[0]!=='--job'||args[2]!=='--action'||args.length!==4)throw new Error('Use control --job <directory> --action pause|stop');controlWorker(workspace,args[1],args[3]);emit({type:'control',message:'Worker control sent: '+args[3]});}
 else if(command==='recover'){if(args[0]!=='--job'||args.length!==2)throw new Error('Use recover --job <directory>');recoverWorker(workspace,args[1]);emit({type:'status',message:'Interrupted stage marked for review. Inspect partial work and Retry in the task panel.'});}
 else if(command==='login'){
  // One-time sign-in instructions are shown only in the native window, not persisted to job logs.
  const child=spawn(findEngine(),['login','--device-auth'],{windowsHide:true,stdio:['ignore','pipe','pipe']});
  for(const stream of [child.stdout,child.stderr])stream.on('data',data=>emit({type:'login',message:data.toString().replace(/\x1b\[[0-9;]*m/g,'')}));
  child.once('error',error=>{emit({type:'error',message:redact(error.message)});process.exitCode=1;});
  child.once('close',code=>{emit({type:'login_finished',message:code===0?'Sign-in finished. Check connection to confirm.':'Sign-in did not finish.',code});process.exitCode=code||0;});
 }else if(command==='run'){
  if(args[0]!=='--job'||!args[1]||args.length!==2)throw new Error('Use run --job <job directory>');
  const control=new EventEmitter(),input=readline.createInterface({input:process.stdin});
  input.on('line',line=>{try{const value=JSON.parse(line);if(['pause','stop'].includes(value.command))control.emit('command',value.command);}catch{}});
  try{await runWorker({job:args[1],emit,control});}finally{input.close();}
 }else throw new Error('Use doctor, login, or run --job <job directory>');
}catch(error){emit({type:'error',message:redact(error.message)});process.exitCode=1;}
