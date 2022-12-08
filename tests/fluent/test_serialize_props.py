from unittest.mock import Mock

from ansys.fluent.core import Fluent as _FluentCore
from ansys.materials.manager._models import Constant
from ansys.materials.manager.material import Material

TEST_MATERIAL = Material("Fluid", models=[Constant("Reference Temperature", 25.0)])


class materials:
    def __init__(self):
        self._fluid = {}

    @property
    def fluid(self):
        return self._fluid


class setup_root:
    def __init__(self):
        self._materials = materials()

    @property
    def materials(self):
        return self._materials


class MockFluent(_FluentCore):
    class _connection:
        def scheme_eval():
            pass

    def __init__(self):
        super().__init__(fluent_connection=self._connection)
        self._setup = setup_root()

    @property
    def setup(self):
        return self._setup


class TestSerializeConstant:
    def test_valid_constant_succeeds(self):
        model = Constant("Density", 5.0)
        mock_fluent = MockFluent()
        model.write_model(TEST_MATERIAL, mock_fluent)
        print(str(mock_fluent.setup.materials.fluid["Fluid"]))
        assert mock_fluent.setup.materials.fluid["Fluid"] == {
            "density": {"option": "constant", "value": 5.0}
        }
