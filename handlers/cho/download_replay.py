import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/upload")


@router.get("/{replay_path}")
async def download_replay(replay_path: str):
    safe_path = Path("data/replays") / replay_path
    resolved = safe_path.resolve()
    allowed_base = Path("data/replays").resolve()
    if not str(resolved).startswith(str(allowed_base)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not resolved.is_file():
        raise HTTPException(status_code=404, detail="Replay not found")

    from fastapi.responses import FileResponse
    return FileResponse(resolved)
