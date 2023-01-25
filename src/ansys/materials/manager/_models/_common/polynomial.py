from typing import Any, List, Optional, Tuple

import numpy as np

from ansys.materials.manager._models._common._base import _BaseModel, _FluentCore, _MapdlCore
from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._fluent.simple_properties import (
    property_codes as fluent_property_codes,
)
from ansys.materials.manager._models._mapdl.simple_properties import (
    property_codes as mapdl_property_codes,
)
from ansys.materials.manager.util.common import _chunk_data

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.materials.manager.material import Material  # noqa: F401


class Polynomial(_BaseModel):
    """
    Polynomial model for a property.

    Represents a property as a polynomial with a series of coefficients. These are stored in
    ascending powers of the parameters.
    """

    applicable_packages: SupportedPackage.MAPDL | SupportedPackage.FLUENT
    _name: str
    _coefficients: np.ndarray
    _sample_points: np.ndarray

    def __init__(
        self, name: str, coefficients: np.ndarray, sample_points: Optional[np.ndarray] = None
    ) -> None:
        """
        Create a polynomial model for a property.

        This model represents a nth order polynomial, the coefficients are stored
        and entered in ascending order. For some packages the polynomial is evaluated
        and then interpolated. In these cases `sample_points` may be provided and should
        cover the range of interest.

        For example, providing [3., 4., 1.] represents the equation

        .. math::

        f(x) = 3 + 4x + x^{2}

        This property will be created in the default unit system of the solver. Ensure
        you provide values in the correct units.

        Parameters
        ----------
        name: str
            The name of the property to be modelled as a constant.
        coefficients: np.ndarray
            The values of the coefficients for the polynomial model, provide in ascending
            powers of the parameter.
        sample_points: Optional[np.ndarray]
            The values of the parameter to be used for interpolation, required for some packages.
        """
        self._name = name
        self._coefficients = coefficients
        self._sample_points = sample_points

    @property
    def name(self) -> str:
        """Get the name of the quantity modelled by this constant."""
        return self._name

    @property
    def coefficients(self) -> np.ndarray:
        """Get the values of the x array."""
        return self._coefficients

    @coefficients.setter
    def coefficients(self, value: np.ndarray) -> None:
        self._coefficients = value

    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        """
        Write this model to MAPDL.

        Should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object with which this model will be associated.
        pyansys_session: Any
            Configured instance of PyAnsys session.
        """
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException("\n".join(issues))

        if isinstance(pyansys_session, _MapdlCore):
            self._write_mapdl(pyansys_session, material)
        elif isinstance(pyansys_session, _FluentCore):
            self._write_fluent(pyansys_session, material)
        else:
            raise TypeError(
                "This model is only supported by MAPDL and Fluent, ensure you have the correct"
                "type of `pyansys_session`."
            )

    def _write_mapdl(self, mapdl: "_MapdlCore", material: "Material") -> None:
        if self._coefficients.size > 5:
            raise ValueError(
                "MAPDL Supports up to 5 coefficients, corresponding to a fourth order polynomial,"
                f"you provided {self._coefficients.size}"
            )
        if self._sample_points is not None:
            if self._sample_points.size > 100:
                raise ValueError(
                    "MAPDL Supports up to 100 sample points for interpolation, "
                    f"you provided {self._sample_points.size}"
                )
            for index, chunk in enumerate(_chunk_data(self._sample_points)):
                mapdl.mptemp(6 * index + 1, *chunk)
        mapdl_property_code = mapdl_property_codes[self._name.lower()]
        mapdl.mp(mapdl_property_code, material.material_id, *self._coefficients)

    def _write_fluent(self, fluent: "_FluentCore", material: "Material") -> None:
        fluent_property_code = fluent_property_codes[self._name.lower()]
        pass

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
        if self._coefficients is None or self._coefficients.size == 0:
            failures.append("coefficients is empty, provide at least one value")
            is_ok = False
        if not is_ok:
            return is_ok, failures
        if self._coefficients.ndim > 1:
            failures.append(f"coefficients must have one dimension, not {self._coefficients.ndim}.")
            is_ok = False
        if self._sample_points is not None and self._sample_points.ndim > 1:
            failures.append(
                f"sample_points must have one dimension, not {self._sample_points.ndim}."
            )
            is_ok = False
        return is_ok, failures
