from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal


def load(path, start=None, end=None):
    """Load audio as float64, shape (samples, channels). start/end in seconds."""
    info = sf.info(str(path))
    sr = info.samplerate
    a = int(start * sr) if start else 0
    b = int(end * sr) if end else None
    x, sr = sf.read(str(path), start=a, stop=b, dtype="float64", always_2d=True)
    return x, sr


def save(path, x, sr, normalize=None, subtype="PCM_24"):
    """Write audio. normalize=0.85 peak-normalizes (for listening aids only!)."""
    x = np.asarray(x, dtype=float)
    if normalize:
        x = x / max(np.abs(x).max(), 1e-12) * normalize
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), x, sr, subtype=subtype)


def band(x, sr, lo, hi, order=6):
    """Zero-phase Butterworth band-pass. Use lo=None for low-pass, hi=None for high-pass.

    Zero-phase (filtfilt) keeps timing aligned but smears transients a little.
    """
    if lo and hi:
        sos = signal.butter(order, [lo, hi], btype="bandpass", fs=sr, output="sos")
    elif hi:
        sos = signal.butter(order, hi, btype="lowpass", fs=sr, output="sos")
    else:
        sos = signal.butter(order, lo, btype="highpass", fs=sr, output="sos")
    return signal.sosfiltfilt(sos, x, axis=0)


def mid_side(x):
    """Split stereo into mid (what's in mono) and side (what's only in stereo)."""
    return (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2


def db(v):
    return 20 * np.log10(np.maximum(np.abs(v), 1e-12))


def rms_db(x):
    """RMS level in dBFS."""
    return float(db(np.sqrt(np.mean(np.square(x)))))
