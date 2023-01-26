"""Provides the ``mapdl_reader`` module."""
from typing import Dict

from ansys.mapdl.core.mapdl import _MapdlCore

from ansys.materials.manager.material import Material

from .mpdata_parser import MP_MATERIAL_HEADER_REGEX, _MaterialDataParser


def read_mapdl(mapdl: _MapdlCore) -> Dict[str, Material]:
    """
    Read materials from a provided MAPDL session.

    Returns them indexed by the material ID.

    Parameters
    ----------
    mapdl : _MapdlCore
        Active pyMAPDL session.

    Returns
    -------
    Dict[str, Material]
        Materials currently active in the MAPDL session, indexed by their material ID.
    """
    materials = []
    data = mapdl.mplist()
    material_ids = list(MP_MATERIAL_HEADER_REGEX.findall(data))
    for material_id in material_ids:
        material_properties = _MaterialDataParser.parse_material(data, int(material_id))
        materials.append(Material("", material_id, models=material_properties))
    return {
        material.material_id: material for material in materials if material.material_id is not None
    }
