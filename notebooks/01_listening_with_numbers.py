# %% [markdown]
# # 01 — Listening with numbers
#
# Goal: learn the five measurements you'll use on every song.
# Each section is **listen → measure → interpret → what it means for your synth patch**.
#
# 1. Level & loudness
# 2. Spectrogram (and the time/frequency trade-off)
# 3. Frequency bands & stereo width (mid/side)
# 4. Pitch of the bass (→ note names)
# 5. Harmonics (→ oscillator shape / saturation)
#
# **Which audio?** Set `FILE` below to a float WAV of yours. If you leave it as `None`, the notebook uses the first `songs/*/audio/*_float.wav` it finds, or a built-in **demo sound** (a saturated saw bass on D♯1 with a filter envelope, plus a wide pluck) so it works on a fresh clone.
# To get your own song: `pixi run new-song my-song` then `pixi run fetch <url> my-song 0 30`.
#
# **How to run:** this is a plain Python file with `# %%` cells.
# - VS Code / Cursor / PyCharm: click "Run Cell" above each `# %%` (select the pixi env `.pixi/envs/default` as interpreter).
# - JupyterLab: `pixi run lab`, then right-click the file → *Open With → Notebook* (via jupytext).
# - Whole script: `pixi run python notebooks/01_listening_with_numbers.py` (plots pop up; audio players won't).
#
# > Tip: always **listen first** and write down what you hear, then check it against the plots. The plots train your ears, not the other way round.

# %%
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import librosa
import pyloudnorm as pyln
from IPython.display import Audio, display

import sdtools as sd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else (
    Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd())
FILE = None                    # e.g. ROOT / "songs/my-song/audio/source_float.wav"
START, END = None, 20          # seconds; keep it short while learning

if FILE is None:
    FILE = next(iter(sorted(ROOT.glob("songs/*/audio/*_float.wav"))), None)
if FILE is not None:
    x, sr = sd.load(FILE, START, END)   # shape (samples, 2), float
    print("using", FILE.relative_to(ROOT))
else:
    from sdtools.demo import demo_sound
    sr = 48000; x = demo_sound(sr)
    print("no song audio found → using the built-in demo sound")
mono = x.mean(axis=1)
print(f"{len(x)/sr:.1f} s, {sr} Hz, {x.shape[1]} channels")
display(Audio(x.T * 0.5, rate=sr, normalize=False))

# %% [markdown]
# ## 1. Level & loudness
# - **Peak** = the single loudest sample. **RMS** = average energy. **LUFS** = loudness as ears perceive it (what streaming services normalise to).
# - Peak − RMS (crest factor) tells you how compressed/limited a mix is: modern electronic masters are often only 8–10 dB.

# %%
meter = pyln.Meter(sr)
print(f"peak      {sd.db(np.abs(x).max()):6.1f} dBFS")
print(f"RMS       {sd.rms_db(x):6.1f} dBFS")
print(f"loudness  {meter.integrated_loudness(x):6.1f} LUFS")

# Loudness over time: where does the track 'drop'?
hop = sr // 10
frames = [sd.rms_db(x[i:i+hop]) for i in range(0, len(x) - hop, hop)]
plt.figure(figsize=(14, 3)); plt.plot(np.arange(len(frames)) / 10, frames)
plt.xlabel("Seconds"); plt.ylabel("RMS dBFS (100 ms)"); plt.title("Level over time"); plt.show()

# %% [markdown]
# ## 2. Spectrogram: time vs. frequency
# A spectrogram is many short FFTs side by side. The window size `n` is a trade-off you must choose:
# - **large `n`** (8192): sharp horizontal lines → read bass notes and harmonics
# - **small `n`** (512): sharp vertical lines → see attacks, drums, rhythmic gating
#
# Compare the two plots below. Which one shows *when* things start better? Which one shows the bass *notes* better?

# %%
fig, ax = plt.subplots(2, 1, figsize=(14, 9), layout="constrained")
sd.spectrogram(mono, sr, n=8192, fmax=2000, ax=ax[0], title="n=8192: frequency detail")
sd.spectrogram(mono, sr, n=512, ax=ax[1], title="n=512: timing detail")
plt.show()

# %% [markdown]
# ## 3. Bands & stereo width
# Split into bands and ask of each: *how loud?* and *how wide?*
# - **L/R correlation** ≈ 1 → mono (centred). ≈ 0 → wide/decorrelated. < 0 → phasey, will cancel in mono.
# - Rule of thumb you'll see confirmed again and again: **sub is mono, width lives in the mids and highs.**
#
# Listen to each band — these are *listening aids*, not stems.

# %%
bands = {"sub": (25, 120), "bass body": (120, 500), "mids": (500, 6000), "air": (6000, 18000)}
for name, (lo, hi) in bands.items():
    y = sd.band(x, sr, lo, hi)
    mid, side = sd.mid_side(y)
    corr = np.corrcoef(y.T)[0, 1]
    print(f"{name:10s} {lo:>5}-{hi:<5} Hz  level {sd.rms_db(y):6.1f} dB   L/R corr {corr:5.2f}   side/mid {sd.rms_db(side)-sd.rms_db(mid):6.1f} dB")
    display(Audio(y.T, rate=sr))   # normalised for listening

# %% [markdown]
# ## 4. Bass pitch → notes
# `librosa.pyin` estimates the fundamental frequency frame by frame. We low-pass first so the mids don't confuse it.
# Unvoiced frames (no clear pitch) are NaN — that's honest, not a bug.
#
# Hum or play the notes it finds on a keyboard: do they match what you hear? (The demo sound is a D♯1 bass.)

# %%
low = sd.band(mono, sr, None, 250)
low_ds = librosa.resample(low, orig_sr=sr, target_sr=4000)   # bass doesn't need 48 kHz; faster
f0, voiced, prob = librosa.pyin(low_ds, fmin=25, fmax=120, sr=4000, frame_length=2048, hop_length=80)
t = librosa.times_like(f0, sr=4000, hop_length=80)

plt.figure(figsize=(14, 4)); plt.plot(t, f0, ".", ms=2)
for n in ["A#0", "C1", "D#1", "F1", "G1", "A1", "C2", "D#2"]:
    h = sd.note_to_hz(n); plt.axhline(h, c="gray", alpha=.3); plt.text(t[-1], h, n)
plt.xlabel("Seconds"); plt.ylabel("f0 (Hz)"); plt.title("Bass fundamental (pyin)"); plt.show()

for sec in range(int(t[-1]) + 1):
    sel = (t >= sec) & (t < sec + 1) & voiced
    if sel.any():
        print(f"{sec:2d}-{sec+1:2d}s  median {np.nanmedian(f0[sel]):5.1f} Hz  {sd.hz_to_note(np.nanmedian(f0[sel]))}")

# %% [markdown]
# ## 5. Harmonics → what to load in the oscillator
# Take one moment where the bass is held and look at its spectrum. Peaks at integer multiples of f0 are harmonics.
# - only odd harmonics (1, 3, 5…) → square/triangle-ish or symmetric saturation
# - odd + even, falling smoothly → saw, or asymmetric saturation
# - almost only the fundamental → sine
#
# `AT` and `F0` are picked automatically (the most confidently pitched moment from step 4); override them to inspect other moments.

# %%
k = int(np.nanargmax(np.where(voiced, prob, 0)))
AT, F0 = float(t[k]), float(f0[k])  # or set by hand, e.g. AT, F0 = 9.5, 39.0
print(f"inspecting {AT:.2f} s, f0 {F0:.1f} Hz = {sd.hz_to_note(F0)}")
seg = mono[int(AT * sr): int((AT + 0.5) * sr)] * np.hanning(sr // 2)
spec = np.abs(np.fft.rfft(seg, n=sr * 2)); f = np.fft.rfftfreq(sr * 2, 1 / sr)
spec_db = sd.db(spec / spec.max())

plt.figure(figsize=(14, 4)); plt.plot(f, spec_db); plt.xlim(20, 600); plt.ylim(-70, 2)
for k in range(1, 15):
    plt.axvline(k * F0, c="red", alpha=.25); plt.text(k * F0, 0, str(k), ha="center")
plt.xlabel("Hz"); plt.ylabel("dB"); plt.title(f"Spectrum at {AT}s, harmonics of {F0} Hz in red"); plt.show()

for k in range(1, 8):
    i = np.argmin(np.abs(f - k * F0))
    print(f"harmonic {k}  {k*F0:6.1f} Hz  {spec_db[i-3:i+4].max():6.1f} dB")

# %% [markdown]
# ## Your turn
# 1. Write 3 sentences: what's the sub doing, what's the mid range doing, how wide is each? Then check against the numbers above.
# 2. Build the bass in Serum 2 (start: sine on the note from step 4 + Distortion). Export it into `songs/<slug>/attempts/bass_v01.wav` and run `pixi run compare <reference> <attempt> --band 20 500` (or `/compare-attempt` in Claude Code).
# 3. Pick a new song with `pixi run new-song`, and do sections 1–5 on it *before* reading anyone else's analysis.
