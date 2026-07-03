from pydantic import BaseModel


class BeatmapDifficultyAttributesModel(BaseModel):
    speed: float = 0.0
    aim: float = 0.0
    flashlight: float = 0.0
    total: float = 0.0
