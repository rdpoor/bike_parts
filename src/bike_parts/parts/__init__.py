"""All available bike parts."""

from bike_parts.parts.example import ExampleBracket
from bike_parts.parts.example_split_clamp import (
    PipeClamp,
    SplitPipeClampBottom,
    SplitPipeClampTop,
)

ALL_PARTS: list[type] = [
    ExampleBracket,
    PipeClamp,
    SplitPipeClampTop,
    SplitPipeClampBottom,
]

__all__ = [
    "ALL_PARTS",
    "ExampleBracket",
    "PipeClamp",
    "SplitPipeClampBottom",
    "SplitPipeClampTop",
]
