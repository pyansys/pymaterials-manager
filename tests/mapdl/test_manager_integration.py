from ansys.mapdl.core import Mapdl
import numpy as np
from numpy.testing import assert_array_equal
import pytest

pytestmark = pytest.mark.mapdl_integration

from ansys.materials.manager._models import Constant, PiecewiseLinear, Polynomial
from ansys.materials.manager.material import Material
from ansys.materials.manager.material_manager import MaterialManager


@pytest.fixture
def mapdl():
    mapdl = Mapdl()
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
    assert ref_temp.name.lower() == "reference temperature"
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
    mat = Material("TestMaterial", id_, reference_temperature=23.0)
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

    assert_array_equal(density_model.y, expected_output)
