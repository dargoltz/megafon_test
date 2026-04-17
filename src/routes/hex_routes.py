from fastapi import APIRouter

from ..service import get_inner_cells, get_avg_cells_in_resolution

hex_router = APIRouter()


@hex_router.get("/hex")
async def get_hex(hex: str):
    return get_inner_cells(hex)


@hex_router.get("/avg")
async def get_hex_avg(resolution: int):
    return get_avg_cells_in_resolution(resolution)


@hex_router.get("/bbox")
async def get_in_bbox():
    ...  # todo


@hex_router.get("/bbox_kml")
async def get_in_bbox_kml():
    ...  # todo
