from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from objects.schemas.beatmap import BeatmapSchema


class BeatmapRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def from_md5(self, md5: str) -> BeatmapSchema | None:
        result = await self.session.execute(
            select(BeatmapSchema).where(BeatmapSchema.md5 == md5),
        )
        beatmap = result.scalar_one_or_none()
        return beatmap

    async def from_id(self, beatmap_id: int) -> BeatmapSchema | None:
        return await self.session.get(BeatmapSchema, beatmap_id)

    async def from_set_id(self, set_id: int) -> list[BeatmapSchema]:
        result = await self.session.execute(
            select(BeatmapSchema).where(BeatmapSchema.set_id == set_id),
        )
        return list(result.scalars().all())

    async def save(self, beatmap: BeatmapSchema) -> None:
        stmt = (
            insert(BeatmapSchema)
            .values(
                id=beatmap.id,
                set_id=beatmap.set_id,
                md5=beatmap.md5,
                artist=beatmap.artist,
                title=beatmap.title,
                version=beatmap.version,
                creator=beatmap.creator,
                last_update=beatmap.last_update,
                total_length=beatmap.total_length,
                max_combo=beatmap.max_combo,
                bpm=beatmap.bpm,
            )
            .on_conflict_do_update(
                index_elements=[BeatmapSchema.id],
                set_={
                    "set_id": beatmap.set_id,
                    "md5": beatmap.md5,
                    "artist": beatmap.artist,
                    "title": beatmap.title,
                    "version": beatmap.version,
                    "creator": beatmap.creator,
                    "last_update": beatmap.last_update,
                    "total_length": beatmap.total_length,
                    "max_combo": beatmap.max_combo,
                    "bpm": beatmap.bpm,
                },
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
