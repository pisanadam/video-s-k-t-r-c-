"""Soundtrack for trol.html: sneaky troll tune, falling whistles, mining clinks,
block pops, balloon pop, and a 'troll sting' (cheeky hehehe + boom) after every prank."""
import numpy as np, wave, sys
SR = 44100; DUR = 31.5
out = np.zeros(int(SR * DUR)); rs = np.random.RandomState(8)
def add(sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(out), i + len(sig)); out[i:j] += sig[:j - i] * gain
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=0.1):
    t = tt(d); return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (d - t) / r))
def note(n): return 440 * 2 ** ((n - 69) / 12)
def square(f, d, duty=0.5): t = tt(d); return np.where((t * f) % 1 < duty, 1.0, -1.0) * env(d, 0.003, 0.03)
def boom(d=1.2):
    t = tt(d); f = 55 * np.exp(-t * 1.2) + 30; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(3 * (np.sin(ph) + 0.5 * np.sin(2 * ph)) * np.exp(-t * 2.4))
def he(f0, d=0.13):
    t = tt(d); saw = 2 * ((t * f0) % 1) - 1
    v = saw + 0.8 * np.sin(2 * np.pi * 530 * t) * saw + 0.5 * np.sin(2 * np.pi * 1850 * t) * saw
    return np.tanh(1.6 * v) * env(d, 0.008, 0.05)
def sting(t0):
    """the troll-face moment: boom + cheeky 'he-he-he-he' climbing up"""
    add(boom(), t0, 0.8)
    add(np.tanh(5 * rs.randn(int(0.12 * SR)) * np.exp(-tt(0.12) * 25)), t0, 0.25)
    for k in range(6): add(he(240 + k * 22), t0 + 0.12 + k * 0.15, 0.32)
def fall(t0, d=0.6):
    t = tt(d); add(np.sin(2 * np.pi * np.cumsum(1800 * np.exp(-t * 2.2) + 200) / SR) * env(d, 0.01, 0.05), t0, 0.18)
def thud(t0): t = tt(0.3); add(np.sin(2 * np.pi * (90 * np.exp(-t * 10) + 40) * t) * np.exp(-t * 12) + rs.randn(len(t)) * np.exp(-t * 40) * 0.3, t0, 0.8)
def clink(t0): t = tt(0.25); add((np.sin(2 * np.pi * 2300 * t) + 0.6 * np.sin(2 * np.pi * 3700 * t)) * np.exp(-t * 18) + rs.randn(len(t)) * np.exp(-t * 60) * 0.5, t0, 0.3)
def crunch(t0): t = tt(0.4); add(np.convolve(rs.randn(len(t)), np.ones(20) / 20, 'same') * np.exp(-t * 8) * 4, t0, 0.5)
def blockpop(t0): t = tt(0.08); add(rs.randn(len(t)) * np.exp(-t * 60) + np.sin(2 * np.pi * 160 * t) * np.exp(-t * 40), t0, 0.35)
def pop(t0): t = tt(0.3); add(np.tanh(2.5 * (rs.randn(len(t)) * np.exp(-t * 30) + np.sin(2 * np.pi * (180 * np.exp(-t * 20) + 60) * t) * np.exp(-t * 18))), t0, 0.9)
def cry(t0, d=1.0):
    t = tt(d); f = 520 + 120 * np.sin(2 * np.pi * 3 * t) - 150 * t / d; add(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, 0.05, 0.2), t0, 0.1)

# sneaky troll tune (original): staccato bass + plucky lead, plays under everything except the stings
bpm = 112; b = 60 / bpm
bass = [45, 0, 52, 0, 45, 0, 51, 52, 45, 0, 52, 0, 50, 0, 49, 48]
lead = [69, 0, 72, 0, 76, 75, 0, 72, 69, 0, 72, 0, 74, 72, 71, 0]
STINGS = [7.8, 13.8, 19.6, 24.6, 30.2]
def in_sting(t): return any(s <= t < s + 1.2 for s in STINGS)
for i in range(int(DUR / (b / 2))):
    t0 = i * b / 2
    if in_sting(t0): continue
    if bass[i % 16]: add(square(note(bass[i % 16]), b / 2 * 0.45, 0.35), t0, 0.12)
    if lead[i % 16]: add(square(note(lead[i % 16] + 12), b / 2 * 0.3, 0.25), t0, 0.05)
    if i % 4 == 2: add(rs.randn(int(0.04 * SR)) * np.exp(-tt(0.04) * 90), t0, 0.08)

# TROL #1
fall(6.2, 0.45); thud(6.62); add(boom(), 6.62, 0.3)
# TROL #2
for k in range(4): clink(10.45 + k * 0.5)
crunch(12.0); cry(12.8, 1.0)
# TROL #3
for k in range(9): blockpop(16.6 + k * 1.4 / 9)
# TROL #4
pop(23.4); cry(23.8, 0.8)
# TROL #5
for k in range(8): add(he(300 + (k % 2) * 30), 26.1 + k * 0.18, 0.25)  # troll laughing at himself
fall(28.2, 0.5); thud(28.68); add(boom(), 28.68, 0.4)
add(np.tanh(4 * rs.randn(int(0.4 * SR)) * np.exp(-tt(0.4) * 6)), 28.2, 0.2)  # karma thunder crack
for s in STINGS: sting(s)

out = out / np.max(np.abs(out)) * 0.9
f = int(0.3 * SR); out[-f:] *= np.linspace(1, 0, f)
with wave.open(sys.argv[1], 'wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes())
