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

import pytest

from ansys.materials.manager.util.matml import MatmlReader, convert_matml_materials

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class TestMatmlToMaterial:
    def test_conversion_to_material_object(self):
        """read a xml file with steel and e-glass UD"""
        xml_file_path = os.path.join(DIR_PATH, "..", "data", "steel_eglass_air.xml")
        reader = MatmlReader(xml_file_path)
        num_materials = reader.parse_matml()
        assert num_materials == 3

        materials = convert_matml_materials(reader.materials, reader.transfer_ids, 3)

        steel = materials[2]

        assert steel.material_id == 6
        assigned_models = steel.models
        assert len(assigned_models) == 18
        assert steel.uuid == "636a7e55-fe81-4d04-9d98-a2cdd31e962a"

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
            "secant thermal expansion coefficient x direction": 1.2e-5,
            "secant thermal expansion coefficient y direction": 1.2e-5,
            "secant thermal expansion coefficient z direction": 1.2e-5,
            "specific heat capacity": 434.0,
            "thermal conductivity x direction": 60.5,
            "thermal conductivity y direction": 60.5,
            "thermal conductivity z direction": 60.5,
        }
        for name, expected_value in expected_results.items():
            assigned_model = steel.get_model_by_name(name)
            assert len(assigned_model) == 1
            assert assigned_model[0].value == pytest.approx(expected_value)

        eglass = materials[1]
        assert eglass.material_id == 5
        assigned_models = eglass.models
        assert len(assigned_models) == 17
        assert eglass.uuid == "a1f2e775-77fe-4ad6-a822-54d353e0ea0e"

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
            "thermal conductivity x direction": 30.0,
            "thermal conductivity y direction": 5.0,
            "thermal conductivity z direction": 5.0,
            "secant thermal expansion coefficient x direction": -1e-6,
            "secant thermal expansion coefficient y direction": 1e-5,
            "secant thermal expansion coefficient z direction": 1e-5,
        }
        for name, expected_value in expected_results.items():
            assigned_model = eglass.get_model_by_name(name)
            assert len(assigned_model) == 1
            assert assigned_model[0].value == pytest.approx(expected_value)

        air = materials[0]
        assert air.material_id == 4
        assigned_models = air.models
        assert len(assigned_models) == 8
        assert air.uuid == "370e7536-77c0-11ed-8eeb-6c6a77744180"
        expected_results = {
            "strain reference temperature": 0.0,
            "density": 1.225,
            "specific heat capacity": 1006.43,
            "thermal conductivity x direction": 0.0242,
            "thermal conductivity y direction": 0.0242,
            "thermal conductivity z direction": 0.0242,
            "viscosity": 1.7894e-05,
            "speed of sound": 346.25,
        }
        for name, expected_value in expected_results.items():
            assigned_model = air.get_model_by_name(name)
            assert len(assigned_model) == 1
            assert assigned_model[0].value == pytest.approx(expected_value)
