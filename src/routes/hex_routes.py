from fastapi import APIRouter

hex_router = APIRouter(tags=["hex"])


@hex_router.get("/hex")
async def get_hex():
    ...  # todo


@hex_router.get("/avg")
async def get_hex_avg():
    ...  # todo


@hex_router.get("/bbox")
async def get_in_bbox():
    ...  # todo


@hex_router.get("/bbox_kml")
async def get_in_bbox_kml():
    ...  # todo
