import math
import statistics

import h3

from ..core import cells_storage
from ..models import HexCell


def get_inner_cells(h: str) -> list[HexCell]:
    resolution = h3.get_resolution(h)

    if resolution > cells_storage.RES:
        return []
    elif resolution == cells_storage.RES:
        return [HexCell(h_index=h)] if h in cells_storage.cells else []
    else:
        children_cells = set(h3.cell_to_children(h, cells_storage.RES))
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
    if resolution < cells_storage.RES:
        return {
            h3.cell_to_parent(h, resolution)
            for h in cells_storage.cells
        }
    elif resolution == cells_storage.RES:
        return cells_storage.cells
    else:
        cells_in_current_resolution = set()

        for h in cells_storage.cells:
            children = h3.cell_to_children(h, resolution)

            cells_in_current_resolution.update(children)

        return cells_in_current_resolution

