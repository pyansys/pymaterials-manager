from abc import ABCMeta, abstractmethod
from types import NoneType
from typing import Any, List, Tuple

try:
    from ansys.mapdl.core.mapdl import _MapdlCore
except ImportError:
    _MapdlCore = NoneType

try:
    from ansys.fluent.core import Session as _FluentCore
except ImportError:
    _FluentCore = NoneType

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.materials.manager._models._common._packages import SupportedPackage  # noqa: F401
    from ansys.materials.manager.material import Material  # noqa: F401


class _BaseModel(metaclass=ABCMeta):
    """
    All Nonlinear material models must inherit from this class.

    This allows the MaterialManager to dynamically discover available models, and to dispatch
    deserialization calls to the appropriate model class.
    """

    applicable_packages: "SupportedPackage"

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the model.

        For complex nonlinear models this will be the name of the model, for simple models this
        can be set and should reflect the property being modelled.
        """
        ...

    @abstractmethod
    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        """
        Write this model to MAPDL.

        Should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object with which this model will be associated.
        pyansys_session: Any
            Supported PyAnsys product session, currently only pyMAPDL and pyFluent
            are supported.
        """
        ...

    @abstractmethod
    def validate_model(self) -> "Tuple[bool, List[str]]":
        """
        Perform pre-flight validation of model setup.

        Should not perform any calls to the MAPDL process.

        Returns
        -------
        Tuple
            First element is boolean, true if validation is successful. If false then the second
            element will contain a list of strings with more information.
        """
        ...
