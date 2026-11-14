# Serum 2 — what's in the box

A cheat sheet for turning analysis into patches. The structure and module names come from Xfer's *What's New in Serum 2* guide (v2.0, March 2025). Items marked † come from Serum 1 and carry over. Check them in your own install, because Xfer may rename or extend them in updates.

Signal flow: **Oscillators → (Filter 1 / Filter 2) → Mixer → FX (Main, Bus 1, Bus 2) → Out**. In the Mixer, each source can be sent to Filter, Main, Direct (bypasses FX) or None, and to the FX busses.

---

## 1. Sound sources

| Source | What it is | Key controls | Reach for it when the analysis shows… |
|---|---|---|---|
| **Osc A / B / C** | Three main oscillators. Each has 5 modes (below) | Oct / Sem / Fin / Crs, Pan, Level, Unison, Detune, Blend, Phase + Rand, **two Warp slots** | the main harmonic body |
| **Sub** | Simple sub oscillator: sine, triangle, saw, square variants† | Oct, Crs, Phase, Pan, Level | a clean mono fundamental below ~80 Hz |
| **Noise** | Noise/sample oscillator, e.g. "Geiger". Stereo control | Count, Stereo, Pitch, Pan, Level | air, breath, transients, a band of hiss |

### Oscillator modes
| Mode | What it does | Main knobs |
|---|---|---|
| **Wavetable** | Classic Serum. Scan through single-cycle frames | **WT Pos**, Unison/Detune/Blend, Warp 1+2. Option for smooth WT interpolation |
| **Multisample** | Sampled instruments mapped across keys/velocity (loads SFZ) | **Timbre**, Vel Track, its own amp envelope |
| **Sample** | A sampler: one-shot/loop, start/end and loop points, crossfade, slicing | **Scan**, LS/LE (loop start/end), playback mode |
| **Granular** | Cuts a sample into grains (up to 256) and re-sprays them | Scan, **Dens**(ity), **Length**, Offset, Dir, Pitch, Window amount, several Rand knobs |
| **Spectral** | Resynthesises a sample's spectrum, so time and pitch become independent | Scan (rate/direction), **Cut**/Filter, Mix, Hi/Low freq |

**Tuning modes:** semitone, harmonics, ratio and step.

### Warp modes (2 per oscillator, can be swapped)
Off · **Sync** · **Alt Warp**† (Bend +/−, Mirror, Remap, Quantize…) · **Filter** (filters inside the oscillator) · **Distortion** · **FM** (true FM from another osc/sub/noise) · **PD** (phase distortion) · **AM** · **RM** (ring mod).

These add harmonics and movement before the filter. Hard-sync sweeps, FM growl and PD "honk" usually come from here.

---

## 2. Filters
- **Filter 1 + Filter 2**, in **series or parallel**. Each has Cutoff, Res, **Drive** (with a new Clean mode), **Fat**, Pan, Mix, Level. You can drag the cutoff/resonance point on the display.
- **Filter type menus:** Normal / Multi / Flanges / Misc / **New**.
  - New in Serum 2: Wsp, DJ Mixer, Diffusor, **MG Ladder**, **Acid Ladder**, EMS Ladder, MG Dirty, PZ SVF, Comb 2, Exp MM, Exp BPF.
  - Carried over from Serum 1†: MG Low 6/12/18/24, Low/High/Band/Peak/Notch 12/24, multi-mode combos, Comb/Flange/Phaser, Formant I–III, French/German LP, Allpass, Ramp, etc.
- **Which filter for which job:**
  - Formant → vowel sounds
  - Comb → the evenly spaced resonant peaks we found in the Flume intro (~47 Hz spacing → ~21 ms comb)
  - Acid Ladder → squelch
  - Peak/Band → a single resonant band

---

## 3. Modulation
| Source | Count | Details |
|---|---|---|
| **Envelopes** | **4** (Env 1 is hard-wired to amp) | Atk, Hold, Dec, Sus, Rel, with curve shaping. **BPM** sync option. **Invert legato** (always retrigger) |
| **LFOs** | up to **10** (LFO 7–10 appear once LFO 6 is used) | Drawn shapes + presets. Modes **Free / Retrig / Envelope** (one-shot). Normal or **Chaos** (Lorenz, Rossler). Rate up to **1000 Hz** (audio-rate!), BPM/Hz, Trip/Dot. **Rise, Delay, Smooth, Phase**. Directional playback. Follows swing. Mono option |
| **Macros** | **8** | Each can also be a modulation destination |
| **Velo / Note** | 1 each | Drawable curves for velocity and key tracking |
| **New sources** | — | Any **oscillator or filter output** can be a mod source (audio-rate modulation) |
| **Also available** | — | Mod wheel, pitch wheel, aftertouch, MPE expressions, Active Voices, etc. |

**Mod Matrix:** source → amount → destination, plus an **Aux source** that scales it. Source and aux curves are editable. Rows can be reordered, bypassed and removed, and amounts show live.

**Voicing:** Mono / Poly count, Legato, **Porta** (glide) + curve, Always/Scaled glide.

**Clip sequencer + Arpeggiator:** 12 slots each, key/scale, swing, MIDI out. These are useful for testing patterns without a DAW.

---

## 4. FX rack
Three racks: **Main**, **Bus 1**, **Bus 2**. Modules can be reordered, bypassed and used more than once (e.g. two Distortions).

| Effect | What it's for | Notable controls |
|---|---|---|
| **Bode** (new) | Frequency shifter: inharmonic, metallic, barber-pole movement | Shift, Range, Dir, Width, Delay, Feed, Balance, Blur |
| **Chorus** | Width, thickening | Rate, Delay 1/2, Depth, Feedback, LPF |
| **Compressor** | Glue, pumping, OTT-style squash in multiband mode | Single / **Multiband**, Thresh, Ratio, Attack, Release, Gain |
| **Convolve** (new) | Impulse-response reverb or resonant bodies | Size, Tone, Min-phase, Pre-dly, Attack, Decay, Damp, IR gain |
| **Delay** | Echoes. **HQ** mode is now the default | Normal / Ping-Pong† / Tap†, L/R time (BPM/ms), Feedback, Freq/Q filter |
| **Distortion** | Harmonics: the most-used effect in bass design | Modes: **Tube**, **Overdrive** (new), Soft Clip†, Hard Clip†, Diode 1/2†, Lin Fold†, Sin Fold†, Zero-Square†, Downsample†, Asym†, Rectify†, X-Shaper(+Asym)†, Sine Shaper†, Stomp Box†, Tape Stop†. Pre/Post filter, Freq, Q, Drive, **DC bias** (new: asymmetry → even harmonics) |
| **Equalizer** | Tone shaping | Low/high shelf and peak bands† |
| **Filter** | An extra filter inside the FX chain | Same types as the main filters |
| **Flanger** | Jet / comb sweeps | Rate, Depth, Feedback |
| **Hyper/Dimension** | Super-wide unison-style stereo | Hyper: Rate, Detune, Unison. Dimension: Size† |
| **Phaser** | Notch sweeps | Rate, Depth, Freq, Feedback |
| **Reverb** | Space | Types: Hall†, Plate†, **Vintage**, **Nitrous**, **Basin** (new). Size, Pre-dly, Damp, Width, Lo/Hi cut |
| **Utility** (new) | Housekeeping | Polarity invert L/R, LPF, HPF, **Mono Bass** + freq, Width, Pan |
| **Splitter L/H, L/M/H, M/S** (new) | Process bands or mid/side separately | Crossover freqs, then a chain per band |

---

## 5. Measurement → Serum control (symptom map)
How to read a comparison: **reference** = the song, **mine** = your render. Fix the rows from top to bottom. Pitch and level come first, because nothing else makes sense until they match.

| Analysis shows | Likely cause | Try in Serum 2 |
|---|---|---|
| f0 / note differs | wrong pitch | Osc Oct/Sem/Fin, or the MIDI note. Check the Sub octave |
| Pitch drops/rises at note start in the ref | pitch envelope | Env 2/3 → Osc A/B/C Pitch (or Main Tuning) in the Matrix: short Dec, Sus 0 |
| Smooth slide between notes | glide | Voicing: Mono + Legato, Porta time + curve |
| Ref has more energy in the 2nd/4th harmonics (even) | asymmetric saturation, saw-like source | Distortion **Tube/Asym/Overdrive + DC bias**, or blend in a saw |
| Ref has mostly odd harmonics (3rd, 5th) | symmetric clipping, square/triangle | Distortion **Soft/Hard Clip**, square/triangle wave, Sub square |
| Ref harmonics fall off faster above X Hz | lower cutoff | Filter cutoff ≈ X Hz, MG Low 12/24. Reduce Drive |
| Spectral centroid moves over time in ref, flat in mine | filter/WT movement | Env 2 or LFO → Filter Cutoff or WT Pos. Match the speed to the centroid curve |
| Rhythmic level/brightness wobble at a tempo-synced rate | LFO | LFO (BPM, 1/8, 1/16…) → Cutoff / Level / WT Pos. Retrig mode |
| Attack slower/faster than ref | amp envelope | Env 1 Atk. Check Hold, then Dec/Sus |
| Tail longer/shorter than ref | release / reverb | Env 1 Rel, Reverb Size/Decay, Delay Feedback |
| Evenly spaced resonant peaks in the spectrum | comb filtering | Comb filter (delay ≈ 1/spacing), Flanger with high feedback |
| Inharmonic or metallic peaks | FM, RM, frequency shift | Warp FM/RM, **Bode** |
| Ref is wider in the mids (low L/R correlation) | stereo processing | Unison voices + Detune + Width, Chorus, Hyper/Dimension. Splitter M/S |
| Mine is wide in the sub (corr < 0.9 below 120 Hz) | stereo bass, phase problems | Unison off for the sub, Sub osc, **Utility → Mono Bass** (~120 Hz) |
| Ref is louder overall but with similar peaks (lower crest factor) | compression/limiting | Compressor (Multiband for OTT style), Distortion drive. Match **LUFS**, not peak |
| Noisy upper band in ref, clean in mine | noise layer, grit | Noise osc (band-pass it), Distortion Downsample, Granular |
| Grainy, smeared texture | granular/spectral processing | Granular osc (Dens, Length, Rand) or Spectral osc |
