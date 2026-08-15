from pydantic import BaseModel
import config

class PerformanceAttributesModel(BaseModel):
    speed: float = 0.0
    aim: float = 0.0
    acc: float = 0.0
    flashlight: float = 0.0
    reading: float = 0.0
    total: float = 0.0
    pp_version: str = config.pp_version