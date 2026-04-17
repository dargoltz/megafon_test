import h3
from pydantic import BaseModel, computed_field, model_serializer


class HexCell(BaseModel):
    h_index: str

    @computed_field
    @property
    def h_index_base(self) -> int:
        return h3.str_to_int(self.h_index) // 512

    @computed_field
    @property
    def level(self) -> int:
        return (self.h_index_base % 74) - 120

    @computed_field
    @property
    def cell_id(self) -> int:
        return (self.h_index_base % 100) + 1

    @model_serializer
    def serialize(self):
        return [self.h_index, self.level, self.cell_id]
