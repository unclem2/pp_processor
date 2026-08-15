from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from objects.dependencies.services import get_beatmap_service
from objects.models.beatmap_diff_attrs import BeatmapDifficultyAttributesModel
from objects.services.beatmap import BeatmapService

router = APIRouter(prefix="/get_diff_attrs")


class BeatmapDifficultyAttributesRequestModel(BaseModel):
    beatmap_id: int
    mods: list[dict] = []


@router.post("/", response_model=BeatmapDifficultyAttributesModel)
async def get_diff_attrs(
    request: BeatmapDifficultyAttributesRequestModel,
    beatmap_service: BeatmapService = Depends(get_beatmap_service),
):
    beatmap = await beatmap_service.from_id(request.beatmap_id)
    if beatmap is None:
        raise HTTPException(status_code=404, detail="Beatmap not found")
    diff_attrs, beatmap_attrs, rosu_beatmap, modlist, clock_rate = await beatmap_service.calculate_diff_attrs(beatmap, mods=request.mods)

    diff_attrs_model = BeatmapDifficultyAttributesModel(
        aim=diff_attrs.aim,
        speed=diff_attrs.speed,
        flashlight=diff_attrs.flashlight,
        reading=diff_attrs.reading,
        total=diff_attrs.stars,
    )
    return diff_attrs_model
