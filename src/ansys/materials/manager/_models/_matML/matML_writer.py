from ansys.materials.manager._models._fluent.simple_properties import (
    property_codes as fluent_property_codes,
)

from ansys.materials.manager._models._common.constant import (
    ConstantModel
)
from ansys.materials.manager.util.matml.matml_from_material import write_matml


class MatMLWriter:
    def __init__(self, path):
        self._path = path


    def constant(self, material: "Material", constant_model: ConstantModel):
        write_matml([material])