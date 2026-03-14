"""Tests for pipe clamp and split pipe clamp parts."""

from pathlib import Path

from pythonopenscad import PoscBase

from bike_parts.parts.example_split_clamp import (
    PipeClamp,
    SplitPipeClampBottom,
    SplitPipeClampTop,
)


def test_pipe_clamp_build_defaults() -> None:
    assert isinstance(PipeClamp().build(), PoscBase)


def test_pipe_clamp_build_custom() -> None:
    assert isinstance(
        PipeClamp(pipe_diameter=32.0, thickness=6.0, width=25.0).build(), PoscBase
    )


def test_split_clamp_top_build() -> None:
    assert isinstance(SplitPipeClampTop().build(), PoscBase)


def test_split_clamp_bottom_build() -> None:
    assert isinstance(SplitPipeClampBottom().build(), PoscBase)


def test_pipe_clamp_render(tmp_path: Path) -> None:
    PipeClamp().render(tmp_path)
    assert (tmp_path / "PipeClamp.scad").exists()
    assert (tmp_path / "PipeClamp.stl").exists()


def test_split_clamp_top_render(tmp_path: Path) -> None:
    SplitPipeClampTop().render(tmp_path)
    assert (tmp_path / "SplitPipeClampTop.scad").exists()
    assert (tmp_path / "SplitPipeClampTop.stl").exists()


def test_split_clamp_bottom_render(tmp_path: Path) -> None:
    SplitPipeClampBottom().render(tmp_path)
    assert (tmp_path / "SplitPipeClampBottom.scad").exists()
    assert (tmp_path / "SplitPipeClampBottom.stl").exists()
