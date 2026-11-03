const {chromium,devices}=require('playwright');
const IDS=['home','food','jobs','weather','feel','senses','healthy','daynight','transport','nextnum','letterfind','shapesreal','colormix','clock','dots','group','spot','xo','ispy','balloons','mix'];
(async()=>{const b=await chromium.launch();const c=await b.newContext({...devices['iPhone 13']});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.addInitScript(()=>{if(!sessionStorage.x){sessionStorage.x=1;const d=new Date(),k=d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();localStorage.setItem('nabta-garden',JSON.stringify({v:1,named:1,name:'سلمى',brand:1,gtut:1,coins:333,level:4,age:5,daily:{last:k,streak:1,best:1},look:{pot:'pink',head:'flower'}}))}});
await p.goto('file:///tmp/claude-0/-home-user/873d36e4-d936-5efd-8447-973afa772e0b/scratchpad/test28.html');await p.waitForTimeout(800);
await p.evaluate(()=>{document.querySelector('#tPlay')?.click()});await p.waitForTimeout(500);
await p.evaluate(()=>{document.querySelector('#scrim.open [data-close]')?.click();document.querySelector('[data-tab="play"]').click()});await p.waitForTimeout(500);
await p.screenshot({path:'s28/hub.png',fullPage:true});
for(const lv of [1,5]){
for(const id of IDS){
 await p.evaluate(([id,lv])=>{const S=__T.S;S.glvl=S.glvl||{};S.glvl[id]=lv;S.tut=S.tut||{};},[id,lv]);
 if(lv===1&&id==='xo'){await p.evaluate(id=>{delete __T.S.tut[id];__T.openGame(id)},id);await p.waitForTimeout(500);await p.screenshot({path:'s28/tut_xo.png'});await p.evaluate(()=>document.querySelector('[data-tutgo]').click())}
 else await p.evaluate(id=>__T.openGame(id,true),id);
 await p.waitForTimeout(lv===1?500:200);if(lv===1||id==='clock'||id==='spot')await p.screenshot({path:`s28/${id}_${lv}.png`});
 let n=0,done=false;
 while(n<200&&!done){n++;
  done=await p.evaluate(()=>!!document.querySelector('.ribbon'));if(done)break;
  await p.evaluate(()=>{const {Q,DT,SP,XO,BL}=__T;
   const ok=document.querySelector('#stage [data-ok="1"]:not(.good):not(.blo)');if(ok&&!(Q&&Q.busy)){ok.click();return}
   if(DT&&!DT.busy){document.querySelector(`[data-dot="${DT.i}"]`)?.dispatchEvent(new MouseEvent("click",{bubbles:true}));return}
   if(SP&&!SP.busy){const i=[...SP.diff].find(i=>!SP.found.has(i));document.querySelector(`[data-sp="${i}"]`)?.click();return}
   if(XO&&!XO.busy){const f=XO.b.findIndex(v=>!v);document.querySelector(`[data-xo="${f}"]`)?.click();return}
   if(BL){const bl=[...document.querySelectorAll('.blo[data-ok="1"]:not(.pop)')].find(x=>{const r=x.getBoundingClientRect();return r.top>0&&r.bottom<innerHeight});bl&&bl.click();return}
  });
  await p.waitForTimeout(id==='balloons'?300:id==='dots'?120:350);
 }
 const r=await p.evaluate(()=>[document.querySelector('.ribbon')?.textContent,document.querySelectorAll('.bigstars span:not(.off)').length]);
 console.log(lv,id,n,r.join(' '));
 if(lv===1&&['xo','balloons','dots'].includes(id))await p.screenshot({path:`s28/${id}_end.png`});
}}
console.log('ERR',errs);await b.close()})();
