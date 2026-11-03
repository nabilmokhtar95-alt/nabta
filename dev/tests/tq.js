const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:60,level:3,age:5,zoo:[],tut:{catch:1,home:1}}))}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1200);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});
const tap=async s=>{const e=await p.$(s);const bb=await e.boundingBox();await p.mouse.click(bb.x+bb.width/2,bb.y+bb.height/2)};
await p.evaluate(()=>document.querySelector('[data-tab="play"]').click());await p.waitForTimeout(600);await p.evaluate(()=>__T.openGame('catch'));await p.waitForTimeout(1200);
await p.evaluate(()=>{const b=[...document.querySelectorAll('#stage button')].find(x=>/ابدأ/.test(x.textContent));b.click()});await p.waitForTimeout(5500);
const a1=await p.evaluate(()=>[__T.AR.state,__T.AR.t.toFixed(1),__T.AR.score]);
await tap('[data-tut]');await p.waitForTimeout(400);await p.screenshot({path:'w10/q1.png'});await p.waitForTimeout(2000);
const a2=await p.evaluate(()=>[__T.AR.state,__T.AR.t.toFixed(1),__T.AR.score,!!document.querySelector('#tutOv')]);
await tap('[data-tutx]');await p.waitForTimeout(1500);const a3=await p.evaluate(()=>[__T.AR.state,__T.AR.t.toFixed(1),!!document.querySelector('#tutOv')]);
console.log('catch',JSON.stringify([a1,a2,a3]));
await p.evaluate(()=>document.querySelector('[data-back]')&&document.querySelector('[data-back]').click());await p.waitForTimeout(500);
await p.evaluate(()=>__T.openGame('home'));await p.waitForTimeout(1200);
for(let i=0;i<2;i++){await p.evaluate(()=>{const o=document.querySelector('#stage [data-ok="1"]');o&&o.click()});await p.waitForTimeout(1800)}
const q1=await p.evaluate(()=>[__T.Q.n,__T.Q.id]);await tap('[data-tut]');await p.waitForTimeout(800);await tap('[data-tutx]');await p.waitForTimeout(500);
const q2=await p.evaluate(()=>[__T.Q.n,__T.Q.id,!!document.querySelector('#stage [data-ok]')]);console.log('quiz',JSON.stringify([q1,q2]));
console.log('ERR',errs);await b.close()})();
