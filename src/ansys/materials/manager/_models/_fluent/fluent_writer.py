from ansys.materials.manager._models._fluent.simple_properties import (
    property_codes as fluent_property_codes,
)

from ansys.materials.manager._models._common.constant import (
    ConstantModel
)
class FluentWriter:
    def __init__(self, fluent: "_FluentCore"):
        self._fluent = fluent


    def constant(self, material: "Material", constant_model: ConstantModel):
        try:
            fluent_property_code = fluent_property_codes[constant_model.name.lower()]
            if isinstance(constant_model.value, str):
                propState = {fluent_property_code: {"option": constant_model.value}}
            else:
                propState = {fluent_property_code: {"option": "constant", "value": constant_model.value}}
            self._fluent.setup.materials.fluid[material.name] = propState
        except (RuntimeError, KeyError):
            pass