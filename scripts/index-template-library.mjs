import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=file=>JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));
const catalog=read('config/template-catalog.json');
const extraction=read('vendor/templates/library-extraction.json');
const hash=buffer=>crypto.createHash('sha256').update(buffer).digest('hex');
for(const file of extraction.files){
 const actual=fs.readFileSync(path.join(root,extraction.directory,file.path));
 if(actual.length!==file.length||hash(actual)!==file.sha256)throw new Error(`Source mismatch: ${file.path}`);
}
const templates=catalog.templates.map(template=>{
 const directory=extraction.directory+'/'+template.download.replace(/\.zip$/,'');
 const relativeStyle=['assets/style.css','static/assets/site.css'].find(file=>fs.existsSync(path.join(root,directory,file)));
 if(!relativeStyle)throw new Error(`No main stylesheet found for ${template.id}`);
 const stylesheet=directory+'/'+relativeStyle;
 const css=fs.readFileSync(path.join(root,stylesheet));
 return {...template,demo_url:catalog.catalog_url+'/demos/'+template.id+'/',download_url:catalog.catalog_url+'/downloads/'+template.download,source_directory:directory,stylesheet_path:stylesheet,stylesheet_sha256:hash(css),source_files:extraction.files.filter(f=>f.path.startsWith(template.download.replace(/\.zip$/,'')+'/')).length,source_kind:fs.existsSync(path.join(root,directory,'package.json'))?'node-static':'python-static',ready:true};
});
if(templates.length!==catalog.templates.length||new Set(templates.map(t=>t.id)).size!==catalog.templates.length)throw new Error('Expected every catalog template exactly once');
const manifest={schema_version:1,catalog_url:catalog.catalog_url,version:extraction.archive_sha256,obtained_from:extraction.source_url,archive_path:extraction.archive_path,archive_sha256:extraction.archive_sha256,indexed_at:new Date().toISOString(),template_count:templates.length,source_files_verified:extraction.files.length,templates};
fs.writeFileSync(path.join(root,'vendor/templates/library-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({templates:templates.length,sourceFiles:extraction.files.length,ready:templates.every(t=>t.ready),choices:templates.map(t=>`${t.id}: ${t.name}`)},null,2));
