---
name: analyze-sound
description: Analyse a sound in a reference song (a time range and/or a single element such as bass, lead, pad) and write a step-by-step Serum 2 recreation guide. Use when the user wants to learn how a sound was made, asks "how do I make this in Serum", gives a song + timestamp, or a YouTube link to analyse.
---

# Analyse a sound → Serum 2 recreation guide

Arguments (any order, all optional): a song slug or URL, a time range like `8.9-10.5`, and an element name (`bass`, `lead`, `pad`, `pluck`, `texture`, `fx`…).

## 1. Locate the audio
- Song folders live in `songs/<slug>/`. Source audio is in `songs/<slug>/audio/` (prefer `*_float.wav`).
- Given a URL for a new song: `pixi run new-song <artist-title>` then `pixi run fetch <url> <artist-title> [start end]`.
- No time range given: run `pixi run analyze <file>` on the whole file first, look at `analysis.png`, and propose 2–3 interesting sections to the user.

## 2. Ear first (learning step)
Before showing numbers, ask the user in one short question what they hear in that section (role, movement, character). Skip it if they've already said, or say "just analyse".

## 3. Measure
Pick a band per element so other instruments in the mix don't pollute the measurements:

| element | `--band` | `--fmin/--fmax` |
|---|---|---|
| sub/bass | `20 500` | `25 200` |
| mid bass / reese | `40 2000` | `30 400` |
| lead / pluck / vocal-ish | `300 8000` | `100 1600` |
| pad / texture | `150 12000` | pitch is often unreliable; ignore it |
| hats / air / noise | `5000 18000` | none |

```bash
pixi run analyze songs/<slug>/audio/<file> --start S --end S --band LO HI --fmin A --fmax B
```
Also run it **without** `--band` once if the element's relation to the full mix matters, e.g. its width compared with the rest.
Read `analysis.png` (Read tool) **and** the printed summary. Zoom with additional `--start/--end` runs if a transient or slide matters.

## 4. Interpret with the symptom map
Open `docs/serum2.md` (section 5 = measurement → Serum control). Translate each measurement into a decision:
- **pitch / range** → note, octave, glide, pitch envelope
- **harmonics** (levels, even−odd) → waveform choice, warp, distortion mode
- **brightness** median + 10–90 % range, and its movement over time → filter type/cutoff, and whether an envelope/LFO drives it (and at what rate)
- **envelope** attack / decay → Env 1 settings
- **band levels + L/R correlation** → unison/width, mono-bass requirement
- evenly spaced peaks → comb; inharmonic peaks → FM/RM/Bode; grainy/smeared → granular/spectral
Say how sure you are of each inference.

## 5. Write the guide
Write `songs/<slug>/guides/<element>_<start>-<end>.md`:

```markdown
# <Element> @ <start>–<end> s
## What the analysis shows   ← 3–6 bullets, each: measurement → meaning
## Serum 2 patch, step by step
1. Init preset. Voicing: …
2. Oscillators: Osc A (mode, wave, WT Pos, warp…), Sub, Noise …
3. Filter: type, cutoff, res, drive …
4. Envelopes: Env 1 (amp) A/H/D/S/R; Env 2 → ... (matrix amount)
5. LFOs: …
6. FX (Main / Bus): order + key settings
7. Macros worth mapping for experimentation
   – for each step a one-line **why**, tied to a measurement
## Render it for comparison
- Play: <note(s)>, <length>, BPM <x>; export the Serum track only, 48 kHz, 24-bit or 32-bit float WAV, normalise OFF
- Save as `songs/<slug>/attempts/<element>_v01.wav` then run `/compare-attempt`
## What to listen for
- 2–3 ear-training prompts (A/B the reference band file vs your render)
```
Starting values are suggestions to audition, not claims about the original producer's patch. Keep the patch as simple as the evidence allows; add layers only when a measurement demands it.

Also write a band-limited listening copy of the reference so the user can A/B in the DAW:
```bash
pixi run python -c "import sdtools as sd; x,sr=sd.load('<file>',S,E); sd.save('songs/<slug>/renders/<element>_ref.wav', sd.band(x,sr,LO,HI), sr, normalize=0.8)"
```

## 6. Report
Tell the user the guide path, the 2–3 most important insights, and the exact render instructions.
