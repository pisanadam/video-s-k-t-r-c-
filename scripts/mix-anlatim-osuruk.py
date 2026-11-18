# Speko (Cartesia "Aykut") ile üretilen anlatımı cümle cümle videoya yerleştirir, müziği altında kısar.
# Kullanım: python3 scripts/mix-anlatim-osuruk.py cikti.mp4 osuruk-ham.mp4 assets/anlatim/osuruk-anlatim.mp3
import subprocess,sys
seg=[(100,2900,.3),(3100,5000,3.3),(5400,8000,5.6),(8200,10200,8.2),(10400,11900,10.5),(12200,14100,13.7),(14700,16300,16.0),(16500,17800,18.4),(18100,19600,20.7),(20000,21800,23.1),
(22100,23200,26.4),(23400,25100,28.7),(25400,26700,31.1),(27000,28200,33.4),(28500,29500,35.8),(29800,31500,39.1),(31900,34000,41.4),(34500,36900,43.8),(37300,39300,46.3),(39600,40600,48.6),(41000,42200,51.8),(42400,45800,54.4)]
f=[];lab=[]
for i,(a,b,t) in enumerate(seg):
    s=max(0,a-80)/1000; e=min(45920,b+160)/1000; d=int(t*1000)
    f.append(f"[1:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.06:.3f}:d=0.06,adelay={d}|{d}[n{i}]"); lab.append(f"[n{i}]")
f.append(''.join(lab)+f"amix=inputs={len(seg)}:normalize=0,aresample=44100,pan=stereo|c0=c0|c1=c0,volume=5.5,asplit=2[nar][sc]")
f.append("[0:a]aresample=44100[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[duck]")
f.append("[duck][nar]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]")
cmd=['ffmpeg','-v','error','-y','-i',sys.argv[2],'-i',sys.argv[3],'-filter_complex',';'.join(f),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',sys.argv[1]]
subprocess.run(cmd,check=True)
