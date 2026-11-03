const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:60,level:3,age:4,dailyGift:1,
 plots:[{type:'carrot',growth:.4,water:.5},{type:'tulip',growth:.6,water:.5},null],zoo:[{e:'🐰',n:'أرنوب',food:'carrot',lvl:0,xp:0,full:.2,joy:.6,t:Date.now()},{e:'🐢',n:'سلحوفة',food:'strawberry',lvl:0,xp:0,full:.9,joy:.8,t:Date.now()},{e:'🐥',n:'كتكوت',food:'tulip',lvl:1,xp:0,full:.9,clean:.1,joy:.8,t:Date.now()},{e:'🦄',n:'يونيكورن',food:'tulip',lvl:0,xp:0,full:.9,joy:.8,t:Date.now()}]}))}});
const cdp=await c.newCDPSession(p);await cdp.send('Emulation.setCPUThrottlingRate',{rate:6});
await p.goto('file://'+process.cwd()+'/'+(process.argv[2]||'test28.html'));await p.waitForTimeout(1500);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(2500);
await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});await p.waitForTimeout(1500);
await cdp.send('Profiler.enable');await cdp.send('Profiler.start');
if(process.argv[3])await p.evaluate(process.argv[3]);await p.waitForTimeout(300);const r=await p.evaluate(()=>new Promise(res=>{let n=0,worst=0,last=performance.now();const t0=last;const f=t=>{n++;worst=Math.max(worst,t-last);last=t;if(t-t0<4000)requestAnimationFrame(f);else res({fps:n/4,worst:Math.round(worst),pfps:NG.game?Math.round(NG.game.loop.actualFps):null})};requestAnimationFrame(f)}));
const prof=(await cdp.send('Profiler.stop')).profile;
const self={};const byId={};prof.nodes.forEach(n=>byId[n.id]=n);const dt=prof.timeDeltas;const samples=prof.samples;
for(let i=0;i<samples.length;i++){const n=byId[samples[i]];const k=(n.callFrame.functionName||'(anon)')+' @'+n.callFrame.lineNumber;self[k]=(self[k]||0)+(dt[i]||0)}
console.log(JSON.stringify(r));console.log(Object.entries(self).sort((a,b)=>b[1]-a[1]).slice(0,18).map(([k,v])=>Math.round(v/1000)+'ms '+k).join('\n'));
await b.close()})();
