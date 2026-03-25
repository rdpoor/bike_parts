#!/usr/bin/env python3
"""
sketch of side panel to attach to lamp escutcheon, for dimension check only

Run:
    uv run python scripts/test.py
"""
import math
from solid2 import circle, linear_extrude, polygon
from solid2.core.object_base import OpenSCADObject
from pystl.utils import write_model, setup_logging

s = 7
p = s * 2/math.sqrt(3)

hex_insert2d = circle(r=p, _fn=6)
hex_insert = hex_insert2d.linear_extrude(1)

def main() -> None:
    """render LampSidePanel."""
    write_model(hex_insert, 'output/test')

if __name__ == "__main__":
    setup_logging()
    main()

