from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..storage import cells_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    cells_storage.setup()
    yield
