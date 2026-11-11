const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+__dirname+'/ep1.html');await p.waitForTimeout(800);
if(process.argv[2]==='prev'){const T=process.argv.slice(3).map(Number);for(const t of T){await p.evaluate(t=>setT(t),t);await p.waitForTimeout(120);await p.screenshot({path:`pv_${t}.png`})}}
else{require('fs').mkdirSync('fr',{recursive:true});const N=Math.round(61.5*30);for(let i=0;i<N;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:`fr/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}}
console.log(errs.slice(0,3));await b.close()})();
