from math import floor, log10
import os

from ansys.mapdl.core import Mapdl
import numpy as np
from numpy.testing import assert_array_equal
import pytest

from ansys.materials.manager._models._mapdl.anisotropic_elasticity import (
    AnisotropicElasticity,
    ElasticityMode,
)
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

pytestmark = pytest.mark.mapdl_integration

from ansys.materials.manager._models import Constant, PiecewiseLinear, Polynomial
from ansys.materials.manager.material import Material
from ansys.materials.manager.material_manager import MaterialManager


# This is necessary because MAPDL only returns 5 significant figures when we execute TBLIST...
def round_sig(x, sig_figs=4):
    return round(x, sig_figs - int(floor(log10(abs(x)))))


@pytest.fixture
def mapdl():
    mapdl = Mapdl(ip="127.0.0.1", port="50052", local=False)
    mapdl.prep7()
    yield mapdl
    mapdl.mpdele("all", "all")


@pytest.fixture
def manager(mapdl):
    return MaterialManager(mapdl)


def test_can_write_and_return_reference_temperature(manager):
    mat = Material("TestMaterial", "1", models=[Constant("Strain Reference Temperature", 23.0)])
    manager.write_material(mat)

    results = manager.read_materials_from_session()
    assert len(results) == 1
    assert "1" in results
    material_result = results["1"]
    assert material_result.material_id == "1"
    assert len(material_result.models) == 1
    ref_temp = material_result.models[0]
    assert ref_temp.name.lower() == "strain reference temperature"
    assert ref_temp.value == pytest.approx(23.0)
    assert isinstance(ref_temp, Constant)


def test_can_write_and_return_constant_property(manager):
    id_ = "2"
    mat = Material("TestMaterial", id_, models=[Constant("Strain Reference Temperature", 23.0)])
    model = Constant("Density", 3200.0)
    mat.models.append(model)
    manager.write_material(mat)

    results = manager.read_materials_from_session()
    assert len(results) == 1
    assert id_ in results
    material_result = results[id_]
    assert material_result.material_id == id_
    assert len(material_result.models) == 2
    density_model = next(
        model_ for model_ in material_result.models if model_.name.lower() == "density"
    )
    assert isinstance(density_model, Constant)
    assert density_model.value == pytest.approx(3200.0)


def test_can_write_and_return_interpolated_property(manager):
    id_ = "3"
    mat = Material("TestMaterial", id_, models=[Constant("Strain Reference Temperature", 23.0)])
    x_data = np.arange(273, 473, 10)
    y_data = np.arange(1.2e6, 1e6, -1e4)
    model = PiecewiseLinear("Density", x_data, y_data)
    mat.models.append(model)
    manager.write_material(mat)

    results = manager.read_materials_from_session()
    assert len(results) == 1
    assert id_ in results
    material_result = results[id_]
    assert material_result.material_id == id_
    assert len(material_result.models) == 2
    density_model = next(
        model_ for model_ in material_result.models if model_.name.lower() == "density"
    )
    assert isinstance(density_model, PiecewiseLinear)
    assert_array_equal(density_model.x, x_data)
    assert_array_equal(density_model.y, y_data)


def test_can_write_and_return_polynomial_property(manager):
    id_ = "4"
    mat = Material("TestMaterial", id_)
    x_data = np.arange(273, 473, 10)
    coefficients = np.array([1.0, 2.0, 3.0])
    model = Polynomial("Density", coefficients=coefficients, sample_points=x_data)
    mat.models.append(model)
    manager.write_material(mat)

    results = manager.read_materials_from_session()
    assert len(results) == 1
    assert id_ in results
    material_result = results[id_]
    assert material_result.material_id == id_
    assert len(material_result.models) == 2
    density_model = next(
        model_ for model_ in material_result.models if model_.name.lower() == "density"
    )
    assert isinstance(density_model, PiecewiseLinear)
    assert_array_equal(density_model.x, x_data)

    expected_output = np.polyval(np.flip(coefficients), x_data)
    rounded_output = [round_sig(val) for val in expected_output]

    assert_array_equal(density_model.y, rounded_output)


def test_can_write_material_from_matml(manager):
    xml_file_path = os.path.join(DIR_PATH, "..", "data", "steel_eglass_air.xml")
    reader = MatmlReader(xml_file_path)
    num_materials = reader.parse_matml()
    assert num_materials == 3

    materials = convert_matml_materials(reader.materials, reader.transfer_ids, 3)

    steel = materials[2]

    manager.write_material(steel)

    results = manager.read_materials_from_session()
    assert len(results) == 1


def test_can_write_anisotropic_elasticity(manager):
    id_ = "8"
    mat = Material("AnisotropicTestMaterial", id_)

    coefficients = (
        np.array(
            [
                [100, 1, 2, 3, 4, 5],
                [1, 150, 6, 7, 8, 9],
                [
                    2,
                    6,
                    200,
                    10,
                    11,
                    12,
                ],
                [
                    3,
                    7,
                    10,
                    50,
                    13,
                    14,
                ],
                [
                    4,
                    8,
                    11,
                    13,
                    60,
                    15,
                ],
                [5, 9, 12, 14, 15, 70],
            ]
        )
        * 1e6
    )
    mat.models.append(
        AnisotropicElasticity(
            n_dimensions=2,
            coefficient_type=ElasticityMode.STIFFNESS,
            coefficients=coefficients,
            temperature=20,
        )
    )

    manager.write_material(mat)

    results = manager.read_materials_from_session()
    assert len(results) == 1

    manager.write_material(mat)
