import h3


class CellsStorage:
    LAT, LON = 56.0, 38.0
    RES = 12
    R_KM = 7

    def __init__(self):
        self.cells: dict[str, tuple[int, int]] = {}

    def setup(self):
        center = h3.latlng_to_cell(self.LAT, self.LON, self.RES)
        edge_length = h3.average_hexagon_edge_length(self.RES)

        k = int(self.R_KM / edge_length)
        grid_disk = h3.grid_disk(center, k)

        for h in grid_disk:
            if h3.great_circle_distance((self.LAT, self.LON), h3.cell_to_latlng(h)) < self.R_KM:
                h_int = h3.str_to_int(h)
                base = h_int // 512

                self.cells[h] = (self._get_level(base), self._get_cell_id(base))

    @staticmethod
    def _get_level(base: int) -> int:
        return (base % 74) - 120

    @staticmethod
    def _get_cell_id(base: int) -> int:
        return (base % 100) + 1


cells_storage = CellsStorage()
