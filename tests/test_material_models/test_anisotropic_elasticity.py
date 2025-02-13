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

import copy

import numpy as np
import pytest

from ansys.materials.manager._models._mapdl.anisotropic_elasticity import (
    AnisotropicElasticity,
    ElasticityMode,
)


class TestModelSerialization:
    pass


class TestModelDeserialization:
    pass


class TestGeneralProperties:
    def test_valid_settings_creates_model(self):
        model = AnisotropicElasticity(n_dimensions=2, coefficient_type=ElasticityMode.STIFFNESS)
        assert isinstance(model.coefficients, np.ndarray)
        assert len(model.coefficients) == 0
        assert isinstance(model.temperature, np.ndarray)
        assert len(model.temperature) == 0
        assert model._n_dimensions == 2
        assert model.name == "Anisotropic Elasticity"

    def test_repr(self):
        n_dimensions = 2
        mode = ElasticityMode.STIFFNESS
        model = AnisotropicElasticity(n_dimensions=n_dimensions, coefficient_type=mode)
        repr = model.__repr__()
        assert "AnisotropicElasticity" in repr
        assert f"n_dimensions={n_dimensions}" in repr
        assert f"mode={mode.name}" in repr
        assert "temperature_count=0" in repr

    def test_invalid_dimension_throws(self):
        with pytest.raises(ValueError):
            _ = AnisotropicElasticity(n_dimensions=4, coefficient_type=ElasticityMode.STIFFNESS)

    def test_temperature_as_float_sets_one_element_array(self):
        n_dimensions = 2
        mode = ElasticityMode.STIFFNESS
        temperature = 293
        model = AnisotropicElasticity(
            n_dimensions=n_dimensions, coefficient_type=mode, temperature=temperature
        )
        assert isinstance(model.temperature, np.ndarray)
        assert len(model.temperature) == 1
        assert model.temperature[0] == pytest.approx(temperature)

    def test_temperature_as_array_sets_array(self):
        n_dimensions = 2
        mode = ElasticityMode.STIFFNESS
        temperature = np.array([293.0, 313.0, 333.0, 353.0])
        model = AnisotropicElasticity(
            n_dimensions=n_dimensions, coefficient_type=mode, temperature=temperature
        )
        assert isinstance(model.temperature, np.ndarray)
        assert len(model.temperature) == 4
        assert model.temperature == pytest.approx(temperature)

    def test_coefficients_as_array_sets_coefficients(self):
        n_dimensions = 2
        mode = ElasticityMode.STIFFNESS
        temperature = 293.0
        coefficients = np.array(
            [
                [1.0, 2.0, 3.0, 4.0],
                [2.0, 5.0, 6.0, 7.0],
                [3.0, 6.0, 8.0, 9.0],
                [4.0, 7.0, 9.0, 10.0],
            ]
        )
        model = AnisotropicElasticity(
            n_dimensions=n_dimensions,
            coefficient_type=mode,
            temperature=temperature,
            coefficients=coefficients,
        )
        assert isinstance(model.coefficients, np.ndarray)
        assert model.coefficients.shape == (4, 4)
        assert model.coefficients == pytest.approx(coefficients)


class TestModelValidation:
    n_dimensions = 2
    mode = ElasticityMode.STIFFNESS
    temperature = 293.0
    coefficients = np.array(
        [
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 5.0, 6.0, 7.0],
            [3.0, 6.0, 8.0, 9.0],
            [4.0, 7.0, 9.0, 10.0],
        ]
    )
    valid_model = AnisotropicElasticity(
        n_dimensions=n_dimensions,
        coefficient_type=mode,
        temperature=temperature,
        coefficients=coefficients,
    )

    def test_valid_model_is_valid(self):
        valid, errors = self.valid_model.validate_model()
        assert valid
        assert len(errors) == 0

    @pytest.mark.parametrize("temperatures", [[], [1.0, 2.0]])
    def test_inconsistent_temperature_count_is_invalid(self, temperatures):
        invalid_model = copy.copy(self.valid_model)
        invalid_model.temperature = np.array(temperatures, dtype=float)
        valid, errors = invalid_model.validate_model()
        assert not valid
        assert len(errors) == 1
        assert "Inconsistent number of temperature values" in errors[0]

    def test_more_than_six_temperatures_is_invalid(self):
        invalid_model = copy.copy(self.valid_model)
        invalid_model.temperature = np.array(range(0, 11), dtype=float)
        valid, errors = invalid_model.validate_model()
        assert not valid
        assert len(errors) == 2
        assert any("maximum of six temperature values" in error for error in errors)
        assert any("Inconsistent number of temperature values (11)" in error for error in errors)

    @pytest.mark.parametrize("coefficients", [[0.0], [[[[0.0]]]]])
    def test_unsupported_dimensionality_is_invalid(self, coefficients):
        invalid_model = copy.copy(self.valid_model)
        invalid_model.coefficients = np.array(coefficients, dtype=float)
        valid, errors = invalid_model.validate_model()
        assert not valid
        assert len(errors) == 1
        assert "Invalid dimension of coefficients array" in errors[0]
