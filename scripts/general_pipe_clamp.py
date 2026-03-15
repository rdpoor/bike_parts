#!/usr/bin/env python3
"""Render GeneralPipeClamp variants (full, top, bottom)."""

import argparse
from pathlib import Path

from bike_parts.cli import add_output_arg, add_part_args, build_part, setup_logging
from bike_parts.parts import (
    GeneralPipeClamp,
    GeneralPipeClampBottom,
    GeneralPipeClampTop,
)

VARIANTS: dict[str, type[GeneralPipeClamp]] = {
    "full": GeneralPipeClamp,
    "top": GeneralPipeClampTop,
    "bottom": GeneralPipeClampBottom,
}


def main() -> None:
    """Parse arguments and render the selected GeneralPipeClamp variant."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Render GeneralPipeClamp to .scad")
    parser.add_argument(
        "--variant",
        choices=list(VARIANTS),
        default="full",
        help="Which variant to render (default: full)",
    )
    add_output_arg(parser)
    add_part_args(parser, GeneralPipeClamp)
    args = parser.parse_args()
    part_cls = VARIANTS[args.variant]
    build_part(part_cls, args).render(Path(args.output))


if __name__ == "__main__":
    main()
