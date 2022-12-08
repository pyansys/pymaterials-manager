from typing import Any, List, Tuple, Protocol

from ansys.materials.manager._models._common._base import _BaseModel, _FluentCore, _MapdlCore
from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common._packages import SupportedPackage




TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.materials.manager.material import Material  # noqa: F401

class ConstantModel(Protocol):
    name: str
    value: float

class ConstantWriter(Protocol):
    def constant(self, material: "Material", constant_model: ConstantModel) -> None:
        pass

class Constant(_BaseModel):
    """Represents a constant property value in a solver."""

    applicable_packages: SupportedPackage.MAPDL | SupportedPackage.FLUENT
    _name: str
    _value: float

    def __init__(self, name: str, value: float) -> None:
        """
        Create a constant property value.

        This property will be created in the default unit system of the solver. Ensure
        you provide the value in the correct units.

        Parameters
        ----------
        name: str
            The name of the property to be modelled as a constant.
        value: float
            The value of the constant property.
        """
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        """Get the name of the quantity modelled by this constant."""
        return self._name

    @property
    def value(self) -> float:
        """Get the constant value of this quantity."""
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    def write(self, writer, material):
        writer.constant(material, self)

    def write_model(self, material: "Material", writer: ConstantWriter) -> None:
        """
        Should make some effort to validate the model state before writing.

        Parameters
        ----------
        writer: ConstantWriter
            Writer that supports the ConstantWriter Protocol

        material: Material
            Material object with which this model will be associated.
        """
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException("\n".join(issues))

        if not hasattr(writer, "constant"):
            raise TypeError(
                "This model is only supported by MAPDL and Fluent, ensure you have the correct"
                "type of `pyansys_session`."
            )
        writer.constant(material, self)



    def validate_model(self) -> "Tuple[bool, List[str]]":
        """
        Perform pre-flight validation of model setup.

        Returns
        -------
        Tuple
            First element is boolean, true if validation is successful. If false then the second
            element will contain a list of strings with more information.
        """
        failures = []
        is_ok = True

        if self._name is None or self._name == "":
            failures.append("Invalid property name")
            is_ok = False
        if self._value is None:
            failures.append("Value cannot be None")
            is_ok = False
        return is_ok, failures
