import os
import tempfile

from ansys.materials.manager.util.matml.matml_from_material import write_matml
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMatmlFromMaterial:
    def test_matml_from_material(self):
        """Verify that materials can be exported as XML"""

        xml_file_path = os.path.join(dir_path, "data", "steel_eglass_ud.xml")
        reader_engd = MatmlReader(xml_file_path)
        num_materials = reader_engd.parse_matml()
        assert num_materials == 2

        mapdl_materials = convert_matml_materials(
            reader_engd.materials, reader_engd.transfer_ids, 0
        )

        with tempfile.TemporaryDirectory() as tmpdirname:
            export_path = os.path.join(tmpdirname, "engd.xml")
            write_matml(export_path, mapdl_materials)

            reader_materials_manager = MatmlReader(export_path)
            num_materials = reader_materials_manager.parse_matml()
            assert num_materials == 2
