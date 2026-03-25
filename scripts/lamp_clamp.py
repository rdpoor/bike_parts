"""General pipe clamp v1.0"""

import math
from solid2 import cube, cylinder
from solid2.core.object_base import OpenSCADObject
from pystl.utils import write_model, setup_logging


def build_lamp_clamp(
    inner_diameter: float = 45,
    outer_diameter: float = 55,
    height: float = 10,
    left_tab_length: float = 24,
    left_tab_width: float = 17,
    right_tab_length: float = 10,
    right_tab_width: float = 17,
    bolt_hole_diameter: float = 4.3,
    split_gap: float = 3.0
) -> OpenSCADObject:
    """Clamps to attach headlamp to front fork.

    Attributes:
        inner_diameter: diameter of the pipe
        outer_diameter: diameter of the finished clamp
        height: height of the clamp
        left_tab_length: length of front mounting tab extending beyond
            outer_diameter
        left_tab_width: width of the front mounting tab
        right_tab_length: length of rear mounting tab extending beyond
            outer_diameter
        right_tab_width: width of the rear mounting tab
        bolt_hole_diameter: diameter of the bolt hole through the tabs
        split_gap: distance bewween left and right halves
    """
    r = outer_diameter / 2  # radius of outer diameter
    outer = cylinder(h=height, r=r, center=True, _fn=128)
    inner = cylinder(
        h=height + 1, r=inner_diameter / 2, center=True, _fn=128
    )

    # create a rectangular prism for the mounting tab.
    # it has an end cap of radius height/2, so we shorten the length by that
    # amount, shift x to the left
    left_tab = cube(
        [left_tab_length - height / 2, left_tab_width, height], center=True
    )
    x1 = math.sqrt(r ** 2 - (left_tab_width / 2) ** 2)
    x2 = x1 + (left_tab_length - height / 2) / 2
    x3 = x1 + left_tab_length - height / 2
    left_tab = left_tab.translate([-x2, 0, 0])
    left_end_cap = cylinder(
        h=left_tab_width, r=height / 2, center=True, _fn=32
    )
    left_end_cap = left_end_cap.rotate(90, 0, 0)
    left_end_cap = left_end_cap.translate([-x3, 0, 0])

    left_bolt_hole = cylinder(
        h=left_tab_width + 1, r=bolt_hole_diameter / 2, _fn=128, center=True
    )
    left_bolt_hole = left_bolt_hole.rotate(90, 0, 0)
    left_bolt_hole = left_bolt_hole.translate([-x3, 0, 0])

    # create a rectangular prism for the mounting tab, shift x to the right
    right_tab = cube(
        [right_tab_length - height / 2, right_tab_width, height], center=True
    )
    x1 = math.sqrt(r ** 2 - (right_tab_width / 2) ** 2)
    x2 = x1 + (right_tab_length - height / 2) / 2
    x3 = x1 + right_tab_length - height / 2
    right_tab = right_tab.translate([x2, 0, 0])
    right_end_cap = cylinder(
        h=right_tab_width, r=height / 2, center=True, _fn=32
    )
    right_end_cap = right_end_cap.rotate(90, 0, 0)
    right_end_cap = right_end_cap.translate([x3, 0, 0])

    right_bolt_hole = cylinder(
        h=right_tab_width + 1, r=bolt_hole_diameter / 2, _fn=128, center=True
    )
    right_bolt_hole = right_bolt_hole.rotate(90, 0, 0)
    right_bolt_hole = right_bolt_hole.translate([x3, 0, 0])

    # create a thin rectagular prism to split the entire assembly
    split_plane = cube(
        [
            outer_diameter + 2 * max(left_tab_length, right_tab_length),
            split_gap,
            height + 1,
        ],
        center=True,
    )
    model = (
        (outer + left_tab + left_end_cap + right_tab + right_end_cap)
        - (inner + split_plane + left_bolt_hole + right_bolt_hole)
    )

    return model


def main() -> None:
    """render LampSidePanel."""
    lamp_clamp = build_lamp_clamp()
    write_model(lamp_clamp, "output/lamp_clamp_01")


if __name__ == "__main__":
    setup_logging()
    main()
