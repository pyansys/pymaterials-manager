from unittest.mock import MagicMock

from ansys.fluent.core.session_solver import Solver as _FluentCore
import pytest

from ansys.materials.manager._models import Constant
from ansys.materials.manager.material import Material

TEST_MATERIAL = Material("Fluid", models=[Constant("Reference Temperature", 25.0)])


class TestSerializeConstant:
    def test_valid_constant_succeeds(self):
        model = Constant("Density", 5.0)
        mock_fluent = MagicMock(spec=_FluentCore)
        model.write_model(TEST_MATERIAL, mock_fluent)
        mock_fluent.setup.materials.fluid.__setitem__.assert_called_once()
        args = mock_fluent.setup.materials.fluid.__setitem__.call_args
        assert args[0][0] == "Fluid"
        assert args[0][1] == {"density": {"option": "constant", "value": pytest.approx(5.0)}}
