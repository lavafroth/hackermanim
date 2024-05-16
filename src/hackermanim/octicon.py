from manim import SVGMobject
from pathlib import Path

def octicon(name: str, *args, **kwargs) -> SVGMobject:
    here = Path.cwd()
    for x in range(3):
        octicons_dir = here / 'octicons'
        if octicons_dir.exists():
            return SVGMobject(octicons_dir / 'icons' / name, *args, **kwargs)
        here = here.parent
    raise FileNotFoundError
