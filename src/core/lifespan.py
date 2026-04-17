from contextlib import asynccontextmanager
from fastapi import FastAPI
from .hexes_storage import hexes_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    hexes_storage.setup()
    yield
