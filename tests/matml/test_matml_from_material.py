import os
import tempfile
import pytest
import xml.etree.ElementTree as ET

from ansys.materials.manager._models import Constant
from ansys.materials.manager.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class TestMatmlFromMaterial:
    def test_roundtrip_from_to(self):
        """Verify that materials can be exported to Matml after loading them from a Matml"""

        xml_file_path = os.path.join(DIR_PATH, "..", "data", "steel_eglass_air.xml")
        reader_engd = MatmlReader(xml_file_path)
        num_materials = reader_engd.parse_matml()
        assert num_materials == 3

        mapdl_materials = convert_matml_materials(
            reader_engd.materials, reader_engd.transfer_ids, 0
        )

        with tempfile.TemporaryDirectory() as tmpdirname:
            export_path = os.path.join(tmpdirname, "engd.xml")
            matml_writer = MatmlWriter(mapdl_materials)
            matml_writer.export(export_path)
            matml_writer2 = MatmlWriter(mapdl_materials[1:3])
            matml_writer2.export(r"D:\tmp\test2.xml")

            matml_writer2 = MatmlWriter(mapdl_materials)
            matml_writer2.export(r"D:\tmp\test3.xml")

            reader_materials_manager = MatmlReader(export_path)
            num_materials = reader_materials_manager.parse_matml()
            assert num_materials == 3

            tree = ET.parse(export_path)
            ref_tree = ET.parse(os.path.join(DIR_PATH, "..", "data", "ref_steel_eglass_air.xml"))
            assert ET.tostring(tree.getroot()) == ET.tostring(ref_tree.getroot())



    def test_matml_from_material(self):
        """
        Verify that manually constructed materials can be exported to matml.
        The matml is imported back and the data is compared with the initial values.
        """
        material = Material("Steel", material_id="1")

        parameters = {
            "density": 25.0,
            "young's modulus x direction": 210e9,
            "young's modulus y direction": 210e9,
            "young's modulus z direction": 210e9,
            "shear modulus xy": 80769230769.23077,
            "shear modulus yz": 80769230769.23077,
            "shear modulus xz": 80769230769.23077,
            "poisson's ratio xy": 0.3,
            "poisson's ratio yz": 0.3,
            "poisson's ratio xz": 0.3,
            "thermal expansion coefficient x direction": -1e-6,
            "thermal expansion coefficient y direction": 1e-4,
            "thermal expansion coefficient z direction": 2.3e-4,
            "specific heat capacity": 435.0,
            "thermal conductivity x direction": 30.0,
            "thermal conductivity y direction": 56.0,
            "thermal conductivity z direction": 35.0,
            "viscosity": 2333.0,
            "speed of sound": 1100.0,
        }

        for key, value in parameters.items():
            material.models.append(Constant(key, value))

        with tempfile.TemporaryDirectory() as tmpdirname:
            export_path = os.path.join(tmpdirname, "engd.xml")
            matml_writer = MatmlWriter([material])
            matml_writer.export(export_path)

            reader = MatmlReader(export_path)
            reader.parse_matml()
            imported_materials = convert_matml_materials(reader.materials, reader.transfer_ids, 0)
            assert len(imported_materials) == 1
            steel = imported_materials[0]

            for name, expected_value in parameters.items():
                assigned_model = steel.get_model_by_name(name)
                assert len(assigned_model) == 1
                assert assigned_model[0].value == pytest.approx(expected_value)
