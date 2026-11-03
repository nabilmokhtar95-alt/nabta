const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/ERR_FILE|TUNNEL/.test(m.text()))errs.push(m.text())});
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:60,level:2,age:4,adv2:1,
 zoo:[{e:'🐥',n:'كتكوت',food:'tulip',lvl:1,xp:0,full:.9,clean:.1,joy:.8,t:Date.now()},{e:'🐰',n:'أرنوب',food:'carrot',lvl:0,xp:0,full:.9,joy:.6,t:Date.now()}]}))}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.screenshot({path:'w7/0title.png'});
await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1500);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});await p.waitForTimeout(1500);
const G=await p.evaluate(()=>{const g=NG.game.scene.getScene('garden'),D=NG.D,cv=document.querySelector('#gGame').getBoundingClientRect();return{x:cv.left+g.pets[0].x/D,y:cv.top+(g.petY-g.pets[0].h/2)/D}});
await p.mouse.click(G.x,G.y);await p.waitForTimeout(900);await p.screenshot({path:'w7/1bath.png'});
const w=await (await p.$('.bathw')).boundingBox();for(let i=0;i<6;i++){await p.mouse.click(w.x+w.width*(.3+.08*i),w.y+w.height*.5);await p.waitForTimeout(120)}await p.screenshot({path:'w7/2bath_mid.png'});
for(let i=0;i<6;i++){await p.mouse.click(w.x+w.width*.5,w.y+w.height*.4);await p.waitForTimeout(120)}await p.waitForTimeout(900);await p.screenshot({path:'w7/3bath_done.png'});
await p.evaluate(()=>document.querySelector('[data-pcx]').click());
await p.evaluate(()=>document.querySelector('[data-tab="map"]').click());await p.waitForTimeout(1200);await p.evaluate(()=>document.querySelector('.anode.next').click());await p.waitForTimeout(2500);await p.evaluate(()=>document.querySelector('.aigo').click());
for(let k=0;k<160;k++){const r=await p.evaluate(()=>{const sc=__T.ADV&&__T.ADV.game&&__T.ADV.game.scene.getScene('adv');if(!sc||sc.done)return 'done';
  const bf=sc.bf.find(b=>b.active&&!b.got&&b.x>sc.nab.x-30&&b.x<sc.nab.x+200);if(bf&&!sc.jumping){sc.tx=bf.x;sc.want=bf}else sc.tx=Math.min(sc.cx-110,sc.nab.x+220);if(sc.blocked)sc.jump();return [Math.round(sc.nab.x),__T.ADV.got,sc.nF,__T.ADV.coins]});
  if(r==='done')break;await p.waitForTimeout(220);if(k===20||k===40)await p.screenshot({path:'w7/4adv'+k+'.png'})}const chst=await p.evaluate(()=>{const sc=__T.ADV.game.scene.getScene('adv');return [!!sc.pet,sc.ch&&sc.ch.open]});console.log('pet,chest',JSON.stringify(chst));
await p.waitForTimeout(3500);await p.screenshot({path:'w7/5win.png'});
console.log('ERR',errs,await p.evaluate(()=>JSON.stringify([__T.S.zoo[0].clean,__T.S.adv2,__T.S.coins])));await b.close()})();
