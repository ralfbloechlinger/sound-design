"""Compare your render (from Ableton / FL) against the reference.

    pixi run compare <reference> <attempt> [--ref-start S] [--ref-end S] [--att-start S] [--att-end S]
                     [--no-trim] [--out DIR]

What it does to make the comparison fair:
  1. cuts leading silence from both (so attacks line up; disable with --no-trim)
  2. crops both to the shorter length
  3. matches loudness (LUFS) by changing the attempt's gain, so "louder" doesn't fool you
Then it measures both with the same extractor and plots them on top of each other.

Writes <out>/compare.png and <out>/compare.json and prints a delta table.
Default out: next to the attempt as <attempt-stem>_compare/.
"""
import argparse
import json
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import sdtools as sd
from sdtools.features import extract, loudness, trim_silence

REF_C, ATT_C = "#1f77b4", "#d62728"


def prep(path, start, end, trim):
    x, sr = sd.load(path, start, end)
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    return (trim_silence(x, sr) if trim else x), sr


def deltas(r, a):
    d = {
        "lufs_before_match": a["_lufs_raw"] - r["lufs"],
        "crest_db": a["crest_db"] - r["crest_db"],
        "attack_ms": a["envelope"]["attack_ms"] - r["envelope"]["attack_ms"],
        "brightness_median_pct": 100 * (a["brightness_hz"]["median"] / r["brightness_hz"]["median"] - 1),
        "bands": {k: {"level_db": a["bands"][k]["level_db"] - r["bands"][k]["level_db"],
                      "lr_corr": a["bands"][k]["lr_corr"] - r["bands"][k]["lr_corr"]}
                  for k in r["bands"] if k in a["bands"]},
    }
    rd, ad = r["envelope"]["decay_20db_ms"], a["envelope"]["decay_20db_ms"]
    d["decay_20db_ms"] = (ad - rd) if (rd and ad) else None
    if "median_hz" in r["pitch"] and "median_hz" in a["pitch"]:
        d["pitch_cents"] = 1200 * np.log2(a["pitch"]["median_hz"] / r["pitch"]["median_hz"])
    if r.get("harmonics") and a.get("harmonics"):
        d["harmonics_db"] = [round(y - x, 1) for x, y in zip(r["harmonics"]["levels_db"], a["harmonics"]["levels_db"])]
        d["even_minus_odd_db"] = a["harmonics"]["even_minus_odd_db"] - r["harmonics"]["even_minus_odd_db"]
    return json.loads(json.dumps(d, default=float), parse_float=lambda v: round(float(v), 1))


def plot(xr, xa, sr, r, a, cr, ca, title, out_png):
    fig = plt.figure(figsize=(18, 17), layout="constrained")
    gs = fig.add_gridspec(4, 2)
    fig.suptitle(title, fontsize=14)
    sd.spectrogram(xr.mean(axis=1), sr, n=2048, ax=fig.add_subplot(gs[0, 0]), title="REFERENCE", vmax=-20)
    sd.spectrogram(xa.mean(axis=1), sr, n=2048, ax=fig.add_subplot(gs[0, 1]), title="ATTEMPT (loudness-matched)", vmax=-20)

    ax = fig.add_subplot(gs[1, 0])
    (f, sr_), (_, sa) = cr["spectrum"], ca["spectrum"]
    ax.semilogx(f, sr_, c=REF_C, label="ref"); ax.semilogx(f, sa, c=ATT_C, label="attempt")
    top = np.nanmax(np.r_[sr_, sa])
    ax.set(title="Average spectrum", xlabel="Hz", ylabel="dB", ylim=(top - 80, top + 5)); ax.legend()
    ax = fig.add_subplot(gs[1, 1])
    diff = np.where((sr_ > top - 70) | (sa > top - 70), sa - sr_, np.nan)  # hide noise floor
    ax.semilogx(f, diff, c="k"); ax.axhline(0, c="gray")
    ax.fill_between(f, 0, diff, where=diff > 0, color=ATT_C, alpha=.3, label="attempt has MORE")
    ax.fill_between(f, 0, diff, where=diff < 0, color=REF_C, alpha=.3, label="attempt has LESS")
    ax.set(title="Spectrum difference (attempt − ref)", xlabel="Hz", ylabel="dB", ylim=(-24, 24)); ax.legend()

    for (key, ttl, ylab, log), pos in zip(
            [("env", "Level envelope", "dB", False), ("centroid", "Brightness (centroid) over time", "Hz", True),
             ("f0", "Pitch (f0) — grey lines = semitones", "Hz", False)],
            [gs[2, 0], gs[2, 1], gs[3, 0]]):
        ax = fig.add_subplot(pos)
        for c, col, lab in [(cr, REF_C, "ref"), (ca, ATT_C, "attempt")]:
            t, v = c[key]
            ax.plot(t, v, ".", ms=2, c=col, label=lab) if key == "f0" else ax.plot(t, v, c=col, label=lab, lw=1)
        ax.set(title=ttl, xlabel="s", ylabel=ylab, yscale="log" if log else "linear"); ax.legend()
        if key == "env":
            m = cr["env"][1].max(); ax.set_ylim(m - 60, m + 6)
        if key == "f0":
            v = np.r_[cr["f0"][1], ca["f0"][1]]
            if np.isfinite(v).any():
                lo, hi = np.nanpercentile(v, 2) / 2 ** (2 / 12), np.nanpercentile(v, 98) * 2 ** (2 / 12)
                ax.set_yscale("log"); ax.set_ylim(lo, hi)
                ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
                m0, m1 = int(np.floor(69 + 12 * np.log2(lo / 440))), int(np.ceil(69 + 12 * np.log2(hi / 440)))
                step = max(1, (m1 - m0) // 12)
                ticks = [440 * 2 ** ((m - 69) / 12) for m in range(m0, m1 + 1, step)]
                for h in ticks:
                    ax.axhline(h, c="gray", alpha=.2, lw=.8)
                ax.set_yticks(ticks, [f"{sd.hz_to_note(h).split()[0]}  {h:.0f}" for h in ticks])

    ax = fig.add_subplot(gs[3, 1])
    names = list(r["bands"])
    xs = np.arange(len(names))
    ax.bar(xs - .2, [r["bands"][n]["level_db"] for n in names], .4, color=REF_C, label="ref level")
    ax.bar(xs + .2, [a["bands"][n]["level_db"] for n in names], .4, color=ATT_C, label="attempt level")
    ax.set_xticks(xs, [f"{n}\ncorr {r['bands'][n]['lr_corr']:.2f}/{a['bands'][n]['lr_corr']:.2f}" for n in names])
    ax.set(title="Band levels (dB) — L/R correlation ref/attempt under labels", ylim=(-90, 0)); ax.legend()
    fig.savefig(out_png, dpi=100)
    plt.close(fig)


def table(r, a, d):
    def row(name, rv, av, dv, unit=""):
        return f"  {name:22s} {str(rv):>14s} {str(av):>14s} {str(dv):>10s}{unit}"
    L = [row("", "REFERENCE", "ATTEMPT", "Δ")]
    L.append(row("loudness (pre-match)", f"{r['lufs']} LUFS", f"{a['_lufs_raw']:.1f} LUFS", d["lufs_before_match"], " dB"))
    L.append(row("crest (peak−rms)", r["crest_db"], a["crest_db"], d["crest_db"], " dB"))
    if "pitch_cents" in d:
        L.append(row("pitch", r["pitch"]["median_note"], a["pitch"]["median_note"], d["pitch_cents"], " cents"))
    L.append(row("attack", f"{r['envelope']['attack_ms']:.0f} ms", f"{a['envelope']['attack_ms']:.0f} ms", d["attack_ms"], " ms"))
    L.append(row("decay to −20 dB", f"{r['envelope']['decay_20db_ms'] or '—'} ms", f"{a['envelope']['decay_20db_ms'] or '—'} ms", d["decay_20db_ms"] or "—", " ms"))
    L.append(row("brightness median", f"{r['brightness_hz']['median']:.0f} Hz", f"{a['brightness_hz']['median']:.0f} Hz",
                 d["brightness_median_pct"], " %"))
    L.append(row("brightness 10–90%", f"{r['brightness_hz']['p10']:.0f}-{r['brightness_hz']['p90']:.0f}",
                 f"{a['brightness_hz']['p10']:.0f}-{a['brightness_hz']['p90']:.0f}", ""))
    for k, b in d["bands"].items():
        L.append(row(f"{k} level / corr", f"{r['bands'][k]['level_db']} / {r['bands'][k]['lr_corr']}",
                     f"{a['bands'][k]['level_db']} / {a['bands'][k]['lr_corr']}", b["level_db"], " dB"))
    if "harmonics_db" in d:
        L.append(f"  harmonics ref     {r['harmonics']['levels_db']}")
        L.append(f"  harmonics attempt {a['harmonics']['levels_db']}")
        L.append(f"  even−odd balance Δ {d['even_minus_odd_db']} dB (+ = attempt has relatively more even harmonics)")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reference", type=Path)
    ap.add_argument("attempt", type=Path)
    ap.add_argument("--ref-start", type=float); ap.add_argument("--ref-end", type=float)
    ap.add_argument("--att-start", type=float); ap.add_argument("--att-end", type=float)
    ap.add_argument("--no-trim", action="store_true", help="keep leading silence")
    ap.add_argument("--band", type=float, nargs=2, metavar=("LO", "HI"),
                    help="band-pass BOTH signals first, e.g. --band 20 500 to judge only the bass in a full mix")
    ap.add_argument("--fmin", type=float, default=25); ap.add_argument("--fmax", type=float, default=1600)
    ap.add_argument("--out", type=Path)
    o = ap.parse_args()

    xr, sr = prep(o.reference, o.ref_start, o.ref_end, not o.no_trim)
    xa, sra = prep(o.attempt, o.att_start, o.att_end, not o.no_trim)
    if sra != sr:
        import librosa
        xa = librosa.resample(xa.T, orig_sr=sra, target_sr=sr).T
    if o.band:
        xr, xa = sd.band(xr, sr, *o.band), sd.band(xa, sr, *o.band)
    n = min(len(xr), len(xa)); xr, xa = xr[:n], xa[:n]

    raw = loudness(xa, sr)
    xa = xa * 10 ** ((loudness(xr, sr) - raw) / 20)

    r, cr = extract(xr, sr, o.fmin, o.fmax)
    a, ca = extract(xa, sr, o.fmin, o.fmax)
    a["_lufs_raw"] = raw
    d = deltas(r, a)

    out = o.out or o.attempt.resolve().parent / f"{o.attempt.stem}_compare"
    out.mkdir(parents=True, exist_ok=True)
    plot(xr, xa, sr, r, a, cr, ca, f"{o.attempt.name}  vs  {o.reference.name} "
         f"[{o.ref_start or 0:g}–{o.ref_end if o.ref_end is not None else '':}s]"
         + (f"  band {o.band[0]:g}–{o.band[1]:g} Hz" if o.band else ""), out / "compare.png")
    a.pop("_lufs_raw")
    (out / "compare.json").write_text(json.dumps({
        "reference": {"file": str(o.reference), "start": o.ref_start, "end": o.ref_end, **r},
        "attempt": {"file": str(o.attempt), "start": o.att_start, "end": o.att_end, "lufs_raw": raw, **a},
        "band_hz": o.band,
        "delta_attempt_minus_ref": d}, indent=2, default=float))
    a["_lufs_raw"] = raw
    print(f"compared {n / sr:.2f} s, attempt gain-matched by {r['lufs'] - raw:+.1f} dB\n")
    print(table(r, a, d))
    print(f"\n→ {out / 'compare.png'}\n→ {out / 'compare.json'}")


if __name__ == "__main__":
    main()
