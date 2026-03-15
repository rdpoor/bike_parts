#!/usr/bin/env python3
"""Render the FilletedRect part."""

import argparse
from pathlib import Path

from bike_parts.cli import add_output_arg, add_part_args, build_part, setup_logging
from bike_parts.parts import FilletedRect


def main() -> None:
    """Parse arguments and render FilletedRect."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Render FilletedRect to .scad")
    add_output_arg(parser)
    add_part_args(parser, FilletedRect)
    args = parser.parse_args()
    build_part(FilletedRect, args).render(Path(args.output))


if __name__ == "__main__":
    main()
