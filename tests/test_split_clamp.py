"""Tests for pipe clamp and split pipe clamp parts."""

import shutil
from pathlib import Path

import pytest
from solid2.core.object_base import OpenSCADObject

from bike_parts.parts.example_split_clamp import (
    PipeClamp,
    SplitPipeClampBottom,
    SplitPipeClampTop,
)


def test_pipe_clamp_build_defaults() -> None:
    assert isinstance(PipeClamp().build(), OpenSCADObject)


def test_pipe_clamp_build_custom() -> None:
    assert isinstance(
        PipeClamp(pipe_diameter=32.0, thickness=6.0, width=25.0).build(), OpenSCADObject
    )


def test_split_clamp_top_build() -> None:
    assert isinstance(SplitPipeClampTop().build(), OpenSCADObject)


def test_split_clamp_bottom_build() -> None:
    assert isinstance(SplitPipeClampBottom().build(), OpenSCADObject)


def test_pipe_clamp_render_scad(tmp_path: Path) -> None:
    PipeClamp().render(tmp_path)
    assert (tmp_path / "PipeClamp.scad").exists()


def test_split_clamp_top_render_scad(tmp_path: Path) -> None:
    SplitPipeClampTop().render(tmp_path)
    assert (tmp_path / "SplitPipeClampTop.scad").exists()


def test_split_clamp_bottom_render_scad(tmp_path: Path) -> None:
    SplitPipeClampBottom().render(tmp_path)
    assert (tmp_path / "SplitPipeClampBottom.scad").exists()


@pytest.mark.skipif(shutil.which("openscad") is None, reason="openscad not in PATH")
def test_pipe_clamp_render_stl(tmp_path: Path) -> None:
    PipeClamp().render(tmp_path)
    assert (tmp_path / "PipeClamp.stl").exists()


@pytest.mark.skipif(shutil.which("openscad") is None, reason="openscad not in PATH")
def test_split_clamp_top_render_stl(tmp_path: Path) -> None:
    SplitPipeClampTop().render(tmp_path)
    assert (tmp_path / "SplitPipeClampTop.stl").exists()


@pytest.mark.skipif(shutil.which("openscad") is None, reason="openscad not in PATH")
def test_split_clamp_bottom_render_stl(tmp_path: Path) -> None:
    SplitPipeClampBottom().render(tmp_path)
    assert (tmp_path / "SplitPipeClampBottom.stl").exists()
