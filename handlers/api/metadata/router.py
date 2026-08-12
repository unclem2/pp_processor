from fastapi import APIRouter

from .pp_version import router as pp_version_router

router = APIRouter(prefix="/metadata", tags=["metadata"])
router.include_router(pp_version_router)
