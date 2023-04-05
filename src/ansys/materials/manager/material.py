"""Provides the ``Material`` class."""
from typing import List, Optional

from ._models import _BaseModel
from ._models._common.constant import Constant


class Material:
    """
    Provides a wrapper class for managing a material.

    This class associates a material ID with one or more properties and nonlinear material models.
    """

    _models: List[_BaseModel]
    _id: str
    _name: str
    _uuid: str

    def __init__(
        self, material_name: str, material_id: str = None, models: List[_BaseModel] = None
    ):
        """
        Create an instance of a material.

        Optionally specify a material ID, or other properties.

        Parameters
        ----------
        material_name : str
            Name of the material.
        material_id : str, optional
            ID to associate with this material. The default is ``None``.
        models : Dict[str, _BaseModel]
            Dictionary of nonlinear material models. Models are specified with their
            model codes (from the TB command) and the model object.
        """
        self._models = []
        self._name = material_name
        self._id = material_id
        self._uuid = ""
        if models is not None:
            self.models.extend(models)
        if len(self.get_model_by_name("Strain Reference Temperature")) == 0:
            self.models.append(Constant("Strain Reference Temperature", 0))

    @property
    def name(self) -> str:
        """Name of the material."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def material_id(self) -> Optional[str]:
        """Material ID."""
        return self._id

    @material_id.setter
    def material_id(self, value: str):
        self._id = value

    @property
    def uuid(self) -> str:
        """UUID (transfer ID), which is unique."""
        return self._uuid

    @uuid.setter
    def uuid(self, value: str) -> None:
        self._uuid = value

    @property
    def models(self) -> "List[_BaseModel]":
        """Currently assigned material models."""
        return self._models

    def get_model_by_name(self, model_name: str) -> "List[_BaseModel]":
        """Get the material model or models with a given model name."""
        return [model for model in self.models if model.name.lower() == model_name.lower()]

    @property
    def reference_temperature(self) -> float:
        """Strain reference temperature for the model."""
        reference_temperature = self.get_model_by_name("Strain Reference Temperature")[0]
        assert isinstance(reference_temperature, Constant)
        return reference_temperature.value

    @reference_temperature.setter
    def reference_temperature(self, value: float) -> None:
        reference_temperature = self.get_model_by_name("Strain Reference Temperature")[0]
        assert isinstance(reference_temperature, Constant)
        reference_temperature.value = value
