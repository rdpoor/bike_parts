"""Base class and render utilities for bike parts."""

import logging
from dataclasses import dataclass
from pathlib import Path

from pythonopenscad import PoscBase
from pythonopenscad.m3dapi import M3dRenderer

log = logging.getLogger(__name__)


@dataclass
class Part:
    """Base class for all bike parts. Subclass and implement build()."""

    def build(self) -> PoscBase:
        """Build and return the OpenSCAD model for this part.

        Returns:
            The pythonopenscad model object.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError

    def render(self, output_dir: Path) -> None:
        """Render this part to .scad and .stl in output_dir.

        Args:
            output_dir: Directory where output files will be written.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        name = type(self).__name__
        model = self.build()

        scad_path = output_dir / f"{name}.scad"
        model.write(str(scad_path))
        log.info("Wrote %s", scad_path)

        stl_path = output_dir / f"{name}.stl"
        result = model.renderObj(M3dRenderer())
        result.write_solid_stl(str(stl_path))
        log.info("Wrote %s", stl_path)
