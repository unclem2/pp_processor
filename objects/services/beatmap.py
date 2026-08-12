import logging
import pathlib

import aiohttp
import osudroid_api_wrapper as od
import rosu_pp_py
from anyio import Path
from osudroid_api_wrapper import ModList

from objects.calculators.beatmap_attrs import BeatmapAttributesCalculator
from objects.calculators.beatmap_diff_attrs import BeatmapDifficultyAttributesCalculator
from objects.calculators.performance_attrs import (
    PerformanceAttributesCalculator,
)
from objects.mappers.beatmap import (
    from_api as beatmap_from_api,
)
from objects.mappers.beatmap import (
    to_model as beatmap_to_model,
)
from objects.models.beatmap import BeatmapModel
from objects.models.beatmap_attrs import BeatmapAttributesModel
from objects.repositories.beatmap import BeatmapRepository


# @lru_cache(maxsize=128)
def open_rosu_beatmap(beatmap_id: int) -> rosu_pp_py.Beatmap:
    beatmap_path = f"/srv/odrx_storage/beatmaps/{beatmap_id}.osu"
    return rosu_pp_py.Beatmap(path=beatmap_path)


class BeatmapService:
    def __init__(
        self,
        repository: BeatmapRepository,
        osuapi_client,
        diff_calculator: BeatmapDifficultyAttributesCalculator,
        attrs_calculator: BeatmapAttributesCalculator,
        performance_calculator: PerformanceAttributesCalculator,
    ) -> None:
        self.repository = repository
        self.osuapi_client = osuapi_client
        self.diff_calculator = diff_calculator
        self.attrs_calculator = attrs_calculator
        self.performance_calculator = performance_calculator

    async def from_md5(self, md5: str) -> BeatmapModel | None:
        try:
            if request := await self.repository.from_md5(md5):
                return beatmap_to_model(request)
            if request := await self.osuapi_client.beatmap(checksum=md5):
                schema = beatmap_from_api(request, request.beatmapset())
                await self.repository.save(schema)
                beatmap = beatmap_to_model(schema)
                await self.download(beatmap)
                return beatmap
            return None
        except ValueError:
            logging.exception("[BeatmapService] %s - not found", md5)
            return None
        except Exception:
            logging.exception("[BeatmapService] %s - error fetching beatmap", md5)
            return None

    async def from_id(self, beatmap_id: int) -> BeatmapModel | None:
        try:
            if request := await self.repository.from_id(beatmap_id):
                return beatmap_to_model(request)
            if request := await self.osuapi_client.beatmap(beatmap_id=beatmap_id):
                schema = beatmap_from_api(request, request.beatmapset())
                await self.repository.save(schema)
                beatmap = beatmap_to_model(schema)
                await self.download(beatmap)
                return beatmap
            return None
        except ValueError:
            logging.exception("[BeatmapService] %s - not found", beatmap_id)
            return None
        except Exception:
            logging.exception("[BeatmapService] %s - error fetching beatmap", beatmap_id)
            return None

    async def download(self, beatmap: BeatmapModel) -> Path | None:
        path = Path(f"/srv/odrx_storage/beatmaps/{beatmap.id}.osu")
        if await path.exists():
            return path

        url = f"https://old.ppy.sh/osu/{beatmap.id}"
        try:
            async with aiohttp.ClientSession() as sess, sess.get(url) as res:
                if not res or res.status != 200:
                    return None

                content = await res.read()

            await path.write_bytes(content)
            return path
        except Exception:
            logging.exception("[BeatmapService] Failed to download beatmap %s", beatmap.id)
            return None

    def prepare_modlist(self, mods: list[dict]) -> tuple[ModList, float | None]:
        modlist: ModList = ModList.from_dict(mods)
        speed_multiplier = modlist.get_mod("CS")
        rate = None
        if speed_multiplier is not None:
            rate_setting = speed_multiplier.settings.get_setting("rateMultiplier")
            rate = rate_setting.value if rate_setting is not None else None
            if rate is not None:
                if mod := modlist.get_mod("DT"):
                    mod.settings.add_setting(
                        od.classes.mods.settings.Setting(
                            name="speed_change", value=1.5 * rate,
                        ),
                    )
                elif mod := modlist.get_mod("HT"):
                    mod.settings.add_setting(
                        od.classes.mods.settings.Setting(
                            name="speed_change", value=0.75 * rate,
                        ),
                    )
                elif mod := modlist.get_mod("NC"):
                    mod.settings.add_setting(
                        od.classes.mods.settings.Setting(
                            name="speed_change", value=1.5 * rate,
                        ),
                    )
        return modlist, rate

    async def prepare_beatmap(self, beatmap: BeatmapModel) -> rosu_pp_py.Beatmap:
        beatmap_path = pathlib.Path(f"/srv/odrx_storage/beatmaps/{beatmap.id}.osu")
        if not beatmap_path.exists():
            result = await self.download(beatmap)
            if result is None:
                raise FileNotFoundError(f"Failed to download beatmap {beatmap.id}")

        return open_rosu_beatmap(beatmap.id)

    async def calculate_attrs(
        self,
        beatmap: BeatmapModel,
        mods: list[dict],
    ) -> tuple[
        BeatmapAttributesModel,
        rosu_pp_py.Beatmap,
        ModList,
        int | float | None,
    ]:
        modlist, clock_rate = self.prepare_modlist(mods)
        rosu_beatmap = await self.prepare_beatmap(beatmap)
        beatmap_attrs = self.attrs_calculator.calculate(
            rosu_beatmap,
            modlist,
            clock_rate,
        )
        return beatmap_attrs, rosu_beatmap, modlist, clock_rate

    async def calculate_diff_attrs(
        self,
        beatmap: BeatmapModel,
        mods: list[dict],
    ) -> tuple[
        rosu_pp_py.DifficultyAttributes,
        BeatmapAttributesModel,
        rosu_pp_py.Beatmap,
        ModList,
        int | float | None,
    ]:
        beatmap_attrs, rosu_beatmap, modlist, clock_rate = await self.calculate_attrs(
            beatmap,
            mods,
        )
        difficulty_attrs = self.diff_calculator.calculate(
            rosu_beatmap,
            beatmap_attrs,
            modlist,
            clock_rate,
        )
        return difficulty_attrs, beatmap_attrs, rosu_beatmap, modlist, clock_rate
