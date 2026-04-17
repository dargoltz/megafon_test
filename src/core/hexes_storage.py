import h3

from src.models import Hex


class HexesStorage:
    LAT, LON = 56.0, 38.0
    RES = 12
    R_KM = 7

    def __init__(self):
        self.hexes = None

    def setup(self):
        center = h3.latlng_to_cell(self.LAT, self.LON, self.RES)
        edge_length = h3.average_hexagon_edge_length(self.RES)

        k = int(self.R_KM / edge_length)
        hexes_disk = h3.grid_disk(center, k)

        hexes_in_radius = [
            Hex(h3_index_str=h) for h in hexes_disk
            if h3.great_circle_distance((self.LAT, self.LON), h3.cell_to_latlng(h)) < self.R_KM
        ]

        self.hexes = hexes_in_radius


hexes_storage = HexesStorage()
