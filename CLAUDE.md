# sound-design — context for Claude

## Goal
Ralf is **learning sound design**. The synth is **Serum 2**; the DAW is Ableton or FL Studio. The repo is used to
analyse reference songs, get Serum 2 recreation guides, then compare Ralf's renders against the reference.

**Teaching style matters more than speed:**
- Explain *why* each setting follows from a measurement ("H3 is only 2 dB below H1 → strong odd harmonics → clip-type distortion").
- Give at most **3 changes per iteration**, ordered: pitch → level/envelope → harmonics/filter → movement (LFO/env mod) → width → FX/space.
- Ask Ralf what they hear before revealing analysis when it's cheap to do so; ear training is the point.
- Be honest about uncertainty: a full mix is not a stem; spectral evidence suggests, it rarely proves.

## Where things are
- `docs/serum2.md` — Serum 2 modules, FX, modulation, and a **measurement → Serum control symptom map** (section 5). Use Serum's real module names from it.
- `songs/<slug>/` — `audio/` (source, git-ignored), `attempts/` (Ralf's DAW renders + `LOG.md`), `guides/` (recreation guides), `figures/`, `data/`, `notes*.md`.
- `src/sdtools/` — helpers; `features.py` is the shared feature extractor.
- Run everything through pixi: `pixi run analyze …`, `pixi run compare …`, `pixi run fetch …`, `pixi run new-song …`.

## Tools
- `pixi run analyze <audio> --start S --end S [--band LO HI]` → `analysis.png` + `analysis.json` + text summary.
- `pixi run compare <ref> <attempt> --ref-start S --ref-end S [--band LO HI]` → trims silence, crops, LUFS-matches,
  writes `compare.png` + `compare.json` next to the attempt and prints a Δ table.
- **Always use `--band` when the reference is a full mix** (e.g. `20 500` for bass, `500 8000` for a lead) so other instruments don't pollute brightness/width.
- Read the PNGs with the Read tool, they're designed to be legible to you. Ralf may also share **Serum screenshots**; read them to see the actual patch.

## Skills
- `/analyze-sound` — analyse a section/element and write a Serum 2 recreation guide.
- `/compare-attempt` — compare Ralf's latest render to the reference and suggest the next tweaks.

## Conventions
- Never commit audio (git-ignored). Notebooks are stripped of outputs by nbstripout.
- Only analyse audio Ralf is entitled to use.
