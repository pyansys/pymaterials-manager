import os

import pytest

from ansys.materials.manager.util.matml import MatmlReader, convert_matml_materials

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMatmlToMaterial:
    def test_conversion_to_material_object(self):
        """read a xml file with steel and e-glass UD"""
        xml_file_path = os.path.join(dir_path, "data", "steel_eglass_ud.xml")
        reader = MatmlReader(xml_file_path)
        num_materials = reader.parse_matml()
        assert num_materials == 2

        materials = convert_matml_materials(reader.materials, 3)

        steel = materials[0]

        assert steel.material_id == 4
        assigned_models = steel.models
        assert len(assigned_models) == 11

        expected_results = {
            "strain reference temperature": 0.0,
            "density": 7850.0,
            "young's modulus x direction": 200000000000.0,
            "young's modulus y direction": 200000000000.0,
            "young's modulus z direction": 200000000000.0,
            "shear modulus xy": 76923076923.0769,
            "shear modulus yz": 76923076923.0769,
            "shear modulus xz": 76923076923.0769,
            "poisson's ratio xy": 0.3,
            "poisson's ratio yz": 0.3,
            "poisson's ratio xz": 0.3,
        }
        for name, expected_value in expected_results.items():
            assigned_model = steel.get_model_by_name(name)
            assert len(assigned_model) == 1
            assert assigned_model[0].value == pytest.approx(expected_value)

        eglass = materials[1]
        assert eglass.material_id == 5
        assigned_models = eglass.models
        assert len(assigned_models) == 11

        expected_results = {
            "strain reference temperature": 0.0,
            "density": 2000.0,
            "young's modulus x direction": 45000000000.0,
            "young's modulus y direction": 10000000000.0,
            "young's modulus z direction": 10000000000.0,
            "shear modulus xy": 5000000000.0,
            "shear modulus yz": 3846150000.0,
            "shear modulus xz": 5000000000.0,
            "poisson's ratio xy": 0.3,
            "poisson's ratio yz": 0.4,
            "poisson's ratio xz": 0.3,
        }
        for name, expected_value in expected_results.items():
            assigned_model = eglass.get_model_by_name(name)
            assert len(assigned_model) == 1
            assert assigned_model[0].value == pytest.approx(expected_value)
