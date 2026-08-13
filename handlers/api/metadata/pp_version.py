from fastapi import APIRouter, Request

import config

router = APIRouter(prefix="/pp_version")


@router.get("/")
async def get_processor_pp_version(request: Request):

    return config.pp_version
