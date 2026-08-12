from fastapi import APIRouter, Depends, HTTPException

from objects.dependencies.services import get_beatmap_service
from objects.models.beatmap import BeatmapModel
from objects.models.beatmap_diff_attrs import BeatmapDifficultyAttributesModel
from objects.services.beatmap import BeatmapService

router = APIRouter(prefix="/get_beatmap")


@router.get("/{beatmap_id}", response_model=BeatmapModel)
async def get_beatmap_by_id(
    beatmap_id: int, beatmap_service: BeatmapService = Depends(get_beatmap_service),
):
    beatmap = await beatmap_service.from_id(beatmap_id)
    if beatmap is None:
        raise HTTPException(status_code=404, detail="Beatmap not found")
    diff_attrs, beatmap_attrs, rosu_beatmap, modlist, clock_rate = await beatmap_service.calculate_diff_attrs(beatmap, mods=[])

    diff_attrs_model = BeatmapDifficultyAttributesModel(
        aim=diff_attrs.aim,
        speed=diff_attrs.speed,
        flashlight=diff_attrs.flashlight,
        total=diff_attrs.stars,
    )

    beatmap.attributes = beatmap_attrs
    beatmap.star = diff_attrs_model
    return beatmap


@router.get("/md5/{md5}", response_model=BeatmapModel)
async def get_beatmap_by_md5(
    md5: str, beatmap_service: BeatmapService = Depends(get_beatmap_service),
):
    beatmap = await beatmap_service.from_md5(md5)
    if beatmap is None:
        raise HTTPException(status_code=404, detail="Beatmap not found")
    diff_attrs, beatmap_attrs, rosu_beatmap, modlist, clock_rate = await beatmap_service.calculate_diff_attrs(beatmap, mods=[])

    diff_attrs_model = BeatmapDifficultyAttributesModel(
        aim=diff_attrs.aim,
        speed=diff_attrs.speed,
        flashlight=diff_attrs.flashlight,
        total=diff_attrs.stars,
    )

    beatmap.attributes = beatmap_attrs
    beatmap.star = diff_attrs_model
    return beatmap
