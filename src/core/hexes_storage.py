import h3


class CellsStorage:
    LAT, LON = 56.0, 38.0
    RES = 12
    R_KM = 7

    def __init__(self):
        self.cells: set[str] | None = None

    def setup(self):
        center = h3.latlng_to_cell(self.LAT, self.LON, self.RES)
        edge_length = h3.average_hexagon_edge_length(self.RES)

        k = int(self.R_KM / edge_length)
        grid_disk = h3.grid_disk(center, k)

        cells_in_area = {
            h for h in grid_disk
            if h3.great_circle_distance((self.LAT, self.LON), h3.cell_to_latlng(h)) < self.R_KM
        }

        self.cells = cells_in_area


cells_storage = CellsStorage()
