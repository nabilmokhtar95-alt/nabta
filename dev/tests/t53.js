const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/ERR_FILE|TUNNEL/.test(m.text()))errs.push(m.text())});
await p.addInitScript(()=>{Date.prototype.getHours=function(){return 14};if(!sessionStorage.x){sessionStorage.x=1;const Z=(e,n,f,full,clean)=>({e,n,food:f,lvl:0,xp:0,full,clean:clean??1,joy:.8,t:Date.now()});localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,brand:1,gtut:1,coins:30,level:6,age:4,dailyGift:1,barn:{corn:1},
 zoo:[Z('🐰','أرنوب','carrot',.9),Z('🐢','سلحوفة','tulip',.9),Z('🐥','كتكوت','strawberry',.9),Z('🐑','خروفة','sunflower',.9),Z('🦔','قنفود','tomato',.9),Z('🐪','جمل','corn',.2),Z('🦎','سحلية','carrot',.9),Z('🐠','سمكة','tulip',.9),Z('🐧','بطريق','strawberry',.9,.1)]}))}});
let n=0;const shot=async t=>{n++;await p.screenshot({path:`w8/${String(n).padStart(2,'0')}_${t}.png`})};
const st=()=>p.evaluate(()=>{const g=NG.game.scene.getScene('garden'),D=NG.D,cv=document.querySelector('#gGame').getBoundingClientRect();return{page:NG.page,pets:g.pets.map(q=>[q.i,cv.left+q.x/D,cv.top+(g.petY-q.h/2)/D]),arr:g.arrows.map(A=>A.c.visible?[A.dir,cv.left+A.c.x/D,cv.top+A.c.y/D,A.bd.visible]:null),hand:g.hand.visible?[Math.round(g.hand.x/D),Math.round(g.hand.y/D)]:null,chip:document.querySelector('#ngTask').textContent}});
await p.goto('file://'+process.cwd()+'/test28.html');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#tPlay').click());await p.waitForTimeout(1500);await p.evaluate(()=>{document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click())});await p.waitForTimeout(2500);
let S0=await st();console.log('p0',JSON.stringify(S0));await shot('page0');
const R=S0.arr.find(a=>a&&a[0]>0);await p.mouse.click(R[1],R[2]);await p.waitForTimeout(1200);S0=await st();console.log('p1',JSON.stringify(S0));await shot('page1');
const camel=S0.pets.find(q=>q[0]===5);await p.mouse.click(camel[1],camel[2]);await p.waitForTimeout(3000);await shot('fed');
console.log('camel full',await p.evaluate(()=>__T.S.zoo[5].full));
// swipe left to page 2
const y=S0.pets[0][2];await p.mouse.move(320,y);await p.mouse.down();await p.mouse.move(200,y,{steps:5});await p.mouse.move(80,y,{steps:5});await p.mouse.up();await p.waitForTimeout(1500);
S0=await st();console.log('p2',JSON.stringify(S0));await shot('page2');
// back with left arrow twice
for(let k=0;k<2;k++){const L=(await st()).arr.find(a=>a&&a[0]<0);if(L){await p.mouse.click(L[1],L[2]);await p.waitForTimeout(1200)}}
console.log('back',JSON.stringify(await st()));
// tap every pet on every page (non-needy -> card), close cards
for(let pg=0;pg<3;pg++){const s1=await st();for(const q of s1.pets){await p.mouse.click(q[1],q[2]);await p.waitForTimeout(700);await p.evaluate(()=>{const x=document.querySelector('[data-pcx]');if(x&&x.offsetParent)x.click();document.querySelectorAll('#scrim.open [data-close]').forEach(e=>e.click());const bx=document.querySelector('.bathw');if(bx){const c=document.querySelector('.bathx,[data-bx]');c&&c.click()}})}
  const Rr=(await st()).arr.find(a=>a&&a[0]>0);if(Rr){await p.mouse.click(Rr[1],Rr[2]);await p.waitForTimeout(1200)}}
await shot('end');
console.log('ERR',errs);await b.close()})();
