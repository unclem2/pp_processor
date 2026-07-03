import osudroid_api_wrapper as od
import rosu_pp_py

from objects.models.beatmap_attrs import BeatmapAttributesModel
from objects.models.beatmap_diff_attrs import BeatmapDifficultyAttributesModel


class BeatmapDifficultyAttributesCalculator:
    def __init__(self):
        pass

    def calculate(
        self, beatmap: rosu_pp_py.Beatmap, beatmap_attrs: BeatmapAttributesModel, mods: od.ModList, clock_rate: int | float | None
    ) -> rosu_pp_py.DifficultyAttributes:
        difficulty = rosu_pp_py.Difficulty()
        difficulty.set_ar(ar=beatmap_attrs.ar, fixed=True)
        difficulty.set_cs(cs=beatmap_attrs.cs, fixed=True)
        difficulty.set_od(od=beatmap_attrs.od, fixed=True)
        difficulty.set_hp(hp=beatmap_attrs.hp, fixed=True)
        difficulty.set_mods(mods.as_calculable_mods)
        if clock_rate is not None:
            difficulty.set_clock_rate(clock_rate)
        difficulty_attributes = difficulty.calculate(map=beatmap)


        return difficulty_attributes
