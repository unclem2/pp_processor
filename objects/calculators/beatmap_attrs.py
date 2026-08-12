from dataclasses import dataclass
from math import floor

import osudroid_api_wrapper as od
import rosu_pp_py

from objects.models.beatmap_attrs import BeatmapAttributesModel


def droid_cs_to_standard_cs(cs: float) -> float:
    """Converts Droid CS to standard CS.
    Formulas taken from Rian8337 osu-droid-module:
    https://github.com/Rian8337/osu-droid-module/blob/master/packages/osu-base/src/utils/CircleSizeCalculator.ts
    """
    old_assumed_droid_height = 681
    base_radius = 64
    old_droid_scale_multiplier = (0.5 * (11 - 5.2450170716245195)) / 5
    broken_gamefield_rounding_allowance = 1.00041

    old_droid_scale = max(
        ((old_assumed_droid_height / 480) * (54.42 - cs * 4.48)) / base_radius + old_droid_scale_multiplier,
        1e-3,
    )

    standard_radius = (base_radius * old_droid_scale) / ((old_assumed_droid_height * 0.85) / 384)

    scale = standard_radius / base_radius

    standard_cs = 5 + (5 * (1 - (2 * scale) / broken_gamefield_rounding_allowance)) / 0.7
    return standard_cs


@dataclass
class HitWindows:
    great: float
    ok: float
    meh: float


def precise_droid(od: float) -> HitWindows:
    return HitWindows(
        great=55 + 6 * (5 - od),
        ok=120 + 8 * (5 - od),
        meh=180 + 10 * (5 - od),
    )


def standard(od: float) -> HitWindows:
    return HitWindows(
        great=floor(80 - 6 * od) - 0.5,
        ok=floor(140 - 8 * od) - 0.5,
        meh=floor(200 - 10 * od) - 0.5,
    )


def droid(od: float) -> HitWindows:
    return HitWindows(
        great=75 + 5 * (5 - od),
        ok=150 + 10 * (5 - od),
        meh=250 + 10 * (5 - od),
    )


def precise_from_great(ms: float) -> float:
    return 5 - (ms - 55) / 6


def droid_from_great(ms: float) -> float:
    return 5 - (ms - 75) / 5


def standard_from_great(ms: float) -> float:
    return (80 - (ms + 0.5)) / 6


class BeatmapAttributesCalculator:
    def __init__(self):
        pass

    def calculate(
        self, beatmap: rosu_pp_py.Beatmap, mods: od.ModList, clock_rate: float | None,
    ) -> BeatmapAttributesModel:
        """This one must return model instead of raw object, because droid attributes are calculated differently
        """
        beatmap_attributes = rosu_pp_py.BeatmapAttributesBuilder(map=beatmap)

        beatmap_attributes.set_mods(mods.as_calculable_mods)
        if clock_rate is not None:
            beatmap_attributes.set_clock_rate(clock_rate)

        attrs = beatmap_attributes.build()

        beatmap_attrs_model = BeatmapAttributesModel(
            ar=attrs.ar,
            ar_hit_window=attrs.ar_hit_window,
            base_ar=attrs.base_ar,
            base_od=attrs.base_od,
            clock_rate=attrs.clock_rate,
            cs=droid_cs_to_standard_cs(attrs.cs),
            # cs=attrs.cs,
            hp=attrs.hp,
            od=attrs.od,
            od_great_hit_window=attrs.od_great_hit_window,
            od_meh_hit_window=attrs.od_meh_hit_window,
            od_ok_hit_window=attrs.od_ok_hit_window,
        )
        if mods.get_mod("PR") is not None:
            hit_window = precise_droid(beatmap_attrs_model.od)
        else:
            hit_window = droid(beatmap_attrs_model.od)
        beatmap_attrs_model.od_great_hit_window = hit_window.great
        beatmap_attrs_model.od_ok_hit_window = hit_window.ok
        beatmap_attrs_model.od_meh_hit_window = hit_window.meh
        beatmap_attrs_model.od = standard_from_great(hit_window.great)
        beatmap_attrs_model.base_od = standard_from_great(droid(beatmap_attrs_model.base_od).great)
        return beatmap_attrs_model
