# sound-design

**Learning sound design by reverse-engineering songs in Serum 2.**

The loop:

```
 reference song ──► analyse (spectral, pitch, harmonics, envelope, width)
                          │
                          ▼
              Serum 2 recreation guide  ◄───────────────┐
                          │                             │
                          ▼                             │
        build patch in Serum 2 (Ableton / FL)           │
                          │                             │
                          ▼                             │
        export WAV ─► compare against reference ─► next 1–3 tweaks
```

The point isn't to copy presets. It's to train your ears: each suggestion is tied to a measurement you can see and then learn to hear.

## Setup
```bash
pixi install                 # python 3.12, librosa, scipy, ffmpeg, yt-dlp, jupyter…
pixi run check
```

## Branches: template vs. your work
`main` is a **clean, reusable template**: tools, docs, skills, lessons, and an empty `songs/`. Keep your own analyses (guides, figures, logs) on a personal branch:

```bash
git switch -c my-analysis          # once
```
```bash
git switch my-analysis && git merge main   # pull template improvements into your work
```

Improve the tooling on `main` (or on a feature branch → `main`), and do song work on your branch. Audio is git-ignored on every branch, so it stays on disk when you switch.

## Working with Claude (Claude Code skills)
Open this folder in Claude Code and use:

| Command | What happens |
|---|---|
| `/analyze-sound <song> <start-end> <element>` | Measures the sound and writes `songs/<slug>/guides/<element>_<range>.md`: what the analysis shows, and a step-by-step Serum 2 patch with a *why* for every setting |
| `/compare-attempt` | Takes your newest render in `songs/<slug>/attempts/`, compares it with the reference, and gives you max 3 concrete Serum tweaks. Logs progress in `attempts/LOG.md` |

Plain questions work too: *"why does the reference sound wider?"*, *"explain warp FM"*, *"what does even-vs-odd harmonics mean?"*.
[CLAUDE.md](CLAUDE.md) gives Claude the context: goal, teaching style, tools.

### Getting your sound to Claude
Claude can't listen to Ableton or FL live. It reads **audio files** and **images** (plots and screenshots), so the handover is a file in `songs/<slug>/attempts/`:

**Ableton Live**
1. Loop-brace the region (e.g. the 1.6 s bass note). Solo or select the Serum track.
2. `File → Export Audio/Video` (⇧⌘R). Rendered Track: *your Serum track*. WAV, **48 kHz**, 24-bit or 32-bit float, **Normalize off**.
3. Save as `songs/<slug>/attempts/bass_v01.wav`.

**FL Studio**
1. Select the time range in the Playlist (or put the notes in a pattern). Route Serum to its own mixer track and solo it.
2. `File → Export → WAVE file` (Ctrl+R). **48 kHz**, 24-bit or 32-bit float, normalise off.
3. Save as `songs/<slug>/attempts/bass_v01.wav`.

Then say `/compare-attempt`.

**Tips**
- Play the **same note and length** as in the guide. Pitch differences make everything else harder to compare.
- Number versions (`_v01`, `_v02`, …) so the log shows your progress.
- **Screenshot Serum** (⇧⌘4 on macOS) and drop it in the chat, or save it as `attempts/bass_v01.png`. Claude can read the knobs and see the actual patch.
- Load `songs/<slug>/renders/<element>_ref.wav` (the band-limited reference that `/analyze-sound` makes) into your DAW to A/B by ear.

## Doing it by hand
```bash
pixi run new-song artist-title                               # scaffold songs/artist-title/
pixi run fetch <url> artist-title 0 30                       # download + float WAV of 0–30 s
pixi run analyze songs/artist-title/audio/source_float.wav --start 8.9 --end 10.5 --band 20 500
pixi run compare songs/artist-title/audio/source_float.wav songs/artist-title/attempts/bass_v01.wav \
    --ref-start 8.9 --ref-end 10.5 --band 20 500
pixi run lab                                                 # notebooks/: lessons (open .py → Notebook)
```
Use `--band LO HI` whenever the reference is a full mix (e.g. `20 500` for bass). Otherwise hats and pads distort the brightness and width readings.

## What the measurements mean
| Measurement | Tells you | Serum 2 area |
|---|---|---|
| pitch (f0, note) | note, octave, slides | Osc tuning, Porta, pitch env |
| harmonics + even−odd | waveform and saturation type | Osc wave / Warp, Distortion mode |
| brightness (spectral centroid) + movement | filter cutoff, and whether it's modulated | Filter, Env 2 / LFO → Cutoff |
| envelope (attack, decay) | amp shape | Env 1 |
| band levels + L/R correlation | where energy sits, how wide | Unison, Chorus, Hyper/Dimension, Utility mono bass |
| LUFS / crest | loudness and squash | Compressor, Distortion drive |

Full mapping and a Serum 2 module overview: **[docs/serum2.md](docs/serum2.md)**.

## Layout
```
CLAUDE.md               context for Claude
docs/serum2.md          Serum 2 reference + measurement→control symptom map
.claude/skills/         /analyze-sound, /compare-attempt
notebooks/              lessons as `# %%` .py files (start with 01_listening_with_numbers.py)
src/sdtools/            helpers + features.py (shared feature extractor)
tools/                  analyze, compare, fetch, new_song
songs/<slug>/
  README.md, notes      your findings
  guides/               Serum 2 recreation guides
  attempts/             your renders (*.wav ignored) + LOG.md + compare plots
  figures/ data/        analysis results
  audio/ renders/       git-ignored (copyrighted / regenerable)
```

Only analyse audio you're allowed to use. Source audio and renders never go into git.
