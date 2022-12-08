from ansys.materials.manager._models._common.constant import ConstantModel
from ansys.materials.manager._models._mapdl.simple_properties import (
    property_codes as mapdl_property_codes,
)

class MapdlWriter:
    def __init__(self, mapdl: "_MapdlCore"):
        self._mapdl = mapdl


    def constant(self, material: "Material", constant_model: ConstantModel):
        mapdl_property_code = mapdl_property_codes[constant_model.name.lower()]
        self._mapdl.mp(mapdl_property_code, material.material_id, constant_model.value)
        
        
        