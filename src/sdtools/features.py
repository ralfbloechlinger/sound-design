"""One feature extractor shared by analyze.py and compare.py.

Every number here maps to a synth decision; see docs/serum2.md section 5.
"""
import warnings

import librosa
import numpy as np
import pyloudnorm as pyln
from scipy import signal

from .audio import band, db, mid_side, rms_db
from .notes import hz_to_note

BANDS = {
    "sub": (20, 120),
    "low_mid": (120, 500),
    "mid": (500, 2000),
    "high_mid": (2000, 6000),
    "air": (6000, 18000),
}
HOP_S = 0.01  # 10 ms analysis hop


def trim_silence(x, sr, thresh_db=-50):
    """Cut leading silence so attacks line up when comparing."""
    env = db(np.abs(x).max(axis=1))
    above = np.where(env > db(np.abs(x).max()) + thresh_db)[0]
    return x[above[0]:] if len(above) else x


def loudness(x, sr):
    if len(x) < 0.5 * sr:
        return float("nan")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return float(pyln.Meter(sr).integrated_loudness(x))


def avg_spectrum(mono, sr, n=8192, frac=6):
    """Long-term average spectrum, smoothed to 1/frac octave, in dB. Returns (freqs, dB)."""
    f, p = signal.welch(mono, sr, nperseg=min(n, len(mono)))
    centers = 20 * 2 ** (np.arange(0, np.log2(18000 / 20) * frac) / frac)
    out = []
    for c in centers:
        lo, hi = c * 2 ** (-0.5 / frac), c * 2 ** (0.5 / frac)
        sel = (f >= lo) & (f < hi)
        out.append(10 * np.log10(p[sel].mean() + 1e-20) if sel.any() else np.nan)
    return centers, np.array(out)


def envelope(mono, sr):
    """RMS envelope in dB with a 10 ms hop. Returns (times, dB)."""
    hop = int(sr * HOP_S)
    r = librosa.feature.rms(y=mono, frame_length=hop * 4, hop_length=hop)[0]
    return np.arange(len(r)) * HOP_S, db(r)


def attack_release(t, env_db):
    """Attack = time from 10% to 90% of peak amplitude. Decay = peak until 20 dB below peak."""
    lin = 10 ** (env_db / 20)
    pk = int(np.argmax(lin))
    a10 = np.argmax(lin >= 0.1 * lin[pk])
    a90 = np.argmax(lin >= 0.9 * lin[pk])
    after = np.where(env_db[pk:] < env_db[pk] - 20)[0]
    return {
        "attack_ms": float((t[a90] - t[a10]) * 1000),
        "peak_at_s": float(t[pk]),
        "decay_20db_ms": float(after[0] * HOP_S * 1000) if len(after) else None,
    }


def brightness(mono, sr):
    """Spectral centroid over time: the 'filter cutoff' your ear hears."""
    hop = int(sr * HOP_S)
    c = librosa.feature.spectral_centroid(y=mono, sr=sr, n_fft=2048, hop_length=hop)[0]
    rms = librosa.feature.rms(y=mono, frame_length=2048, hop_length=hop)[0]
    c[db(rms) < db(rms.max()) - 40] = np.nan  # ignore near-silence
    return np.arange(len(c)) * HOP_S, c


def pitch(mono, sr, fmin=25, fmax=1600):
    """pyin f0 track. Returns (times, f0 Hz with NaN when unvoiced, voiced probability)."""
    target = 8000 if fmax < 2000 else 16000
    y = librosa.resample(mono, orig_sr=sr, target_sr=target)
    hop = int(target * HOP_S)
    f0, voiced, prob = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=target,
                                    frame_length=4096 if fmin < 50 else 2048, hop_length=hop)
    return np.arange(len(f0)) * HOP_S, f0, prob


def harmonics(mono, sr, f0, at_s, n=10, win_s=0.25):
    """Level of harmonics 1..n relative to the strongest, at time at_s."""
    a = max(0, int((at_s - win_s / 2) * sr))
    seg = mono[a:a + int(win_s * sr)]
    if len(seg) < 256 or not f0 or np.isnan(f0):
        return None
    nfft = 1 << int(np.ceil(np.log2(sr * 2)))
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n=nfft))
    f = np.fft.rfftfreq(nfft, 1 / sr)
    lv = []
    for k in range(1, n + 1):
        sel = (f > k * f0 * 0.97) & (f < k * f0 * 1.03)
        lv.append(float(spec[sel].max()) if sel.any() else 0.0)
    lv = np.array(lv)
    rel = db(lv / max(lv.max(), 1e-12))
    odd, even = np.sum(lv[0::2][1:] ** 2), np.sum(lv[1::2] ** 2)  # odd excludes fundamental
    return {
        "f0_hz": float(f0),
        "at_s": float(at_s),
        "levels_db": [round(float(v), 1) for v in rel],
        "even_minus_odd_db": round(float(10 * np.log10((even + 1e-20) / (odd + 1e-20))), 1),
    }


def extract(x, sr, fmin=25, fmax=1600):
    """All features for a (samples, channels) float array. Returns (summary dict, curves dict)."""
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    mono = x.mean(axis=1)
    s = {
        "duration_s": round(len(x) / sr, 3),
        "peak_db": round(float(db(np.abs(x).max())), 2),
        "rms_db": round(rms_db(x), 2),
        "lufs": round(loudness(x, sr), 2),
    }
    s["crest_db"] = round(s["peak_db"] - s["rms_db"], 2)

    s["bands"] = {}
    for name, (lo, hi) in BANDS.items():
        if hi >= sr / 2:
            continue
        y = band(x, sr, lo, hi)
        mid, side = mid_side(y)
        s["bands"][name] = {
            "range_hz": [lo, hi],
            "level_db": round(rms_db(y), 1),
            "lr_corr": round(float(np.corrcoef(y.T)[0, 1]), 2),
            "side_minus_mid_db": round(rms_db(side) - rms_db(mid), 1),
        }

    t_env, env = envelope(mono, sr)
    s["envelope"] = attack_release(t_env, env)

    t_c, cen = brightness(mono, sr)
    s["brightness_hz"] = {
        "median": round(float(np.nanmedian(cen)), 0),
        "p10": round(float(np.nanpercentile(cen, 10)), 0),
        "p90": round(float(np.nanpercentile(cen, 90)), 0),
    }

    t_f, f0, prob = pitch(mono, sr, fmin, fmax)
    voiced = ~np.isnan(f0)
    s["pitch"] = {"voiced_fraction": round(float(voiced.mean()), 2)}
    if voiced.any():
        med = float(np.nanmedian(f0))
        s["pitch"].update({
            "median_hz": round(med, 2),
            "median_note": hz_to_note(med),
            "range_notes": [hz_to_note(float(np.nanpercentile(f0, 5))),
                            hz_to_note(float(np.nanpercentile(f0, 95)))],
        })
        # Harmonics at the most confidently pitched loud frame
        loud = np.interp(t_f, t_env, env)
        score = np.where(voiced, prob, 0) * (loud > loud.max() - 12)
        k = int(np.argmax(score))
        s["harmonics"] = harmonics(mono, sr, f0[k], t_f[k])

    f_sp, sp = avg_spectrum(mono, sr)
    curves = {"env": (t_env, env), "centroid": (t_c, cen), "f0": (t_f, f0), "spectrum": (f_sp, sp)}
    return s, curves
