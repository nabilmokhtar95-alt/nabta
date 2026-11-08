// site.js — checks the published site end to end (store + game.html)
// run:  npx http-server -p 8765 -s -c-1 .   (from the repo root)   then   NODE_PATH=$(npm root -g) node dev/tests/site.js
const {chromium}=require('playwright');const BASE=process.env.BASE||'http://localhost:8765/';
const ok=(c,m)=>{console.log((c?'✓ ':'✗ ')+m);if(!c)process.exitCode=1};
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844},serviceWorkers:'block'});const errs=[],bad=[];
 const pg=async u=>{const p=await ctx.newPage();p.on('pageerror',e=>errs.push(u+': '+e.message));p.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url())});await p.goto(BASE+u);await p.waitForTimeout(1200);return p};
 // store: order form
 const s=await pg('index.html');
 await s.locator('#grid [data-add]').first().click();await s.click('#cartBtn');await s.waitForTimeout(400);
 await s.fill('#oName','تجربة');await s.fill('#oPhone','٠١٠١٢٣');await s.selectOption('#oGov',{index:1});await s.fill('#oAddr','العنوان');
 await s.click('#orderF button[type=submit]');ok(!(await s.evaluate(()=>document.querySelector('#oErr').hidden)),'store rejects a short phone number');
 await s.fill('#oPhone','٠١٠١٢٣٤٥٦٧٨');await s.click('#orderF button[type=submit]');ok((await s.textContent('#oMsg')||'').includes('01012345678'),'store builds the order message with latin digits');
 await s.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,50))}});await s.waitForTimeout(800);
 ok(await s.evaluate(()=>[...document.images].every(i=>!i.getAttribute('src')||!i.complete||i.naturalWidth>0)),'store images all load');
 // game: title, stories, parent gate
 const g=await pg('game.html');
 await g.click('#tStories');await g.waitForTimeout(400);ok(await g.isVisible('[data-story="worm"]'),'game opens the stories list');
 await g.click('[data-story="worm"]');await g.waitForTimeout(1500);ok(await g.evaluate(()=>document.querySelector('#stVid').currentTime>0),'story video plays');
 await g.evaluate(()=>document.querySelector('#stVid').dispatchEvent(new Event('ended')));await g.click('[data-sop="0"]');await g.waitForTimeout(2200);
 ok(await g.evaluate(()=>!document.querySelector('#storyV').classList.contains('on')),'right answer closes the story');
 await g.click('#tPlay');await g.waitForTimeout(800);await g.keyboard.press('Escape');await g.waitForTimeout(300);await g.click('[data-tab="toys"]');await g.waitForTimeout(500);
 let pops=0;ctx.on('page',()=>pops++);await g.locator('a[href^="http"]:visible').first().click();await g.waitForTimeout(300);
 ok(await g.evaluate(()=>document.querySelector('#pgate').classList.contains('on'))&&pops===0,'outside links ask a grown-up first');
 ok(await g.evaluate(()=>[...document.images].every(i=>!i.getAttribute('src')||!i.complete||i.naturalWidth>0)),'game images all load');
 ok(!errs.length,'no script errors '+errs.join(' | '));ok(!bad.length,'no missing files '+bad.join(' | '));
 await b.close()})();
