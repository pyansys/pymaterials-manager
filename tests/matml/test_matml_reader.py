# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from typing import Dict

import pytest

from ansys.materials.manager.util.matml import MatmlReader

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

STEEL_ID = "Structural Steel"
EPOXY_GLASS_ID = "Epoxy E-Glass UD"
AIR_ID = "Air"


class TestMatmlReader:
    xml_file_path = os.path.join(DIR_PATH, "..", "data", "steel_eglass_air.xml")

    def check_steel(self, steel_data: Dict) -> None:
        assert len(steel_data) == 16
        cte = "Coefficient of Thermal Expansion"
        assert steel_data[cte].name == cte
        assert steel_data[cte].parameters[cte].name == cte
        assert steel_data[cte].parameters[cte].data == 1.2e-5
        assert steel_data[cte].parameters[cte].qualifiers["Variable Type"] == "Dependent"

        rho = "Density"
        assert steel_data[rho].name == rho
        assert steel_data[rho].parameters[rho].name == rho
        assert steel_data[rho].parameters[rho].data == 7850.0
        assert steel_data[rho].parameters[rho].qualifiers["Variable Type"] == "Dependent"
        assert steel_data[rho].parameters["Options Variable"].name == "Options Variable"
        assert steel_data[rho].parameters["Options Variable"].data == "Interpolation Options"
        assert (
            steel_data[rho].parameters["Options Variable"].qualifiers["AlgorithmType"]
            == "Linear Multivariate (Qhull)"
        )
        assert (
            steel_data[rho].parameters["Temperature"].qualifiers["Lower Limit"]
            == "Program Controlled"
        )

    def check_glass(self, glass_data: Dict) -> None:
        assert len(glass_data) == 13
        elast = "Elasticity"
        assert glass_data[elast].name == elast
        assert glass_data[elast].parameters["Poisson's Ratio XY"].name == "Poisson's Ratio XY"
        assert glass_data[elast].parameters["Poisson's Ratio XY"].data == 0.3
        assert (
            glass_data[elast].parameters["Poisson's Ratio XY"].qualifiers["Variable Type"]
            == "Dependent"
        )
        assert glass_data[elast].parameters["Shear Modulus YZ"].name == "Shear Modulus YZ"
        assert glass_data[elast].parameters["Shear Modulus YZ"].data == 3846150000.0
        assert (
            glass_data[elast].parameters["Shear Modulus YZ"].qualifiers["Variable Type"]
            == "Dependent"
        )
        assert glass_data[elast].qualifiers["Behavior"] == "Orthotropic"
        assert glass_data[elast].qualifiers["Field Variable Compatible"] == "Temperature"

    def check_air(self, air_data: Dict) -> None:
        assert len(air_data) == 20
        assert air_data["Viscosity"].parameters["Viscosity"].data == 1.7894e-05

    def test_reader_legacy(self):
        reader = MatmlReader(self.xml_file_path)
        with pytest.warns(DeprecationWarning):
            num_materials = reader.parse_matml()
        assert num_materials == 3
        assert len(reader.transfer_ids) == 3

        assert reader.transfer_ids[AIR_ID] == "370e7536-77c0-11ed-8eeb-6c6a77744180"
        assert reader.transfer_ids[EPOXY_GLASS_ID] == "a1f2e775-77fe-4ad6-a822-54d353e0ea0e"
        assert reader.transfer_ids[STEEL_ID] == "636a7e55-fe81-4d04-9d98-a2cdd31e962a"

        with pytest.warns(DeprecationWarning):
            steel = reader.get_material(STEEL_ID)
            e_glass_ud = reader.get_material(EPOXY_GLASS_ID)
            air = reader.get_material(AIR_ID)

        self.check_air(air)
        self.check_glass(e_glass_ud)
        self.check_steel(steel)

    def test_read_from_file(self):
        parsed_data = MatmlReader.parse_from_file(self.xml_file_path)

        assert len(parsed_data) == 3

        air = parsed_data[AIR_ID]["material"]
        e_glass_ud = parsed_data[EPOXY_GLASS_ID]["material"]
        steel = parsed_data[STEEL_ID]["material"]

        assert parsed_data[AIR_ID]["transfer_id"] == "370e7536-77c0-11ed-8eeb-6c6a77744180"
        assert parsed_data[EPOXY_GLASS_ID]["transfer_id"] == "a1f2e775-77fe-4ad6-a822-54d353e0ea0e"
        assert parsed_data[STEEL_ID]["transfer_id"] == "636a7e55-fe81-4d04-9d98-a2cdd31e962a"

        self.check_air(air)
        self.check_glass(e_glass_ud)
        self.check_steel(steel)

    def test_read_from_text(self):
        with open(self.xml_file_path, "r", encoding="utf8") as fp:
            matml_data = fp.read()
        parsed_data = MatmlReader.parse_text(matml_data)

        assert len(parsed_data) == 3

        air = parsed_data[AIR_ID]["material"]
        e_glass_ud = parsed_data[EPOXY_GLASS_ID]["material"]
        steel = parsed_data[STEEL_ID]["material"]

        assert parsed_data[AIR_ID]["transfer_id"] == "370e7536-77c0-11ed-8eeb-6c6a77744180"
        assert parsed_data[EPOXY_GLASS_ID]["transfer_id"] == "a1f2e775-77fe-4ad6-a822-54d353e0ea0e"
        assert parsed_data[STEEL_ID]["transfer_id"] == "636a7e55-fe81-4d04-9d98-a2cdd31e962a"

        self.check_air(air)
        self.check_glass(e_glass_ud)
        self.check_steel(steel)
