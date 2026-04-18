import datetime
import math
import statistics

import h3
from shapely.geometry import Polygon
import simplekml
from fastapi import Response

from ..core import app_config
from ..storage import cells_storage
from ..models import HexCell


# Текущая реализация подразумевает, что в ячейку большего разрешения не может целиком вместиться ни одна ячейка
# исходного разрешения
def get_inner_cells(h: str) -> list[HexCell]:
    resolution = h3.get_resolution(h)

    if resolution > app_config.BASE_RESOLUTION:
        return []
    elif resolution == app_config.BASE_RESOLUTION:
        return [HexCell(h_index=h)] if h in cells_storage.cells else []
    else:
        children_cells = set(h3.cell_to_children(h, app_config.BASE_RESOLUTION))
        found_cells = children_cells & cells_storage.cells

        return [HexCell(h_index=c) for c in found_cells]


# В условии задания говорилось о группировке по cell_id
# Текущая реализация ориентирована на формат вывода из задания, что больше напоминает сортировку
def get_avg_cells_in_resolution(resolution: int) -> list[HexCell]:
    cells_in_current_resolution = get_cells_in_current_resolution(resolution)
    hex_cells = [HexCell(h_index=h) for h in cells_in_current_resolution]

    median = math.floor(statistics.median([hc.level for hc in hex_cells]))
    filtered_by_median = [hc for hc in hex_cells if hc.level == median]
    filtered_by_median.sort(key=lambda hc: hc.cell_id)

    return filtered_by_median


def get_cells_in_current_resolution(resolution: int) -> set[str]:
    if resolution < app_config.BASE_RESOLUTION:
        return {
            h3.cell_to_parent(h, resolution)
            for h in cells_storage.cells
        }
    elif resolution == app_config.BASE_RESOLUTION:
        return cells_storage.cells
    else:
        cells_in_current_resolution = set()

        for h in cells_storage.cells:
            children = h3.cell_to_children(h, resolution)

            cells_in_current_resolution.update(children)

        return cells_in_current_resolution


def get_cells_in_bbox(borders: list[tuple[float, float]]) -> list[HexCell]:
    h3poly = h3.LatLngPoly(borders)
    cells = set(h3.h3shape_to_cells(h3poly, app_config.BASE_RESOLUTION)) & cells_storage.cells

    if not cells:
        return []

    poly = Polygon([(lon, lat) for lat, lon in borders])
    cells_in_poly = []

    for h in cells:
        cell_poly = Polygon([(lon, lat) for lat, lon in h3.cell_to_boundary(h)])

        if poly.contains(cell_poly):
            cells_in_poly.append(h)

    return [HexCell(h_index=h) for h in cells_in_poly]


def get_cells_in_bbox_kml(borders: list[tuple[float, float]]):
    cells_in_bbox = get_cells_in_bbox(borders)
    kml = simplekml.Kml()

    for c in cells_in_bbox:
        boundary = list(h3.cell_to_boundary(c.h_index))
        boundary.append(boundary[0])

        coords = [(lon, lat) for lat, lon in boundary]

        kml.newpolygon(
            name=c.h_index,
            outerboundaryis=coords,
            description=f"level={c.level}, cell_id={c.cell_id}",
        )

    return Response(
        content=kml.kml(),
        media_type="application/vnd.google-earth.kml+xml",
        headers={
            f"Content-Disposition": f'attachment; filename="{datetime.datetime.now()}.kml"'
        }
    )
