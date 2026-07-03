from ossapi import Beatmap, Beatmapset

from objects.models.beatmap import BeatmapModel
from objects.schemas.beatmap import BeatmapSchema


def from_api(beatmap: Beatmap, beatmapset: Beatmapset) -> BeatmapSchema:
    return BeatmapSchema(
        id=beatmap.id,
        set_id=beatmap.beatmapset_id,
        md5=beatmap.checksum,
        artist=beatmapset.artist,
        title=beatmapset.title,
        version=beatmap.version,
        creator=beatmapset.creator,
        last_update=beatmap.last_updated,
        total_length=beatmap.total_length,
        max_combo=beatmap.max_combo,
        bpm=beatmapset.bpm,
    )


def to_model(beatmap: BeatmapSchema) -> BeatmapModel:
    return BeatmapModel.model_validate(beatmap, from_attributes=True)
