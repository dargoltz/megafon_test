import math
import statistics
from collections import defaultdict

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
        parent_cells = defaultdict(list)

        for cell in cells_storage.cells:
            parent_cells[h3.cell_to_parent(cell, resolution)].append(cell)

        return [HexCell(h_index=c) for c in parent_cells[h]]


def get_avg_cells_in_resolution(resolution: int):
    groups = defaultdict(list)

    for h in cells_storage.cells:
        hc = HexCell(h_index=h)
        groups[(h3.cell_to_parent(h, resolution), hc.cell_id)].append(hc)

    result = []

    for group, hex_cells in groups.items():
        h, cell_id = group
        median = math.floor(statistics.median([h.level for h in hex_cells]))
        result.append([h, median, cell_id])

    return sorted(result, key=lambda r: r[2])


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


def get_cells_in_bbox_kml(borders: list[tuple[float, float]]) -> simplekml.Kml:
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

    return kml
