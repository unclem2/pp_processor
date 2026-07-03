import osudroid_api_wrapper as od
import rosu_pp_py



class PerformanceAttributesCalculator:
    def __init__(self):
        pass

    def calculate(
        self, 
        difficulty_attrs: rosu_pp_py.DifficultyAttributes,
        mods: od.ModList,
        clock_rate: int | float | None = None,
        acc: float | None = None,
        miss: int | None = None,
        combo: int | None = None,
        h300: int | None = None,
        h100: int | None = None,
        h50: int | None = None,
        hgeki: int | None = None,
        hkatsu: int | None = None,
        slidertickhits: int | None = None,
        sliderendhits: int | None = None
    ) -> rosu_pp_py.PerformanceAttributes:
        performance = rosu_pp_py.Performance()

        performance.set_mods(mods.as_calculable_mods)
        if clock_rate is not None:
            performance.set_clock_rate(clock_rate)
        if acc is not None:
            performance.set_accuracy(acc)
        elif h300 is not None and h100 is not None and h50 is not None and hgeki is not None and hkatsu is not None:
            performance.set_n300(h300)
            performance.set_n100(h100)
            performance.set_n50(h50)
            performance.set_n_geki(hgeki)
            performance.set_n_katu(hkatsu)
        if miss is not None:
            performance.set_misses(miss)
        if combo is not None:
            performance.set_combo(combo)
        if slidertickhits is not None:
            performance.set_small_tick_hits(slidertickhits)
        if sliderendhits is not None:
            performance.set_slider_end_hits(sliderendhits)
        if clock_rate is not None:
            performance.set_clock_rate(clock_rate)
        performance_attributes = performance.calculate(difficulty_attrs)
        
        return performance_attributes
