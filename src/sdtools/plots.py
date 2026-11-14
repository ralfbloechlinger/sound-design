import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
from scipy import signal

TICKS = [30, 50, 100, 200, 400, 800, 1500, 3000, 6000, 12000]


def spectrogram(mono, sr, n=4096, fmin=30, fmax=16000, vmin=-85, vmax=-20, ax=None, title=None):
    """Log-frequency spectrogram.

    Bigger n  -> sharper frequency (good for bass notes), blurrier timing.
    Smaller n -> sharper timing (good for transients), blurrier frequency.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(14, 5), layout="constrained")
    f, t, z = signal.stft(mono, sr, nperseg=n, noverlap=n * 7 // 8)
    ax.pcolormesh(t, f, 20 * np.log10(np.maximum(np.abs(z), 1e-7)),
                  vmin=vmin, vmax=vmax, shading="auto", cmap="magma")
    ax.set(ylim=(fmin, fmax), yscale="log", xlabel="Seconds", ylabel="Hz", title=title)
    ax.set_yticks([v for v in TICKS if fmin <= v <= fmax])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    return ax
