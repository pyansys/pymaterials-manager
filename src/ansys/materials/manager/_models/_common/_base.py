from abc import ABCMeta, abstractmethod
from typing import Any, List, Tuple

try:
    from ansys.mapdl.core.mapdl import _MapdlCore
except ImportError:
    _MapdlCore = type(None)

try:
    from ansys.fluent.core import Fluent as _FluentCore
except ImportError:
    _FluentCore = type(None)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.materials.manager._models._common._packages import SupportedPackage  # noqa: F401
    from ansys.materials.manager.material import Material  # noqa: F401


class _BaseModel(metaclass=ABCMeta):
    """
    Provides the base class that all nonlinear material models must inherit from.

    This class allows the Material Manager to dynamically discover available models and to dispatch
    deserialization calls to the appropriate model class.
    """

    applicable_packages: "SupportedPackage"

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the model.

        For complex nonlinear models, this is the name of the model. For simple models, this
        can be set and should reflect the property being modeled.
        """
        ...

    @abstractmethod
    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        """
        Write the model to MAPDL.

        This method should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object to associate this model with.
        pyansys_session: Any
            Supported PyAnsys product session. Only PyMAPDL and PyFluent are
            supported currently.
        """
        ...

    @abstractmethod
    def validate_model(self) -> "Tuple[bool, List[str]]":
        """
        Perform pre-flight validation of the model setup.

        This method should not perform any calls to the MAPDL process.

        Returns
        -------
        Tuple
            First element is Boolean. ``True`` if validation is successful. If ``False``,
            the second element contains a list of strings with more information.
        """
        ...
