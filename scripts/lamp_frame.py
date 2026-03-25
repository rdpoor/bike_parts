#!/usr/bin/env python3
"""
Create an escutcheon by merging a FilletedFrame as a faceplate and another
FilletedFrame as the sidewalls.

Run:
    uv run python scripts/filleted_escutcheon.py [--param val ...] [--outdir dir]
"""

from dataclasses import dataclass
import numpy as np
import math

from solid2 import circle, linear_extrude, polygon
from solid2.core.object_base import OpenSCADObject

from pystl import cli
from pystl.library.filleted_rect import FilletedFrame
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

def build_mounting_ear(ear_thickness: float = 3.0) -> OpenSCADObject:

    lamp_bolt_diameter = 4.3
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
    mounting_bolt_diameter = 5.3
    mounting_bolt_hole = circle(
        r=mounting_bolt_diameter / 2,
        _fn=128,
    )
    left_mounting_bolt = mounting_bolt_hole.translate([-15, 30, 0])
    right_mounting_slot = slotted_arc(0, 0, -10, +10, 30, mounting_bolt_diameter, fn=128)
    right_mounting_slot = right_mounting_slot.translate([-15, 30, 0])
    ear = (plate) - (left_lamp_bolt + right_lamp_bolt + left_mounting_bolt + right_mounting_slot)
    return ear.linear_extrude(ear_thickness)

@dataclass
class LampFrame01(PyStlPart):
    """
    Assemble a frame for the e-moto headlamp, comprising:
    - faceplate - a filleted escutcheon that's frontmost
    - sidewalls - a deep filleted escutcheon that surrounds the lamp assembly
    - mounting_earS - a polygon with holes to hold the captive side panels

    Attributes:
        lamp_width: width of the lamp housing
        lamp_height: height of the housing
        lamp_radius: fillet radius of the lamp housing corner
        cutout_width: width of the faceplate cutout rectangle
        cutout_height: height of the faceplate cutout rectangle
        cutout_radius: fillet radius of the faceplate cutout rectangle
        faceplate_thickness: thickness of the faceplate
        sidewall_thickness: thickness of the sidewall
        sidewall_depth: depth of the sidewall
    """

    lamp_width: float = 169.16 + 1
    lamp_height: float = 107.5 + 1
    lamp_radius: float = 16.5
    cutout_width: float = 160.5
    cutout_height: float = 100.5

    def build(self) -> OpenSCADObject:
        faceplate_outer_width = self.lamp_width + 2 * self.sidewall_thickness
        faceplate_outer_height = self.lamp_height + 2 * self.sidewall_thickness
        faceplate_outer_radius = self.lamp_radius + self.sidewall_thickness

        faceplate = FilletedFrame(
            outer_width=faceplate_outer_width,
            outer_height=faceplate_outer_height,
            outer_radius=faceplate_outer_radius,
            inner_width=self.cutout_width,
            inner_height=self.cutout_height,
            inner_radius=self.cutout_radius,
            depth=self.faceplate_thickness,
        ).build()

        sidewalls = FilletedFrame(
            outer_width=faceplate_outer_width,
            outer_height=faceplate_outer_height,
            outer_radius=faceplate_outer_radius,
            inner_width=self.lamp_width,
            inner_height=self.lamp_height,
            inner_radius=self.lamp_radius,
            depth=self.sidewall_depth,
        ).build()

        # bolt_diameter = 4.5
        # bolt_spacing = 45.7+4.5

        # bolt_hole = circle(
        #     r=bolt_diameter / 2,
        #     _fn=128,
        # )
        # left_bolt = bolt_hole.translate([bolt_spacing/2, 6.5, 0])
        # right_bolt = bolt_hole.translate([-bolt_spacing/2, 6.5, 0])
        # mounting_ear = polygon(
        #     [
        #         [-66/2, 0],
        #         [-66/2, 12],
        #         [-(66/2)+24, 36],
        #         [(66/2)-24, 36],
        #         [66/2, 12],
        #         [66/2, 0],
        #         [-66/2, 0]
        #     ],
        # )
        # # add bolt holes, extrude 2D -> 3D, rotate into correct orientation
        # mounting_ear = mounting_ear - (left_bolt + right_bolt)
        # mounting_ear = mounting_ear.linear_extrude(
        #     height=self.sidewall_thickness,
        #     center=True)
        mounting_ear = build_mounting_ear(self.sidewall_thickness)
        mounting_ear = mounting_ear.rotate(90, 00, 90)
        # translate to form left and right mounting ears
        left_mounting_ear = mounting_ear.translate([
            -self.lamp_width/2 - self.sidewall_thickness,
            0,
            self.sidewall_depth])
        right_mounting_ear = mounting_ear.translate([
            self.lamp_width/2,
            0,
            self.sidewall_depth])
        return faceplate + sidewalls + left_mounting_ear + right_mounting_ear


def main() -> None:
    """Parse arguments and render LampFrame."""
    cli.build_and_render(LampFrame01)


if __name__ == "__main__":
    main()
