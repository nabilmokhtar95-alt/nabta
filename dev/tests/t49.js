const {chromium,devices}=require('playwright');
const out='w6';
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,name:'سلمى',brand:1,gtut:1,coins:60,level:2,age:4,
 zoo:[{e:'🐰',n:'أرنوب',food:'carrot',lvl:0,xp:0,full:.2,joy:.6,t:Date.now()},{e:'🐢',n:'سلحوفة',food:'strawberry',lvl:0,xp:0,full:.9,joy:.8,t:Date.now()},{e:'🐥',n:'كتكوت',food:'tulip',lvl:1,xp:0,full:.9,clean:.1,joy:.8,t:Date.now()}]}))}});
let n=0;const shot=async t=>{n++;await p.screenshot({path:`${out}/${String(n).padStart(2,'0')}_${t}.png`})};
const tapSel=async s=>{const e=await p.$(s);if(!e){console.log('MISSING',s);return}const bb=await e.boundingBox();await p.mouse.click(bb.x+bb.width/2,bb.y+bb.height/2)};
const sc=()=>p.evaluate(()=>{const g=NG.game&&NG.game.scene.getScene("garden");if(!g)return null;const D=NG.D,cv=document.querySelector("#gGame").getBoundingClientRect();return{ox:cv.left,oy:cv.top,beds:g.beds.map(b=>[b.x/D,(g.bedY-40*D)/D]),pets:g.pets.map(q=>[q.x/D,(g.petY-q.h/2)/D]),busy:g.busy}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await tapSel('#tPlay');await p.waitForTimeout(1500);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});await p.waitForTimeout(1500);await shot('garden');
let G=await sc();console.log(JSON.stringify(G));
await p.mouse.click(G.ox+G.pets[0][0],G.oy+G.pets[0][1]);await p.waitForTimeout(800);await shot('tap_hungry');
await tapSel('[data-ngs="carrot"]');await p.waitForTimeout(2500);await shot('planted');
await p.mouse.click(G.ox+G.beds[0][0],G.oy+G.beds[0][1]);await p.waitForTimeout(700);await shot('watering');await p.waitForTimeout(1500);
await p.evaluate(()=>{__T.S.plots[0].growth=1});await p.waitForTimeout(800);await shot('ready');
await p.mouse.click(G.ox+G.beds[0][0],G.oy+G.beds[0][1]);await p.waitForTimeout(2200);await shot('harvested');
await p.mouse.click(G.ox+G.pets[0][0],G.oy+G.pets[0][1]);await p.waitForTimeout(800);await shot('feeding');await p.waitForTimeout(1500);await shot('fed');
console.log('ERR',errs,await p.evaluate(()=>JSON.stringify([__T.S.zoo[0].full,__T.S.barn,__T.S.plots.slice(0,3)])));await b.close()})();
