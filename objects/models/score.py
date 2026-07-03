from pydantic import BaseModel

from .beatmap import BeatmapModel
from .performance_attrs import PerformanceAttributesModel


class ScoreModel(BaseModel):
    bmap: BeatmapModel = BeatmapModel()
    md5: str = ""
    pp_attributes: PerformanceAttributesModel = PerformanceAttributesModel()
    score: int = 0
    max_combo: int = 0
    mods: str = ""
    acc: float = 0
    h300: int = 0
    h100: int = 0
    h50: int = 0
    hmiss: int = 0
    hgeki: int = 0
    hkatsu: int = 0
    slidertickhits: int = 0
    sliderendhits: int = 0
