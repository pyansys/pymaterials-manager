import os
from typing import Any, Callable, Iterable, List, Tuple

import CoolProp.CoolProp as coolp
import numpy as np
import numpy.testing
import pytest

from ansys.materials.manager._models import Constant, PiecewiseLinear, _BaseModel
from ansys.materials.manager.common import (
    _chunk_data,
    _chunk_lower_triangular_matrix,
    fill_upper_triangular_matrix,
)
from ansys.materials.manager.material import Material
from ansys.materials.manager.tbdata_parser import _TableDataParser

HEADER_LINES = [
    "LIST DATA TABLE  HILL  FOR ALL MATERIALS",
    "",
    "** * ANSYS - ENGINEERING ANALYSIS SYSTEM  RELEASE 2021 R1          21.1BETA ** *",
    "ANSYS Mechanical Enterprise",
    "00000000  VERSION = LINUX x64    11: 22:54  MAY 26, 2022 CP = 1.165",
    "",
]

ANEL_LINES = [
    "               D Matrix (ANEL) Table For Material    12",
    "",
    "               1   ",
    "   Temps   0.0000    ",
    "    D11    1.0000    ",
    "    D12    2.0000    ",
    "    D13    3.0000    ",
    "    D14    4.0000    ",
    "    D15    5.0000    ",
    "    D16    6.0000    ",
    "    D22    7.0000    ",
    "    D23    8.0000    ",
    "    D24    9.0000    ",
    "    D25    10.000    ",
    "    D26    11.000    ",
    "    D33    12.000    ",
    "    D34    13.0000   ",
    "    D35    14.0000   ",
    "    D36    15.0000   ",
    "    D44    16.0000   ",
    "    D45    17.0000   ",
    "    D46    18.0000   ",
    "    D55    19.0000   ",
    "    D56    20.0000   ",
    "    D66    21.0000   ",
    "",
    "  MATERIAL INPUT USING TB,ANEL COMMANDS FOR MATERIAL NUMBER  12",
    "   Stiffness matrix at temperature =   0.0",
    "     1.0000       2.0000       3.0000       4.0000       5.0000       6.0000    ",
    "     2.0000       7.0000       8.0000       9.0000       10.000       11.000    ",
    "     3.0000       8.0000       12.000       13.000       14.000       15.000    ",
    "     4.0000       9.0000       13.000       16.000       17.000       18.000    ",
    "     5.0000       10.000       14.000       17.000       19.000       20.000    ",
    "     6.0000       11.000       15.000       18.000       20.000       21.000",
]

CHAB_LINES = [
    "               N.L. KIN (CHAB) Table For Material    12",
    "                     1 ",
    " Temps     0.0000000e+00 ",
    " C 1      1.8800000e+01 ",
    " C 2      5.1740000e+06 ",
    " C 3      4.6075000e+06 ",
    " C 4      1.7155000e+04 ",
    " C 5      1.0400000e+03 ",
    " C 6      8.9518000e+02 ",
    " C 7      9.0000000e+00",
]

HILL_LINES = [
    "                        (HILL) Table For Material    11",
    "                     1 ",
    " Temps     0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        0.0000000e+00 ",
    "        1.0000000e+00 ",
    "        1.1000000e+00 ",
    "        9.0000000e-01 ",
    "        8.5000000e-01 ",
    "        9.0000000e-01 ",
    "        8.0000000e-01",
]

VALID_TABLE = os.linesep.join([*HEADER_LINES, *ANEL_LINES, *CHAB_LINES, *HILL_LINES])


class TestCommonFunctions:
    @pytest.mark.parametrize(
        ("iterable_input", "expected_output"),
        [
            ([1.0], [[1.0]]),
            ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]]),
            (
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [7.0]],
            ),
        ],
    )
    @pytest.mark.parametrize("input_type", (list, tuple))
    def test_chunk_data(
        self,
        iterable_input: Iterable[float],
        expected_output: Iterable[Iterable[float]],
        input_type: Callable,
    ):
        iterable_input = input_type(iterable_input)
        chunked_data = _chunk_data(iterable_input)
        for chunk in zip(chunked_data, expected_output):
            assert chunk[0] == chunk[1]

    @pytest.mark.parametrize(
        ("array_input", "expected_output"),
        [
            ([[1.0]], [[1.0]]),
            ([[1.0, 2.0], [3.0, 4.0]], [[1.0, 3.0, 4.0]]),
            (
                [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
                [[1.0, 4.0, 5.0, 7.0, 8.0, 9.0]],
            ),
            (
                [
                    [1.0, 2.0, 3.0, 4.0],
                    [5.0, 6.0, 7.0, 8.0],
                    [9.0, 10.0, 11.0, 12.0],
                    [13.0, 14.0, 15.0, 16.0],
                ],
                [[1.0, 5.0, 6.0, 9.0, 10.0, 11.0], [13.0, 14.0, 15.0, 16.0]],
            ),
        ],
    )
    def test_chunk_lower_triangular_matrix(
        self,
        array_input: Iterable[Iterable[float]],
        expected_output: Iterable[Iterable[float]],
    ):
        np_input = np.asarray(array_input, dtype=float)
        chunked_array = _chunk_lower_triangular_matrix(np_input)
        for chunk in zip(chunked_array, expected_output):
            assert chunk[0] == chunk[1]

    def test_chunk_lower_triangular_throws_with_1_dimension(self):
        input_array = np.array([1.0])
        with pytest.raises(ValueError):
            _ = _chunk_lower_triangular_matrix(input_array)

    def test_chunk_lower_triangular_throws_with_3_dimensions(self):
        input_array = np.array([[[1.0]]])
        with pytest.raises(ValueError):
            _ = _chunk_lower_triangular_matrix(input_array)

    @pytest.mark.parametrize(
        "array_input",
        [[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]],
    )
    def test_chunk_lower_triangular_throws_with_non_square_input(
        self, array_input: Iterable[Iterable[float]]
    ):
        np_input = np.asarray(array_input, dtype=float)
        with pytest.raises(ValueError):
            _ = _chunk_lower_triangular_matrix(np_input)

    @pytest.mark.parametrize(
        ("array_input", "expected_output"),
        [
            ([1.0], [[1.0]]),
            ([1.0, 3.0, 4.0], [[1.0, 3.0], [3.0, 4.0]]),
            (
                [1.0, 2.0, 3.0, 5.0, 6.0, 9.0],
                [[1.0, 2.0, 3.0], [2.0, 5.0, 6.0], [3.0, 6.0, 9.0]],
            ),
            (
                [1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 11.0, 12.0, 16.0],
                [
                    [1.0, 2.0, 3.0, 4.0],
                    [2.0, 6.0, 7.0, 8.0],
                    [3.0, 7.0, 11.0, 12.0],
                    [4.0, 8.0, 12.0, 16.0],
                ],
            ),
        ],
    )
    def test_fill_upper_triangular_matrix(
        self, array_input: List[float], expected_output: Iterable[Iterable[float]]
    ):
        filled_array = fill_upper_triangular_matrix(array_input)
        expected_output = np.asarray(expected_output, dtype=float)
        numpy.testing.assert_array_equal(expected_output, filled_array)

    def test_invalid_input_length(self):
        input_data = [1.0, 2.0, 3.0, 4.0]
        with pytest.raises(ValueError):
            _ = fill_upper_triangular_matrix(input_data)


def make_material_with_properties() -> Material:
    id_ = "3"
    name = "Test_Material"
    models = [
        Constant("Density", 3000.0),
        Constant("Elastic Modulus", 6_000_000.0),
        Constant("Reference Temperature", 23.0),
    ]
    return Material(material_name=name, material_id=id_, models=models)


class TestMaterial:
    def test_create_empty_material(self):
        id_ = "3"
        name = "MaterialName"
        material = Material(material_name=name, material_id=id_)
        assert material.name == name
        assert material.material_id == id_

    def test_default_reference_temperature(self):
        id_ = "1"
        name = "MaterialName"
        material = Material(material_name=name, material_id=id_)
        assert material.reference_temperature == pytest.approx(0.0)

    def test_setting_material_id_works(self):
        name = "MaterialName"
        material = Material(material_name=name, material_id=1)
        material.material_id = "2"
        assert material.material_id == "2"

    def test_create_material_with_simple_properties(self):
        name = "MaterialName"
        id_ = "3"
        models = [
            Constant("Density", 3000.0),
            Constant("Elastic Modulus (11-axis)", 6_000_000.0),
            Constant("Reference Temperature", 23.0),
        ]
        material = Material(material_name=name, material_id=id_, models=models)
        assert material.material_id == id_
        assigned_models = material.models
        assert len(assigned_models) == 3
        for model in models:
            matching_model = next(
                assigned_model
                for assigned_model in assigned_models
                if assigned_model.name == model.name
            )
            assert matching_model.value == pytest.approx(model.value)

    def test_create_material_with_coolprop(self):
        name = "Air"
        coolp_fluid = "Air"
        ref_pressure = 101325.0
        ref_temperature = 298.15
        models = [
            Constant("Reference Pressure", ref_pressure),
            Constant(
                "Density",
                "ideal-gas",
            ),
            Constant(
                "Viscosity",
                coolp.PropsSI("V", "P", ref_pressure, "T", ref_temperature, coolp_fluid),
            ),
            Constant(
                "Specific Heat Capacity",
                coolp.PropsSI("C", "P", ref_pressure, "T", ref_temperature, coolp_fluid),
            ),
            Constant(
                "Thermal Conductivity (11-axis)",
                coolp.PropsSI("L", "P", ref_pressure, "T", ref_temperature, coolp_fluid),
            ),
            Constant(
                "Thermal Expansion Coefficient (11-axis)",
                coolp.PropsSI(
                    "ISOBARIC_EXPANSION_COEFFICIENT",
                    "P",
                    ref_pressure,
                    "T",
                    ref_temperature,
                    coolp_fluid,
                ),
            ),
            Constant(
                "Molar Mass",
                coolp.PropsSI("M", "P", ref_pressure, "T", ref_temperature, coolp_fluid) * 1000.0,
            ),
        ]
        material = Material(
            material_name=name, models=models, reference_temperature=ref_temperature
        )
        assigned_models = material.models
        assert len(assigned_models) == 8
        for model in models:
            matching_model = next(
                assigned_model
                for assigned_model in assigned_models
                if assigned_model.name == model.name
            )
            if isinstance(matching_model.value, float):
                assert matching_model.value == pytest.approx(model.value)
            else:
                assert matching_model.value == model.value

    def test_create_material_with_functional_properties(self):
        name = "MaterialName"
        id_ = "3"
        temperature_values = np.asarray([0.0, 100.0, 200.0])
        models = [
            PiecewiseLinear(
                "Density", x=temperature_values, y=np.asarray([4000.0, 3700.0, 3400.0])
            ),
            PiecewiseLinear(
                "Elastic Modulus (11-axis)", x=temperature_values, y=np.asarray([6e6, 5.5e6, 5e6])
            ),
        ]
        material = Material(material_name=name, material_id=id_, models=models)
        assert material.material_id == id_
        assigned_models = material.models
        for model in models:
            matching_model = next(
                assigned_model
                for assigned_model in assigned_models
                if assigned_model.name == model.name
            )
            np.testing.assert_array_equal(model.x, matching_model.x)
            np.testing.assert_array_equal(model.y, matching_model.y)

    def test_create_material_with_reference_temperature(self):
        name = "MaterialName"
        id_ = "5"
        ref_temperature = 25.0
        material = Material(
            material_name=name, material_id=id_, reference_temperature=ref_temperature
        )
        assert material.material_id == id_
        assert material.reference_temperature == pytest.approx(ref_temperature)
        assert material.get_model_by_name("Reference Temperature")[0].value == pytest.approx(
            ref_temperature
        )

    def test_assigning_reference_temperature(self):
        material = Material(material_name="MaterialName", material_id="10")
        reference_temperature = 23.0
        material.reference_temperature = reference_temperature
        assert material.get_model_by_name("Reference Temperature")[0].value == pytest.approx(
            reference_temperature
        )

    def test_create_material_with_nonlinear_model(self):
        material = Material(
            material_name="MaterialName",
            material_id="1",
            models=[TestNonlinearModel()],
        )
        model = material.get_model_by_name("TestModel")
        assert len(model) == 1
        assert isinstance(model[0], TestNonlinearModel)


class TestNonlinearModel(_BaseModel):
    model_codes = ("TEST",)

    @property
    def name(self) -> str:
        return "TestModel"

    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        return None

    def validate_model(self) -> "Tuple[bool, List[str]]":
        return True, []

    @classmethod
    def deserialize_model(cls, model_code: str, model_data: List[str]) -> "_BaseModel":
        return TestNonlinearModel()


class TestTableDataParser:
    def test_valid_table_with_material_id(self):
        parsed_data = _TableDataParser._get_tb_sections_with_id(VALID_TABLE, 12)
        assert len(parsed_data) == 2
        assert "ANEL" in parsed_data
        anel_data = parsed_data["ANEL"]
        assert len(anel_data) == 34
        assert anel_data == ANEL_LINES
        assert "CHAB" in parsed_data
        chab_data = parsed_data["CHAB"]
        assert len(chab_data) == 10
        assert chab_data == CHAB_LINES

    def test_valid_table_with_missing_id(self):
        with pytest.raises(IndexError):
            _TableDataParser._get_tb_sections_with_id(VALID_TABLE, 10)

    def test_deserializing_model_works(self):
        parser = _TableDataParser({"STUB": TestNonlinearModel})
        model = parser.deserialize_model("STUB", ["BLANK"])
        assert model is not None
        assert isinstance(model, TestNonlinearModel)

    def test_deserializing_unsupported_model_throws(self):
        parser = _TableDataParser({"STUB": TestNonlinearModel})
        with pytest.raises(NotImplementedError):
            _ = parser.deserialize_model("NOTSTUB", ["BLANK"])
