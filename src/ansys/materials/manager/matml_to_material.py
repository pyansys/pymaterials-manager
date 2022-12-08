from collections.abc import Iterable
from typing import Dict, Sequence

from .material import Material
from .matml_property_map import MATML_PROPERTY_MAP

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

        converted_properties = {}
        # loop over the defined property sets
        for propset_name, property_set in material_data.items():

            if "Behavior" in property_set.qualifiers.keys():
                propset_name += "::" + property_set.qualifiers["Behavior"]

            # check if the Material object supports this property set
            if propset_name in MATML_PROPERTY_MAP.keys():
                parameter_map = MATML_PROPERTY_MAP[propset_name]

                for matml_key, prop_codes in parameter_map.items():
                    param = property_set.parameters[matml_key]
                    value = param.data
                    if isinstance(value, Iterable):
                        if len(value) > 1:
                            raise RuntimeError(
                                f"Only constant material properties are supported ATM. "
                                f"Value of `{matml_key}` is `{value}`"
                            )
                        value = value[0]
                    converted_properties.update([(prop_code, value) for prop_code in prop_codes])

        materials.append(
            Material(
                material_name=mat_id,
                material_id=global_material_index,
                properties=converted_properties,
            )
        )

        global_material_index += 1

    return materials
