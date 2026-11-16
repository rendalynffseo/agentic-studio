import fs from 'node:fs';
import path from 'node:path';
import {prepareUserContent,validatePlacementMap,verifyUserContent,renderUserContent} from '../lib/user-content.mjs';
const [command,...rest]=process.argv.slice(2);const args={};
try{
 for(let i=0;i<rest.length;i+=2){if(!rest[i].startsWith('--')||!rest[i+1])throw new Error('Options need values');const key=rest[i].slice(2);if(!['job','site','block'].includes(key)||Object.hasOwn(args,key))throw new Error('Unknown or repeated option');args[key]=rest[i+1];}
 if(!args.job)throw new Error('Use prepare, check-map, render --block <id>, or verify --site <built-directory>, all with --job <directory>');
 const job=path.resolve(args.job),read=file=>JSON.parse(fs.readFileSync(path.join(job,file),'utf8'));
 const brief=read('brief.json');const snapshot=prepareUserContent(job,brief);if(!snapshot){console.log('Agent-written content mode; no supplied-copy placement is required.');process.exit(0);}
 if(command==='prepare'){console.log(JSON.stringify({source:'artifacts/user-content-source.json',sha256:snapshot.source_sha256,mode:snapshot.mode,blocks:snapshot.blocks.map(b=>({id:b.id,label:b.label,preferred:b.placement})),next:'Write artifacts/content-placement.json with schema_version:1, source_sha256, and one placement per block: block_id, page, section, reason, preserve_exact:true.'},null,2));}
 else{
  const map=read('artifacts/content-placement.json');validatePlacementMap(brief,snapshot,map);
  if(command==='check-map')console.log('Every block has a valid exact-content placement.');
  else if(command==='render'){const block=snapshot.blocks.find(b=>b.id===args.block);if(!block)throw new Error('Unknown --block ID');console.log(renderUserContent(block,map.placements.find(p=>p.block_id===block.id)));}
  else if(command==='verify'){if(!args.site)throw new Error('verify requires --site');const report=verifyUserContent(brief,snapshot,map,args.site);fs.writeFileSync(path.join(job,'artifacts/content-verification.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));if(!report.passed)process.exitCode=1;}
  else throw new Error('Unknown command');
 }
}catch(error){console.error('Error: '+error.message);process.exitCode=1;}
