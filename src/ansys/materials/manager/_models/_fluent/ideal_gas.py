from typing import Any, List, Tuple

from ansys.materials.manager._models import ModelValidationException, _BaseModel
from ansys.materials.manager._models._common._base import _FluentCore
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._fluent.simple_properties import (
    property_codes as fluent_property_codes,
)
from ansys.materials.manager.material import Material


class IdealGas(_BaseModel):
    r"""
    Ideal Gas Model for fluid properties.

    This model can be applied to Density and Specific Heat Capacity properties within fluent,
    it requires that the Molar mass be set as a property and models the following equation:

    .. math::

     P * V = \frac{m * R * T}{M}
    """

    applicable_packages = SupportedPackage.FLUENT
    _name: str

    def __init__(self, name: str):
        """Create an Ideal Gas model for the Fluent solver."""
        self._name = name

    @property
    def name(self) -> str:
        """Get the name of the property modelled."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        """
        Write this model to Fluent.

        Should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object with which this model will be associated.
        pyansys_session: Any
            Configured instance of PyAnsys session.
        """
        if not isinstance(pyansys_session, _FluentCore):
            raise TypeError(
                "This model is only supported by Fluent, ensure you have the correct"
                "type of `pyansys_session`."
            )

        is_ok, issues = self.validate_model()

        molar_mass_prop = material.get_model_by_name("molar mass")
        if len(molar_mass_prop) == 0:
            is_ok = False
            issues.append("Molar Mass must be provided for the Ideal Gas model.")
        if not is_ok:
            raise ModelValidationException("\n".join(issues))

        fluent_property_code = fluent_property_codes[self._name.lower()]
        pyansys_session.setup.materials.fluid[material.name][fluent_property_code] = {
            "option": "ideal_gas"
        }

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

        return is_ok, failures
