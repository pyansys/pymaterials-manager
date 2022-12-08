import json
import pathlib
from typing import Dict, Union

from ansys.materials.manager._models import Constant
from ansys.materials.manager.material import Material


def _material_as_dict(material: Material) -> Dict:
    d = {"name": material.name}
    if material.material_id is not None:
        d.update({"id": material.material_id})
    for model in material.models:
        if isinstance(model, Constant):
            propData = {"option": "constant", "value": model.value}
        else:
            propData = {"option": "ideal_gas"}
        d.update({model.name: propData})
    return d


def serialize_material(material: Material) -> str:
    """
    Output json representation of a material in fluent format.

    Parameters
    ----------
    material: Material
        Material to be serialized

    Returns
    -------
    str
        String representation of a material in fluent format.
    """
    d = _material_as_dict(material)
    return json.dumps(d)


def serialize_material_to_file(material: Material, file_name: Union[str, pathlib.Path]):
    """
    Output json representation of a material in fluent format to a file.

    Parameters
    ----------
    material: Material
        Material to be serialized
    file_name: Union[str, pathlib.Path]
        Name of file to be created
    """
    sm = serialize_material(material)
    with open(file_name, "w", encoding="utf8") as f:
        f.write(sm)
