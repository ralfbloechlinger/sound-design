"""Download a song's audio and decode a float WAV for analysis.

    pixi run fetch <url> <song-slug> [start_sec] [end_sec]

Writes songs/<slug>/audio/source.<ext> and songs/<slug>/audio/source_float.wav
(48 kHz, 32-bit float — float keeps peaks above 0 dBFS instead of clipping them).
Only analyse material you have the right to use; audio/ is git-ignored.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    url, slug = sys.argv[1], sys.argv[2]
    start = sys.argv[3] if len(sys.argv) > 3 else None
    end = sys.argv[4] if len(sys.argv) > 4 else None

    audio = ROOT / "songs" / slug / "audio"
    audio.mkdir(parents=True, exist_ok=True)

    subprocess.run(["yt-dlp", "-f", "bestaudio", "-o", str(audio / "source.%(ext)s"), url], check=True)
    src = next(p for p in audio.glob("source.*") if p.suffix != ".wav")

    cmd = ["ffmpeg", "-y", "-i", str(src)]
    if start:
        cmd += ["-ss", start]
    if end:
        cmd += ["-to", end]
    cmd += ["-ar", "48000", "-c:a", "pcm_f32le", str(audio / "source_float.wav")]
    subprocess.run(cmd, check=True)
    print(f"\nReady: {audio / 'source_float.wav'}")


if __name__ == "__main__":
    main()
