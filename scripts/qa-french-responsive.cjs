/* Real-Chromium responsive and interaction audit for the 18 live French routes. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const routes = [
  '/', '/a-propos/', '/checklist-securite-vps/', '/choisir-localisation-vps/',
  '/contact/', '/dimensionnement-vps-site-web/', '/hebergement-vps-fastpanel/',
  '/heberger-site-web-sur-vps/', '/migration-site-web-vers-vps/',
  '/politique-de-confidentialite/', '/strategie-sauvegarde-vps/', '/supervision-vps/',
  '/vps-avec-panneau-de-controle/', '/vps-infogere-ou-non-infogere/',
  '/vps-ou-hebergement-mutualise/', '/vps-pour-plusieurs-sites/',
  '/vps-pour-woocommerce/', '/vps-pour-wordpress/'
];
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
const widths=[320,360,390,430,768,1024,1280,1920];
const out='/tmp/qa-fr-responsive';
fs.mkdirSync(out,{recursive:true});
const findings=[],samples=[],formChecks=[];
const fail=(route,width,message,detail)=>{findings.push({route,width,message,detail});console.error('FR_QA_FAIL',route,width,message,JSON.stringify(detail||{}).slice(0,900));};

async function examine(page,route,width){
  const url='https://vpsforwebsite.com/fr'+route+'?responsive-qa=20261020-'+width;
  const errors=[];
  page.removeAllListeners('pageerror');
  page.on('pageerror',e=>errors.push(e.message));
  let resp=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  if(!resp || resp.status()!==200){
    fail(route,width,'non-200 response',resp&&resp.status());return;
  }
  await page.locator('main h1').first().waitFor({timeout:16000});
  await page.evaluate(async()=>{if(document.fonts)await document.fonts.ready;});
  // Candidate stylesheet preview: the working-branch Chromium run injects only
  // the proposed FR home CSS; the main-branch run audits deployed CSS alone.
  if(process.env.GITHUB_REF_NAME==='work/fr-responsive-qa-20261020' && route==='/'){
    await page.addStyleTag({path:path.resolve('static/css/fr-home-responsive.v1.css')});
  }
  await page.waitForTimeout(120);
  const audit=await page.evaluate(()=>{
    const W=document.documentElement.clientWidth;
    const elmain=document.querySelector('main');
    const isVisible=(el)=>{
      const cs=getComputedStyle(el),r=el.getBoundingClientRect();
      return cs.display!=='none' && cs.visibility!=='hidden' && r.width>0 && r.height>0;
    };
    const box=(el)=>{const r=el.getBoundingClientRect();return {tag:el.tagName.toLowerCase(),cls:String(el.className||'').slice(0,80),left:Math.round(r.left*10)/10,right:Math.round(r.right*10)/10,width:Math.round(r.width*10)/10};};
    const selector='header .navbar,main h1,main h2,main h3,main .content,main .vps-page-header,main .vps-hero-copy,main [class*="-hero-grid"],main form,main form select,main form input,main button,main a.btn,main .vps-table-scroll,main .vps-affiliate-disclosure,footer .container';
    const blockers=[...document.querySelectorAll(selector)]
      .filter(isVisible).map(box)
      .filter(r=>r.left< -2.5 || r.right>W+2.5)
      .slice(0,15);
    const textOverflow=[...document.querySelectorAll('main h1, main h2, main h3, main a.btn, main button, main form select')]
      .filter(isVisible).filter(el=>{
        const s=getComputedStyle(el);
        return (el.scrollWidth>el.clientWidth+3) && !['scroll','auto'].includes(s.overflowX);
      }).map(el=>({text:el.textContent.trim().slice(0,95),tag:el.tagName,width:el.clientWidth,scroll:el.scrollWidth})).slice(0,12);
    const wrappers=[...document.querySelectorAll('main .vps-table-scroll')].filter(isVisible);
    const tableBoxes=wrappers.map(el=>({clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,overflowX:getComputedStyle(el).overflowX,right:el.getBoundingClientRect().right,left:el.getBoundingClientRect().left}));
    const css=document.querySelector('#site-critical-css');
    const links=[...document.querySelectorAll('main a[href^="#"]')].map(x=>x.getAttribute('href')).filter(x=>x && x.length>1);
    const missingAnchors=[...new Set(links)].filter(x=>{try{return !document.getElementById(decodeURIComponent(x.slice(1)));}catch{return false;}});
    return {
      doc:document.documentElement.scrollWidth,
      body:document.body.scrollWidth,
      client:document.documentElement.clientWidth,
      lang:document.documentElement.lang,
      title:document.title.trim(),
      h1:[...document.querySelectorAll('main h1')].map(x=>x.innerText.trim()),
      blockerCount:blockers.length,blockers,textOverflow,
      tableBoxes,tableCount:document.querySelectorAll('main table').length,
      forms:document.querySelectorAll('main form').length,
      picker:!!document.querySelector('details.language-picker'),
      criticalCSS:!!css && !!css.sheet,
      missingAnchors,
      hero:elmain&&elmain.getBoundingClientRect().width
    };
  });
  samples.push({route,width,audit});
  if(audit.doc>width+2||audit.body>width+2)fail(route,width,'document horizontal overflow',{doc:audit.doc,body:audit.body});
  if(audit.blockers.length)fail(route,width,'major element outside viewport',audit.blockers);
  if(audit.textOverflow.length)fail(route,width,'text clipped / overflowing',audit.textOverflow);
  if(audit.lang!=='fr')fail(route,width,'incorrect html lang',audit.lang);
  if(audit.h1.length!==1||audit.title!==audit.h1[0])fail(route,width,'title/H1 mismatch',{title:audit.title,h1:audit.h1});
  if(!audit.criticalCSS)fail(route,width,'site critical CSS failed to load');
  if(audit.missingAnchors.length)fail(route,width,'broken internal anchors',audit.missingAnchors.slice(0,10));
  for(const b of audit.tableBoxes){
    if(b.right>width+2.5 || b.left< -2.5)fail(route,width,'table scroll wrapper overflow',b);
    if(b.scrollWidth>b.clientWidth+2 && !['auto','scroll'].includes(b.overflowX))fail(route,width,'wide table has no local horizontal scrolling',b);
  }
  if(errors.length)fail(route,width,'uncaught JS errors',errors.slice(0,6));
  if(width===320||width===390){
    let picker=page.locator('details.language-picker').first();
    if(await picker.count()){
      try{
        await picker.locator('summary').click({timeout:6000});
        const b=await picker.locator('.lp-panel').evaluate(el=>{let r=el.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,screen:document.documentElement.clientWidth}});
        if(b.left < -2 || b.right>b.screen+2)fail(route,width,'language picker panel escapes viewport',b);
        await page.keyboard.press('Escape');
      }catch(e){fail(route,width,'language picker interaction',String(e).slice(0,240));}
    }else fail(route,width,'missing language picker');
  }
  if(width===390){
    const forms=await page.locator('main form[id]').evaluateAll(els=>els.map(x=>x.id));
    for(const id of forms){
      const target=outputs[id];
      if(!target){fail(route,width,'unmapped form',id);continue;}
      const form=page.locator('[id="'+id+'"]');
      try{
        const mandatory=await form.locator('input[type=number][required]').all();
        for(const inp of mandatory){
          const v=await inp.inputValue();if(v.trim())continue;
          const min=Number(await inp.getAttribute('min')||0),max=Number(await inp.getAttribute('max')||500000);
          const placeholder=Number(await inp.getAttribute('placeholder')||512);
          const value=String(Math.max(min,Math.min(max,Number.isFinite(placeholder)?placeholder:512)));
          await inp.fill(value);
        }
        await form.locator('button[type=submit]').first().click({timeout:10000});
        const result=page.locator('[id="'+target+'"]');
        await result.waitFor({state:'attached',timeout:6000});
        const txt=(await result.textContent()||'').trim();
        if(txt.length<10)fail(route,width,'form produced empty result',{form:id,result:target,text:txt});
        else formChecks.push({route,form:id,chars:txt.length});
      }catch(e){fail(route,width,'form submission failed',{form:id,reason:String(e).slice(0,300)});}
    }
  }
  if([320,390,1280].includes(width) && ['/', '/strategie-sauvegarde-vps/', '/vps-pour-plusieurs-sites/', '/politique-de-confidentialite/', '/supervision-vps/'].includes(route)){
    const safe=(route==='/'?'home':route.replace(/\W+/g,'-'));
    try{await page.screenshot({path:path.join(out,'fr-'+safe+'-'+width+'.png'),fullPage:width!==320,timeout:25000});}
    catch(e){console.warn('Screenshot unavailable',route,width,String(e).slice(0,130));}
  }
  console.log('FR_QA_CASE',route,width,'doc',audit.doc,'body',audit.body,'table',audit.tableCount,'forms',audit.forms,'blocks',audit.blockers.length);
}
(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    for(const width of widths){
      const context=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,isMobile:width<=430,hasTouch:width<=430});
      const page=await context.newPage();
      for(const route of routes){
        try{await examine(page,route,width);}
        catch(e){fail(route,width,'uncaught audit exception',String(e.stack||e).slice(0,550));}
      }
      await context.close();
      console.log('FR_QA_WIDTH_DONE',width,'issues-so-far',findings.length);
    }
  }finally{await browser.close();}
  const report={total:routes.length*widths.length,failures:findings.length,formsPassed:formChecks.length,findings,forms:formChecks,samples};
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));
  console.log('FR_QA_SUMMARY',JSON.stringify({cases:report.total,failed:findings.length,formsPassed:formChecks.length,issues:findings.slice(0,25)}));
  if(findings.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack||e);process.exitCode=1;});
