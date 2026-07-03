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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("DB connected")
    await init(engine)
    yield

    # shutdown
    await engine.dispose()
    print("DB closed")


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

    response = await call_next(request)

    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    print(f"{request.method} {request.url.path}: {process_time:.3f}s")

    return response