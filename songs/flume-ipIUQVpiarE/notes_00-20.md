# Bass and slide, opening 20 seconds

Source: https://www.youtube.com/watch?v=ipIUQVpiarE

Analysis is based on the decoded waveform and spectral curves, without direct auditory evaluation. Times are approximate video times. Octaves use C4 = MIDI 60.

## Sustained low bass

| Time | Best supported note | Frequency |
|---|---|---|
| 0–8.4 s | No reliably transcribed deep bass; mostly midrange texture | — |
| 8.4–8.9 s | Attack/pitch settling; do not treat each spectral peak as a separate note | — |
| 8.9–10.5 s | D♯1 / E♭1 | ~39 Hz |
| 10.6–11.4 s | A♯0 / B♭0 | ~29 Hz |
| 11.4–13.2 s | Overlapping slide, transients, and low components | See below |
| 13.3–16.0 s | A♯0 / B♭0 | ~29 Hz |
| 16.0–17.1 s | Transition/effects; no confident single-note transcription | — |
| 17.2–17.7 s | Bass attack settling | — |
| 17.7–19.3 s | D♯1 / E♭1 | ~39 Hz |
| 19.4–20 s | A♯0 / B♭0 | ~29 Hz |

39 Hz is corroborated by partials near 78, 117, 156, and 195 Hz and waveform periodicity. 29 Hz is corroborated by ~58, 88, 117, and 146 Hz. Some transition regions contain additional half-spacing components, so these are audible-range bass-note estimates rather than proof of the original oscillator's octave.

## Slide around 12 seconds

This is not a clean sequence of discrete notes. A dominant moving spectral ridge overlaps other components. The following points describe that ridge, not an independently isolated fundamental or MIDI transcription:

| Time | Ridge frequency | Nearest pitch |
|---|---|---|
| 11.60 s | ~197 Hz | G3 |
| 11.75 s | ~165 Hz | E3 |
| 11.85–11.95 s | ~192–195 Hz | G3 vicinity |
| 12.10–12.20 s | ~130–133 Hz | C3 vicinity |
| 12.30 s | ~118 Hz | A♯2 / B♭2 |
| 12.35 s | ~111 Hz | A2 |
| 12.45 s | ~97 Hz | G2 |
| 12.60 s | ~58 Hz | A♯1 / B♭1 |
| 12.65–12.70 s | ~53 Hz | G♯1 / A1 vicinity |
| 12.75 s | ~50 Hz | G1 vicinity |

There are overlapping descending curves, and dominance changes around 11.85 s. Do not read the table as proof of one oscillator jumping E3→G3. From about 12.1 to 12.75 s the prominent ridge falls roughly 17 semitones, with bends and uneven speed. Its later low-frequency tail merges into bass attacks around 12.8–13.2 s, making a precise final slide note unreliable.

## Distortion and sound design

The held bass contains both odd and even harmonics, so a pure sine alone will not recreate it. Mildly asymmetric saturation, a saturated triangle, or a filtered saw are useful experiments. Harmonic content alone cannot distinguish distortion from a harmonically rich oscillator.

The slide's strongest band shifts and has changing partial levels. Some portions, particularly near 12.1 s, have approximately integer-related upper components; other portions are much less clearly harmonic. Pitch movement plus filtering/resonance and overlapping layers is a better starting reconstruction than static distortion alone. A resonant filter sweep can also create a pitched ridge; the spectrum cannot establish that every ridge point is the synth's oscillator fundamental.

Suggested experiment: keep the held sub on its own centered track. Add a separate mono pitched effect; draw a curved descending pitch automation using the ridge table as a listening starting point, and layer a second short descent for the earlier overlap. Add moderate saturation, then automate a low-pass or band-pass filter to change which harmonics dominate. Match pitch and envelope before increasing drive. Try a resonant filter sweep as an alternative if oscillator pitch bends do not match. No particular distortion, FM, wavefolding, or bitcrushing algorithm is established by this analysis.

## Artifacts

- `opening_00-20.wav`: stereo PCM listening copy, gain reduced by 6.02 dB to avoid clipping decoded peaks.
- `bass_00-20.wav`: independently normalized 25–250 Hz listening aid, not an isolated stem.
- `slide_10-14.wav`: full mix excerpt covering the slide.
- `slide_detail.png`: 80 ms spectral windows; better temporal detail, poorer frequency resolution.
- `bass_pitch20.png`: 240 ms windows; includes a strongest-low-peak trace that can jump to harmonics. The trace is diagnostic and is not a validated fundamental-frequency transcription.
- `bass_pitch_track.csv`: same unvalidated strongest-low-peak data; nearest-note column is not MIDI ground truth.
- `pitch20.py`: repeatable extraction and plots.
