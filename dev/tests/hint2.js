const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:60,level:3,age:5,zoo:[]}))}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1200);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});
const all=require('fs').readFileSync(process.argv[2]||'gids.txt','utf8').split(',');
const res=[];let n=0;
for(const id of all){await p.evaluate(()=>document.querySelector('[data-tab="play"]').click());await p.waitForTimeout(300);await p.evaluate(id=>__T.openGame(id,true),id);await p.waitForTimeout(3600);
  const r=await p.evaluate(()=>{const h=document.querySelector('#hintHand.on'),t=document.querySelector('.hintme');return h&&t?(String(t.getAttribute('class')||'').split(' ')[0]||t.tagName):'-'});res.push(id+':'+r);
  if(['home','dots','memory','spot','paint','sort'].includes(id)&&n<4&&r!=='-'){n++;await p.waitForTimeout(250);await p.screenshot({path:`w10/h_${id}.png`})}}
console.log(res.join('  '));console.log('ERR',errs);await b.close()})();
