"""Soundtrack for sinif.html: sneaky chiptune, record scratch, jumpscare booms, 'bohohoho' laugh, phonk, yeets."""
import numpy as np, wave, sys
SR = 44100; DUR = 26.0
out = np.zeros(int(SR * DUR)); rs = np.random.RandomState(3)
def add(sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(out), i + len(sig)); out[i:j] += sig[:j - i] * gain
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=0.1):
    t = tt(d); return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (d - t) / r))
def note(n): return 440 * 2 ** ((n - 69) / 12)
def square(f, d, duty=0.5): t = tt(d); return np.where((t * f) % 1 < duty, 1.0, -1.0) * env(d, 0.003, 0.03)
def boom(d=1.4):
    t = tt(d); f = 55 * np.exp(-t * 1.2) + 30; ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(3 * (np.sin(ph) + 0.5 * np.sin(2 * ph)) * np.exp(-t * 2.2))

# A: chalk taps + calm classroom melody (0-3.6)
for i in range(14): add(rs.randn(int(0.03 * SR)) * np.exp(-tt(0.03) * 120), 0.1 + i * 0.25 + (i % 3) * 0.04, 0.25)
calm = [64, 67, 72, 71, 67, 64, 65, 69, 72, 71, 69, 65]
for i in range(int(3.6 / 0.3)): add(square(note(calm[i % 12]), 0.27, 0.25), i * 0.3, 0.07)
# B: sneaky staccato bassline (3.6-7.6)
sneak = [40, 0, 42, 0, 43, 0, 44, 45, 0, 40, 0, 46, 45, 0, 40, 0]
st = 60 / 120 / 2
for i in range(int(4.0 / st)):
    n = sneak[i % 16]
    if n: add(square(note(n + 12), st * 0.5, 0.3), 3.6 + i * st, 0.16); add(square(note(n + 24), st * 0.3, 0.5), 3.6 + i * st, 0.04)
# C: record scratch at 7.6 + silence, boom when head turns
t = tt(0.35); add(rs.randn(len(t)) * np.sin(2 * np.pi * (40 - 90 * t) * t) * np.exp(-t * 4), 7.6, 0.5)
add(boom(), 8.35, 0.7)
# D: angry footsteps speeding up (8.5-10.3)
for k, ts in enumerate(np.arange(8.55, 10.25, 0.22)):
    tt_ = tt(0.12); add(np.sin(2 * np.pi * 70 * tt_) * np.exp(-tt_ * 30) + rs.randn(len(tt_)) * np.exp(-tt_ * 80) * 0.4, ts, 0.6)
d = tt(1.8); add(np.sin(2 * np.pi * (200 + 300 * d / 1.8) * d) * 0.12 * d / 1.8, 8.5)  # rising tension
# E: OĞLUM SEN NE YAPIYORSUN — distorted double boom, then censor beep
add(boom(1.2), 10.3, 1.0); add(np.tanh(6 * rs.randn(int(0.5 * SR)) * np.exp(-tt(0.5) * 6)), 10.3, 0.35)
add(np.sin(2 * np.pi * 1000 * tt(0.9)) * env(0.9, 0.01, 0.02), 11.4, 0.35)  # bleep
# F: alt-tab click + error ding, then "BO-HO-HO-HO-HYT" laugh (formant-ish 'o')
add(rs.randn(int(0.02 * SR)), 12.45, 0.4); add(rs.randn(int(0.02 * SR)), 12.6, 0.4)
for f, tdg in [(1046, 12.7), (784, 12.82)]: add(np.sin(2 * np.pi * f * tt(0.4)) * np.exp(-tt(0.4) * 8), tdg, 0.25)
def ho(f0, d=0.2):
    t = tt(d); saw = 2 * ((t * f0) % 1) - 1
    v = saw + 0.7 * np.sin(2 * np.pi * 450 * t) * saw + 0.4 * np.sin(2 * np.pi * 800 * t) * saw
    return np.tanh(1.5 * v) * env(d, 0.01, 0.07)
for i, f0 in enumerate([180, 170, 160, 150, 140, 210]):
    add(ho(f0 * (1 + 0.05 * np.sin(i)), 0.2 if i < 5 else 0.35), 13.85 + i * 0.22, 0.35)
add(boom(), 13.8, 0.5)
# G + I: phonk
bpm = 130; b = 60 / bpm
def kick():
    t = tt(0.35); f = 160 * np.exp(-t * 25) + 45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def b808(n, d):
    t = tt(d); f = note(n) * (1 + 0.5 * np.exp(-t * 40)); return np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(d, 0.004, 0.08)
def cowbell(n, d=0.22):
    t = tt(d); f = note(n); return (np.sign(np.sin(2*np.pi*f*t)) + np.sign(np.sin(2*np.pi*f*1.48*t))) * np.exp(-t * 14) * 0.5
cow = [80, 80, 83, 80, 78, 78, 75, 78, 80, 80, 83, 85, 83, 80, 78, 75]; bass = [44, 44, 47, 42]
def phonk(t0, t1, g=1.0):
    for i in range(int((t1 - t0) / (b / 4))):
        t = t0 + i * b / 4
        if i % 8 in (0, 3) or i % 16 == 10: add(kick(), t, 0.7 * g)
        if i % 8 == 4: add(rs.randn(int(0.12 * SR)) * np.exp(-tt(0.12) * 30), t, 0.25 * g)
        add(rs.randn(int(0.05 * SR)) * np.exp(-tt(0.05) * 90), t, 0.08 * g)
        if i % 2 == 0: add(cowbell(cow[(i // 2) % 16]), t, 0.12 * g)
        if i % 16 == 0: add(b808(bass[(i // 16) % 4], b * 3.8), t, 0.32 * g)
phonk(15.4, 20.4); add(boom(), 18.0, 0.6)
# H: MÜDÜR ODASINA — yeet whooshes + boings
add(boom(), 20.4, 0.6)
for i in range(3):
    ts = 20.9 + i * 0.6; w = tt(0.5)
    add(rs.randn(len(w)) * np.sin(np.pi * w / 0.5) * 0.5, ts, 0.5)
    add(np.sin(2 * np.pi * np.cumsum(300 + 500 * np.sin(2 * np.pi * 6 * w) * np.exp(-w * 3)) / SR) * np.exp(-w * 4), ts + 0.3, 0.3)
phonk(23.4, 26.0, 0.85)

out = out / np.max(np.abs(out)) * 0.9
f = int(0.6 * SR); out[-f:] *= np.linspace(1, 0, f)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
