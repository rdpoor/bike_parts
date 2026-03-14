"""Tests for GeneralPipeClamp and its split variants."""

import pytest
from solid2.core.object_base import OpenSCADObject

from bike_parts.parts.general_pipe_clamp import (
    GeneralPipeClamp,
    GeneralPipeClampBottom,
    GeneralPipeClampTop,
)


def test_build_defaults() -> None:
    """build() with default params returns an OpenSCADObject."""
    result = GeneralPipeClamp().build()
    assert isinstance(result, OpenSCADObject)


def test_build_custom_params() -> None:
    """build() with overridden params returns an OpenSCADObject."""
    result = GeneralPipeClamp(inner_diameter=25.0, tab_depth=12.0).build()
    assert isinstance(result, OpenSCADObject)


def test_top_bottom_inherit_params() -> None:
    """Top and Bottom pass through overridden params (e.g. inner_diameter=35)."""
    top = GeneralPipeClampTop(inner_diameter=35.0)
    bottom = GeneralPipeClampBottom(inner_diameter=35.0)

    top_scad = top.build().as_scad()
    bottom_scad = bottom.build().as_scad()

    # inner_diameter=35 → radius=17.5 in the cylinder call
    assert "17.5" in top_scad, f"Expected '17.5' (r=35/2) in top SCAD:\n{top_scad}"
    assert "17.5" in bottom_scad, f"Expected '17.5' (r=35/2) in bottom SCAD:\n{bottom_scad}"


def test_render_writes_scad(tmp_path: pytest.TempPathFactory) -> None:
    """render() produces a .scad file in the output directory."""
    part = GeneralPipeClamp()
    part.render(tmp_path)
    scad_files = list(tmp_path.glob("*.scad"))
    assert scad_files, f"No .scad files found in {tmp_path}"
