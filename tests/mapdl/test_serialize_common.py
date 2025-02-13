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

from unittest.mock import MagicMock, call

from ansys.mapdl.core import Mapdl as _MapdlCore
import numpy as np
import pytest

from ansys.materials.manager._models import (
    Constant,
    ModelValidationException,
    PiecewiseLinear,
    Polynomial,
)
from ansys.materials.manager.material import Material

TEST_MATERIAL = Material(
    "Test Material", material_id="1", models=[Constant("Strain Reference Temperature", 25.0)]
)


class TestSerializeConstant:
    def test_valid_constant_succeeds(self):
        model = Constant("Density", 5.0)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        model.write_model(TEST_MATERIAL, mock_mapdl)
        mock_mapdl.mp.assert_called_once_with("DENS", "1", 5.0)

    def test_no_name_fails(self):
        model = Constant(None, 5.0)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="Invalid property name"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_no_value_fails(self):
        model = Constant("Density", None)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="Value cannot be None"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_invalid_name_fails(self):
        model = Constant("Nonsense Quantity", 5.0)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(KeyError):
            model.write_model(TEST_MATERIAL, mock_mapdl)


class TestSerializePiecewiseLinear:
    x_data = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    y_data = np.array([10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0])

    def test_valid_data_succeeds(self):
        model = PiecewiseLinear("Density", x=self.x_data, y=self.y_data)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        model.write_model(TEST_MATERIAL, mock_mapdl)
        mock_mapdl.mptemp.assert_has_calls([call(1, *self.x_data[0:6]), call(7, self.x_data[6])])
        mock_mapdl.mpdata.assert_has_calls(
            [
                call("DENS", TEST_MATERIAL.material_id, 1, *self.y_data[0:6]),
                call("DENS", TEST_MATERIAL.material_id, 7, self.y_data[6]),
            ]
        )

    def test_no_name_fails(self):
        model = PiecewiseLinear(None, x=self.x_data, y=self.y_data)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="Invalid property name"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_no_value_fails(self):
        model = PiecewiseLinear("Density", x=None, y=None)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="x_values is empty"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_invalid_name_fails(self):
        model = PiecewiseLinear("Nonsense Quantity", x=self.x_data, y=self.y_data)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(KeyError):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_mismatched_lengths_fails(self):
        model = PiecewiseLinear("Density", x=self.x_data, y=self.y_data[0:6])
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="Length mismatch"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_array_too_long_fails(self):
        model = PiecewiseLinear("Density", x=np.arange(0, 200, 1), y=np.arange(0, 200, 1))
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ValueError, match="MAPDL supports up to 100 points"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_invalid_dimension_fails(self):
        model = PiecewiseLinear("Density", x=np.array([[1, 2], [3, 4]]), y=np.arange(0, 4, 1))
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(
            ModelValidationException, match="x_values must have one dimension, not 2"
        ):
            model.write_model(TEST_MATERIAL, mock_mapdl)


class TestSerializePolynomial:
    coefficients = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    x_data = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    def test_valid_data_succeeds(self):
        model = Polynomial("Density", coefficients=self.coefficients)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        model.write_model(TEST_MATERIAL, mock_mapdl)
        mock_mapdl.mp.assert_has_calls(
            [
                call("DENS", TEST_MATERIAL.material_id, *self.coefficients),
            ]
        )

    def test_valid_data_with_sample_points_succeeds(self):
        model = Polynomial("Density", coefficients=self.coefficients, sample_points=self.x_data)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        model.write_model(TEST_MATERIAL, mock_mapdl)
        mock_mapdl.mptemp.assert_has_calls([call(1, *self.x_data[0:6]), call(7, self.x_data[6])])
        mock_mapdl.mp.assert_has_calls(
            [
                call("DENS", TEST_MATERIAL.material_id, *self.coefficients),
            ]
        )

    def test_no_name_fails(self):
        model = Polynomial(None, coefficients=self.coefficients)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="Invalid property name"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_no_value_fails(self):
        model = Polynomial("Density", coefficients=None)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ModelValidationException, match="Coefficients is empty"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_invalid_name_fails(self):
        model = Polynomial("Nonsense Quantity", coefficients=self.coefficients)
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(KeyError):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_sample_points_too_long_fails(self):
        model = Polynomial(
            "Density", coefficients=self.coefficients, sample_points=np.arange(0, 200, 1)
        )
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ValueError, match="MAPDL supports up to 100 sample points"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_coefficients_too_long_fails(self):
        model = Polynomial("Density", coefficients=np.arange(0, 200, 1))
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(ValueError, match="MAPDL supports up to 5 coefficients"):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_invalid_coefficients_dimension_fails(self):
        model = Polynomial("Density", coefficients=np.array([[1, 2], [3, 4]]))
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(
            ModelValidationException, match="Coefficients must have one dimension, not 2"
        ):
            model.write_model(TEST_MATERIAL, mock_mapdl)

    def test_invalid_sample_points_dimension_fails(self):
        model = Polynomial(
            "Density", coefficients=self.coefficients, sample_points=np.array([[1, 2], [3, 4]])
        )
        mock_mapdl = MagicMock(spec=_MapdlCore)
        with pytest.raises(
            ModelValidationException, match="Sample points must have one dimension, not 2"
        ):
            model.write_model(TEST_MATERIAL, mock_mapdl)
