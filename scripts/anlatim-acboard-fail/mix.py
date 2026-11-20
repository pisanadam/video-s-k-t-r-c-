import subprocess,sys
from lines import SEG
f=[];lab=[]
for j,(t,a,b,_) in enumerate(SEG):
    s=max(0,a-80)/1000; e=min(24800,b+150)/1000; d=int(t*1000)
    f.append(f"[1:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.06:.3f}:d=0.06,adelay={d}|{d}[n{j}]"); lab.append(f"[n{j}]")
    if j and t < SEG[j-1][0]+(SEG[j-1][2]-SEG[j-1][1])/1000: print('OVERLAP',j)
f.append(''.join(lab)+f"amix=inputs={len(SEG)}:normalize=0,aresample=44100,pan=stereo|c0=c0|c1=c0,volume=5.5,apad,asplit=2[nar][sc]")
f.append("[0:a]aresample=44100[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[duck]")
f.append("[duck][nar]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i',sys.argv[2],'-i',sys.argv[3],'-filter_complex',';'.join(f),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',sys.argv[1]],check=True)
