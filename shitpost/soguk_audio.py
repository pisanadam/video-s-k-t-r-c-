"""Soundtrack for soguk.html: sad trombone, gibberish speech blips, ba-dum-tss, crickets, lonely laugh, phonk."""
import numpy as np, wave, sys
SR = 44100; DUR = 30.0
out = np.zeros(int(SR * DUR)); rs = np.random.RandomState(11)
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
def trombone(n, d, bend=0.0):
    t = tt(d); f = note(n) * (1 + bend * t / d) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2 * (np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph))) * env(d, 0.03, 0.12)
def sad_trombone(t0, g=0.3):
    for k, n in enumerate([55, 54, 53]): add(trombone(n, 0.45), t0 + k * 0.5, g)
    add(trombone(52, 1.3, -0.04), t0 + 1.5, g)
def blips(t0, d, base):
    """Gibberish 'talking' blips while a speech bubble is up."""
    for k in range(int(d / 0.09)):
        f = base * 2 ** (rs.randint(-3, 5) / 12)
        add(square(f, 0.06, 0.25), t0 + k * 0.09, 0.07)
def badum(t0):
    for k, f in enumerate([150, 110]):
        t = tt(0.25); add(np.sin(2 * np.pi * f * (1 + 0.6 * np.exp(-t * 30)) * t) * np.exp(-t * 12), t0 + k * 0.14, 0.5)
    t = tt(0.9); add(rs.randn(len(t)) * np.exp(-t * 4) * (1 + 0.3 * np.sin(2 * np.pi * 7000 * t)), t0 + 0.32, 0.25)
def crickets(t0, d):
    t = tt(d); chirp = (np.sin(2 * np.pi * 28 * t) > 0.55) * (np.sin(2 * np.pi * 0.9 * t) > -0.2)
    add(np.sin(2 * np.pi * 4300 * t) * chirp * 0.05 + rs.randn(len(t)) * 0.004, t0)
def wind(t0, d):
    t = tt(d); n = np.convolve(rs.randn(len(t)), np.ones(60) / 60, 'same')
    add(n * np.sin(np.pi * t / d) * 1.2, t0, 0.5)
def ho(f0, d=0.2):
    t = tt(d); saw = 2 * ((t * f0) % 1) - 1
    v = saw + 0.7 * np.sin(2 * np.pi * 450 * t) * saw + 0.4 * np.sin(2 * np.pi * 800 * t) * saw
    return np.tanh(1.5 * v) * env(d, 0.01, 0.07)

# 0–3 title: sad trombone over chalk taps

# ---------------------------------------------------------------------------
# "Haydi Döndür" — an original party song (darbuka groove, hicaz lead, synth vocal).
# It is rendered as one continuous track and then gated: it plays on the title,
# during each joke setup, and on the final yeet, and cuts dead at every punchline.
# ---------------------------------------------------------------------------
def resonate(x, f, bw):
    r = np.exp(-np.pi * bw / SR); c = 2 * r * np.cos(2 * np.pi * f / SR); y = np.zeros_like(x); y1 = y2 = 0.0
    g = 1 - r
    for i in range(len(x)):
        y0 = g * x[i] + c * y1 - r * r * y2; y[i] = y0; y2 = y1; y1 = y0
    return y
VOWELS = {'a': (800, 1250), 'i': (320, 2300), 'ö': (460, 1500), 'ü': (310, 1750), 'e': (530, 1850)}
def sing(vowel, n, d):
    t = tt(d); f = note(n) * (1 + 0.015 * np.sin(2 * np.pi * 5.8 * t) * np.minimum(1, t * 4))
    src = 2 * ((np.cumsum(f) / SR) % 1) - 1
    f1, f2 = VOWELS[vowel]
    v = resonate(src, f1, 90) * 1.0 + resonate(src, f2, 120) * 0.6
    return np.tanh(3 * v / (np.max(np.abs(v)) + 1e-9)) * env(d, 0.02, 0.06)
SONG = np.zeros(len(out)); BPM = 128; BT = 60 / BPM
def sadd(sig, t0, g=1.0):
    i = int(t0 * SR); j = min(len(SONG), i + len(sig)); SONG[i:j] += sig[:j - i] * g
dum = lambda: np.sin(2 * np.pi * (110 * np.exp(-tt(0.3) * 18) + 70) * tt(0.3)) * np.exp(-tt(0.3) * 9)
tek = lambda: (rs.randn(int(0.08 * SR)) * 0.6 + np.sin(2 * np.pi * 700 * tt(0.08))) * np.exp(-tt(0.08) * 45)
# hicaz on D: D Eb F# G A Bb C
hook = [62, 63, 66, 67, 69, 67, 66, 63, 62, 63, 66, 67, 69, 70, 69, 67]
bassline = [38, 38, 45, 38, 43, 43, 45, 42]
lyric = [('a', 74, 0.5), ('i', 74, 0.5), ('ö', 78, 1.0), ('ü', 76, 1.0), (None, 0, 1.0),     # hay-di dön-dür
         ('ö', 78, 0.5), ('ü', 76, 0.5), ('ö', 75, 0.5), ('ü', 74, 0.5), (None, 0, 2.0)]    # dön-dür dön-dür
n16 = int(DUR / (BT / 4))
for i in range(n16):
    t0 = i * BT / 4
    if i % 16 in (0, 6, 8): sadd(dum(), t0, 0.7)
    if i % 16 in (4, 10, 12, 14): sadd(tek(), t0, 0.3)
    if i % 2 == 1: sadd(rs.randn(int(0.03 * SR)) * np.exp(-tt(0.03) * 120), t0, 0.12)
    if i % 2 == 0: sadd(square(note(hook[(i // 2) % 16] + 12), BT / 2 * 0.8, 0.25), t0, 0.07)
    if i % 4 == 0: sadd(np.tanh(2 * np.sin(2 * np.pi * note(bassline[(i // 4) % 8]) * tt(BT * 0.9))) * env(BT * 0.9, 0.005, 0.05), t0, 0.16)
# vocal: the hook repeats every 2 bars, but only where the song is audible
WINDOWS = [(0, 3.0)] + [(3.0 + k * 4.8, 3.0 + k * 4.8 + 2.6) for k in range(4)] + [(27.6, DUR)]
tv = 0.0
while tv < DUR:
    for vw, n, beats in lyric:
        d = beats * BT
        if vw and any(a - 0.05 <= tv < b for a, b in WINDOWS): sadd(sing(vw, n, d * 0.92), tv, 0.22)
        tv += d
gate = np.zeros(len(SONG))
for a, b in WINDOWS:
    i, j = int(a * SR), min(len(SONG), int(b * SR)); gate[i:j] = 1
    fi = int(0.02 * SR); gate[i:i + fi] *= np.linspace(0, 1, fi)
out += SONG * gate
for i in range(10): add(rs.randn(int(0.03 * SR)) * np.exp(-tt(0.03) * 120), 0.1 + i * 0.28, 0.2)

J0, JLEN = 3.0, 4.8
voices = [520, 440, 380, 220]
for i in range(4):
    s = J0 + i * JLEN
    blips(s + 0.1, 1.1, voices[i]); blips(s + 1.4, 1.1, voices[i])
    badum(s + 2.6)
    crickets(s + 3.05, JLEN - 3.05); wind(s + 3.05, JLEN - 3.05)
    if i == 3:  # hoca laughs alone
        for k, f0 in enumerate([120, 115, 110, 105, 100, 95, 90]): add(ho(f0, 0.2), s + 3.15 + k * 0.23, 0.3)

# 22.2–26 sigma: phonk
bpm = 130; b = 60 / bpm
def kick():
    t = tt(0.35); f = 160 * np.exp(-t * 25) + 45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
def b808(n, d):
    t = tt(d); f = note(n) * (1 + 0.5 * np.exp(-t * 40)); return np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(d, 0.004, 0.08)
def cowbell(n, d=0.22):
    t = tt(d); f = note(n); return (np.sign(np.sin(2*np.pi*f*t)) + np.sign(np.sin(2*np.pi*f*1.48*t))) * np.exp(-t * 14) * 0.5
cow = [78, 78, 81, 78, 76, 76, 73, 76, 78, 78, 81, 83, 81, 78, 76, 73]; bass = [42, 42, 45, 40]
for i in range(int(3.8 / (b / 4))):
    t = 22.2 + i * b / 4
    if i % 8 in (0, 3) or i % 16 == 10: add(kick(), t, 0.7)
    if i % 8 == 4: add(rs.randn(int(0.12 * SR)) * np.exp(-tt(0.12) * 30), t, 0.25)
    add(rs.randn(int(0.05 * SR)) * np.exp(-tt(0.05) * 90), t, 0.08)
    if i % 2 == 0: add(cowbell(cow[(i // 2) % 16]), t, 0.12)
    if i % 16 == 0: add(b808(bass[(i // 16) % 4], b * 3.8), t, 0.32)
add(boom(), 23.5, 0.6)

# 26–30 the late laugh, then yeet + final sad trombone
crickets(26.0, 0.3)
for k, f0 in enumerate([260, 250, 270, 240, 260, 230, 250]): add(ho(f0, 0.18), 26.15 + k * 0.21, 0.32)
add(boom(), 27.6, 0.7)
w = tt(0.6); add(rs.randn(len(w)) * np.sin(np.pi * w / 0.6) * 0.5, 27.6, 0.5)
add(np.sin(2 * np.pi * np.cumsum(300 + 500 * np.sin(2 * np.pi * 6 * w) * np.exp(-w * 3)) / SR) * np.exp(-w * 4), 28.0, 0.3)

out = out / np.max(np.abs(out)) * 0.9
f = int(0.4 * SR); out[-f:] *= np.linspace(1, 0, f)
with wave.open(sys.argv[1], 'wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes())
