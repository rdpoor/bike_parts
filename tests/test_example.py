"""Tests for the ExampleBracket part."""

from pathlib import Path

from pythonopenscad import PoscBase

from bike_parts.parts.example import ExampleBracket


def test_build_returns_poscbase() -> None:
    """build() with default params returns a PoscBase instance."""
    part = ExampleBracket()
    result = part.build()
    assert isinstance(result, PoscBase)


def test_build_custom_params() -> None:
    """build() with custom params returns a PoscBase instance."""
    part = ExampleBracket(width=40.0, height=50.0, depth=8.0, hole_diameter=6.0)
    result = part.build()
    assert isinstance(result, PoscBase)


def test_render_writes_files(tmp_path: Path) -> None:
    """render() writes both .scad and .stl files."""
    part = ExampleBracket()
    part.render(tmp_path)

    scad_file = tmp_path / "ExampleBracket.scad"
    stl_file = tmp_path / "ExampleBracket.stl"

    assert scad_file.exists(), f"{scad_file} was not created"
    assert stl_file.exists(), f"{stl_file} was not created"
    assert scad_file.stat().st_size > 0, "SCAD file is empty"
    assert stl_file.stat().st_size > 0, "STL file is empty"
