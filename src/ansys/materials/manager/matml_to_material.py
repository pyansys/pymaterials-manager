from .property_codes import PropertyCode
from .material import Material

from collections.abc import Iterable
from typing import Dict, Sequence

PROPERTY_MAP = {
    "Density": {"Density": [PropertyCode.DENS]},
    "Elasticity": {"Young's Modulus": [PropertyCode.EX, PropertyCode.EY, PropertyCode.EZ],
                   "Shear Modulus": [PropertyCode.GXY, PropertyCode.GXZ, PropertyCode.GYZ]}
}

def convert_matml_materials(materials_dict: Dict,
                            index_offset: int) -> Sequence[Material]:
    """Convert a list of materials into Material objects.

    Parameters
    ----------
    material_data:
        dict of raw material data from a matml import
    index_offset:
        int to offset the material id (numbers) to avoid conflicts

    Returns a list of Material objects
    """

    materials = []

    global_material_index = 1 + index_offset
    # loop over the materials
    for id, material_data in materials_dict.items():
        name = id

        converted_properties = {}
        # loop over the supported property sets
        for property_set_key, matml_properties in PROPERTY_MAP.items():

            # check if the property set is defined for this material
            if property_set_key in material_data.keys():

                # convert properties from MATML to Material properties
                property_set = material_data[property_set_key]
                for param_key, property_codes in matml_properties.items():
                    value = property_set[param_key]
                    if isinstance(value, Iterable):
                        if len(value) > 1:
                            raise RuntimeError("Only constant material properties are supported ATM.")
                        value = value[0]
                    converted_properties.update([(prop_code, value) for prop_code in property_codes])

        materials.append(Material(material_name=name,
                                  material_id=global_material_index,
                                  properties=converted_properties)
                         )

        global_material_index += 1

    return materials

