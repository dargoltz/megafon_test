import h3

from .config import app_config


class CellsStorage:
    def __init__(self):
        self.cells: set[str] | None = None

    def setup(self):
        center = h3.latlng_to_cell(app_config.CENTER_LAT, app_config.CENTER_LON, app_config.BASE_RESOLUTION)
        edge_length = h3.average_hexagon_edge_length(app_config.BASE_RESOLUTION)

        k = int(app_config.BASE_RADIUS_KM / edge_length)
        grid_disk = h3.grid_disk(center, k)

        cells_in_area = {
            h for h in grid_disk
            if h3.great_circle_distance(h3.cell_to_latlng(center), h3.cell_to_latlng(h)) < app_config.BASE_RESOLUTION
        }

        self.cells = cells_in_area


cells_storage = CellsStorage()
