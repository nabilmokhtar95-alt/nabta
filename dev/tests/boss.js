const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:60,level:3,age:4,adv2:2,zoo:[{e:'🐰',n:'أرنوب',food:'carrot',lvl:0,xp:0,full:.9,joy:.6,t:Date.now()}]}))}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1500);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});
await p.evaluate(()=>document.querySelector('[data-tab="map"]').click());await p.waitForTimeout(1200);await p.screenshot({path:'bugs/b0.png'});
await p.evaluate(()=>document.querySelector('.anode.next').click());await p.waitForTimeout(2500);await p.screenshot({path:'bugs/b1.png'});await p.evaluate(()=>document.querySelector('.aigo').click());
let shot=0;
for(let k=0;k<260;k++){const r=await p.evaluate(()=>{const sc=__T.ADV&&__T.ADV.game&&__T.ADV.game.scene.getScene('adv');if(!sc||sc.done)return 'done';
  if(sc.bossOn&&sc.king&&!sc.king.out){const lim=sc.king.x-sc.king.displayWidth*.4-35;sc.tx=lim;if(Math.abs(sc.nab.x-lim)<25&&!sc.jumping)sc.jump();return 'boss'+sc.king.hp}
  sc.tx=Math.min(sc.cx-110,sc.nab.x+220);if(sc.blocked)sc.jump();return [Math.round(sc.nab.x),__T.ADV.got]});
  if(r==='done')break;if(String(r).startsWith('boss')&&shot<2){shot++;await p.waitForTimeout(shot==1?1600:300);await p.screenshot({path:'bugs/b'+(shot+1)+'.png'})}
  await p.waitForTimeout(200)}
console.log(await p.evaluate(()=>{const sc=__T.ADV.game.scene.getScene('adv');return JSON.stringify({x:Math.round(sc.nab.x),cx:sc.cx,got:__T.ADV.got,nF:sc.nF,king:!!sc.king,kx:sc.king&&sc.king.x,bossOn:sc.bossOn,busy:sc.busy,fl:sc.fl.map(f=>[f.x,f.st]),blocked:sc.blocked,rocks:sc.rocks.map(r=>r.x)})}));await p.waitForTimeout(800);await p.screenshot({path:'bugs/b4.png'});await p.waitForTimeout(3500);
console.log('adv2',await p.evaluate(()=>__T.S.adv2),'ERR',errs);await b.close()})();
