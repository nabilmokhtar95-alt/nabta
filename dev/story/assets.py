# assets.py — pulls the character art out of the game source into dev/story/a/ (not committed; run once per machine)
import os,json,base64
D=os.path.dirname(os.path.abspath(__file__));O=os.path.join(D,'a');os.makedirs(O,exist_ok=True)
s=open(os.path.join(D,'..','src','nabta-garden.html'),encoding='utf8').read()
n=0
for name in ['NART','PART','BART','ZART']:
    d,_=json.JSONDecoder().raw_decode(s[s.index('const '+name+'=')+len('const '+name+'='):])
    def walk(o,pre):
        global n
        for k,v in o.items():
            if isinstance(v,dict):walk(v,pre+k+'_')
            elif isinstance(v,str) and v.startswith('data:image'):
                open(os.path.join(O,f'{name}_{pre}{k}.webp'),'wb').write(base64.b64decode(v.split(',',1)[1]));n+=1
    walk(d,'')
print('extracted',n,'images to',O)
