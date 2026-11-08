# make.py — rebuilds the game from dev/src/nabta-garden.html
#   out/nabta-game.html  : version for the claude.ai artifact
#   out/test28.html      : same + test hooks (window.__T / NG / __D) for dev/tests
#   ../game.html         : the published game (manifest, offline worker, install button)
import os
D=os.path.dirname(os.path.abspath(__file__));O=os.path.join(D,'out');os.makedirs(O,exist_ok=True)
s=open(os.path.join(D,'src','nabta-garden.html'),encoding='utf8').read()
i=s.index('</style>')+len('</style>')
art=f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="جنينة نبتة: لعبة تعليمية للأطفال من نبتة - Fun Learning Activities">
<meta name="theme-color" content="#0faeb0">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}</style>
{s[:i]}
</head><body>
{s[i:]}
</body></html>
'''
open(os.path.join(O,'nabta-game.html'),'w',encoding='utf8').write(art)
s=art
m="/* =================== TITLE =================== */"
s=s.replace(m,"window.__T={get S(){return S},openGame,get Q(){return Q},get DT(){return DT},get SP(){return SP},get XO(){return XO},get BL(){return BL},get AR(){return AR},get G(){return G},startLevel,get ADV(){return ADV}};window.NG=NG;window.__D={drawNabta:(...a)=>drawNabta(...a),NA,DEFLOOK,naPose:(...a)=>naPose(...a),NP};\n"+m,1)
open(os.path.join(O,'test28.html'),'w',encoding='utf8').write(s)
s=art
head='''<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#0faeb0">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="نبتة">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="apple-touch-icon" href="icons/icon-192.png">
<link rel="icon" type="image/png" href="icons/icon-192.png">
'''
tail='''<style>.pwa-inst{position:fixed;left:50%;top:calc(10px + env(safe-area-inset-top,0px));translate:-50% 0;z-index:500;display:flex;align-items:center;gap:8px;max-width:calc(100vw - 24px);background:#fff;color:#0b6f71;font-weight:800;font-size:13.5px;line-height:1.35;text-align:start;border:0;border-radius:999px;padding:10px 18px;box-shadow:0 5px 0 #0b8587,0 10px 24px rgba(0,0,0,.2);font-family:inherit}.pwa-inst b{font-size:22px}.pwa-inst i{font-style:normal;opacity:.5;margin-inline-start:6px}</style>
<script>
(()=>{if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost'))addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));
 const standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone;if(standalone)return;
 let dp=null;const show=(txt,fn)=>{if(document.querySelector('.pwa-inst'))return;const b=document.createElement('button');b.className='pwa-inst';b.innerHTML='<b>📲</b>'+txt+'<i data-x>✕</i>';
   b.onclick=e=>{if(e.target.closest('[data-x]')){b.remove();try{localStorage.setItem('nabta-pwa-x','1')}catch(_){}return}fn&&fn(b)};document.body.appendChild(b)};
 try{if(localStorage.getItem('nabta-pwa-x'))return}catch(_){}
 addEventListener('beforeinstallprompt',e=>{e.preventDefault();dp=e;show('نثبّت اللعبة على الموبايل',b=>{dp.prompt();dp.userChoice.finally(()=>b.remove())})});
 if(/iphone|ipad|ipod/i.test(navigator.userAgent))setTimeout(()=>{if(!document.documentElement.classList.contains('boot'))show('للتثبيت: ⬆️ مشاركة ثم «إضافة إلى الشاشة الرئيسية»',b=>b.remove())},6000);
})();
</script>
'''
assert '</head>' in s and '</body>' in s
# hosted build: move the inline webp art out to ga/*.webp so the page itself is small and loads fast
import re,hashlib,base64,glob
GA=os.path.join(D,'..','ga');os.makedirs(GA,exist_ok=True);keep=set()
def ext(m):
    b=base64.b64decode(m.group(1));n=hashlib.sha1(b).hexdigest()[:12]+'.webp';keep.add(n)
    f=os.path.join(GA,n)
    if not os.path.exists(f):open(f,'wb').write(b)
    return 'ga/'+n
s=re.sub(r'data:image/webp;base64,([A-Za-z0-9+/=]+)',ext,s)
for f in glob.glob(os.path.join(GA,'*.webp')):
    if os.path.basename(f) not in keep:os.remove(f)
open(os.path.join(GA,'index.js'),'w').write('self.GA='+repr(sorted('ga/'+k for k in keep)).replace("'",'"')+';\n')
s=s.replace('</head>',head+'</head>',1)
i=s.rfind('</body>');s=s[:i]+tail+s[i:]
open(os.path.join(D,'..','game.html'),'w',encoding='utf8').write(s);print('built',len(s))
