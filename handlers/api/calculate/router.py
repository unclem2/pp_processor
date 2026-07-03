from fastapi import APIRouter

from .score import router as calculate_router

router = APIRouter(prefix="/api/calculate", tags=["calculate"])
router.include_router(calculate_router)
