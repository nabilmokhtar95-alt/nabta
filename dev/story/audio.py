# builds audio.wav (voice + original synthesized music + sfx) and env.json (voice loudness per frame, drives the talking motion)
import numpy as np,subprocess,json,wave,sys
SR=44100;DUR=47.0;FPS=30;V='/home/user/nabta/voice/'
VO=[(4.6,'011',1.6),(7.0,'034',0),(10.0,'082',1.75),(13.3,'003',0),(15.4,'052',0),(18.3,'053',0),(23.2,'029',0),(26.6,'085',0),(28.2,'085',0),(29.8,'088',0),(32.4,'004',0),(34.0,'046',0),(38.0,'094',0),(39.9,'001',0),(41.3,'021',0)]
def load(n,cut):
    a=['ffmpeg','-v','error','-i',V+n+'.mp3']+(['-t',str(cut)] if cut else [])+['-f','f32le','-ac','1','-ar',str(SR),'-']
    x=np.frombuffer(subprocess.run(a,capture_output=True).stdout,dtype=np.float32).copy()
    f=int(.06*SR);x[-f:]*=np.linspace(1,0,f);return x/max(1e-6,np.abs(x).max())*.9
N=int(DUR*SR);voice=np.zeros(N);music=np.zeros(N);sfx=np.zeros(N)
def put(buf,t,x,g=1.0):
    i=int(t*SR);x=x[:max(0,N-i)];buf[i:i+len(x)]+=x*g
env=np.zeros(int(DUR*FPS)+1)
for t,n,c in VO:
    x=load(n,c);put(voice,t,x)
    for k in range(int(len(x)/SR*FPS)+1):
        seg=x[int(k*SR/FPS):int((k+1)*SR/FPS)]
        if len(seg):env[int(t*FPS)+k]=min(1,float(np.sqrt((seg**2).mean()))*3.2)
tt=lambda d:np.arange(int(d*SR))/SR
def mar(f,d=.5,g=1):t=tt(d);return g*(np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*4*t)*np.exp(-t*30))*np.exp(-t*7)
def pluck(f,d=.35,g=1):t=tt(d);return g*(np.sign(np.sin(2*np.pi*f*t))*.25+np.sin(2*np.pi*f*t))*np.exp(-t*14)
def pad(f,d,g=1):t=tt(d);e=np.minimum(1,t/.3)*np.minimum(1,(d-t)/.4);return g*e*(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.005*t))
NT={'C':261.63,'D':293.66,'E':329.63,'F':349.23,'G':392.0,'A':440.0,'B':493.88}
def fq(s):
    o=int(s[-1]);return NT[s[0]]*2**(o-4)
# A: happy garden theme, 120bpm
A_mel='E5 G5 C6 G5 A5 G5 E5 - D5 F5 A5 F5 G5 E5 C5 - E5 G5 C6 E6 D6 C6 A5 - G5 A5 G5 E5 D5 E5 C5 -'.split()
A_bas='C3 G3 C3 G3 F3 C4 F3 C4 G3 D4 G3 D4 C3 G3 C3 G3'.split()
def sectA(t0,t1,g=1.0,step=.25):
    t=t0;i=0
    while t<t1-.1:
        m=A_mel[i%len(A_mel)]
        if m!='-':put(music,t,mar(fq(m),.5),.5*g)
        if i%2==0:put(music,t,mar(fq(A_bas[(i//2)%len(A_bas)]),.6),.55*g)
        t+=step;i+=1
def sectB(t0,t1):
    seq='A2 - C3 - E3 - C3 - A2 - C3 - F3 E3 D3 -'.split();t=t0;i=0
    while t<t1-.1:
        m=seq[i%len(seq)]
        if m!='-':put(music,t,pluck(fq(m),.4),.7)
        if i%8==4:put(music,t,pluck(fq('E4'),.2),.25);put(music,t+.15,pluck(fq('D4'),.2),.25)
        t+=.3;i+=1
sectA(0.2,20.6);put(music,20.6,pad(fq('A2'),1.2),.3)
sectB(21.0,30.4)
for k,n in enumerate('C5 E5 G5 C6'.split()):put(music,30.6+k*.12,mar(fq(n),.8),.6)
sectA(32.6,45.0,1.1,.22)
for n in ('C4','E4','G4','C5'):put(music,45.0,pad(fq(n),1.9),.16)
# sfx
def sweep(f0,f1,d,g=1,sh='sin'):t=tt(d);f=f0*(f1/f0)**(t/d);ph=2*np.pi*np.cumsum(f)/SR;return g*np.sin(ph)*np.minimum(1,t/.01)*np.minimum(1,(d-t)/.05)
rng=np.random.default_rng(3)
def noise(d,g=1,lp=.2):
    x=rng.standard_normal(int(d*SR));y=np.zeros_like(x);a=0.
    for i in range(len(x)):a+=lp*(x[i]-a);y[i]=a
    t=tt(d);return g*y*np.minimum(1,t/.03)*np.minimum(1,(d-t)/.1)*3
pop=lambda:sweep(300,900,.09,.8);boing=lambda:sweep(220,660,.22,.6)*(1+.3*np.sin(2*np.pi*30*tt(.22)))
thud=lambda:sweep(160,50,.18,1.0)+noise(.1,.25,.5)[:int(.1*SR)].tolist().__len__()*0
def chime(ns,gap=.07,g=.5):
    for k,n in enumerate(ns):put(sfx,chime.t+k*gap,mar(fq(n),.7),g)
S=[(2.6,noise(.35,.35,.08)),(8.0,sweep(500,1200,.3,.3)),(8.55,sweep(160,50,.18,.9)),(8.6,pop()),(10.9,noise(1.2,.35,.6)),(12.0,pop()),(13.0,pop()),
   (15.0,sweep(600,200,.7,.35)),(17.6,noise(1.1,.35,.6)),(26.6,boing()),(27.2,sweep(160,50,.18,1)),(28.2,boing()),(28.8,sweep(160,50,.18,1)),(29.8,boing()),(30.4,sweep(140,40,.25,1.2)),(30.4,noise(.2,.5,.3)),
   (30.6,sweep(300,1800,.9,.35)),(37.2,boing()*.6),(37.65,boing()*.6)]
for t in np.arange(3.2,4.4,.2):S.append((t,sweep(200,120,.06,.35)))
for t in np.arange(21.2,23.2,.5):S.append((t,sweep(180,320,.16,.3)))
for t,x in S:put(sfx,t,x)
for t,ns in [(13.05,['E6','G6']),(18.8,['C6','E6','G6']),(32.0,['G6','C7']),(33.2,['C6','E6','G6','C7','E7']),(39.6,['C5','E5','G5','C6'])]:chime.t=t;chime(ns)
# duck music under the voice
venv=np.convolve(np.abs(voice),np.ones(int(.25*SR))/int(.25*SR),'same');duck=1-np.clip(venv*6,0,.6)
mix=voice*1.0+music*.22*duck+sfx*.5
mix=mix/max(1,np.abs(mix).max())*.97
f=int(.8*SR);mix[-f:]*=np.linspace(1,0,f)
w=wave.open('audio.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
json.dump([round(float(v),2) for v in env],open('env.json','w'));print('ok',len(env))
