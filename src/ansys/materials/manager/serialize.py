import json
from typing import Dict

from ansys.materials.manager.material import Material


def _material_as_dict(material: Material) -> Dict:
    d = {"name": material.name, "reference_temperature": material.reference_temperature}
    if material.material_id is not None:
        d.update({"id": material.material_id})
    for model in material.models:
        if isinstance(model.value, str):
            propData = {"option": model.value}
        else:
            propData = {"option": "constant", "value": model.value}
        d.update({model.name: propData})
    return d


def serialize_material(material: Material) -> str:
    d = _material_as_dict(material)
    return json.dumps(d)


def serialize_material_to_file(material: Material, fileName: str):
    sm = serialize_material(material)
    with open(fileName, "w") as f:
        f.write(sm)
