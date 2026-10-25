from fastapi import APIRouter, Depends

from objects.dependencies.rate_limit import osu_api_rate_limit

from .score import router as calculate_router

router = APIRouter(
    prefix="/api/calculate",
    tags=["calculate"],
    dependencies=[Depends(osu_api_rate_limit)],
)
router.include_router(calculate_router)
