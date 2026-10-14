import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {PurgeCSS} from 'purgecss';
import {transform,Features} from 'lightningcss';

// Keep the rules used by each generated page, including interactive JS states.
// Run after the final Hugo build: node scripts/optimize-css.mjs public
const root=path.resolve(process.argv[2]||'public');
async function files(dir) {
  const entries=await fs.readdir(dir,{withFileTypes:true});
  return (await Promise.all(entries.map(e=>e.isDirectory()?files(path.join(dir,e.name)):[path.join(dir,e.name)]))).flat();
}
const all=await files(root);
const js=(await Promise.all(all.filter(p=>p.endsWith('.js')).map(p=>fs.readFile(p,'utf8')))).join('\n');
let pages=0, original=0, optimized=0;
const inputs=new Set();
for(const file of all.filter(p=>p.endsWith('.html'))) {
  const html=await fs.readFile(file,'utf8');
  const link=html.match(/<link\b(?=[^>]*\bid=(?:"site-critical-css"|'site-critical-css'|site-critical-css\b))[^>]*>/);
  if(!link)continue;
  const href=link[0].match(/\bhref=(?:"([^"]+)"|'([^']+)'|([^\s>]+))/)?.slice(1).find(Boolean);
  if(!href)throw Error('Missing stylesheet URL in '+file);
  const name=path.posix.basename(new URL(href,'https://local.invalid').pathname);
  if(!/^style(?:\.min)?\.[a-f0-9]+\.css$/.test(name))throw Error('Unexpected stylesheet '+name);
  const css=await fs.readFile(path.join(root,'css',name),'utf8');
  inputs.add(name);
  // Expand Tailwind 4 native nesting before selector pruning.
  const flat=transform({filename:name,code:Buffer.from(css),include:Features.Nesting,minify:true}).code.toString();
  const result=await new PurgeCSS().purge({
    content:[{raw:html+'\n'+js,extension:'html'}],css:[{raw:flat}],
    dynamicAttributes:['class','href','target','rel','aria-expanded','aria-selected'],
    defaultExtractor:content=>[
      ...(content.match(/[\w-/:]+(?<!:)/g)||[]),
      ...[...content.matchAll(/\bclass=(?:"([^"]+)"|'([^']+)'|([^\s>]+))/g)].flatMap(m=>(m[1]||m[2]||m[3]).split(/\s+/)),
    ],
    // Preserve native CSS nesting: a bare '&' has no class/tag for PurgeCSS to match.
    safelist:{standard:['&','dark','not-prose','active','show','open','hidden','visible','invisible','block','flex','grid','overflow-hidden'],greedy:[/data-/,/aria-/]},
    keyframes:false,fontFace:false,variables:false,
  });
  const clean=result[0].css;
  if(!clean || /<\/style/i.test(clean))throw Error('Invalid optimized stylesheet for '+file);
  const hash=crypto.createHash('sha256').update(clean).digest();
  const outputName='style.min.'+hash.toString('hex')+'.css';
  await fs.writeFile(path.join(root,'css',outputName),clean);
  const outputURL=href.slice(0,href.lastIndexOf('/')+1)+outputName;
  await fs.writeFile(file,html.replace(link[0],()=>'<link id="site-critical-css" rel="stylesheet" href="'+outputURL+'" integrity="sha256-'+hash.toString('base64')+'" crossorigin="anonymous">'));
  original+=Buffer.byteLength(css);optimized+=Buffer.byteLength(clean);pages++;
}
const rendered=(await Promise.all(all.filter(p=>p.endsWith('.html')).map(p=>fs.readFile(p,'utf8')))).join('\n');
for(const name of inputs) {
  if(!rendered.includes(name))await fs.unlink(path.join(root,'css',name));
}
console.log(`Optimized CSS for ${pages} pages: ${original} -> ${optimized} bytes before compression`);
