import logging
import os
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from ossapi import OssapiAsync

# Other imports
import handlers
from objects.db.db import engine, init

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("DB connected")
    await init(engine)
    yield

    # shutdown
    await engine.dispose()
    logger.info("DB closed")


def make_app() -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan)
    routes = handlers.load_routers()
    for route in routes:
        fastapi_app.include_router(route)
    return fastapi_app


app = make_app()
ossapi_client = OssapiAsync(os.getenv("OSU_CLIENT_ID"), os.getenv("OSU_CLIENT_SECRET"))
app.state.osuapi_client = ossapi_client


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Request %s %s failed", request.method, request.url.path)
        raise
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    logger.info("%s %s: %.3fs", request.method, request.url.path, process_time)

    return response
