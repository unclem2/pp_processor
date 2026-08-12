from fastapi import Depends

from objects.dependencies.calculators import (
    get_beatmap_attributes_calculator,
    get_difficulty_attributes_calculator,
    get_performance_attributes_calculator,
)
from objects.dependencies.clients import get_osuapi_client
from objects.dependencies.repositories import (
    get_beatmap_repository,
    get_score_repository,
)
from objects.calculators.performance_attrs import PerformanceAttributesCalculator
from objects.repositories.beatmap import BeatmapRepository
from objects.repositories.score import ScoreRepository
from objects.services.beatmap import BeatmapService
from objects.services.score import ScoreService


async def get_beatmap_service(
    repository: BeatmapRepository = Depends(get_beatmap_repository),
    osuapi_client=Depends(get_osuapi_client),
    diff_calculator=Depends(get_difficulty_attributes_calculator),
    attrs_calculator=Depends(get_beatmap_attributes_calculator),
    performance_calculator=Depends(get_performance_attributes_calculator),
) -> BeatmapService:
    return BeatmapService(
        repository,
        osuapi_client,
        diff_calculator,
        attrs_calculator,
        performance_calculator,
    )


async def get_score_service(
    performance_calculator: PerformanceAttributesCalculator = Depends(get_performance_attributes_calculator),
    beatmap_service: BeatmapService = Depends(get_beatmap_service),
    score_repository: ScoreRepository = Depends(get_score_repository),
) -> ScoreService:
    return ScoreService(performance_calculator, beatmap_service, score_repository)
