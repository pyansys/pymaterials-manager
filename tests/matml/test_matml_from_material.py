import os
import tempfile

import pytest

from ansys.materials.manager._models import Constant
from ansys.materials.manager.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMatmlFromMaterial:
    def test_roundtrip_from_to(self):
        """Verify that materials can be exported to Matml after loading them from a Matml"""

        xml_file_path = os.path.join(dir_path, "..", "data", "steel_eglass_air.xml")
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

            reader_materials_manager = MatmlReader(export_path)
            num_materials = reader_materials_manager.parse_matml()
            assert num_materials == 3

    def test_matml_from_material(self):
        """Verify that manually constructed materials can be exported"""
        material = Material("Steel", material_id="1")
        material.models.append(Constant("Density", 25.0))
        material.models.append(Constant("Young's Modulus X Direction", 210e9))
        material.models.append(Constant("Young's Modulus Y Direction", 210e9))
        material.models.append(Constant("Young's Modulus Z Direction", 210e9))
        material.models.append(Constant("Poisson's Ratio XY", 0.3))
        material.models.append(Constant("Poisson's Ratio XZ", 0.3))
        material.models.append(Constant("Poisson's Ratio YZ", 0.3))
        material.models.append(Constant("Shear Modulus XY", 80769230769.23077))
        material.models.append(Constant("Shear Modulus XZ", 80769230769.23077))
        material.models.append(Constant("Shear Modulus YZ", 80769230769.23077))

        with tempfile.TemporaryDirectory() as tmpdirname:
            export_path = os.path.join(tmpdirname, "engd.xml")
            matml_writer = MatmlWriter([material])
            matml_writer.export(export_path)

            reader = MatmlReader(export_path)
            reader.parse_matml()
            imported_materials = convert_matml_materials(reader.materials, reader.transfer_ids, 0)
            assert len(imported_materials) == 1
            steel = imported_materials[0]

            expected_results = {
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
            }
            for name, expected_value in expected_results.items():
                assigned_model = steel.get_model_by_name(name)
                assert len(assigned_model) == 1
                assert assigned_model[0].value == pytest.approx(expected_value)
