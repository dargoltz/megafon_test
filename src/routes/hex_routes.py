import h3
import datetime
from fastapi import APIRouter, Query, HTTPException, Depends, Response

from ..core import parse_borders
from ..service import get_inner_cells, get_avg_cells_in_resolution, get_cells_in_bbox, get_cells_in_bbox_kml

hex_router = APIRouter()


@hex_router.get("/hex")
async def get_hex(hex: str):
    if not h3.is_valid_cell(hex):
        raise HTTPException(status_code=400, detail="Invalid h3 index")

    return get_inner_cells(hex)


@hex_router.get("/avg")
async def get_hex_avg(resolution: int = Query(ge=0, lt=15)):
    return get_avg_cells_in_resolution(resolution)


@hex_router.get("/bbox")
async def get_in_bbox(borders=Depends(parse_borders)):
    if len(borders) < 3:
        raise HTTPException(status_code=400, detail="Need at least 3 borders")

    return get_cells_in_bbox(borders)


@hex_router.get("/bbox_kml")
async def get_in_bbox_kml(borders=Depends(parse_borders)):
    if len(borders) < 3:
        raise HTTPException(status_code=400, detail="Need at least 3 borders")

    kml = get_cells_in_bbox_kml(borders)

    return Response(
        content=kml.kml(),
        media_type="application/vnd.google-earth.kml+xml",
        headers={
            f"Content-Disposition": f'attachment; filename="{datetime.datetime.now()}.kml"'
        }
    )
