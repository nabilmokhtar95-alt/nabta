# builds audio.wav (voice + original synthesized music + sfx) and env.json (voice loudness per frame: drives the talking mouth)
import numpy as np,subprocess,json,wave
SR=44100;DUR=61.5;FPS=30;V='/home/user/nabta/voice/'
VO=[(4.6,'011',1.6),(7.0,'034',0),(10.0,'082',1.75),(13.0,'053',0),(21.4,'003',0),(24.8,'029',0),(27.6,'085',0),(29.2,'085',0),(30.8,'088',0),(32.9,'004',0),(39.9,'046',0),(46.6,'105',1.12),(49.4,'105',0),(52.6,'001',0),(54.0,'021',0)]
def load(n,cut):
    a=['ffmpeg','-v','error','-i',V+n+'.mp3']+(['-t',str(cut)] if cut else [])+['-f','f32le','-ac','1','-ar',str(SR),'-']
    x=np.frombuffer(subprocess.run(a,capture_output=True).stdout,dtype=np.float32).copy()
    f=int(.06*SR);x[-f:]*=np.linspace(1,0,f);return x/max(1e-6,np.abs(x).max())*.9
N=int(DUR*SR);voice=np.zeros(N);music=np.zeros(N);sfx=np.zeros(N)
def put(buf,t,x,g=1.0):
    i=int(t*SR);x=x[:max(0,N-i)];buf[i:i+len(x)]+=x*g
env=np.zeros(int(DUR*FPS)+2)
for t,n,c in VO:
    x=load(n,c);put(voice,t,x)
    for k in range(int(len(x)/SR*FPS)+1):
        seg=x[int(k*SR/FPS):int((k+1)*SR/FPS)]
        if len(seg):env[int(t*FPS)+k]=min(1,float(np.sqrt((seg**2).mean()))*3.2)
tt=lambda d:np.arange(int(d*SR))/SR
def mar(f,d=.5,g=1):t=tt(d);return g*(np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*4*t)*np.exp(-t*30))*np.exp(-t*7)
def box(f,d=1.2,g=1):t=tt(d);return g*(np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*3*t))*np.exp(-t*3.2)
def pluck(f,d=.35,g=1):t=tt(d);return g*(np.sign(np.sin(2*np.pi*f*t))*.25+np.sin(2*np.pi*f*t))*np.exp(-t*14)
def pad(f,d,g=1):t=tt(d);e=np.minimum(1,t/.4)*np.minimum(1,(d-t)/.5);return g*e*(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.005*t))
NT={'C':261.63,'D':293.66,'E':329.63,'F':349.23,'G':392.0,'A':440.0,'B':493.88}
fq=lambda s:NT[s[0]]*2**(int(s[-1])-4)
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
def lull(t0,t1):   # night: music box over soft chords
    mel='E5 G5 E5 C5 D5 F5 D5 B4 C5 E5 G5 E5 D5 - C5 -'.split();ch=[('C3','G3','E4'),('G2','D3','B3'),('A2','E3','C4'),('F2','C3','A3')]
    t=t0;i=0
    while t<t1-.2:
        if i%4==0:
            for n in ch[(i//4)%4]:put(music,t,pad(fq(n),2.3),.22)
        m=mel[i%len(mel)]
        if m!='-':put(music,t,box(fq(m)*2,1.4),.33)
        t+=.55;i+=1
def sad(t0,t1):
    ch=[('A2','E3','C4'),('F2','C3','A3'),('D3','A3','F4'),('E3','B3','G4')];mel='E5 - D5 C5 - A4 - - F5 - E5 D5 - B4 - -'.split()
    t=t0;i=0
    while t<t1-.2:
        if i%4==0:
            for n in ch[(i//4)%4]:put(music,t,pad(fq(n),2.6),.3)
        m=mel[i%len(mel)]
        if m!='-':put(music,t,box(fq(m),1.6),.4)
        t+=.6;i+=1
sectA(0.2,15.3)
lull(15.6,20.4)
for k,n in enumerate('G5 C6 E6 G6'.split()):put(music,20.5+k*.14,mar(fq(n),.9),.5)
sectA(21.2,22.4)
put(music,22.5,pad(fq('A2'),1.2),.3);sectB(22.9,31.3)
for k,n in enumerate('C5 E5 G5 C6'.split()):put(music,31.5+k*.12,mar(fq(n),.8),.5)
sad(33.9,38.9)
sectA(39.5,51.9,1.0)
sectA(52.0,57.0,1.15,.2)
for n in ('C4','E4','G4','C5'):put(music,57.0,pad(fq(n),3.6),.16)
for k,n in enumerate('C5 E5 G5 C6 E6'.split()):put(music,57.2+k*.18,box(fq(n),2),.3)
def sweep(f0,f1,d,g=1):t=tt(d);f=f0*(f1/f0)**(t/d);ph=2*np.pi*np.cumsum(f)/SR;return g*np.sin(ph)*np.minimum(1,t/.01)*np.minimum(1,(d-t)/.05)
rng=np.random.default_rng(3)
def noise(d,g=1,lp=.2):
    x=rng.standard_normal(int(d*SR));y=np.zeros_like(x);a=0.
    for i in range(len(x)):a+=lp*(x[i]-a);y[i]=a
    t=tt(d);return g*y*np.minimum(1,t/.03)*np.minimum(1,(d-t)/.1)*3
pop=lambda:sweep(300,900,.09,.8)
def boing():t=tt(.22);return sweep(220,660,.22,.6)*(1+.3*np.sin(2*np.pi*30*t))
def rumble():t=tt(.9);return np.sin(2*np.pi*(70+25*np.sin(2*np.pi*7*t))*t)*np.minimum(1,t/.1)*np.minimum(1,(.9-t)/.3)*.9
S=[(2.6,noise(.35,.35,.08)),(8.0,sweep(500,1200,.3,.3)),(8.55,sweep(160,50,.18,.9)),(8.6,pop()),(10.9,noise(1.5,.35,.6)),(12.0,pop()),
   (23.6,rumble()),(27.6,boing()),(28.17,sweep(160,50,.18,1)),(29.2,boing()),(29.77,sweep(160,50,.18,1)),(30.8,boing()),(31.37,sweep(140,40,.25,1.2)),(31.37,noise(.2,.5,.3)),
   (31.45,sweep(700,180,1.0,.3)),(34.5,sweep(900,500,.25,.25)),(34.9,sweep(850,450,.3,.25)),(36.2,rumble()),(38.0,mar(1760,.6,.6)),(38.12,mar(2349,.8,.6)),
   (45.9,sweep(500,1100,.3,.3)),(46.4,pop()),(47.45,boing()*.6),(47.95,boing()*.6),(48.8,sweep(500,1100,.3,.3)),(49.3,pop())]
for t in np.arange(3.2,4.4,.2):S.append((t,sweep(200,120,.06,.35)))
for t in np.arange(22.9,24.6,.5):S.append((t,sweep(180,320,.16,.3)))
for t in np.arange(44.1,45.5,.28):S.append((t,sweep(200,120,.06,.3)))
for t in np.arange(16.6,19.6,.75):                       # crickets
    for k in range(3):S.append((t+k*.07,sweep(4200,4400,.04,.07)))
for t in (46.7,47.0,47.3,49.6,49.9,50.2):S.append((t,sweep(260,200,.07,.4)))   # chewing
for t,x in S:put(sfx,t,x)
def chime(t,ns,gap=.07,g=.5):
    for k,n in enumerate(ns):put(sfx,t+k*gap,mar(fq(n),.7),g)
chime(12.05,['E6','G6']);chime(18.3,['C6','E6','G6','C7'],.12,.35);chime(39.2,['C6','E6','G6','C7','E7']);chime(46.45,['E6','G6']);chime(52.3,['C5','E5','G5','C6'])
venv=np.convolve(np.abs(voice),np.ones(int(.25*SR))/int(.25*SR),'same');duck=1-np.clip(venv*6,0,.6)
mix=voice*1.0+music*.24*duck+sfx*.5
mix=mix/max(1,np.abs(mix).max())*.97
f=int(1.0*SR);mix[-f:]*=np.linspace(1,0,f)
w=wave.open('audio.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
json.dump([round(float(v),2) for v in env],open('env.json','w'));print('ok',len(env))
