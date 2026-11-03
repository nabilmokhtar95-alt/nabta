const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:60,level:2,age:4,plots:[{type:'tulip',growth:.1,water:1},null,null],zoo:[{e:'🐰',n:'أرنوب',food:'carrot',lvl:0,xp:0,full:.9,joy:.6,t:Date.now()}]}))}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1500);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});await p.waitForTimeout(2500);
const G=await p.evaluate(()=>{const g=NG.game.scene.getScene('garden'),D=NG.D,cv=document.querySelector('#gGame').getBoundingClientRect();return{x:cv.left+g.beds[0].x/D,y:cv.top+(g.bedY-40*D)/D}});
const g0=await p.evaluate(()=>__T.S.plots[0].growth);
for(let i=0;i<5;i++){await p.mouse.click(G.x,G.y);await p.waitForTimeout(900)}
const g1=await p.evaluate(()=>__T.S.plots[0].growth);await p.screenshot({path:'w10/grow.png'});
console.log('growth',g0.toFixed(2),'->',g1.toFixed(2),'chip',await p.evaluate(()=>document.querySelector('#ngTask').innerText),'ERR',errs);await b.close()})();
