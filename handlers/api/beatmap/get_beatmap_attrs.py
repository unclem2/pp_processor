from fastapi import APIRouter, Depends
from pydantic import BaseModel

from objects.dependencies.services import get_beatmap_service
from objects.models.beatmap_attrs import BeatmapAttributesModel
from objects.services.beatmap import BeatmapService

router = APIRouter(prefix="/get_diff_attrs")


class BeatmapDifficultyAttributesRequestModel(BaseModel):
    beatmap_id: int
    mods: list[dict] = []


@router.post("/", response_model=BeatmapAttributesModel)
async def get_beatmap_attrs(
    request: BeatmapDifficultyAttributesRequestModel,
    beatmap_service: BeatmapService = Depends(get_beatmap_service),
):
    beatmap = await beatmap_service.from_id(request.beatmap_id)
    if beatmap is None:
        return {"error": "Beatmap not found"}
    beatmap_attrs, rosu_beatmap, modlist, clock_rate = await beatmap_service.calculate_attrs(beatmap, mods=request.mods)


    return beatmap_attrs
