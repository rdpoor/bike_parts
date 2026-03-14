# bike_parts

Adventures in parameterized 3D printing with [SolidPython2](https://github.com/jeff-dh/SolidPython) (the actively maintained V2 fork).

Each part is a Python dataclass — tweak a number, re-run, get a new STL. No OpenSCAD editor required.

## One-time setup

Requires Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo>
cd bike_parts
uv sync
```

STL export requires the [OpenSCAD](https://openscad.org/downloads.html) CLI to be in `PATH`. Without it, `render.py` writes `.scad` files only and logs a warning.

## Render parts

```bash
# Render all parts to output/
uv run python render.py

# Render a single part
uv run python render.py --part ExampleBracket

# Override parameters on the command line
uv run python render.py --part GeneralPipeClamp --inner_diameter=25 --tab_depth=12

# See all available parameters for a part
uv run python render.py --part GeneralPipeClamp --help

# Custom output directory
uv run python render.py --output /tmp/prints
```

When `--part` is given, every dataclass field on that part becomes a CLI flag. Omitted flags use the class defaults.

Output files land in `output/` (gitignored):

```
output/
  ExampleBracket.scad   ← OpenSCAD source, inspect or tweak in the OpenSCAD GUI
  ExampleBracket.stl    ← ready to slice (requires openscad in PATH)
```

## Adding a new part

1. Create `src/bike_parts/parts/<name>.py`:

```python
from dataclasses import dataclass
from solid2 import cube
from solid2.core.object_base import OpenSCADObject
from bike_parts.base import Part

@dataclass
class MyPart(Part):
    width: float = 30.0

    def build(self) -> OpenSCADObject:
        return cube([self.width, self.width, self.width])
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

Install [OpenSCAD](https://openscad.org/downloads.html) to inspect or tweak the `.scad` source interactively, and to enable STL export.

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

## SolidPython2 API reference

- **GitHub / docs:** https://github.com/jeff-dh/SolidPython
- **Primitives:** `cube`, `sphere`, `cylinder`, `polyhedron`, …
- **Transforms:** `.translate()`, `.rotate()`, `.scale()`, `.mirror()`, …
- **Boolean ops:** `a + b` (union), `a - b` (difference), `a * b` (intersection)
- **Output:** `model.save_as_scad("file.scad")` · STL via `openscad -o file.stl file.scad`

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
    __init__.py            — ALL_PARTS registry
    example.py             — ExampleBracket (starter part)
    general_pipe_clamp.py  — GeneralPipeClamp + Top/Bottom split variants
render.py          — CLI render script (auto-exposes dataclass fields as flags)
tests/             — pytest suite
output/            — generated .scad and .stl (gitignored)
```
