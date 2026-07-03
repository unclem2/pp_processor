from objects.calculators.beatmap_attrs import BeatmapAttributesCalculator
from objects.calculators.beatmap_diff_attrs import BeatmapDifficultyAttributesCalculator
from objects.calculators.performance_attrs import (
    PerformanceAttributesCalculator,
)


async def get_difficulty_attributes_calculator() -> (
    BeatmapDifficultyAttributesCalculator
):
    return BeatmapDifficultyAttributesCalculator()


async def get_beatmap_attributes_calculator() -> BeatmapAttributesCalculator:
    return BeatmapAttributesCalculator()


async def get_performance_attributes_calculator() -> (
    PerformanceAttributesCalculator
):
    return PerformanceAttributesCalculator()

