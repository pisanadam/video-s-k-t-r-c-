"""Synthesizes the soundtrack: chiptune intro, vine-boom jumpscares, phonk sigma beat, TNT, outro."""
import numpy as np, wave, sys
SR = 44100; DUR = 25.0
out = np.zeros(int(SR * DUR))
rs = np.random.RandomState(7)

def add(sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(out), i + len(sig)); out[i:j] += sig[:j - i] * gain
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=0.1):
    t = tt(d); e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (d - t) / r)); return e
def square(f, d): return np.sign(np.sin(2 * np.pi * f * tt(d))) * env(d, 0.003, 0.03)
def note(n): return 440 * 2 ** ((n - 69) / 12)

# 0-7.6s: happy chiptune
mel = [72, 76, 79, 84, 79, 76, 74, 77, 81, 86, 81, 77, 71, 74, 79, 83, 79, 74, 72, 76, 79, 84, 88, 84]
step = 0.16
for i in range(int(7.5 / step)):
    add(square(note(mel[i % len(mel)]), step * 0.9), i * step, 0.10)
    if i % 2 == 0: add(square(note(mel[(i // 4 * 4) % len(mel)] - 24), step * 1.8) , i * step, 0.08)
# question "dun dun" sting at 5.9
for k, n in enumerate([60, 59, 58]): add(square(note(n), 0.25), 5.9 + k * 0.28, 0.12)
# crickets 7.6-8.2
c = tt(0.6); add(np.sin(2*np.pi*4200*c) * (np.sin(2*np.pi*30*c) > 0.6) * 0.05, 7.6)

def boom(d=1.4):
    t = tt(d); f = 55 * np.exp(-t * 1.2) + 30
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.2 * rs.randn(len(t)) * np.exp(-t * 30)
    return np.tanh(3 * s * np.exp(-t * 2.2))
# 8.2-12.4: jumpscare booms + drone
for i in range(4): add(boom(), 8.2 + i * 0.9, 0.8)
d = tt(3.6); add(np.tanh(2*np.sin(2*np.pi*46*d) + np.sin(2*np.pi*69.5*d)) * 0.15 * np.minimum(1, d), 8.2)
add(rs.randn(int(0.6 * SR)) * np.linspace(0.3, 0, int(0.6 * SR)), 11.8, 0.3)  # whoosh for head spin

# 12.4-18.6 & 20.2-25: phonk
bpm = 130; b = 60 / bpm
def kick():
    t = tt(0.35); f = 160 * np.exp(-t * 25) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def b808(n, d):
    t = tt(d); f = note(n) * (1 + 0.5 * np.exp(-t * 40))
    return np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(d, 0.004, 0.08)
def cowbell(n, d=0.22):
    t = tt(d); f = note(n)
    s = np.sign(np.sin(2*np.pi*f*t)) + np.sign(np.sin(2*np.pi*f*1.48*t))
    return s * np.exp(-t * 14) * 0.5
def hat():
    t = tt(0.05); return rs.randn(len(t)) * np.exp(-t * 90)
cow = [79, 79, 82, 79, 77, 77, 74, 77, 79, 79, 82, 84, 82, 79, 77, 74]
bass = [43, 43, 46, 41]
def phonk(t0, t1, gain=1.0):
    n16 = int((t1 - t0) / (b / 4))
    for i in range(n16):
        t = t0 + i * b / 4
        if i % 8 in (0, 3) or i % 16 == 10: add(kick(), t, 0.7 * gain)
        if i % 8 == 4: add(rs.randn(int(0.12*SR)) * np.exp(-tt(0.12)*30), t, 0.25 * gain)
        add(hat(), t, 0.08 * gain)
        if i % 2 == 0: add(cowbell(cow[(i // 2) % 16]), t, 0.12 * gain)
        if i % 16 == 0: add(b808(bass[(i // 16) % 4], b * 4 * 0.95), t, 0.32 * gain)
phonk(12.4, 18.6)
# 18.6-20.2: fuse hiss, then explosion
h = tt(1.6); add(rs.randn(len(h)) * (0.5 + 0.5 * np.sin(2*np.pi*8*h)) * 0.08, 18.6)
e = tt(2.0); add(np.tanh(4 * rs.randn(len(e)) * np.exp(-e * 2.5)) * 0.6 + boom(2.0) * 0.6, 20.2)
phonk(21.6, 25.0, 0.9)
# vine boom for the moai at 17.6
add(boom(), 17.6, 0.6)

out = out / np.max(np.abs(out)) * 0.9
fade = int(0.6 * SR); out[-fade:] *= np.linspace(1, 0, fade)
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
