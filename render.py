#!/usr/bin/env python3
"""Render all bike parts to output/."""

import argparse
import dataclasses
import logging
from pathlib import Path

from bike_parts.parts import ALL_PARTS


def setup_logging() -> None:
    """Configure root logger and silence noisy third-party loggers."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main() -> None:
    """Parse arguments and render selected or all parts."""
    setup_logging()

    # First pass: resolve --part and --output only, leaving unknown args for the part.
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--part", help="Render only this part class name")
    pre_parser.add_argument(
        "--output", default="output", help="Output directory (default: output)"
    )
    pre_args, remaining = pre_parser.parse_known_args()

    output_dir = Path(pre_args.output)
    parts = [
        p for p in ALL_PARTS if pre_args.part is None or p.__name__ == pre_args.part
    ]

    if not parts:
        logging.error(
            "No part named %r found. Available: %s",
            pre_args.part,
            [p.__name__ for p in ALL_PARTS],
        )
        raise SystemExit(1)

    # Second pass: full parser with per-part field args for --help and validation.
    # When multiple parts are rendered we just use defaults (remaining args ignored).
    parser = argparse.ArgumentParser(description="Render bike parts to .scad and .stl")
    parser.add_argument("--part", help="Render only this part class name")
    parser.add_argument(
        "--output", default="output", help="Output directory (default: output)"
    )

    if len(parts) == 1:
        part_cls = parts[0]
        for field in dataclasses.fields(part_cls):
            field_type = (
                field.type if isinstance(field.type, type) else eval(field.type)
            )  # noqa: S307
            parser.add_argument(
                f"--{field.name}",
                type=field_type,
                default=None,
                metavar=str(field.default),
                help=f"{field.name} (default: {field.default})",
            )

    args = parser.parse_args()

    for part_cls in parts:
        if len(parts) == 1:
            kwargs = {
                k: v
                for k, v in vars(args).items()
                if v is not None and k not in {"part", "output"}
            }
            part_cls(**kwargs).render(output_dir)
        else:
            part_cls().render(output_dir)


if __name__ == "__main__":
    main()
