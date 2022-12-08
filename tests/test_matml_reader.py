import os

from ansys.materials.manager.util.matml import MatmlReader

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMatmlReader:
    def test_reader(self):
        """read a xml file with steel and e-glass UD"""
        xml_file_path = os.path.join(dir_path, "data", "steel_eglass_ud.xml")
        reader = MatmlReader(xml_file_path)
        num_materials = reader.parse_matml()
        assert num_materials == 2
        assert len(reader.transfer_ids) == 2

        steel = reader.get_material("Structural Steel")


        cte = "Coefficient of Thermal Expansion"
        assert steel[cte].name == cte
        assert steel[cte].parameters[cte].name == cte
        assert steel[cte].parameters[cte].data == 1.2e-5
        assert steel[cte].parameters[cte].qualifiers["Variable Type"] == "Dependent"

        rho = "Density"
        assert steel[rho].name == rho
        assert steel[rho].parameters[rho].name == rho
        assert steel[rho].parameters[rho].data == 7850.0
        assert steel[rho].parameters[rho].qualifiers["Variable Type"] == "Dependent"
        assert steel[rho].parameters["Options Variable"].name == "Options Variable"
        assert steel[rho].parameters["Options Variable"].data == "Interpolation Options"
        assert (
            steel[rho].parameters["Options Variable"].qualifiers["AlgorithmType"]
            == "Linear Multivariate (Qhull)"
        )
        assert (
            steel[rho].parameters["Temperature"].qualifiers["Lower Limit"] == "Program Controlled"
        )

        elast = "Elasticity"
        e_glass_ud = reader.get_material("Epoxy E-Glass UD")
        assert e_glass_ud[elast].name == elast
        assert e_glass_ud[elast].parameters["Poisson's Ratio XY"].name == "Poisson's Ratio XY"
        assert e_glass_ud[elast].parameters["Poisson's Ratio XY"].data == 0.3
        assert (
            e_glass_ud[elast].parameters["Poisson's Ratio XY"].qualifiers["Variable Type"]
            == "Dependent"
        )
        assert e_glass_ud[elast].parameters["Shear Modulus YZ"].name == "Shear Modulus YZ"
        assert e_glass_ud[elast].parameters["Shear Modulus YZ"].data == 3846150000.0
        assert (
            e_glass_ud[elast].parameters["Shear Modulus YZ"].qualifiers["Variable Type"]
            == "Dependent"
        )
        assert e_glass_ud[elast].qualifiers["Behavior"] == "Orthotropic"
        assert e_glass_ud[elast].qualifiers["Field Variable Compatible"] == "Temperature"
