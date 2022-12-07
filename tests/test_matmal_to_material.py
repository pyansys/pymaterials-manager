
from ansys.materials.manager.matml_parser import MatmlReader
from ansys.materials.manager.matml_to_material import convert_matml_materials
from ansys.materials.manager.property_codes import PropertyCode
import os
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
        assigned_properties = steel.get_properties()
        assert len(assigned_properties) == 11
        assert assigned_properties[PropertyCode.REFT] == 0.0
        assert assigned_properties[PropertyCode.DENS] == 7850.0
        assert assigned_properties[PropertyCode.EX] == 200000000000.0
        assert assigned_properties[PropertyCode.EY] == 200000000000.0
        assert assigned_properties[PropertyCode.EZ] == 200000000000.0
        assert assigned_properties[PropertyCode.GXY] == 76923076923.0769
        assert assigned_properties[PropertyCode.GXZ] == 76923076923.0769
        assert assigned_properties[PropertyCode.GYZ] == 76923076923.0769
        assert assigned_properties[PropertyCode.PRXY] == 0.3
        assert assigned_properties[PropertyCode.PRXZ] == 0.3
        assert assigned_properties[PropertyCode.PRYZ] == 0.3

        eglass = materials[1]
        assert eglass.material_id == 5
        assigned_properties = eglass.get_properties()
        assert len(assigned_properties) == 11
        assert assigned_properties[PropertyCode.REFT] == 0.0
        assert assigned_properties[PropertyCode.DENS] == 2000.0
        assert assigned_properties[PropertyCode.EX] == 45000000000.0
        assert assigned_properties[PropertyCode.EY] == 10000000000.0
        assert assigned_properties[PropertyCode.EZ] == 10000000000.0
        assert assigned_properties[PropertyCode.GXY] == 5000000000.0
        assert assigned_properties[PropertyCode.GXZ] == 5000000000.0
        assert assigned_properties[PropertyCode.GYZ] == 3846150000.0
        assert assigned_properties[PropertyCode.PRXY] == 0.3
        assert assigned_properties[PropertyCode.PRXZ] == 0.3
        assert assigned_properties[PropertyCode.PRYZ] == 0.4


