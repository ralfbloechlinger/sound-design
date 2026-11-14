# songs/

One folder per analysed song, created with `pixi run new-song <artist-title>`:

```
songs/<artist-title>/
  README.md     listening notes + findings
  audio/        source audio (git-ignored)
  guides/       Serum 2 recreation guides (/analyze-sound)
  attempts/     your DAW renders (audio git-ignored), compare plots, LOG.md (/compare-attempt)
  renders/      band-limited listening copies (git-ignored)
  figures/ data/ scripts/
```

On `main` this folder stays empty so the repo remains a clean starting point.
Keep your own analyses on a personal branch (see the top-level README).
