---
name: compare-attempt
description: Compare the user's rendered Serum 2 attempt (exported from Ableton or FL Studio) against the reference sound and suggest the next concrete Serum tweaks. Use when the user says they exported/bounced/rendered a version, asks "how close is it", "what should I change", or drops a WAV or a Serum screenshot.
---

# Compare an attempt against the reference

## 1. Find the files
- **Attempt:** the path the user gave, otherwise the newest audio file in `songs/*/attempts/`:
  `ls -t songs/*/attempts/*.{wav,aif,aiff,flac} 2>/dev/null | head -3`. Confirm the pick in one line if it's ambiguous.
- **Reference + range + band:** take them from the matching guide in `songs/<slug>/guides/` (its file name holds the range) or from the previous entry in `songs/<slug>/attempts/LOG.md`. If neither exists, ask.
- **Screenshots:** if the user attached or saved Serum screenshots (e.g. `attempts/<name>.png`), read them, since they show the actual patch. Also ask for one when the numbers are ambiguous: *"Can you screenshot Serum's OSC page (and FX/Matrix if used)?"*

## 2. Run the comparison
```bash
pixi run compare <reference> <attempt> --ref-start S --ref-end S --band LO HI --fmin A --fmax B
```
- `--band` is mandatory when the reference is a full mix.
- Add `--att-start/--att-end` if the render has a count-in or several notes.
- If the render is a different note than the reference, say so and focus on timbre: the harmonic *pattern*, brightness ratio and envelope still compare fine.

Read `compare.png` (Read tool) and the printed Δ table.

## 3. Diagnose (in this priority order, stop at the first 1–3 real problems)
1. **Pitch** — Δ cents > ±30 or wrong octave.
2. **Envelope** — attack/decay Δ, shape of the level curve (plucky vs sustained, pumping).
3. **Harmonics / tone** — harmonic table differences, even−odd balance, spectrum-difference panel (where attempt has MORE/LESS).
4. **Brightness & movement** — median Δ %, and whether the reference centroid moves while the attempt is flat (→ modulation).
5. **Width** — L/R corr per band. The sub must stay ~1.0.
6. **Dynamics / FX** — crest Δ (compression), tails (reverb/delay).

Map each problem to a Serum 2 control with `docs/serum2.md` section 5. Give **specific** moves with values or directions and the expected change in the metric. For example: "Distortion → Soft Clip, Drive ~30 %: should lift H3/H5 by ~10 dB toward the reference's −2/−10 dB".

## 4. Respond (keep it short, this is a lesson)
- A score-free, plain summary: what's already close (encouragement grounded in numbers), what's furthest off.
- **Max 3 changes** for the next version, each: *Serum location → setting → why (measurement) → what to listen for*.
- One ear-training prompt: what to A/B against `renders/<element>_ref.wav`.
- Ask them to export `<element>_v<NN+1>.wav` into the same folder and rerun `/compare-attempt`.

## 5. Log it
Append to `songs/<slug>/attempts/LOG.md` (create with a header if missing):
```markdown
## <attempt file> — <date>
ref: <file> <S>–<E> s, band <LO>–<HI> Hz
key Δ: pitch …, attack …, brightness …, harmonics …, width …
suggested: 1) … 2) … 3) …
```
This log is how progress gets tracked across sessions; read the previous entries first so you don't repeat advice that didn't work.
