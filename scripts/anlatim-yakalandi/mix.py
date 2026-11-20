import subprocess,sys
from lines import L
from words import W
cnt=[len(x[1].split()) for x in L]; print(sum(cnt),len(W)); assert sum(cnt)==len(W)
seg=[];i=0
prev=0
for (t,txt),n in zip(L,cnt):
    a0,b0=W[i][0],W[i+n-1][1]; tt=max(t,prev+.15); seg.append((a0,b0,tt)); prev=tt+(b0-a0)/1000; i+=n
    if tt>t+.05: print('shift',txt[:30],round(tt-t,2))
f=[];lab=[]
for j,(a,b,t) in enumerate(seg):
    s=max(0,a-80)/1000; e=min(71680,b+180)/1000; d=int(t*1000)
    f.append(f"[1:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.06:.3f}:d=0.06,adelay={d}|{d}[n{j}]"); lab.append(f"[n{j}]")
f.append(''.join(lab)+f"amix=inputs={len(seg)}:normalize=0,aresample=44100,pan=stereo|c0=c0|c1=c0,volume=5.5,asplit=2[nar][sc]")
f.append("[0:a]aresample=44100[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[duck]")
f.append("[duck][nar]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i',sys.argv[2],'-i',sys.argv[3],'-filter_complex',';'.join(f),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',sys.argv[1]],check=True)
for (a,b,t) in seg: 
    if t+(b-a)/1000 > 102.3: print('OVER',t)
