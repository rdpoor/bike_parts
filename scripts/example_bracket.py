#!/usr/bin/env python3
"""Render the ExampleBracket part."""

import argparse
from pathlib import Path

from bike_parts.cli import add_output_arg, add_part_args, build_part, setup_logging
from bike_parts.parts import ExampleBracket


def main() -> None:
    """Parse arguments and render ExampleBracket."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Render ExampleBracket to .scad")
    add_output_arg(parser)
    add_part_args(parser, ExampleBracket)
    args = parser.parse_args()
    build_part(ExampleBracket, args).render(Path(args.output))


if __name__ == "__main__":
    main()
