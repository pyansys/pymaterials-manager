"""Provides the ``matml_parser`` module."""
from dataclasses import dataclass
import os
from typing import Any, Dict, Union
import xml.etree.ElementTree as ET

_PATH_TYPE = Union[str, os.PathLike]

MATERIALS_ELEMENT_KEY = "Materials"
MATML_DOC_KEY = "MatML_Doc"
METADATA_KEY = "Metadata"
BULKDATA_KEY = "BulkDetails"
UNITLESS_KEY = "Unitless"
BEHAVIOR_KEY = "Behavior"
WBTRANSFER_KEY = "ANSYSWBTransferData"
MAT_TRANSFER_ID = "DataTransferID"


# Todos:
#   variable material properties with interpolation settings
#   version handling
#   support of units (exponents)


@dataclass
class Parameter:
    """Define a parameter such as density or Young's Modulus."""

    # todo: units

    name: str
    data: Any
    qualifiers: Dict


@dataclass
class PropertySet:
    """Define a PropertySet which contains one or several parameters."""

    name: str
    parameters: Dict
    qualifiers: Dict


class MatmlReader:
    """
    Parse a MATML (engineering data xml) file.

    Fills a nested dict with all the materials and their properties.
    The key of the first layer are the material names.
    The conversion into a specific format/object representation is implemented separately.

    The data can be accessed via matml_reader.materials
    """

    materials: Dict
    transfer_ids = Dict
    matml_file_path: _PATH_TYPE

    def __init__(self, file_path: _PATH_TYPE):
        """
        Create a new MATML reader object.

        Parameters
        ----------
        file_path :
            Matml (engineering data xml) file path
        """
        self.matml_file_path = file_path
        if not os.path.exists(file_path):
            raise RuntimeError(f"Cannot initialize MatmlReader {file_path}. File does not exist!")

    def _convert(self, data: str, target: str) -> Union[str, float]:
        # convert a string into a certain format (e.g. float)

        if target == "string":
            return data

        if target != "float":
            raise RuntimeError(f"unsupported format {target}. Skipped formatting {data}")

        if not data or not data.strip():
            return 0.0

        if data.count(",") > 0:
            data = data.split(",")
            return [float(v) for v in data]
        else:
            return float(data)

    def _read_metadata(self, metadata_node: Any) -> Dict:
        # Read the metadata

        data = {}
        for item in metadata_node.iter("ParameterDetails"):
            id = item.attrib["id"]
            name = item.find("Name").text
            if item.find(UNITLESS_KEY) is not None:
                unit = item.find(UNITLESS_KEY).tag
            elif item.find("Units") is not None:
                unit = item.find("Units").attrib["name"]
            else:
                raise RuntimeError(f"unhandled case {id}")

            data[id] = {"Name": name, "Units": unit}

        for item in metadata_node.iter("PropertyDetails"):
            id = item.attrib["id"]
            name = item.find("Name").text
            unit = UNITLESS_KEY

            data[id] = {"Name": name, "Units": unit}

        return data

    def _read_qualifiers(self, property_node: Any) -> Dict:
        # returns the qualifiers such as behavior, interpolation options etc.
        qualifiers = {}
        for item in property_node.findall("Qualifier"):
            qualifiers[item.attrib["name"]] = item.text
        return qualifiers

    def _read_property_sets_and_parameters(self, bulkdata: Any, metadata_dict: Dict) -> Dict:
        prop_dict = {}

        # iterate over the property sets
        for prop_data in bulkdata.findall("PropertyData"):
            property_key = prop_data.attrib["property"]
            property_name = metadata_dict[property_key]["Name"]
            prop_set_qualifiers = self._read_qualifiers(prop_data)

            parameters = {}

            # iterate over each parameter
            for parameter in prop_data.findall("ParameterValue"):
                parameter_key = parameter.attrib["parameter"]
                parameter_name = metadata_dict[parameter_key]["Name"]
                parameter_format = parameter.attrib["format"]
                param_qualifiers = self._read_qualifiers(parameter)
                data = self._convert(parameter.find("Data").text, parameter_format)

                parameters[parameter_name] = Parameter(
                    name=parameter_name, data=data, qualifiers=param_qualifiers
                )

            prop_dict[property_name] = PropertySet(
                name=property_name, qualifiers=prop_set_qualifiers, parameters=parameters
            )

        return prop_dict

    def _read_materials(self, matml_doc_node: Any, metadata_dict: Dict) -> Dict:
        # Import the material properties and parameters

        materials = {}
        for material in matml_doc_node.findall("Material"):
            bulkdata = material.find("BulkDetails")
            name = bulkdata.find("Name").text
            data = self._read_property_sets_and_parameters(bulkdata, metadata_dict)
            materials[name] = data

        return materials

    def _read_transfer_ids(self, root: ET.Element) -> int:
        # reads the material transfer IDs
        self.transfer_ids = {}
        wb_transfer_element = root.find(WBTRANSFER_KEY)
        if wb_transfer_element:
            materials_element = wb_transfer_element.find(MATERIALS_ELEMENT_KEY)
            for mat in materials_element.findall("Material"):
                mat_name = mat.find("Name").text
                transfer_id_element = mat.find(MAT_TRANSFER_ID)

                if not mat_name in self.materials.keys():
                    raise RuntimeError(f"Transfer ID could not be set for material {mat_name}")

                self.transfer_ids[mat_name] = transfer_id_element.text

        return len(self.transfer_ids)

    def parse_matml(self) -> bool:
        """Read MATML (engineering data XML) file.

        Output can be consumed via matml_reader.materials or
        matml_reader.get_material(name).

        Returns the number of imported materials.
        """
        tree = ET.parse(self.matml_file_path)
        root = tree.getroot()
        materials_node = root.find(MATERIALS_ELEMENT_KEY)
        if not materials_node:
            raise RuntimeError(
                "Materials node not found. Please check if this is a valid MATML file."
            )

        matml_doc_node = materials_node.find(MATML_DOC_KEY)
        if not matml_doc_node:
            raise RuntimeError("MATML node not found. Please check if this is a valid MATML file.")

        metadata_node = matml_doc_node.find(METADATA_KEY)
        if not metadata_node:
            raise RuntimeError(
                "Metadata node not found. Please check if this is a valid MATML file."
            )
        metadata_dict = self._read_metadata(metadata_node)

        self.materials = self._read_materials(matml_doc_node, metadata_dict)

        self._read_transfer_ids(root)
        return len(self.materials)

    def get_material(self, name: str) -> Dict:
        """Return a certain material."""
        if not name in self.materials.keys():
            available_keys = ", ".join(self.materials.keys())
            raise RuntimeError(
                f"Material {name} does not exist. Available materials are {available_keys}"
            )

        return self.materials[name]
