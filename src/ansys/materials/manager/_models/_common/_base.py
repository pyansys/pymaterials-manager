from abc import ABCMeta, abstractmethod
from typing import List, Tuple

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.materials.manager.material import Material  # noqa: F401


class _BaseModel(metaclass=ABCMeta):
    """
    All Nonlinear material models must inherit from this class.

    This allows the MaterialManager to dynamically discover available models, and to dispatch
    deserialization calls to the appropriate model class.
    """

    model_codes: Tuple

    @abstractmethod
    def write_model(self, material: "Material") -> None:
        """
        Write this model to MAPDL.

        Should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object with which this model will be associated.
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

    @classmethod
    @abstractmethod
    def deserialize_model(cls, model_code: str, model_data: List[str]) -> "_BaseModel":
        """
        Convert output from a solver command into a model object representing that model.

        The input should be a section of output referring to one model from one material.

        Parameters
        ----------
        model_code: str
            String model code.
        model_data: List[str]
            Lines from solver output corresponding to this model for one material.

        Returns
        -------
        _BaseModel
            Wrapper for the underlying MAPDL material model
        """
        ...
