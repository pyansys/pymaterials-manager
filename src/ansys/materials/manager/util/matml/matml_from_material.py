import os
from typing import Dict, Sequence, Union
import xml.etree.ElementTree as ET

from ansys.materials.manager.material import Material

from .matml_parser import (
    BULKDATA_KEY,
    MATERIALS_ELEMENT_KEY,
    MATML_DOC_KEY,
    METADATA_KEY,
    UNITLESS_KEY,
    WBTRANSFER_KEY
)
from .matml_property_map import MATML_PROPERTY_MAP

_PATH_TYPE = Union[str, os.PathLike]

ROOT_ELEMENT = "EngineeringData"
VERSION = "18.0.0.60"
VERSION_DATE = "29.08.2016 15:02:00"


# todo: convert into class


def _inverse_property_map(properties_map: Dict) -> Dict:
    inverse_map = {}
    for key, prop_codes in properties_map.items():
        for prop in prop_codes:
            inverse_map[prop] = key

    return inverse_map


def _add_parameters(
    property_element: ET.Element,
    material: Material,
    parameters: Sequence[str],
    metadata_parameters: Dict,
):
    # add the parameters of a property set to the tree

    for key in parameters:
        if key in metadata_parameters.keys():
            para_key = metadata_parameters[key]
        else:
            index = len(metadata_parameters) + 1
            para_key = f"pa{index}"
            metadata_parameters[key] = para_key

        param_element = ET.SubElement(
            property_element, "ParameterValue", {"parameter": para_key, "format": "float"}
        )
        data_element = ET.SubElement(param_element, "Data")
        data_element.text = str(material.get_model_by_name(key)[0].value)
        qualifier_element = ET.SubElement(param_element, "Qualifier", {"name": "Variable Type"})
        qualifier_element.text = "Dependent"


def _add_property_set(
    bulkdata_element: ET.Element,
    material: Material,
    property_set_name: str,
    parameter_map: Dict,
    behavior: str,
    metadata_properties: Dict,
    metadata_parameters: Dict,
):
    """Add the property set to the XML tree."""
    # check if at least one parameter is specified
    available_mat_properties = [model.name for model in material.models]
    property_set_parameters = parameter_map["properties"]
    property_set_parameters.extend(
        mapped_properties for matml_key, mapped_properties in parameter_map["mappings"].items()
    )

    parameters = list(set(property_set_parameters) & set(available_mat_properties))

    if len(parameters) > 0:
        # get property id from metadata or add it if it does not exist yet
        if property_set_name in metadata_properties.keys():
            property_id = metadata_properties[property_set_name]
        else:
            index = len(metadata_properties) + 1
            property_id = f"pr{index}"
            metadata_properties[property_set_name] = property_id

        property_data_element = ET.SubElement(
            bulkdata_element, "PropertyData", {"property": property_id}
        )
        data_element = ET.SubElement(property_data_element, "Data", {"format": "string"})
        data_element.text = "-"
        if behavior:
            behavior_element = ET.SubElement(
                property_data_element, "Qualifier", {"name": "Behavior"}
            )
            behavior_element.text = behavior

        _add_parameters(property_data_element, material, parameters, metadata_parameters)


def _add_materials(
    materials: Sequence[Material],
    materials_element: ET.Element,
    metadata_properties: Dict,
    metadata_parameters: Dict,
):
    """Add the material data to the XML tree."""
    for material in materials:
        mat_element = ET.SubElement(materials_element, "Material")
        bulkdata_element = ET.SubElement(mat_element, BULKDATA_KEY)
        name_element = ET.SubElement(bulkdata_element, "Name")
        name_element.text = material.name

        for property_set_name, parameters in MATML_PROPERTY_MAP.items():
            # property sets are exported as orthotropic if it can have an isotropic or
            # orthotropic representation,
            if len(property_set_name.split("::")) == 2:
                behavior = property_set_name.split("::")[1]
            else:
                behavior = ""
            if behavior != "Isotropic":
                _add_property_set(
                    bulkdata_element,
                    material,
                    property_set_name.split("::")[0],
                    parameters,
                    behavior,
                    metadata_properties,
                    metadata_parameters,
                )


def _add_metadata(metadata_element: ET.Element, property_set_dict: Dict, parameter_set_dict: Dict):
    # add the metadata to the XML tree
    for key, value in property_set_dict.items():
        prop_element = ET.SubElement(metadata_element, "PropertyDetails", {"id": value})
        ET.SubElement(prop_element, UNITLESS_KEY)
        name_element = ET.SubElement(prop_element, "Name")
        name_element.text = key

    for key, value in parameter_set_dict.items():
        prop_element = ET.SubElement(metadata_element, "ParameterDetails", {"id": value})
        ET.SubElement(prop_element, UNITLESS_KEY)
        name_element = ET.SubElement(prop_element, "Name")
        name_element.text = key


def _add_transfer_ids(root: ET.Element, materials: Sequence[Material]) -> None:
    # add the WB transfer IDs to the XML tree
    wb_transfer_element = ET.SubElement(root, WBTRANSFER_KEY)
    materials_element = ET.SubElement(wb_transfer_element, MATERIALS_ELEMENT_KEY)
    for mat in materials:
        mat_element = ET.SubElement(materials_element, "Material")
        name_element = ET.SubElement(mat_element, "Name")
        name_element.text = mat.name
        transfer_element = ET.SubElement(mat_element, "DataTransferID")
        transfer_element.text = mat.uuid

def write_matml(path: _PATH_TYPE, materials: Sequence[Material]):
    """
    Write a Matml (engineering data xml file from scratch).

    Parameters
    ----------
    path:
        File path
    materials:
        list of materials
    """
    root = ET.Element(ROOT_ELEMENT)
    tree = ET.ElementTree(root)

    root.attrib["version"] = VERSION
    root.attrib["versiondate"] = VERSION_DATE
    notes_element = ET.SubElement(root, "Notes")
    notes_element.text = "Engineering data xml file generated by pyMaterials."

    materials_element = ET.SubElement(root, MATERIALS_ELEMENT_KEY)
    matml_doc_element = ET.SubElement(materials_element, MATML_DOC_KEY)

    metadata_property_set = {}
    metadata_parameters = {}

    _add_materials(materials, matml_doc_element, metadata_property_set, metadata_parameters)

    # add metadata to the XML tree
    metadata_element = ET.SubElement(matml_doc_element, METADATA_KEY)
    _add_metadata(metadata_element, metadata_property_set, metadata_parameters)

    # add transfer id to the XML tree
    _add_transfer_ids(root, materials)

    print(f"write xml to {path}")
    tree.write(path)
