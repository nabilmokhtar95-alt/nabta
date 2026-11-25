# builds audio.wav (voice + original synthesized music + sfx) and env.json (voice loudness per frame: drives the talking mouth)
import numpy as np,subprocess,json,wave,os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ep2')
SR=44100;DUR=45.2;FPS=30;V='/home/user/nabta/voice/'
VO=[(4.6,'011',1.6),(7.2,'052',0),(19.0,'053',0),(23.2,'003',0),(25.6,'058',0),(34.0,'101',0),(36.0,'095',0),(38.4,'001',0)]
def load(n,cut):
    a=['ffmpeg','-v','error','-i',V+n+'.mp3']+(['-t',str(cut)] if cut else [])+['-f','f32le','-ac','1','-ar',str(SR),'-']
    x=np.frombuffer(subprocess.run(a,capture_output=True).stdout,dtype=np.float32).copy()
    f=int(.06*SR);x[-f:]*=np.linspace(1,0,f);return x/max(1e-6,np.abs(x).max())*.9
N=int(DUR*SR);voice=np.zeros(N);music=np.zeros(N);sfx=np.zeros(N);rain_=np.zeros(N);SPL=[15.4,16.5]
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
def rainm(t0,t1):   # playful pizzicato in the rain (pentatonic)
    seq='C5 - E5 G5 - E5 A5 G5 E5 - D5 - C5 D5 E5 -'.split();bas='A2 E3 F2 C3 G2 D3 C3 G2'.split();t=t0;i=0
    while t<t1-.1:
        m=seq[i%len(seq)]
        if m!='-':put(music,t,pluck(fq(m),.3),.55)
        if i%2==0:put(music,t,pluck(fq(bas[(i//2)%len(bas)]),.4),.6)
        t+=.27;i+=1
def bath(t0,t1):    # bubbly music box
    mel='C6 E6 G6 E6 F6 A6 G6 - E6 G6 C7 G6 D6 F6 E6 -'.split();t=t0;i=0
    while t<t1-.1:
        m=mel[i%len(mel)]
        if m!='-':put(music,t,box(fq(m),.9),.3)
        if i%4==0:put(music,t,mar(fq('C3'),.7),.5)
        if i%4==2:put(music,t,mar(fq('G3'),.7),.5)
        t+=.25;i+=1
sectA(0.2,6.9)
for n in ('A2','E3','C4'):put(music,7.0,pad(fq(n),3.0),.25)                      # thirsty: soft minor chord
for n in ('F2','C3','A3'):put(music,9.6,pad(fq(n),1.8),.2)
rainm(11.4,18.6)
for k,n in enumerate('C5 E5 G5 C6 E6'.split()):put(music,19.3+k*.16,box(fq(n),1.6),.35)
sectA(21.6,28.2,.8)
bath(28.4,33.6)
sectA(33.8,41.4,1.05,.22)
for n in ('C4','E4','G4','C5'):put(music,41.8,pad(fq(n),3.2),.16)
for k,n in enumerate('C5 E5 G5 C6 E6'.split()):put(music,42.0+k*.18,box(fq(n),2),.3)
def sweep(f0,f1,d,g=1):t=tt(d);f=f0*(f1/f0)**(t/d);ph=2*np.pi*np.cumsum(f)/SR;return g*np.sin(ph)*np.minimum(1,t/.01)*np.minimum(1,(d-t)/.05)
rng=np.random.default_rng(3)
def noise(d,g=1,lp=.2):
    x=rng.standard_normal(int(d*SR));y=np.zeros_like(x);a=0.
    for i in range(len(x)):a+=lp*(x[i]-a);y[i]=a
    t=tt(d);return g*y*np.minimum(1,t/.03)*np.minimum(1,(d-t)/.1)*3
pop=lambda:sweep(300,900,.09,.8)
def chirp():return sweep(2600,3600,.07,.35)
def thunder():t=tt(2.2);return noise(2.2,1.0,.03)*np.exp(-t*1.4)*1.6+np.sin(2*np.pi*(55+15*np.sin(2*np.pi*3*t))*t)*np.exp(-t*1.8)*.6
def splash():return noise(.45,.8,.5)*np.exp(-tt(.45)*7)
def blub(f):return sweep(f,f*2.2,.08,.35)
S=[(2.6,noise(.35,.35,.08)),(10.4,thunder()*.35),(12.25,pop()*.6),(28.3,pop()),(29.0,splash()),(33.7,splash()*.6),(33.75,pop())]
for t in np.arange(3.2,4.4,.2):S.append((t,sweep(200,120,.06,.35)))
for t in (3.7,4.1,5.6,12.3,14.9,22.8,34.3,36.1,39.0):S+=[(t,chirp()),(t+.12,chirp())]
for a in SPL:S.append((a,splash()))
for t in np.arange(29.5,33.4,.17):S.append((t,blub(500+((t*1000)%7)*90)))
for t,x in S:put(sfx,t,x)
# soft rain: a quiet, filtered bed that fades in and out (and dips under the voice in the mix)
rd=7.8;rainbed=noise(rd,.22,.35);tr=tt(rd);rainbed*=np.minimum(1,tr/1.2)*np.minimum(1,(rd-tr)/1.4);put(rain_,11.2,rainbed)
for i in range(60):                                    # a few individual drops on leaves
    t0=11.6+i*.11+((i*37)%10)*.01
    if t0<18.4:put(rain_,t0,sweep(1800+(i*131)%900,900,.03,.08))
def chime(t,ns,gap=.07,g=.5):
    for k,n in enumerate(ns):put(sfx,t+k*gap,mar(fq(n),.7),g)
chime(19.25,['C6','E6','G6']);chime(23.1,['E6','G6']);chime(33.8,['C6','E6','G6','C7','E7']);chime(38.0,['C6','E6','G6','C7'])
venv=np.convolve(np.abs(voice),np.ones(int(.25*SR))/int(.25*SR),'same');duck=1-np.clip(venv*6,0,.6)
duck2=1-np.clip(venv*10,0,.85)      # the rain all but stops while someone talks
mix=voice*1.0+music*.2*duck+sfx*.45*duck+rain_*.5*duck2
mix=mix/max(1,np.abs(mix).max())*.97
f=int(1.0*SR);mix[-f:]*=np.linspace(1,0,f)
w=wave.open(OUT+'.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
json.dump([round(float(v),2) for v in env],open(OUT+'.env.json','w'));print('ok',len(env))
