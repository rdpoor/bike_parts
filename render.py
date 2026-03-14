#!/usr/bin/env python3
"""Render all bike parts to output/."""

import argparse
import logging
from pathlib import Path

from bike_parts.parts import ALL_PARTS


def setup_logging() -> None:
    """Configure root logger and silence noisy third-party loggers."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logging.getLogger("manifold3d").setLevel(logging.WARNING)


def main() -> None:
    """Parse arguments and render selected or all parts."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Render bike parts to .scad and .stl")
    parser.add_argument("--part", help="Render only this part class name")
    parser.add_argument(
        "--output", default="output", help="Output directory (default: output)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    parts = [p for p in ALL_PARTS if args.part is None or p.__name__ == args.part]

    if not parts:
        logging.error(
            "No part named %r found. Available: %s",
            args.part,
            [p.__name__ for p in ALL_PARTS],
        )
        raise SystemExit(1)

    for part_cls in parts:
        part_cls().render(output_dir)


if __name__ == "__main__":
    main()
