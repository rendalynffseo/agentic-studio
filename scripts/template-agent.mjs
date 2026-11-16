import {loadTemplateLibrary,recommendTemplate,selectForJob,prepareSelectedTemplate,verifyTemplateSources} from '../lib/template-selection.mjs';
import fs from 'node:fs';
const [command,...args]=process.argv.slice(2);const options={};
try{
 for(let i=0;i<args.length;i+=2){if(!args[i].startsWith('--')||!args[i+1])throw new Error('Options require values');const key=args[i].slice(2);if(!['job','brief','template','reason'].includes(key)||Object.hasOwn(options,key))throw new Error('Unknown or repeated option');options[key]=args[i+1];}
 let result;
 if(command==='list'){const {library}=loadTemplateLibrary();const verification=verifyTemplateSources();result={ready:true,template_count:library.template_count,source_files_verified:verification.verified_source_files,version:library.version,templates:library.templates.map(t=>({id:t.id,name:t.name,style:t.style,source_directory:t.source_directory}))};}
 else if(command==='recommend'){if(!options.brief)throw new Error('recommend requires --brief');result=recommendTemplate(JSON.parse(fs.readFileSync(options.brief,'utf8').replace(/^\uFEFF/,'')));}
 else if(command==='choose'){if(!options.job)throw new Error('choose requires --job');result=selectForJob(options.job,{overrideId:options.template,overrideReason:options.reason});}
 else if(command==='prepare'){if(!options.job)throw new Error('prepare requires --job');result=prepareSelectedTemplate(options.job);}
 else throw new Error('Use list, recommend --brief <json>, choose --job <dir> [--template tN --reason <text>], or prepare --job <dir>');
 console.log(JSON.stringify(result,null,2));
}catch(error){console.error('Error: '+error.message);process.exitCode=1;}
