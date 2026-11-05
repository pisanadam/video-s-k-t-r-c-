"""Soundtrack for futbol.html: party chiptune, slow-mo drone, rubber squeaks, balloon pops,
crowd roar, sad violin, funeral beat, referee whistle, one last pop + sad trombone."""
import numpy as np, wave, sys
SR = 44100; DUR = 29.5
out = np.zeros(int(SR * DUR)); rs = np.random.RandomState(21)
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
def lowpass(x, n): return np.convolve(x, np.ones(n) / n, 'same')
def pop(big=False):
    d = 0.5 if big else 0.25; t = tt(d)
    crack = rs.randn(len(t)) * np.exp(-t * (25 if big else 45))
    thump = np.sin(2 * np.pi * (180 * np.exp(-t * 20) + 60) * t) * np.exp(-t * 18)
    return np.tanh(2.5 * (crack + thump))
def squeak(d):
    t = tt(d); f = 900 + 500 * np.sin(2 * np.pi * 7 * t) + 300 * np.sin(2 * np.pi * 2.3 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(3 * np.sin(ph)) * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * t)) * env(d, 0.02, 0.05)
def crowd(d, swell=1.0):
    t = tt(d); n = lowpass(rs.randn(len(t)), 8) - lowpass(rs.randn(len(t)), 80)
    return n * (0.5 + 0.5 * swell * np.minimum(1, t / 0.3)) * env(d, 0.05, 0.4)
def violin(n, d):
    t = tt(d); f = note(n) * (1 + 0.008 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t * 3))
    ph = 2 * np.pi * np.cumsum(f) / SR; saw = sum(np.sin(k * ph) / k for k in range(1, 8))
    return saw * env(d, 0.12, 0.15)
def trombone(n, d, bend=0.0):
    t = tt(d); f = note(n) * (1 + bend * t / d) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2 * (np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph))) * env(d, 0.03, 0.12)

# 0–7.6 party chiptune (original tune) + light crowd
party = [72, 76, 79, 76, 77, 81, 84, 81, 79, 83, 86, 83, 84, 79, 76, 72]
st = 0.15
for i in range(int(7.5 / st)):
    add(square(note(party[i % 16]), st * 0.85, 0.25), i * st, 0.09)
    if i % 2 == 0: add(square(note(party[(i // 4 * 4) % 16] - 24), st * 1.7), i * st, 0.07)
    if i % 4 == 0: add(np.sin(2 * np.pi * 60 * tt(0.15)) * np.exp(-tt(0.15) * 25), i * st, 0.4)
add(crowd(7.6, 0.3), 0, 0.12)
# "BEN HALLEDERİM" — cool riser
r = tt(1.6); add(np.sin(2 * np.pi * np.cumsum(200 + 600 * r / 1.6) / SR) * r / 1.6, 6.0, 0.12)

# 7.6–10.8 slow motion: low drone, heartbeat, rubber squeaks, pops
d = tt(3.2); add(np.tanh(np.sin(2 * np.pi * 41 * d) + 0.5 * np.sin(2 * np.pi * 61.5 * d)) * np.minimum(1, d * 2), 7.6, 0.18)
for hb in np.arange(7.7, 10.8, 0.75):
    for k, dt in enumerate([0, 0.18]): add(np.sin(2 * np.pi * 50 * tt(0.15)) * np.exp(-tt(0.15) * 22), hb + dt, 0.5 - k * 0.15)
add(squeak(1.6), 8.4, 0.14); add(squeak(0.9), 9.3, 0.1)
POP = [9.25, 9.65, 9.98, 10.25, 10.5]
for i, p in enumerate(POP): add(pop(i == 4), p, 0.9 if i == 4 else 0.7)
add(boom(), 10.5, 0.6)
# 10.8–13 the goal: crowd roar
add(crowd(1.3, 0.3), 10.8, 0.1); add(np.sin(2 * np.pi * 120 * tt(0.3)) * np.exp(-tt(0.3) * 10), 12.1, 0.5)  # kick
add(crowd(1.0, 1.0), 12.4, 0.45)

# 13–19.5 sad violin (A minor, slow)
sad = [(69, 1.0), (67, 0.5), (65, 1.0), (64, 1.0), (62, 0.5), (64, 1.2), (60, 1.3)]
tcur = 13.0
for n, du in sad:
    add(violin(n, du * 0.98), tcur, 0.12); add(violin(n - 12, du * 0.98), tcur, 0.06); tcur += du
rain = tt(6.5); add(lowpass(rs.randn(len(rain)), 3) * env(6.5, 0.5, 0.5), 13.0, 0.05)

# 19.5–23.5 funeral march beat (original melody, minor)
bpm = 120; b = 60 / bpm
fun = [57, 57, 64, 64, 62, 62, 60, 60, 59, 59, 60, 62, 64, 64, 64, 64]
for i in range(int(4.0 / (b / 2))):
    t0 = 19.5 + i * b / 2
    if i % 2 == 0: add(np.sin(2 * np.pi * (150 * np.exp(-tt(0.3) * 25) + 45) * tt(0.3)) * np.exp(-tt(0.3) * 8), t0, 0.6)
    if i % 4 == 2: add(rs.randn(int(0.1 * SR)) * np.exp(-tt(0.1) * 35), t0, 0.25)
    add(square(note(fun[i % 16]), b / 2 * 0.9, 0.25), t0, 0.08)
    add(square(note(fun[i % 16] - 24), b / 2 * 0.9, 0.5), t0, 0.06)

# 23.5–26 referee whistle + red card stinger
w = tt(0.55); add(np.sin(2 * np.pi * (2800 + 120 * np.sign(np.sin(2 * np.pi * 28 * w))) * w) * env(0.55, 0.01, 0.05), 23.55, 0.25)
add(boom(), 24.1, 0.8)

# 26–29.5 magic chime as the balloon returns, then the final pop + sad trombone
for k, n in enumerate([84, 88, 91, 96, 91, 96, 100]):
    c = tt(0.5); add(np.sin(2 * np.pi * note(n) * c) * np.exp(-c * 6), 26.1 + k * 0.25, 0.15)
add(pop(True), 28.1, 1.0)
for k, n in enumerate([55, 54, 53]): add(trombone(n, 0.24), 28.35 + k * 0.26, 0.25)
add(trombone(52, 0.55, -0.04), 29.0, 0.25)

out = out / np.max(np.abs(out)) * 0.9
f = int(0.25 * SR); out[-f:] *= np.linspace(1, 0, f)
with wave.open(sys.argv[1], 'wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes())
