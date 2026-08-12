
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from objects.dependencies.services import get_beatmap_service, get_score_service
from objects.models.score import ScoreModel
from objects.services.beatmap import BeatmapService
from objects.services.score import ScoreService

router = APIRouter(prefix="/score")


class CalculateRequestModel(BaseModel):
    beatmap_id: int | None = None
    md5: str | None = None
    acc: float | None = Field(default=100, ge=0, le=100)
    miss: int | None = Field(default=0, ge=0)
    combo: int | None = Field(default=None, ge=0)
    h300: int | None = Field(default=None, ge=0)
    h100: int | None = Field(default=None, ge=0)
    h50: int | None = Field(default=None, ge=0)
    hgeki: int | None = Field(default=None, ge=0)
    hkatsu: int | None = Field(default=None, ge=0)
    slidertickhits: int | None = Field(default=None, ge=0)
    sliderendhits: int | None = Field(default=None, ge=0)
    sliderheadhits: int | None = Field(default=None, ge=0)
    sliderrepeathits: int | None = Field(default=None, ge=0)
    mods: list[dict] = []


@router.post("/", response_model=ScoreModel)
async def calculate(
    request: CalculateRequestModel,
    beatmap_service: BeatmapService = Depends(get_beatmap_service),
    score_service: ScoreService = Depends(get_score_service),
):

    if request.md5:
        beatmap = await beatmap_service.from_md5(request.md5)
    elif request.beatmap_id:
        beatmap = await beatmap_service.from_id(request.beatmap_id)
    else:
        raise HTTPException(status_code=400, detail="Specify beatmap_id or md5")
    if beatmap is None:
        raise HTTPException(status_code=404, detail="Beatmap not found")

    result = await score_service.calculate(
        beatmap,
        request.mods,
        request.acc,
        request.miss,
        request.combo,
        request.h300,
        request.h100,
        request.h50,
        request.hgeki,
        request.hkatsu,
        request.slidertickhits,
        request.sliderendhits,
        request.sliderheadhits,
        request.sliderrepeathits
    )

    return result
