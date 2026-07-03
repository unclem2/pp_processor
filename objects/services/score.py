
from objects.calculators.performance_attrs import PerformanceAttributesCalculator
from objects.models.beatmap import BeatmapModel
from objects.models.performance_attrs import PerformanceAttributesModel
from objects.models.score import ScoreModel
from objects.services.beatmap import BeatmapService


class ScoreService:
    def __init__(self, performance_calculator: PerformanceAttributesCalculator, beatmap_service: BeatmapService) -> None:
        self.performance_calculator = performance_calculator
        self.beatmap_service = beatmap_service

    def calculate(
        self,
        beatmap: BeatmapModel,
        mods: list,
        acc: float | None,
        miss: int | None,
        combo: int | None,
        h300: int | None,
        h100: int | None,
        h50: int | None,
        hgeki: int | None,
        hkatsu: int | None,
        slidertickhits: int | None,
        sliderendhits: int | None,
    ) -> ScoreModel:
    
        diff_attrs, beatmap_attrs_model, rosu_beatmap, modlist, clock_rate = self.beatmap_service.calculate_diff_attrs(beatmap, mods)
        perf_attrs = self.performance_calculator.calculate(
            difficulty_attrs=diff_attrs,
            mods=modlist,
            clock_rate=clock_rate,
            acc=acc,
            miss=miss,
            combo=combo,
            h300=h300,
            h100=h100,
            h50=h50,
            hgeki=hgeki,
            hkatsu=hkatsu,
            slidertickhits=slidertickhits,
            sliderendhits=sliderendhits,
        )
        performance_attrs_model = PerformanceAttributesModel(
            aim=perf_attrs.pp_aim,
            speed=perf_attrs.pp_speed,
            accuracy=perf_attrs.pp_accuracy,
            flashlight=perf_attrs.pp_flashlight,
            total=perf_attrs.pp,
        )
        return ScoreModel(
            bmap=beatmap,
            md5=beatmap.md5,
            pp_attributes=performance_attrs_model,
            score=0,
            max_combo=combo if combo is not None else 0,
            mods=modlist.as_json_string,
            acc=acc if acc is not None else 100,
            h300=h300 if h300 is not None else 0,
            h100=h100 if h100 is not None else 0,
            h50=h50 if h50 is not None else 0,
            hmiss=miss if miss is not None else 0,
            hgeki=hgeki if hgeki is not None else 0,
            hkatsu=hkatsu if hkatsu is not None else 0,
            slidertickhits=slidertickhits if slidertickhits is not None else 0,
            sliderendhits=sliderendhits if sliderendhits is not None else 0,
        )
