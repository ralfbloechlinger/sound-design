"""Create a new song folder with the standard layout.

    pixi run new-song <artist-title-slug>
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

README = """# {slug}

Source: <url>

## Listening first (before any code)
- What are the main sound roles? (sub, bass, lead, pad, texture, drums, fx)
- What moves over time? (filter, pitch, volume, width)
- What would I reach for to make this?

## Findings
| Time | Element | Evidence (plot / number) | Reconstruction idea |
|---|---|---|---|

## Reconstruction log
What I tried in the synth, and how close it got.
"""


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    song = ROOT / "songs" / slug
    if song.exists():
        sys.exit(f"{song} already exists")
    for sub in ["audio", "renders", "figures", "data", "scripts"]:
        (song / sub).mkdir(parents=True)
    (song / "README.md").write_text(README.format(slug=slug))
    print(f"Created {song}\nNext: pixi run fetch <url> {slug}")


if __name__ == "__main__":
    main()
