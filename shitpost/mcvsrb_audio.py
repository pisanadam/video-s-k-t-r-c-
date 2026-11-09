"""Soundtrack for mcvsrb.html: epic VS intro, ding/buzzer list reveals, crash glitch,
notification pop + rage boom, tweet whooshes, like counter, phonk, crown fanfare,
a (tasteful) cartoon fart, sword shing, fall-apart clatter, outro jingle."""
import numpy as np, wave, sys
SR = 44100; DUR = 34.0
out = np.zeros(int(SR * DUR)); rs = np.random.RandomState(4)
def add(sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(out), i + len(sig)); out[i:j] += sig[:j - i] * gain
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=0.1):
    t = tt(d); return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (d - t) / r))
def note(n): return 440 * 2 ** ((n - 69) / 12)
def square(f, d, duty=0.5): t = tt(d); return np.where((t * f) % 1 < duty, 1.0, -1.0) * env(d, 0.003, 0.03)
def saw(f, d): t = tt(d); return (2 * ((t * f) % 1) - 1) * env(d, 0.01, 0.08)
def boom(d=1.3):
    t = tt(d); f = 55 * np.exp(-t * 1.2) + 30; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(3 * (np.sin(ph) + 0.5 * np.sin(2 * ph)) * np.exp(-t * 2.2))
def lp(x, n): return np.convolve(x, np.ones(n) / n, 'same')
def ding(t0): c = tt(0.5); add((np.sin(2 * np.pi * 1318 * c) + 0.5 * np.sin(2 * np.pi * 1976 * c)) * np.exp(-c * 7), t0, 0.22)
def buzz(t0): add(np.tanh(3 * saw(110, 0.35) + 2 * saw(116.5, 0.35)), t0, 0.12)
def whoosh(t0, d=0.4): w = tt(d); add(lp(rs.randn(len(w)), 6) * np.sin(np.pi * w / d), t0, 0.5)
def hit(t0, n=38): add(np.tanh(2 * (saw(note(n), 0.9) + saw(note(n + 7), 0.9) + saw(note(n + 12), 0.9))) , t0, 0.15); add(boom(1.0), t0, 0.5)

# 0–3.6: epic VS intro — brass-ish stabs + riser
for k, (tt0, n) in enumerate([(0.0, 38), (0.9, 41), (1.8, 43), (2.7, 45)]): hit(tt0, n)
r = tt(1.0); add(lp(rs.randn(len(r)), 3) * r * 0.6, 2.6, 0.4)
# 3.6–10: driving beat under the lists
bpm = 128; b = 60 / bpm
for i in range(int(6.3 / (b / 2))):
    t0 = 3.6 + i * b / 2
    if i % 2 == 0: add(np.sin(2 * np.pi * (140 * np.exp(-tt(0.25) * 25) + 45) * tt(0.25)) * np.exp(-tt(0.25) * 9), t0, 0.5)
    add(rs.randn(int(0.03 * SR)) * np.exp(-tt(0.03) * 120), t0 + b / 4, 0.06)
    add(square(note([45, 45, 48, 50][(i // 4) % 4]), b / 2 * 0.8, 0.5), t0, 0.06)
for i in range(5): ding(3.8 + i * 1.0); buzz(4.3 + i * 1.0)
# crash glitch on "Sürekli Çöküyor!"
g = tt(0.5); add(np.sign(np.sin(2 * np.pi * 70 * g)) * (rs.rand(len(g)) > 0.5) * 0.6, 8.6, 0.3)
add(np.sin(2 * np.pi * 880 * tt(0.15)) * env(0.15), 8.7, 0.15); add(np.sin(2 * np.pi * 660 * tt(0.2)) * env(0.2), 8.85, 0.15)  # error chime
hit(9.0, 45)

# 10–14.6: notification pop, then rage
c = tt(0.12); add(np.sin(2 * np.pi * 1200 * c) * np.exp(-c * 30), 10.0, 0.3); add(np.sin(2 * np.pi * 1600 * c) * np.exp(-c * 30), 10.08, 0.3)
add(boom(), 12.0, 1.0); add(np.tanh(6 * rs.randn(int(0.6 * SR)) * np.exp(-tt(0.6) * 5)), 12.0, 0.35)
d = tt(2.6); add(np.tanh(2 * np.sin(2 * np.pi * 46 * d) + np.sin(2 * np.pi * 69 * d)) * np.exp(-d * 0.6), 12.0, 0.2)

# 14.6–21.2: tweet whooshes, likes counting, then a phonk drop on BABADIR/KAKADIR
whoosh(14.6); whoosh(16.4)
for k in range(24): add(np.sin(2 * np.pi * (900 + k * 30) * tt(0.04)) * env(0.04), 17.0 + k * 0.1, 0.12)
def kick(): t = tt(0.35); f = 160 * np.exp(-t * 25) + 45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def b808(n, d): t = tt(d); f = note(n) * (1 + 0.5 * np.exp(-t * 40)); return np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(d, 0.004, 0.08)
def cowbell(n, d=0.22): t = tt(d); f = note(n); return (np.sign(np.sin(2*np.pi*f*t)) + np.sign(np.sin(2*np.pi*f*1.48*t))) * np.exp(-t * 14) * 0.5
cow = [79, 79, 82, 79, 77, 77, 74, 77, 79, 79, 82, 84, 82, 79, 77, 74]; bass = [43, 43, 46, 41]
def phonk(t0, t1, gg=1.0):
    for i in range(int((t1 - t0) / (b / 4))):
        t = t0 + i * b / 4
        if i % 8 in (0, 3) or i % 16 == 10: add(kick(), t, 0.7 * gg)
        if i % 8 == 4: add(rs.randn(int(0.12 * SR)) * np.exp(-tt(0.12) * 30), t, 0.25 * gg)
        add(rs.randn(int(0.05 * SR)) * np.exp(-tt(0.05) * 90), t, 0.07 * gg)
        if i % 2 == 0: add(cowbell(cow[(i // 2) % 16]), t, 0.12 * gg)
        if i % 16 == 0: add(b808(bass[(i // 16) % 4], b * 3.8), t, 0.3 * gg)
phonk(16.9, 21.2, 0.8); add(boom(), 19.6, 0.7)

# 21.2–26: crown fanfare, then the stinky side
for k, n in enumerate([72, 76, 79, 84]): add(square(note(n), 0.18 if k < 3 else 0.7, 0.3), 22.2 + k * 0.13, 0.14)
add(np.sin(2 * np.pi * 2600 * tt(0.6)) * np.exp(-tt(0.6) * 5), 22.2, 0.15)  # sparkle
f = tt(0.7); fart = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(90 + 25 * np.sin(2 * np.pi * 9 * f) - 30 * f) / SR) * (0.6 + 0.4 * (rs.rand(len(f)) > 0.3)))
add(fart * env(0.7, 0.02, 0.15), 22.6, 0.4)
fl = tt(3.3); add(np.sin(2 * np.pi * (220 + 30 * np.sin(2 * np.pi * 11 * fl)) * fl) * 0.5 * (1 + np.sin(2 * np.pi * 0.7 * fl)), 22.7, 0.05)  # flies buzzing
phonk(23.2, 26.0, 0.7)

# 26–31.4: sword shing, epic stabs, fall-apart clatter
s = tt(0.7); add((np.sin(2 * np.pi * 3200 * s) + np.sin(2 * np.pi * 4700 * s)) * np.exp(-s * 5) + lp(rs.randn(len(s)), 2) * np.exp(-s * 12), 26.7, 0.2)
for k, n in enumerate([38, 41, 45, 50]): hit(26.2 + k * 1.3, n)
for k in range(6): c = tt(0.12); add(rs.randn(len(c)) * np.exp(-c * 40) + np.sin(2 * np.pi * (300 + k * 60) * c) * np.exp(-c * 30), 27.65 + k * 0.09, 0.4)
o = tt(0.35); add(np.tanh(2 * np.sin(2 * np.pi * np.cumsum(420 - 300 * o / 0.35) / SR)) * env(0.35, 0.01, 0.1), 27.6, 0.18)  # sad 'ugh'
add(boom(), 28.0, 0.5)

# 31.4–34: outro jingle
for k, n in enumerate([72, 76, 79, 84, 79, 84, 88]): add(square(note(n), 0.2, 0.25), 31.5 + k * 0.2, 0.12)
add(square(note(84), 0.9, 0.25), 32.9, 0.12); add(boom(), 31.5, 0.4)

out = out / np.max(np.abs(out)) * 0.9
fade = int(0.4 * SR); out[-fade:] *= np.linspace(1, 0, fade)
with wave.open(sys.argv[1], 'wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes())
