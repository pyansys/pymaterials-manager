import copy
from typing import Dict

from ansys.mapdl.core.mapdl import _MapdlCore

from ansys.materials.manager.material import Material

from .mpdata_parser import MP_MATERIAL_HEADER_REGEX, _MaterialDataParser
from .output_format import get_format, set_format


def read_mapdl(mapdl: _MapdlCore) -> Dict[str, Material]:
    """
    Read materials from a provided MAPDL session.

    Returns them indexed by the material ID.

    Parameters
    ----------
    mapdl: _MapdlCore
        Active pyMAPDL session

    Returns
    -------
    Dict[str, Material]
        Materials currently active in the MAPDL session, indexed by their material ID.
    """
    materials = []
    current_format_settings = get_format(mapdl)
    new_format_settings = copy.copy(current_format_settings)
    new_format_settings["nwidth"] = 32
    new_format_settings["dsignf"] = 25
    set_format(mapdl, new_format_settings)
    data = mapdl.mplist()
    set_format(mapdl, current_format_settings)
    material_ids = list(MP_MATERIAL_HEADER_REGEX.findall(data))
    for material_id in material_ids:
        material_properties = _MaterialDataParser.parse_material(data, int(material_id))
        materials.append(Material("", material_id, models=material_properties))
    return {
        material.material_id: material for material in materials if material.material_id is not None
    }
