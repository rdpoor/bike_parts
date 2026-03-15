"""Filleted rectangle parts."""

import logging
from dataclasses import dataclass

from solid2 import circle, polygon
from solid2.core.object_base import OpenSCADObject

from bike_parts.base import Part

log = logging.getLogger(__name__)


@dataclass
class FilletedRect2D(Part):
    """A 2D rectangle with filleted corners, centered around the origin.

    Attributes:
        width: width of the rectangle
        height: height of the rectangle
        radius: radius of the 4 fillets
    """

    width: float = 30.0
    height: float = 20.0
    radius: float = 5.0

    def build(self) -> OpenSCADObject:
        """Build the 2D filleted rectangle.

        Returns:
            The SolidPython2 model representing rectangle with filleted corners.
        """
        w2 = self.width/2.0
        h2 = self.height/2.0
        r = self.radius
        fillet = circle(self.radius, _fn=128)
        south_west = fillet.translate([-w2+r, -h2+r, 0])
        south_east = fillet.translate([w2-r, -h2+r, 0])
        north_east = fillet.translate([w2-r, h2-r, 0])
        north_west = fillet.translate([-w2+r, h2-r, 0])
        # body is a rectangle with clipped corners that will be overlaid
        # with the four fillets.
        body = polygon([
            [-w2+r, -h2], [w2-r, -h2], [w2, -h2+r], [w2, h2-r],
            [w2-r, h2], [-w2+r, h2], [-w2, h2-r], [-w2, -h2+r],
            [-w2+r, -h2]
            ])
        return body + south_west + south_east + north_east + north_west


@dataclass
class FilletedRect(FilletedRect2D):
    """A 3D rectangle with filleted corners, extruded to a given depth.

    Attributes:
        depth: extrusion depth along the z-axis
    """

    depth: float = 1.0

    def build(self) -> OpenSCADObject:
        """Build the 3D filleted rectangle by extruding FilletedRect2D.

        Returns:
            The SolidPython2 model representing the extruded filleted rectangle.
        """
        from solid2 import linear_extrude

        return linear_extrude(self.depth)(super().build())

@dataclass
class FilletedFrame(Part):
    """A 3D frame: an outer filleted rect with an inner filleted rect subtracted.

    Attributes:
        outer_width: width of the outer rectangle
        outer_height: height of the outer rectangle
        outer_radius: fillet radius of the outer rectangle
        inner_width: width of the inner cutout rectangle
        inner_height: height of the inner cutout rectangle
        inner_radius: fillet radius of the inner cutout rectangle
        depth: extrusion depth along the z-axis
    """

    outer_width: float = 40.0
    outer_height: float = 30.0
    outer_radius: float = 10.0
    inner_width: float = 30.0
    inner_height: float = 20.0
    inner_radius: float = 5.0
    depth: float = 1.0

    def build(self) -> OpenSCADObject:
        """Build the filleted frame by subtracting an inner from an outer filleted rect.

        Returns:
            The SolidPython2 model representing the extruded filleted frame.
        """
        from solid2 import linear_extrude

        outer_2d = FilletedRect2D(
            width=self.outer_width,
            height=self.outer_height,
            radius=self.outer_radius,
        ).build()
        inner_2d = FilletedRect2D(
            width=self.inner_width,
            height=self.inner_height,
            radius=self.inner_radius,
        ).build()
        return linear_extrude(self.depth)(outer_2d - inner_2d)
