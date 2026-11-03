# split3.py REPO [--apply] : align pauses to sentences by expected length (DP), report fit, optionally cut
import json,os,re,subprocess,sys,math
R=sys.argv[1];APPLY='--apply' in sys.argv;V=os.path.join(R,'voice');D=json.load(open(os.path.join(V,'lines.json')))
L={x['n']:x for x in D['lines']};idx=json.load(open(os.path.join(V,'index.json')))
def sil(f):
    out=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-38dB:d=0.1','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: (-?[\d.]+)',out)];en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',out);total=int(m.group(2))*60+float(m.group(3))
    sp=[(max(0,s),e) for s,e in zip(st,en)]
    head=sp[0][1] if sp and sp[0][0]<=0.05 else 0
    tail=sp[-1][0] if sp and sp[-1][1]>=total-0.05 else total
    inner=[(s,e) for s,e in sp if s>head+0.05 and e<tail-0.05]
    return inner,head,tail
def wl(t):return len(re.sub(r'\s','',t))
out=[]
for b in D['blocks']:
    f=os.path.join(V,'raw','block-%02d.mp3'%b['b'])
    if not os.path.exists(f):continue
    S,head,tail=sil(f);N=len(b['lines']);ch=[wl(L[n]['say']) for n in b['lines']]
    C=[head]+[(s+e)/2 for s,e in S]+[tail];P=[0]+[e-s for s,e in S]+[0];m=len(C)-1
    if m<N:out.append(f'block {b["b"]}: too few pauses ({m})');continue
    a=0.35;k=((tail-head)-N*a)/sum(ch)
    for it in range(4):
        INF=1e18;dp=[[INF]*(m+1) for _ in range(N+1)];bk=[[0]*(m+1) for _ in range(N+1)];dp[0][0]=0
        for i in range(1,N+1):
            pred=a+k*ch[i-1]
            for j in range(i,m+1-(N-i)):
                best=INF;bj=-1
                for p in range(i-1,j):
                    if dp[i-1][p]>=INF:continue
                    seg=C[j]-C[p];c=dp[i-1][p]+((seg-pred)/pred)**2*4-(0.8*math.log(P[j]+0.05) if j<m else 0)
                    if c<best:best=c;bj=p
                dp[i][j]=best;bk[i][j]=bj
        cut=[m];j=m
        for i in range(N,0,-1):j=bk[i][j];cut.append(j)
        cut=cut[::-1];segs=[C[cut[i+1]]-C[cut[i]] for i in range(N)]
        # refit a,k by least squares
        n_=N;sx=sum(ch);sy=sum(segs);sxx=sum(x*x for x in ch);sxy=sum(x*y for x,y in zip(ch,segs))
        k=max(0.02,(n_*sxy-sx*sy)/(n_*sxx-sx*sx or 1));a=max(0.1,(sy-k*sx)/n_)
    pred=[a+k*c for c in ch];err=[abs(s-p)/p for s,p in zip(segs,pred)]
    ok=max(err)<0.5 and sorted(err)[-3]<0.35
    out.append(f'block {b["b"]}: maxErr={max(err):.2f} 3rd={sorted(err)[-3]:.2f} rate={1/k:.1f}ch/s {"OK" if ok else "CHECK"}  segs='+' '.join(f'{s:.1f}' for s in segs))
    if APPLY and ok:
        for i,n in enumerate(b['lines']):
            o='%03d.mp3'%n;s0=C[cut[i]];s1=C[cut[i+1]]
            subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f,'-ss',f'{max(0,s0-0.03):.3f}','-to',f'{s1+0.03:.3f}','-af','silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,afade=t=in:d=0.02,apad=pad_dur=0.05','-b:a','64k',os.path.join(V,o)],check=True)
            idx[L[n]['key']]=o
if APPLY:json.dump(idx,open(os.path.join(V,'index.json'),'w'),ensure_ascii=False,indent=0)
print('\n'.join(out));print('mapped',len(idx))
