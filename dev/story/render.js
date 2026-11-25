// render.js — node render.js <episode.html> <seconds> [prev t1 t2 ...]
//   with "prev": screenshots at the given times (pv_<t>.png); without: every frame at 30fps into fr/
//   the voice loudness file (env json named in the page's data-env) drives the talking motion
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const [file,secs,mode,...ts]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 const envf=path.join(__dirname,file.replace(/\.html$/,'')+'.env.json');
 if(fs.existsSync(envf))await p.addInitScript(`window.__ENV=${fs.readFileSync(envf,'utf8')}`);
 await p.goto('file://'+path.join(__dirname,file));await p.waitForTimeout(800);
 if(mode==='prev'){for(const t of ts.map(Number)){await p.evaluate(t=>setT(t),t);await p.waitForTimeout(120);await p.screenshot({path:path.join(__dirname,`pv_${t}.png`)})}}
 else{const D=path.join(__dirname,'fr');fs.rmSync(D,{recursive:true,force:true});fs.mkdirSync(D);const N=Math.round(+secs*30);
  for(let i=0;i<N;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:`${D}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}}
 console.log('errors',errs.slice(0,3));await b.close()})();
