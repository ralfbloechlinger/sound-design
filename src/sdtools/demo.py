import numpy as np
from scipy import signal


def demo_sound(sr=48000, seconds=4.0, note_hz=38.89):
    """A small synthetic 'song' so lessons work without any downloaded audio.

    Mono saturated saw bass (D#1) with a filter envelope, plus a wide detuned
    pluck an octave+fifth up every half second. Returns (samples, 2) float.
    """
    t = np.arange(int(seconds * sr)) / sr

    # Bass: saw → lowpass whose cutoff falls after each 1 s note → soft clip. Mono.
    saw = 2 * ((t * note_hz) % 1) - 1
    note_t = t % 1.0
    cutoff = 150 + 1200 * np.exp(-note_t * 6)
    out = np.zeros_like(saw)
    for i in range(0, len(t), 512):  # block-wise time-varying filter
        sos = signal.butter(2, cutoff[i], fs=sr, output="sos")
        out[i:i + 512] = signal.sosfilt(sos, saw[i:i + 512])
    bass = np.tanh(2 * out) * np.minimum(note_t / 0.005, 1) * 0.5

    # Pluck: two detuned saws, one per channel → wide stereo.
    pl_t = t % 0.5
    env = np.exp(-pl_t * 12) * np.minimum(pl_t / 0.002, 1)
    f = note_hz * 6
    l = (2 * ((t * f * 1.015) % 1) - 1) * env * 0.3
    r = (2 * ((t * f * 0.985) % 1) - 1) * env * 0.3
    return np.c_[bass + l, bass + r]
