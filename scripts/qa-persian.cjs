'use strict';
// Real Chromium: every Persian page, responsive geometry, language switching,
// and exhaustive select combinations compared with the English reference.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const build = path.resolve(process.argv[2] || 'public');
const manifest = JSON.parse(fs.readFileSync(process.argv[3] || 'qa-output/persian-audit.json', 'utf8'));
const out = path.resolve(process.argv[4] || 'qa-output/browser');
const live = process.env.PERSIAN_QA_LIVE === '1';
// For CSS-only follow-up checks; the default release/CI run always tests forms.
const geometryOnly = process.env.PERSIAN_QA_GEOMETRY_ONLY === '1';
const widths = (process.env.PERSIAN_QA_WIDTHS || '320,390,768,1280,1920').split(',').map(Number);
const outputs = {
  'homepage-vps-fit-checker':'homepage-vps-fit-result',
  'vps-security-checker':'vps-security-result',
  'vps-location-checker':'vps-location-result',
  'ram-budget-estimator-form':'ram-budget-result',
  'shared-hosting-diagnostic':'shared-hosting-result',
  'fastpanel-fit-checker':'fastpanel-fit-result',
  'deployment-path-checker-form':'deployment-path-result',
  'migration-preflight':'migration-preflight-result',
  'vps-backup-strategy-checker-form':'vps-backup-strategy-result',
  'vps-monitoring-checker':'vps-monitoring-result',
  'panel-fit-checker':'panel-fit-result',
  'management-fit-checker-form':'management-fit-result',
  'shared-vs-vps-checker':'shared-vs-vps-result',
  'multi-site-architecture-checker':'multi-site-architecture-result',
  'woocommerce-vps-fit-checker-form':'woocommerce-vps-fit-result',
  'wordpress-vps-fit-checker-form':'wordpress-vps-fit-result'
};
fs.mkdirSync(out, {recursive:true});
const findings = [], geometry = [], forms = [];
const startedAt = new Date().toISOString();
const overallTimeoutMs = 35 * 60 * 1000;
let browser = null;
let terminating = false;
function fail(route, check, detail) {
  findings.push({route, check, detail});
  console.error('FA_QA_FAIL', route, check, JSON.stringify(detail).slice(0, 800));
}
function checkpoint(status) {
  if (terminating && status === 'running') return;
  const report = {status,startedAt,updatedAt:new Date().toISOString(),mode:live?'production':'local',geometryOnly,pages:manifest.routes.length,geometryCases:geometry.length,forms:forms.length,formCases:forms.reduce((n,x)=>n+x.cases,0),findings,formReports:forms,geometry};
  const destination = path.join(out,'report.json');
  fs.writeFileSync(destination+'.tmp',JSON.stringify(report,null,2));
  fs.renameSync(destination+'.tmp',destination);
  return report;
}
function abortRun(status, error) {
  if (terminating) return;
  terminating = true;
  fail('__run__',status,String(error.stack||error));
  try {checkpoint(status);} catch(e) {console.error('FA_QA_REPORT_ERROR',e);}
  // Closing a stuck renderer is best effort: the process still fails promptly.
  const forcedExit = setTimeout(()=>process.exit(1),5000);
  Promise.resolve().then(()=>browser && browser.close()).catch(e=>console.error('FA_QA_CLOSE_ERROR',e)).finally(()=>{
    clearTimeout(forcedExit);
    process.exit(1);
  });
}
async function open(page, route) {
  const response = await page.goto('https://vpsforwebsite.com' + route, {waitUntil:'domcontentloaded', timeout:60000});
  assert.equal(response.status(), 200, route);
  await page.locator('main h1').waitFor();
  await page.evaluate(async()=>{if(document.fonts) await document.fonts.ready;});
  await page.addStyleTag({content:'.vps-home > section:not(.vps-hero),#final-cta{content-visibility:visible!important}*,*::before,*::after{animation:none!important;transition:none!important}'});
}
async function formMatrix(page) {
  return page.evaluate(outputIds=>{
    const reports = [];
    for (const form of document.querySelectorAll('main form[id]')) {
      const result = document.getElementById(outputIds[form.id]);
      if (!result) throw new Error('No output mapped for '+form.id);
      const controls = [...form.querySelectorAll('select,input[type="number"]')];
      const selects = controls.filter(x=>x.tagName==='SELECT');
      const numeric = controls.filter(x=>x.tagName==='INPUT');
      const ids = controls.map(x=>x.id);
      const domains = selects.map(x=>[...x.options].map(o=>o.value));
      const combinations = [];
      function product(i, values) {
        if (i===domains.length) {combinations.push(values);return;}
        for (const value of domains[i]) product(i+1, [...values,value]);
      }
      product(0,[]);
      let numberCases = [[]];
      if(numeric.length) {
        if(form.id !== 'ram-budget-estimator-form') throw new Error('Unmapped numeric form '+form.id);
        numberCases = [
          ['450','500','6','120','300','25'],
          ...[0,1,1024,1025,2048,2049,4096,4097,8192,8193].map(n=>[String(n),'0','0','0','0','0'])
        ];
      }
      const unique = [], sequence = [];
      for(const values of combinations) for(const numbers of numberCases) {
        selects.forEach((el,i)=>el.value=values[i]);
        numeric.forEach((el,i)=>el.value=numbers[i]);
        if(!form.checkValidity()) throw new Error('Invalid test inputs '+form.id);
        result.textContent = 'QA_PENDING';
        form.querySelector('button[type="submit"]').click();
        const text = result.textContent.trim();
        if(text==='QA_PENDING'||text.length<10) throw new Error('Empty/unchanged result '+form.id);
        let index=unique.indexOf(text);
        if(index<0){index=unique.length;unique.push(text);}
        sequence.push(index);
      }
      reports.push({id:form.id,ids,domains,numberCases,unique,sequence,cases:sequence.length});
    }
    return reports;
  }, outputs);
}
async function inspect(page, route, width) {
  const result = await page.evaluate(()=>{
    const visible=el=>{const r=el.getBoundingClientRect(),s=getComputedStyle(el);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden';};
    const box=el=>{const r=el.getBoundingClientRect();return {tag:el.tagName,text:el.textContent.trim().slice(0,80),left:r.left,right:r.right};};
    const W=innerWidth;
    const important=[...document.querySelectorAll('header .navbar,main h1,main h2,main h3,main .content,main .vps-hero-copy,main [class*="-hero-grid"],main form,main form select,main form input,main button,main a.btn,main .vps-table-scroll,main .vps-affiliate-disclosure,footer .container')].filter(visible);
    const outside=important.map(box).filter(r=>r.left< -2.5||r.right>W+2.5);
    const clipped=[...document.querySelectorAll('main h1,main h2,main h3,main button,main a.btn')].filter(visible).filter(el=>el.scrollWidth>el.clientWidth+3&&!['auto','scroll'].includes(getComputedStyle(el).overflowX)).map(box);
    const wrongCodeDirection=[...document.querySelectorAll('main pre,main code,main bdi[dir="ltr"],main input[type="number"],main input[type="email"],main input[type="url"]')].filter(el=>getComputedStyle(el).direction!=='ltr').map(box);
    const wrongLabelFont=[...document.querySelectorAll('main h1,main h2,main h3,main label,main legend')].filter(el=>!getComputedStyle(el).fontFamily.includes('Vazirmatn')).map(box);
    const svgClipped=[...document.querySelectorAll('main svg text')].filter(visible).filter(el=>{const r=el.getBoundingClientRect(),s=el.ownerSVGElement.getBoundingClientRect();return r.left<s.left-2||r.right>s.right+2||r.top<s.top-2||r.bottom>s.bottom+2;}).map(box);
    return {width:W,doc:document.documentElement.scrollWidth,body:document.body.scrollWidth,outside,clipped,wrongCodeDirection,wrongLabelFont,svgClipped,persianFont:document.fonts.check('16px Vazirmatn'),bodyFont:getComputedStyle(document.body).fontFamily,lang:document.documentElement.lang,dir:document.documentElement.dir,title:document.title,h1:[...document.querySelectorAll('main h1')].map(x=>x.innerText.trim()),brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)};
  });
  geometry.push({route,width,...result});
  if(result.doc>width+2||result.body>width+2||result.outside.length||result.clipped.length) fail(route,'geometry at '+width,result);
  if(result.dir!=='rtl'||result.lang.split('-')[0]!=='fa'||result.h1.length!==1||result.title!==result.h1[0]) fail(route,'lang/title/H1',result);
  if(result.brokenImages.length) fail(route,'broken images',result.brokenImages);
  if(result.wrongCodeDirection.length||result.wrongLabelFont.length||result.svgClipped.length||!result.persianFont||!result.bodyFont.includes('Vazirmatn')) fail(route,'RTL typography at '+width,result);
  const picker=page.locator('details.language-picker').first();
  if(await picker.count()) {
    await picker.locator('summary').click();
    const box=await picker.locator('.lp-panel').boundingBox();
    if(!box||box.x< -2||box.x+box.width>width+2) fail(route,'language picker bounds',{width,box});
    const links=await picker.locator('a[hreflang]').evaluateAll(es=>es.map(e=>({lang:e.hreflang,href:e.getAttribute('href')})));
    if(!links.some(l=>l.lang==='fa')||!links.some(l=>l.lang==='en')) fail(route,'language menu missing EN/FA',links);
    await page.keyboard.press('Escape');
  } else fail(route,'missing language picker',width);
  if([390,1280].includes(width)) await page.screenshot({path:path.join(out,(route==='/fa/'?'home':route.split('/').filter(Boolean).at(-1))+'-'+width+'.png')});
}
const watchdog = setTimeout(()=>abortRun('timed_out',new Error('Overall browser QA exceeded 35 minutes')),overallTimeoutMs);
(async()=>{
  checkpoint('running');
  browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const context=await browser.newContext({viewport:{width:1280,height:900},...(!live?{serviceWorkers:'block'}:{})});
  if(!live) await context.route('**/*',async r=>{
    const u=new URL(r.request().url());
    if(u.hostname!=='vpsforwebsite.com') return r.abort();
    let file=path.resolve(build,'.'+decodeURIComponent(u.pathname));
    if(!path.extname(file))file=path.join(file,'index.html');
    if(!file.startsWith(build+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile())return r.fulfill({status:404,body:'Not found'});
    const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.woff2':'font/woff2','.ico':'image/x-icon','.xml':'application/xml'};
    return r.fulfill({status:200,body:fs.readFileSync(file),contentType:types[path.extname(file)]||'application/octet-stream'});
  });
  else await context.route(/google-analytics\.com|googletagmanager\.com/,r=>r.abort());
  const page=await context.newPage();
  page.on('pageerror',e=>fail(new URL(page.url()).pathname,'JavaScript error',e.message));
  try {
    for(const width of widths) {
      await page.setViewportSize({width,height:900});
      for(const pair of manifest.routes) {
        if (terminating) return;
        console.log('FA_QA_PAGE_START',width,pair.fa);
        try {
          await open(page,pair.fa);
          await inspect(page,pair.fa,width);
          if(width===390&&!geometryOnly) {
            const persian=await formMatrix(page);
            console.log('FA_QA_MATRIX_DONE','fa',pair.fa,JSON.stringify(persian.map(f=>({id:f.id,cases:f.cases,outcomes:f.unique.length}))));
            if(persian.length) {
              await open(page,pair.en);
              const english=await formMatrix(page);
              console.log('FA_QA_MATRIX_DONE','en',pair.en,JSON.stringify(english.map(f=>({id:f.id,cases:f.cases,outcomes:f.unique.length}))));
              assert.equal(persian.length,english.length);
              for(let i=0;i<english.length;i++) {
                const e=english[i],d=persian[i];
                for(const key of ['id','ids','domains','numberCases','sequence']) assert.deepEqual(d[key],e[key],pair.fa+' '+key);
                assert.equal(d.unique.length,e.unique.length);
                for(let j=0;j<e.unique.length;j++) {
                  assert.notEqual(d.unique[j],e.unique[j],'Untranslated result '+d.id);
                  assert.deepEqual(d.unique[j].match(/\d+(?:[.,]\d+)?/g),e.unique[j].match(/\d+(?:[.,]\d+)?/g),'Result numbers '+d.id);
                }
                forms.push({route:pair.fa,id:d.id,cases:d.cases,outcomes:d.unique.length,results:d.unique});
              }
              // Actual pointer submission confirms keyboard/event wiring and visible result.
              await open(page,pair.fa);
              for(const f of persian) {
                const form=page.locator('[id="'+f.id+'"]');
                for(const input of await form.locator('input[type="number"]').all()) {
                  const value=await input.inputValue();
                  if(!value)await input.fill(await input.getAttribute('placeholder')||'0');
                }
                await form.locator('button[type="submit"]').click();
                assert.ok((await page.locator('[id="'+outputs[f.id]+'"]').innerText()).length>10);
              }
            }
          }
        } catch(e) {fail(pair.fa,'case at '+width,String(e.stack||e));}
        if (terminating) return;
        checkpoint('running');
        console.log('FA_QA_PAGE_DONE',width,pair.fa,'forms',forms.length,'findings',findings.length);
      }
      console.log('FA_QA_WIDTH_DONE',width,'findings',findings.length);
    }
    // Switch real equivalent pages, not merely inspect href strings.
    await page.setViewportSize({width:1280,height:900});
    for(const pair of [manifest.routes.find(r=>r.fa==='/fa/'),...manifest.routes.filter(r=>/word|migration|location/.test(r.source))].filter(Boolean)) {
      try {
        await open(page,pair.fa);
        await page.locator('details.language-picker summary').first().click();
        await page.locator('details.language-picker a[hreflang="en"]').first().click();
        assert.equal(decodeURIComponent(new URL(page.url()).pathname),pair.en);
        await page.locator('details.language-picker summary').first().click();
        await page.locator('details.language-picker a[hreflang="fa"]').first().click();
        assert.equal(decodeURIComponent(new URL(page.url()).pathname),pair.fa);
      } catch(e) {fail(pair.fa,'language roundtrip',String(e));}
    }
  } finally {await browser.close();}
  if (terminating) return;
  const expectedForms=geometryOnly?0:(manifest.expectedForms ?? 16);
  const report=checkpoint(findings.length||forms.length!==expectedForms?'failed':'completed');
  console.log('FA_QA_SUMMARY',JSON.stringify({pages:report.pages,geometry:report.geometryCases,forms:report.forms,formCases:report.formCases,failures:findings.length}));
  if(findings.length||forms.length!==expectedForms)process.exitCode=1;
  clearTimeout(watchdog);
})().catch(e=>abortRun('failed',e));
