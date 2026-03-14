"""Example bracket part demonstrating the Part pattern."""

import logging
from dataclasses import dataclass

from pythonopenscad import Cube, Cylinder, PoscBase

from bike_parts.base import Part

log = logging.getLogger(__name__)


@dataclass
class ExampleBracket(Part):
    """A simple L-bracket example demonstrating the Part pattern.

    Attributes:
        width: Width of the bracket in mm.
        height: Height of the bracket in mm.
        depth: Depth (thickness) of the bracket in mm.
        hole_diameter: Diameter of the mounting hole in mm.
    """

    width: float = 20.0
    height: float = 30.0
    depth: float = 5.0
    hole_diameter: float = 4.0

    def build(self) -> PoscBase:
        """Build the bracket model.

        Returns:
            The pythonopenscad model representing the bracket with a mounting hole.
        """
        body = Cube([self.width, self.depth, self.height])
        hole = Cylinder(h=self.depth + 1, r=self.hole_diameter / 2, _fn=32)
        hole = hole.translate([self.width / 2, -0.5, self.height / 2])
        return body - hole
