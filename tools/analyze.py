"""Standard analysis of one audio file (or a time range of it).

    pixi run analyze <audio> [--start S] [--end S] [--out DIR] [--fmin HZ] [--fmax HZ]

Writes <out>/analysis.png and <out>/analysis.json and prints a short summary.
Default out: <song>/figures/<file-stem>_<start>-<end>/ when the file lives in songs/<slug>/audio/,
otherwise next to the file.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import sdtools as sd
from sdtools.features import BANDS, extract


def default_out(path, start, end):
    tag = path.stem + (f"_{start:g}-{end:g}s" if start is not None or end is not None else "")
    song = path.parent.parent if path.parent.name in ("audio", "attempts", "renders") else path.parent
    return song / "figures" / tag


def plot(x, sr, s, c, title, out_png):
    mono = x.mean(axis=1)
    fig, ax = plt.subplots(3, 2, figsize=(18, 13), layout="constrained")
    fig.suptitle(title, fontsize=14)

    t, env = c["env"]
    ax[0, 0].plot(t, env); ax[0, 0].set(title="Level (RMS, 10 ms)", xlabel="s", ylabel="dBFS",
                                        ylim=(env.max() - 60, env.max() + 3))
    sd.spectrogram(mono, sr, n=2048, ax=ax[0, 1], title="Spectrogram (n=2048)")
    sd.spectrogram(mono, sr, n=8192, fmax=2000, ax=ax[1, 0], title="Low/mid detail (n=8192)")

    t, cen = c["centroid"]
    ax[1, 1].plot(t, cen); ax[1, 1].set(title="Brightness: spectral centroid (≈ perceived filter cutoff)",
                                        xlabel="s", ylabel="Hz", yscale="log")
    t, f0 = c["f0"]
    ax[2, 0].plot(t, f0, ".", ms=2); ax[2, 0].set(title="Pitch (pyin f0)", xlabel="s", ylabel="Hz", yscale="log")

    f, sp = c["spectrum"]
    ax[2, 1].semilogx(f, sp); ax[2, 1].set(title="Average spectrum (1/6 octave)", xlabel="Hz", ylabel="dB")
    for name, (lo, hi) in BANDS.items():
        ax[2, 1].axvline(lo, c="gray", alpha=.2)
    fig.savefig(out_png, dpi=110)
    plt.close(fig)


def summary_text(s):
    lines = [f"duration {s['duration_s']} s | peak {s['peak_db']} dBFS | {s['lufs']} LUFS | crest {s['crest_db']} dB"]
    for k, b in s["bands"].items():
        lines.append(f"  {k:9s} {b['range_hz'][0]:>5}-{b['range_hz'][1]:<5} Hz  {b['level_db']:6.1f} dB"
                     f"  L/R corr {b['lr_corr']:5.2f}")
    e = s["envelope"]
    lines.append(f"envelope: attack {e['attack_ms']:.0f} ms, peak at {e['peak_at_s']:.2f} s, "
                 f"-20 dB after {e['decay_20db_ms']} ms")
    b = s["brightness_hz"]
    lines.append(f"brightness: median {b['median']:.0f} Hz (10–90%: {b['p10']:.0f}–{b['p90']:.0f})")
    p = s["pitch"]
    if "median_hz" in p:
        lines.append(f"pitch: {p['median_note']} ({p['median_hz']} Hz), range {p['range_notes'][0]} – {p['range_notes'][1]},"
                     f" voiced {p['voiced_fraction']:.0%}")
    h = s.get("harmonics")
    if h:
        lines.append(f"harmonics @ {h['at_s']:.2f}s (dB rel. strongest): {h['levels_db']}  even−odd {h['even_minus_odd_db']} dB")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--band", type=float, nargs=2, metavar=("LO", "HI"), help="band-pass first, e.g. --band 20 500")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--fmin", type=float, default=25, help="lowest pitch to look for (Hz)")
    ap.add_argument("--fmax", type=float, default=1600, help="highest pitch to look for (Hz)")
    a = ap.parse_args()

    x, sr = sd.load(a.audio, a.start, a.end)
    if a.band:
        x = sd.band(x, sr, *a.band)
    out = a.out or default_out(a.audio.resolve(), a.start, a.end)
    out.mkdir(parents=True, exist_ok=True)
    s, c = extract(x, sr, a.fmin, a.fmax)
    s["source"] = {"file": str(a.audio), "start": a.start, "end": a.end, "band_hz": a.band}
    plot(x, sr, s, c, f"{a.audio.name}  {a.start or 0:g}–{a.end or s['duration_s']:g} s", out / "analysis.png")
    (out / "analysis.json").write_text(json.dumps(s, indent=2))
    print(summary_text(s))
    print(f"\n→ {out / 'analysis.png'}\n→ {out / 'analysis.json'}")


if __name__ == "__main__":
    main()
