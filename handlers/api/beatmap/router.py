from fastapi import APIRouter

from .get_beatmap import router as beatmap_router
from .get_beatmap_attrs import router as beatmap_attrs_router
from .get_diff_attrs import router as diff_attrs_router

router = APIRouter(prefix="/api/beatmap", tags=["beatmap"])
router.include_router(beatmap_router)
router.include_router(diff_attrs_router)
router.include_router(beatmap_attrs_router)
