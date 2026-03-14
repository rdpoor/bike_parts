"""All available bike parts."""

from bike_parts.parts.example import ExampleBracket
from bike_parts.parts.example_split_clamp import (
    PipeClamp,
    SplitPipeClampBottom,
    SplitPipeClampTop,
)
from bike_parts.parts.general_pipe_clamp import (
    GeneralPipeClamp,
    GeneralPipeClampBottom,
    GeneralPipeClampTop,
)

ALL_PARTS: list[type] = [
    ExampleBracket,
    GeneralPipeClamp,
    GeneralPipeClampTop,
    GeneralPipeClampBottom,
    PipeClamp,
    SplitPipeClampTop,
    SplitPipeClampBottom,
]

__all__ = [
    "ALL_PARTS",
    "ExampleBracket",
    "GeneralPipeClamp",
    "GeneralPipeClampBottom",
    "GeneralPipeClampTop",
    "PipeClamp",
    "SplitPipeClampBottom",
    "SplitPipeClampTop",
]
