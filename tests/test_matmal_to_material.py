
from ansys.materials.manager.matml_parser import MatmlReader
from ansys.materials.manager.matml_to_material import convert_matml_materials
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMatmlToMaterial:

    def test_conversion_to_material_object(self):
        """read a xml file with steel and e-glass UD"""
        xml_file_path = os.path.join(dir_path, "data", "steel_eglass_ud.xml")
        reader = MatmlReader(xml_file_path)
        num_materials = reader.parse_matml()
        assert num_materials == 2

        materials = convert_matml_materials(reader.materials, 0)

        steel = materials[0]

        assert steel.material_id == 1
        assigned_properties = steel.get_properties()
        assert len(assigned_properties) == 7

