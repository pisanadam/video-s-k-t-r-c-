# "Osuruk" kelimelerindeki s sesini (tıslama) granüler yöntemle uzatır, kelime zamanlarını kaydırır.
import wave, numpy as np, sys
import json
W0=[tuple(x) for x in json.load(open('words_raw.json'))]
OS={18:2.0}
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
