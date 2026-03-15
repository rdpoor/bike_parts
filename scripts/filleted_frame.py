#!/usr/bin/env python3
"""Render the FilletedFrame part."""

import argparse
from pathlib import Path

from bike_parts.cli import add_output_arg, add_part_args, build_part, setup_logging
from bike_parts.parts import FilletedFrame


def main() -> None:
    """Parse arguments and render FilletedFrame."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Render FilletedFrame to .scad")
    add_output_arg(parser)
    add_part_args(parser, FilletedFrame)
    args = parser.parse_args()
    build_part(FilletedFrame, args).render(Path(args.output))


if __name__ == "__main__":
    main()
