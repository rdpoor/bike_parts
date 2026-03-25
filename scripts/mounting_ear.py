#!/usr/bin/env python3
"""
sketch of side panel to attach to lamp escutcheon, for dimension check only

Run:
    uv run python scripts/lamp_side_panel.py [--param val ...] [--outdir dir]
"""
import math
import numpy as np
from dataclasses import dataclass

from solid2 import circle, linear_extrude, polygon
from solid2.core.object_base import OpenSCADObject

from pystl import cli
from pystl.py_stl_base import PyStlPart

def slotted_arc(x_org, y_org, start_deg, end_deg, radius, slot_width, fn=128):
    """
    Create a 2D slotted arc.
    Arguments:
        x_org: x origin of the arc
        y_org: y origin of the arc
        start_deg: starting angle of arc (in degrees [0..360])
        end_deg: ending angle of arc (in degrees [0..360])
        radius: distance from origin to center of the arc's slot
        slot_width: width of the slot
        fn: number of polygon steps to create the arc
    """
    def _dtor(degree):
        return degree * math.pi / 180.0

    k = max(3, fn)

    # Create linearly spaced angles from start to end (inclusive)
    thetas = [_dtor(degree) for degree in np.linspace(start_deg, end_deg, k)]

    r0 = radius - slot_width / 2.0
    r1 = radius + slot_width / 2.0

    inner = [[x_org + r0 * math.cos(theta), y_org + r0 * math.sin(theta)] for theta in thetas]
    outer = [[x_org + r1 * math.cos(theta), y_org + r1 * math.sin(theta)] for theta in reversed(thetas)]

    # drop a circle at either end of the arc to make a rounded slot
    end_cap = circle(r=slot_width/2, _fn=fn)
    e0 = end_cap.translate([
        x_org + radius * math.cos(thetas[0]),
        y_org + radius * math.sin(thetas[0]),
        0])
    e1 = end_cap.translate([
        x_org + radius * math.cos(thetas[-1]),
        y_org + radius * math.sin(thetas[-1]),
        0])
    return polygon(inner + outer) + e0 + e1

@dataclass
class MountingEar(PyStlPart):
    """Create part to union with lamp escutcheon for dimention check only.
    """

    def build(self) -> OpenSCADObject:

        lamp_bolt_diameter = 4.5
        lamp_bolt_spacing = 50
        lamp_bolt_hole = circle(
            r=lamp_bolt_diameter / 2,
            _fn=128, 
        )
        left_lamp_bolt = lamp_bolt_hole.translate([lamp_bolt_spacing/2, 6, 0])
        right_lamp_bolt = lamp_bolt_hole.translate([-lamp_bolt_spacing/2, 6, 0])
        plate = polygon(
            [
                [-66/2, 0],
                [-66/2, 30],
                [-(66/2)+11, 41],
                [(66/2)-11, 41],
                [66/2, 30],
                [66/2, 0],
                [-66/2, 0]
            ],
        )
        mounting_bolt_diameter = 5.5
        mounting_bolt_hole = circle(
            r=mounting_bolt_diameter / 2,
            _fn=128,
        )
        left_mounting_bolt = mounting_bolt_hole.translate([-18, 30, 0])
        right_mounting_slot = slotted_arc(0, 0, -10, +10, 30, mounting_bolt_diameter, fn=128).translate([-18, 30, 0])
        ear = (plate) - (left_lamp_bolt + right_lamp_bolt + left_mounting_bolt + right_mounting_slot)
        return ear.linear_extrude(2.0)

def main() -> None:
    """render LampSidePanel."""
    cli.build_and_render(MountingEar)


if __name__ == "__main__":
    main()
