# "Osuruk" kelimelerindeki s sesini (tıslama) granüler yöntemle uzatır, kelime zamanlarını kaydırır.
import wave, numpy as np, sys
W0=[(100,1400),(1400,1800),(1800,1900),(1900,2300),(2700,3200),(3200,3600),(4000,4600),(5000,5400),(6100,6600),(7000,7500),(7900,8700),(8700,9300),(9500,10200),(10300,10600),(10600,11200),(11300,11700),(11700,12300),(12500,13000),(13000,13600),(13700,14200),(14200,14400),(14400,14900),(15200,15500),(15500,16000),(16400,16600),(16600,17300),(17600,18000),(18000,18600),(18600,19200),(19600,20000),(20000,20400),(20400,20900),(21200,21300),(21300,21600),(21600,22000),(22300,22900),(23100,23600),(23600,24000),(24000,24500),(24900,25300),(25300,25800)]
OS={10:1.0,12:1.0,35:1.6}   # kelime indeksi -> eklenecek tıslama (s)
w=wave.open('raw.wav'); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)
def hiss_region(a,b):
    n=int(sr*.01); fr=np.fft.rfftfreq(n,1/sr); best=[]
    for i in range(int(a*sr/1000),int(b*sr/1000)-n,n):
        f=np.abs(np.fft.rfft(x[i:i+n])); best.append((i, f[fr>3500].sum()/(f[fr<=3500].sum()+1)))
    hs=[i for i,r in best if r>4]
    return (hs[0], hs[-1]+n) if hs else None
out=[]; pos=0; shift=0; W=[]; rr=np.random.RandomState(3)
for k,(a,b) in enumerate(W0):
    if k in OS:
        hr=hiss_region(a,b); print(k, a, b, hr and (hr[0]/sr, hr[1]/sr))
        h0,h1=hr; mid=(h0+h1)//2
        out.append(x[pos:mid]); pos=mid
        L=int(OS[k]*sr); g=int(.04*sr); hop=g//2; win=np.hanning(g).astype(np.float32); buf=np.zeros(L+g,np.float32)
        seg=x[h0+int(.01*sr):h1-int(.01*sr)]
        for s in range(0,L,hop):
            o=rr.randint(0,max(1,len(seg)-g)); buf[s:s+g]+=seg[o:o+g]*win
        buf=buf[:L]*1.0; fade=int(.015*sr); buf[:fade]*=np.linspace(0,1,fade); buf[-fade:]*=np.linspace(1,0,fade)
        # tıslamanın içine yumuşak geçiş: orijinal mid noktası etrafında
        out.append(buf); W.append((a+shift, b+shift+int(OS[k]*1000))); shift+=int(OS[k]*1000)
    else: W.append((a+shift,b+shift))
out.append(x[pos:]); y=np.concatenate(out); y=np.clip(y,-32768,32767).astype(np.int16)
o=wave.open('anlatim.wav','wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
open('words.py','w').write('W='+repr(W)+'\n'); print(len(y)/sr, len(W))
