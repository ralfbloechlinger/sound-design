# sound-design

Learning to hear and rebuild sounds from songs: measure them in Python, then rebuild them in a synth and compare.

## Setup
```bash
pixi install                 # creates .pixi/ env (python 3.12, librosa, scipy, ffmpeg, yt-dlp, jupyter…)
pixi run nbstripout --install --attributes .gitattributes   # once per clone: keep notebook outputs out of git
pixi run check
```

## Workflow per song
```bash
pixi run new-song artist-title                      # scaffold songs/artist-title/
pixi run fetch <url> artist-title 0 30              # download + float WAV of 0–30 s
pixi run lab                                        # open notebooks/
```
1. **Listen** and write what you hear in the song's `README.md`.
2. **Measure** with the notebook: level, spectrogram, bands/stereo, pitch, harmonics.
3. **Rebuild** in your synth, export, run the same measurements on your version.
4. **Compare** and log what got closer.

## Layout
```
notebooks/          lessons (start with 01_listening_with_numbers)
src/sdtools/        small helpers: load/save, band filters, mid/side, note names, spectrogram
tools/              fetch.py, new_song.py
songs/<slug>/
  README.md, notes  your findings
  scripts/          repeatable analysis for this song
  figures/ data/    committed results
  audio/ renders/   git-ignored (copyrighted / regenerable)
```

Only analyse audio you're allowed to use. Source audio never goes into git.
