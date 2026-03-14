# bike_parts

Adventures in parameterized 3D printing with [pythonopenscad](https://github.com/owebeeone/pythonopenscad).

Each part is a Python dataclass — tweak a number, re-run, get a new STL. No OpenSCAD editor required.

## One-time setup

Requires Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo>
cd bike_parts
uv sync
```

## Render parts

```bash
# Render all parts to output/
uv run python render.py

# Render a single part
uv run python render.py --part ExampleBracket

# Custom output directory
uv run python render.py --output /tmp/prints
```

Output files land in `output/` (gitignored):

```
output/
  ExampleBracket.scad   ← OpenSCAD source, inspect or tweak in the OpenSCAD GUI
  ExampleBracket.stl    ← ready to slice
```

## Adding a new part

1. Create `src/bike_parts/parts/<name>.py`:

```python
from dataclasses import dataclass
from pythonopenscad import Cube, PoscBase
from bike_parts.base import Part

@dataclass
class MyPart(Part):
    width: float = 30.0

    def build(self) -> PoscBase:
        return Cube([self.width, self.width, self.width])
```

2. Register it in `src/bike_parts/parts/__init__.py`:

```python
from bike_parts.parts.my_part import MyPart

ALL_PARTS: list[type] = [ExampleBracket, MyPart]
```

3. Render and verify:

```bash
uv run python render.py --part MyPart
```

## Viewing parts

Install [OpenSCAD](https://openscad.org/downloads.html) to inspect or tweak the `.scad` source interactively.

**macOS**
```bash
open output/ExampleBracket.scad          # opens in OpenSCAD if associated
# or, explicitly:
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD output/ExampleBracket.scad
```

**Linux**
```bash
openscad output/ExampleBracket.scad
```

**Windows** (PowerShell)
```powershell
& "C:\Program Files\OpenSCAD\openscad.exe" output\ExampleBracket.scad
```

The `.stl` files can be opened directly in any slicer (PrusaSlicer, Bambu Studio, Cura, etc.).

## pythonopenscad API reference

- **GitHub / README:** https://github.com/owebeeone/pythonopenscad
- **Primitives:** `Cube`, `Sphere`, `Cylinder`, `Polyhedron`, …
- **Transforms:** `.translate()`, `.rotate()`, `.scale()`, `.mirror()`, …
- **Boolean ops:** `a + b` (union), `a - b` (difference), `Intersection().extend([a, b])`
- **Output:** `model.write("file.scad")` · `model.renderObj(M3dRenderer()).write_solid_stl("file.stl")`

## Development

```bash
uv run pytest                        # tests
uv run ruff check . && uv run ruff format .   # lint + format
uv run mypy src/                     # type check
```

## Project structure

```
src/bike_parts/
  base.py          — Part base class (build + render)
  parts/
    __init__.py    — ALL_PARTS registry
    example.py     — ExampleBracket (starter part)
render.py          — CLI render script
tests/             — pytest suite
output/            — generated .scad and .stl (gitignored)
```
