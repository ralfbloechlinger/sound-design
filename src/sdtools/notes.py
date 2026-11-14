import numpy as np

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def hz_to_note(hz, a4=440.0):
    """39 -> 'D#1 (-8c)'. Uses C4 = MIDI 60. Cents show how far off the nearest note."""
    midi = 69 + 12 * np.log2(hz / a4)
    n = int(round(midi))
    cents = int(round((midi - n) * 100))
    return f"{NAMES[n % 12]}{n // 12 - 1} ({cents:+d}c)"


def note_to_hz(name, a4=440.0):
    """'D#1' -> 38.89"""
    letter = name.rstrip("-0123456789")
    octave = int(name[len(letter):])
    midi = NAMES.index(letter) + (octave + 1) * 12
    return a4 * 2 ** ((midi - 69) / 12)
