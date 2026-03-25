"""Geometry utilities for pystl models."""

import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from solid2.core.object_base import OpenSCADObject

log = logging.getLogger(__name__)

def setup_logging() -> None:
    """Configure root logger at INFO level with a simple format."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def write_model(model: OpenSCADObject, model_name: Path):
    """
    Write a model to <model_name>.scad, and if `openscad` is available,
    write the model to <model_name>.stl
    """
    path = Path(model_name)
    output_dir = path.parent
    if output_dir != path:
        output_dir.mkdir(parents=True, exist_ok=True)

    scad_path = path.with_suffix('.scad')
    model.save_as_scad(str(scad_path))
    log.info(f"Wrote {scad_path}")

    if shutil.which("openscad") is not None:
        stl_path = path.with_suffix('.stl')
        subprocess.run(
            ["openscad", "-o", str(stl_path), str(scad_path)],
            check=True,
        )
        log.info(f"Wrote {stl_path}")
    else:
        log.warning("openscad not found in PATH; skipping STL export for %s", model_name)

