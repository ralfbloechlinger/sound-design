# Opening sound-design analysis

Source: https://www.youtube.com/watch?v=ipIUQVpiarE — opening 0–10 seconds.

## Files and method

- `opening_00-10.wav`: 48 kHz, stereo, 24-bit PCM, exactly ten seconds. Reduced by 6.02 dB when converting to integer PCM to preserve decoded peaks without clipping.
- `opening_float.wav`: floating-point decode at the source stream's level. Decoded peaks exceed nominal digital full scale by about 3 dB; this does not establish that the original master was clipped.
- `opening.webm`: extracted YouTube Opus audio. The WAV conversion does not restore information lost in YouTube encoding.
- `sub_band.wav`: 25–120 Hz.
- `bass_body_band.wav`: 120–500 Hz.
- `synth_detail_band.wav`: 500–6,000 Hz.
- `air_band.wav`: 6,000–18,000 Hz.
- `spectrogram.png`, `measurements.json`, `analyze.py`: visual evidence, measurements, and repeatable analysis.

The four band files are independently peak-normalized listening aids, not isolated instruments. Their playback levels do not show the original balance. Filters are offline, sixth-order Butterworth, applied forward and backward; inspect the original for attack timing because these filters can smear transients.

This is a waveform/spectral analysis. I have not performed an auditory evaluation in this session. Patch suggestions below are reconstruction experiments, not identification of Flume's actual instruments, presets, or processing.

## What the evidence shows

**Two different jobs are being done by the opening texture and the later bass.** Between 0.2 and 8.3 seconds, the 25–120 Hz band averages about −45.3 dBFS. Between 8.5 and 10 seconds it averages −11.0 dBFS, an increase of about 34 dB. The late sub's left/right correlation is 0.996: effectively centered. The earlier texture has substantial stereo differences above the sub region.

**The opening texture has a strong resonant midrange.** Several persistent peaks fall near 751, 798, 845, 892, 939, 986, 1,033, 1,126, and 1,173 Hz. Many are spaced about 47 Hz apart. This is compatible with a harmonic source with a missing or suppressed fundamental, a comb resonator, or a repeated short waveform/sample. A 47 Hz comb spacing corresponds to a delay of about 21.3 ms. These possibilities cannot be distinguished from spacing alone. Other peaks coexist, so this is not a clean single-oscillator transcription.

**The texture changes internally.** Early high-frequency vertical bursts extend well above the persistent midrange. High-frequency activity becomes much sparser around 5.5–7 seconds, then returns intermittently. The dominant midrange structure remains. This makes changing excitation, filtering, or edited/resampled articulation useful reconstruction approaches; a single sustained oscillator with fixed EQ would miss that movement.

**The late bass has clear harmonics.** From roughly 8.5 seconds, strong energy lies near 39–44 Hz. Toward the end, peaks near 39, 78, 117, 156, and 195 Hz suggest a harmonic series rooted near 39 Hz, approximately D♯1/E♭1. Treat the note as provisional: the region is short, contains transients, and is not perfectly stationary. The prominent third harmonic supports trying an odd-harmonic-rich source or saturation, but does not prove a specific oscillator shape.

## Practical reconstruction experiments

### Late bass: centered fundamental plus controlled harmonics

1. Start with a mono sine around 39 Hz (D♯1). Use a separate patch from the intro texture.
2. Add soft saturation, or blend in a quiet triangle, to bring out the third harmonic around 117 Hz. Compare the 39/78/117 Hz balance against the original rather than maximizing distortion.
3. Start with a low-pass around 200–350 Hz and little resonance. Adjust by comparison; this is a starting setting, not a measured cutoff.
4. Try a 3–10 ms amplitude attack, 300–700 ms decay, moderate sustain, and 80–200 ms release. These envelope values are suggested audition ranges, not extracted MIDI or envelope measurements.
5. If the entry needs a falling impact, audition a small downward pitch envelope, initially 1–3 semitones over 100–250 ms. Remove it if it makes the result less similar; the analysis does not establish this exact modulation.
6. Keep the sub centered. If more width is needed, process a high-passed harmonic duplicate rather than the fundamental.

### Opening midrange: resonant excitation and resampling

1. Feed a quiet saw/pulse or a short noisy sample into a comb resonator. Begin near 21 ms delay with moderate feedback. Alternatively try a low oscillator near 47 Hz, high-passed so only its upper harmonics remain.
2. Emphasize the broad 750–1,200 Hz region using a band-pass or formant filter. Preserve some lower-mid energy around 200–500 Hz.
3. Add short, irregular amplitude/filter bursts to the excitation. Let the resonator carry a more continuous body underneath.
4. Vary brightness across the phrase, pulling the upper frequencies down in the middle and restoring intermittent bursts later.
5. Add modest stereo differences using slightly different resonator times, a quiet chorus, or short stereo delays. Compare in mono as well.
6. Render a few seconds, crop interesting fragments, and rearrange them. This is a practical way to get articulated variation without requiring one complex real-time patch. It is not evidence that the producer used this exact workflow.

### Brighter accents and space

Use the detail and air band files to examine when upper-frequency bursts occur. Try short filtered-noise or FM plucks above the resonant bed, with separate decay and a quiet stereo ambience return. Spectral bursts alone cannot establish whether these are separate synths, processed sample attacks, or modulation of the same source. Begin with one resonant texture and one bass; add another instrument only if comparison reveals a missing role.

## Most useful comparison order

Match the bass entry and low-frequency level first, then the resonant midrange spacing and emphasis, then articulation and stereo movement. Finally compare brightness over time. Exact synth brands, granular processing, FM, sidechain compression, and reverb algorithms cannot be established from this excerpt's spectral evidence alone.
