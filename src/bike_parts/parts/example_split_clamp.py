"""Pipe clamp and split pipe clamp parts."""

import logging
from dataclasses import dataclass

from pythonopenscad import Cube, Cylinder, Intersection, PoscBase

from bike_parts.base import Part

log = logging.getLogger(__name__)


def _build_clamp_body(
    pipe_diameter: float,
    thickness: float,
    width: float,
    bolt_diameter: float,
    tab_inset: float,
    clearance: float,
) -> PoscBase:
    """Build the pipe clamp body shared by all clamp variants.

    Args:
        pipe_diameter: Outer diameter of the pipe in mm.
        thickness: Wall thickness of the clamp in mm.
        width: Width (length along pipe axis) in mm.
        bolt_diameter: Diameter of the mounting bolt hole in mm.
        tab_inset: How far to inset the mounting tab from the pipe edge in mm.
        clearance: Extra diametric clearance around the pipe in mm.

    Returns:
        The clamp body as a pythonopenscad model.
    """
    effective_pipe_radius = (pipe_diameter + clearance) / 2
    outer_radius = effective_pipe_radius + thickness

    outer = Cylinder(r=outer_radius, h=width)
    inner = Cylinder(r=effective_pipe_radius, h=width)
    clamp_body = outer - inner

    tab_length = outer_radius * 2
    tab_width = thickness * 2
    tab = Cube([tab_length, tab_width, width])

    tab_x = -outer_radius
    tab_y = -tab_width / 2 + tab_inset
    tab = tab.translate([tab_x, tab_y, 0])

    clamp = clamp_body + tab

    bolt_radius = bolt_diameter / 2
    bolt_hole = Cylinder(r=bolt_radius, h=width)

    bolt_y = tab_y + tab_width / 2
    bolt_hole = bolt_hole.translate([0, bolt_y, 0])

    return clamp - bolt_hole


def _make_cutter(pipe_diameter: float, thickness: float, width: float) -> PoscBase:
    """Build the box used to split the clamp into top and bottom halves.

    Args:
        pipe_diameter: Outer diameter of the pipe in mm.
        thickness: Wall thickness of the clamp in mm.
        width: Width (length along pipe axis) in mm.

    Returns:
        The cutter box as a pythonopenscad model.
    """
    cutter = Cube([pipe_diameter * 3, thickness * 3, width * 2])
    return cutter.translate([-pipe_diameter * 1.5, -thickness * 1.5, -width / 2])


@dataclass
class PipeClamp(Part):
    """A parametric pipe clamp with a mounting tab and bolt hole.

    Attributes:
        pipe_diameter: Outer diameter of the pipe in mm.
        thickness: Wall thickness of the clamp in mm.
        width: Width (length along pipe axis) of the clamp in mm.
        bolt_diameter: Diameter of the mounting bolt hole in mm.
        tab_inset: How far to inset the mounting tab from the pipe edge in mm.
        clearance: Extra diametric clearance around the pipe for easy fit in mm.
    """

    pipe_diameter: float = 25.0
    thickness: float = 5.0
    width: float = 20.0
    bolt_diameter: float = 4.0
    tab_inset: float = 0.0
    clearance: float = 0.2

    def build(self) -> PoscBase:
        """Build the full pipe clamp model.

        Returns:
            The full pipe clamp as a pythonopenscad model.
        """
        return _build_clamp_body(
            self.pipe_diameter,
            self.thickness,
            self.width,
            self.bolt_diameter,
            self.tab_inset,
            self.clearance,
        )


@dataclass
class SplitPipeClampTop(Part):
    """Top half of a split pipe clamp (the arc half, away from the mounting tab).

    Attributes:
        pipe_diameter: Outer diameter of the pipe in mm.
        thickness: Wall thickness of the clamp in mm.
        width: Width (length along pipe axis) of the clamp in mm.
        bolt_diameter: Diameter of the mounting bolt hole in mm.
        tab_inset: How far to inset the mounting tab from the pipe edge in mm.
        clearance: Extra diametric clearance around the pipe for easy fit in mm.
    """

    pipe_diameter: float = 25.0
    thickness: float = 5.0
    width: float = 20.0
    bolt_diameter: float = 4.0
    tab_inset: float = 0.0
    clearance: float = 0.2

    def build(self) -> PoscBase:
        """Build the top half of the split clamp.

        Returns:
            The top half of the split pipe clamp.
        """
        clamp = _build_clamp_body(
            self.pipe_diameter,
            self.thickness,
            self.width,
            self.bolt_diameter,
            self.tab_inset,
            self.clearance,
        )
        cutter = _make_cutter(self.pipe_diameter, self.thickness, self.width)
        return clamp - cutter


@dataclass
class SplitPipeClampBottom(Part):
    """Bottom half of a split pipe clamp (the tab half).

    Attributes:
        pipe_diameter: Outer diameter of the pipe in mm.
        thickness: Wall thickness of the clamp in mm.
        width: Width (length along pipe axis) of the clamp in mm.
        bolt_diameter: Diameter of the mounting bolt hole in mm.
        tab_inset: How far to inset the mounting tab from the pipe edge in mm.
        clearance: Extra diametric clearance around the pipe for easy fit in mm.
    """

    pipe_diameter: float = 25.0
    thickness: float = 5.0
    width: float = 20.0
    bolt_diameter: float = 4.0
    tab_inset: float = 0.0
    clearance: float = 0.2

    def build(self) -> PoscBase:
        """Build the bottom half of the split clamp.

        Returns:
            The bottom half of the split pipe clamp (intersection with cutter).
        """
        clamp = _build_clamp_body(
            self.pipe_diameter,
            self.thickness,
            self.width,
            self.bolt_diameter,
            self.tab_inset,
            self.clearance,
        )
        cutter = _make_cutter(self.pipe_diameter, self.thickness, self.width)
        result = Intersection()
        result.extend([clamp, cutter])
        return result
