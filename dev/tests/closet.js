const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:300,level:3,age:4,dailyGift:1,zoo:[]}))}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1500);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});
await p.evaluate(()=>document.querySelector('[data-tab="closet"]').click());await p.waitForTimeout(2000);await p.screenshot({path:'w9/c1.png'});
// try the head tab and an item
const tabs=await p.$$eval('[data-slot],[data-wtab],[data-cat]',els=>els.map(e=>e.outerHTML.slice(0,80)));console.log(tabs.slice(0,10));
await p.evaluate(()=>{const t=[...document.querySelectorAll('button')].find(b=>/على الراس/.test(b.textContent));t&&t.click()});await p.waitForTimeout(1000);
await p.evaluate(()=>document.querySelector('#wardGrid')&&document.querySelector('#wardGrid').scrollIntoView());await p.waitForTimeout(400);await p.screenshot({path:'w9/c2.png'});
await p.evaluate(()=>{const g=document.querySelectorAll('#wardGrid .card');g[2]&&g[2].click()});await p.waitForTimeout(1200);await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:'w9/c3.png'});
console.log('ERR',errs);await b.close()})();
