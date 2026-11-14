# Bass @ 8.9–10.5 s

The held D♯1 bass that enters at ~8.4 s. The 8.9–10.5 s window is its sustain; the entry (8.38–8.9 s) was measured
separately because it carries the pitch drop. Figures: `figures/opening20_float_8.9-10.5s/` (band 20–500 Hz) and
`figures/opening20_float_8.3-9.1s/` (entry zoom). Full mix, not a stem: treat everything below as evidence, not proof.

## What the analysis shows
- **Pitch: D♯1 (39.0 Hz, +5 ct), 100 % voiced, dead steady across the sustain.** No vibrato, no glide inside the window. → one held note, no LFO on pitch. *Confidence: high.*
- **Entry: pitch falls from ≈49 Hz (G1) to 39 Hz over ≈0.6 s**, with the first ≈0.45 s about 10 dB louder than the sustain. → a downward pitch envelope of about 4 semitones plus an amp envelope that decays to a lower sustain: the classic distorted-808 gesture. *Confidence: medium.* Three kick-like transients (≈8.40, 8.53, 8.66 s) sit on top and inflate both the loudness and the pitch trace.
- **Harmonics (rel. H1): H2 −7.5, H3 −1.6, H4 −13, H5 −10, H7 −18 dB; even−odd −5.3 dB.** Odd harmonics dominate → symmetric saturation of a sine (clip or fold), with some asymmetry for H2. H3 only 1.6 dB below H1 is *more* than a hard clip can produce (a perfect square gives H3 at −9.5 dB, tanh-style soft clip ≈ −11 dB). So either the fundamental has been turned down by the mix/master (very common at 39 Hz; YouTube encoding too), or the shaper folds, or both. *Confidence: medium.* Don't chase H3 = H1 exactly.
- **Timbre drifts during the sustain, even though brightness looks flat.** Centroid sits at 105 Hz (10–90 %: 85–125 Hz) the whole time, but under the hood H3 falls from −2.5 to −7.5 dB and H5 from −11 to −19 dB while H2 *rises* from −9 to −1.4 dB. → drive is relaxing over ~1.3 s while the asymmetric (even) part stays. *Confidence: low-medium*: a rising H2 could also come from another part in the mix.
- **Harmonics roll off steadily up to ~500 Hz** (H10 at 390 Hz ≈ −30 dB). → a low-pass after the distortion, somewhere around 300–450 Hz. The band filter hides anything above 500 Hz, so the exact cutoff is a guess.
- **Width: 20–120 Hz L/R corr 0.99 (mono); 120–500 Hz 0.88.** → mono sub, at most a touch of width on the harmonics. The 0.88 may just be other instruments, so start fully mono.

## Serum 2 patch, step by step
1. **Init preset. Voicing: Mono, Legato off, Porta 0.**
   – *why:* single held note; legato off makes the pitch envelope fire on every note.
2. **Oscillators: Osc A = sine** (Wavetable mode, *Basic Shapes*, WT Pos at the sine frame), Oct 0, Unison 1. Sub and Noise off. Route Osc A to Filter in the Mixer.
   – *why:* the fundamental is a stable 39 Hz and the harmonics look like a *processed* sine, not a saw (a saw would give strong even harmonics: H2 at −6 dB, H4 at −12 dB, with no odd dominance).
3. **Filter 1: MG Low 24, cutoff ≈ 380 Hz, Res 0–10 %, Drive 0.** In the FX rack, set the Distortion's filter to *Post* or put an FX **Filter** after the Distortion so the roll-off happens *after* the harmonics are created.
   – *why:* harmonics fade steadily towards 500 Hz; the low-pass has to tame what the distortion adds, so it must sit after it.
4. **Envelopes**
   - **Env 1 (amp): A 2 ms, H 0, D 450 ms, S ≈ −10 dB, R 120 ms.**
     – *why:* fast onset, a loud ≈0.45 s head, then a flat sustain ≈10 dB lower (level panel: −15 ±3 dB for the whole window).
   - **Env 2 → Osc A pitch (Matrix): A 0, H 0, D 600 ms, S 0, R 0.** Set the matrix amount so the note *starts* 4 semitones up (hover the amount and read the value, or tune by ear until the first instant sounds like G1).
     – *why:* the pitch trace falls 49 → 39 Hz over ≈0.6 s. Give the decay curve a slightly concave (fast-then-slow) shape.
   - **Env 3 → Distortion Drive (Matrix), optional for v02: A 0, D 1.3 s, S ≈ 60 %, amount ≈ +25 %.**
     – *why:* odd harmonics (H3, H5) fade over the sustain. Leave it out until pitch, level and basic tone match.
5. **LFOs: none.**
   – *why:* the level wobble (±3 dB) is irregular, not tempo-synced, and pitch is steady. That is most likely the mix, not the patch.
6. **FX (Main), in this order**
   1. **Distortion: Soft Clip, Drive ≈ 50 %, DC bias ≈ 10–15 %.** If H3 stays too quiet even at high drive, try **Sin Fold** at low drive (25–35 %) instead.
      – *why:* odd harmonics dominate → symmetric shaper; H2 at −7.5 dB → a bit of DC bias for asymmetry. Sin Fold is the shaper that can push H3 up near H1.
   2. **Filter** (if you didn't use the Distortion's post filter): MG Low 24, ≈380 Hz.
   3. **Utility: Mono Bass on, 120 Hz** (or Width 0 %).
      – *why:* sub corr 0.99.
   - No reverb, delay or chorus: nothing in the measurements asks for them.
7. **Macros worth mapping**
   - **M1 Drive** → Distortion Drive (the biggest lever on H3/H5).
   - **M2 Tone** → Filter 1 / FX Filter cutoff, range 200–700 Hz.
   - **M3 Drop** → Env 2 → pitch matrix amount, 0–7 semitones.
   - **M4 Asym** → Distortion DC bias (H2 level).

## Render it for comparison
- Play **one note D♯1 (MIDI 27)**, held **2.2 s**, any BPM (120 is fine), velocity 100. Note names differ per DAW: MIDI 27 shows as **D♯0 in Ableton** (C3 = 60) and **D♯2 in FL Studio** (C5 = 60). Check that the analyser says D♯1 / 39 Hz.
- Export the Serum track only, **48 kHz, 24-bit or 32-bit float WAV, normalise OFF**, starting exactly at the note.
- Save as `songs/flume-ipIUQVpiarE/attempts/bass_v01.wav`, then run `/compare-attempt`. It compares two windows:
  - sustain: `--ref-start 8.9 --ref-end 10.5 --att-start 0.52 --band 20 500 --fmin 25 --fmax 200`
  - entry: `--ref-start 8.38 --ref-end 8.9 --band 20 500 --fmin 25 --fmax 200`

## What to listen for
A/B `renders/bass_ref.wav` (8.3–10.6 s, 20–500 Hz, normalised) against your render, level-matched, on headphones or decent monitors. Small speakers will hide the 39 Hz fundamental.
1. **The first half-second:** do you hear the pitch *fall* into the note, or only a louder hit? Turn M3 to 0 and back to see what the drop adds.
2. **On small speakers or a phone:** can you still "hear" the note? That is H3 (117 Hz) and H2 (78 Hz) doing the work. Sweep M1 and notice when yours goes from "sine" to "buzzy" and when it passes the reference.
3. **During the sustain:** does the reference get slightly rounder/warmer towards 10 s? That's the falling-odd / rising-even drift. Only if you hear it, try the Env 3 → Drive step.
