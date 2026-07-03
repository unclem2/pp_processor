# from sqlalchemy.dialects.postgresql import insert
# from sqlalchemy.ext.asyncio import AsyncSession

# from objects.schemas.score import ScoreSchema


# class ScoreRepository:
#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def from_id(self, id: int) -> ScoreSchema | None:
#         return await self.session.get(ScoreSchema, id)

#     async def save(self, score: ScoreSchema) -> None:
#         (
#             insert(ScoreSchema)
#             .values(
#                 id=score.id,
#                 bmap_id=score.bmap_id,
#                 md5=score.md5,
#                 pp=score.pp,
#                 score=score.score,
#                 max_combo=score.max_combo,
#                 mods=score.mods,
#                 acc=score.acc,
#                 h300=score.h300,
#                 h100=score.h100,
#                 h50=score.h50,
#                 hmiss=score.hmiss,
#                 hgeki=score.hgeki,
#                 hkatsu=score.hkatsu,
#                 slidertickhits=score.slidertickhits,
#                 sliderendhits=score.sliderendhits,
#                 grade=score.grade,
#                 fc=score.fc,
#                 date=score.date,
#             )
#             .on_conflict_do_update(
#                 index_elements=[ScoreSchema.id],
#                 set_={
#                     "bmap_id": score.bmap_id,
#                     "md5": score.md5,
#                     "pp": score.pp,
#                     "score": score.score,
#                     "max_combo": score.max_combo,
#                     "mods": score.mods,
#                     "acc": score.acc,
#                     "h300": score.h300,
#                     "h100": score.h100,
#                     "h50": score.h50,
#                     "hmiss": score.hmiss,
#                     "hgeki": score.hgeki,
#                     "hkatsu": score.hkatsu,
#                     "slidertickhits": score.slidertickhits,
#                     "sliderendhits": score.sliderendhits,
#                     "grade": score.grade,
#                     "fc": score.fc,
#                     "date": score.date,
#                 },
#             )
#         )
