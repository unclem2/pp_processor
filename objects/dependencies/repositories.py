from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from objects.dependencies.db import get_db_session
from objects.repositories.beatmap import BeatmapRepository

# from objects.repositories.score import ScoreRepository


async def get_beatmap_repository(
    session: AsyncSession = Depends(get_db_session),
) -> BeatmapRepository:
    return BeatmapRepository(session)


# async def get_score_repository(
#     session: AsyncSession = Depends(get_db_session),
# ) -> ScoreRepository:
#     return ScoreRepository(session)
