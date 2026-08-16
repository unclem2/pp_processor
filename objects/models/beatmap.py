from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .beatmap_attrs import BeatmapAttributesModel
from .beatmap_diff_attrs import BeatmapDifficultyAttributesModel


class BeatmapModel(BaseModel):
    id: int = 0
    set_id: int = 0
    md5: str = ""
    artist: str = ""
    title: str = ""
    version: str = ""
    creator: str = ""
    last_update: datetime = Field(default_factory=datetime.now)
    total_length: int = 0
    max_combo: int = 0
    bpm: float = 0.0
    status: int | None = 0
    attributes: BeatmapAttributesModel | None = BeatmapAttributesModel()
    star: BeatmapDifficultyAttributesModel | None = BeatmapDifficultyAttributesModel()

    model_config = ConfigDict(from_attributes=True)
