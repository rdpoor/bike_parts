#!/usr/bin/env python3
"""
sketch of side panel to attach to lamp escutcheon, for dimension check only

Run:
    uv run python scripts/lamp_side_panel.py [--param val ...] [--outdir dir]
"""
from dataclasses import dataclass

from solid2 import circle, linear_extrude, polygon
from solid2.core.object_base import OpenSCADObject

from pystl import cli
from pystl.library.general_pipe_clamp import GeneralPipeClamp
from pystl.py_stl_base import PyStlPart

@dataclass
class Mumble(PyStlPart):

    def build(self) -> OpenSCADObject:

        clamp = GeneralPipeClamp(
            inner_diameter = 45,
            outer_diameter = 55,
            height = 10,
            tab_width = 10,
            tab_depth = 10,
            bolt_hole_diameter = 4.5,
            split_gap = 2.0).build()

        return clamp

def main() -> None:
    """render LampSidePanel."""
    cli.build_and_render(Mumble)


if __name__ == "__main__":
    main()
