from typing import Dict, Sequence

from ansys.materials.manager._models import Constant
from ansys.materials.manager.material import Material

# todo: add more property sets and parameters to the map
PROPERTY_MAP = {
    "Density": {"properties": ["Density"], "mappings": {}},
    "Elasticity::Isotropic": {
        "properties": [],
        "mappings": {
            "Young's Modulus": [
                "Young's Modulus X direction",
                "Young's Modulus Y direction",
                "Young's Modulus Z direction",
            ],
            "Shear Modulus": [
                "Shear Modulus XY",
                "Shear Modulus XZ",
                "Shear Modulus YZ",
            ],
            "Poisson's Ratio": [
                "Poisson's Ratio XY",
                "Poisson's Ratio XZ",
                "Poisson's Ratio YZ",
            ],
        },
    },
    "Elasticity::Orthotropic": {
        "properties": [
            "Young's Modulus X direction",
            "Young's Modulus Y direction",
            "Young's Modulus Z direction",
            "Shear Modulus XY",
            "Shear Modulus XZ",
            "Shear Modulus YZ",
            "Poisson's Ratio XY",
            "Poisson's Ratio XZ",
            "Poisson's Ratio YZ",
        ],
        "mappings": {},
    },
}


def convert_matml_materials(materials_dict: Dict, index_offset: int) -> Sequence[Material]:
    """Convert a list of materials into Material objects.

    Parameters
    ----------
    materials_dict:
        dict of raw material data from a matml import
    index_offset:
        int to offset the material id (number) to avoid conflicts with already existing materials

    Returns a list of Material objects
    """
    materials = []

    global_material_index = 1 + index_offset
    # loop over the materials
    for mat_id, material_data in materials_dict.items():

        models = []
        # loop over the defined property sets
        for propset_name, property_set in material_data.items():

            if "Behavior" in property_set.qualifiers.keys():
                propset_name += "::" + property_set.qualifiers["Behavior"]

            # check if the Material object supports this property set
            if propset_name in PROPERTY_MAP.keys():
                parameter_map = PROPERTY_MAP[propset_name]

                for property_name in parameter_map["properties"]:
                    param = property_set.parameters[property_name]
                    value = param.data
                    if isinstance(value, Sequence):
                        if len(value) > 1:
                            raise RuntimeError(
                                f"Only constant material properties are supported ATM. "
                                f"Value of `{property_name}` is `{value}`"
                            )
                        value = value[0]
                    models.append(Constant(property_name, value))
                for matml_key, mapped_properties in parameter_map["mappings"].items():
                    param = property_set.parameters[matml_key]
                    value = param.data
                    if isinstance(value, Sequence):
                        if len(value) > 1:
                            raise RuntimeError(
                                f"Only constant material properties are supported ATM. "
                                f"Value of `{matml_key}` is `{value}`"
                            )
                        value = value[0]
                    for mapped_property in mapped_properties:
                        models.append(Constant(mapped_property, value))
        materials.append(
            Material(
                material_name=mat_id,
                material_id=str(global_material_index),
                models=models,
            )
        )

        global_material_index += 1

    return materials
