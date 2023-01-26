"""Provides the ``MaterialManager`` class."""
import inspect
from typing import Any, Dict

import ansys.materials.manager._models as models
from ansys.materials.manager._models._common._base import _FluentCore, _MapdlCore

from ._models import _BaseModel
from .material import Material
from .util.mapdl.mapdl_reader import read_mapdl


class MaterialManager:
    """
    Manage material creation, assignment and other management tasks.

    This class is the main entry-point for the pythonic material management interface.
    """

    model_type_map: Dict[str, models._BaseModel] = {}
    _client: Any

    def __init__(self, pyansys_client: Any):
        """
        Create a new MaterialManager object ready for use.

        Parameters
        ----------
        pyansys_client : Any
            Valid instance of a PyAnsys Client. Only pyMAPDL and pyFluent are currently
            supported.
        """
        self._client = pyansys_client
        # response = inspect.getmembers(models, self.__is_subclass_predicate)
        # model_classes: List[models._BaseModel] = [tple[1] for tple in response]
        # for class_ in model_classes:
        #     supported_model_codes = class_.model_codes
        #     for model_code in supported_model_codes:
        #         self.model_type_map[model_code] = class_

    @staticmethod
    def __is_subclass_predicate(obj: object) -> bool:
        """
        Predicate to determine if a given object is a strict subclass of :obj:`models._BaseModel`.

        Parameters
        ----------
        obj : object
            Any python object.

        Returns
        -------
        bool
            ``True`` if object is strictly a subclass of :obj:`models._BaseModel`, otherwise ``False``.
        """
        return (
            isinstance(obj, type)
            and issubclass(obj, models._BaseModel)
            and not inspect.isabstract(obj)
        )

    def write_material(self, material: Material) -> None:
        """
        Write a material to the Solver.

        Parameters
        ----------
        material : Material
            Material object to be written to MAPDL.
        """
        for model in material.models:
            assert isinstance(model, _BaseModel)
            model.write_model(material, self._client)

    def read_materials_from_session(self) -> Dict[str, Material]:
        """
        Given a pyAnsys session, return the materials present.

        Currently supports only pyMAPDL.

        Returns
        -------
        Dict[str, Material]
            Materials in current session, indexed by an identifier. For MAPDL this is the material
            ID, for Fluent it is the material name.
        """
        if isinstance(self._client, _MapdlCore):
            return self._read_mapdl()
        elif isinstance(self._client, _FluentCore):
            return self._read_fluent()

    def _read_mapdl(self) -> Dict[str, Material]:
        return read_mapdl(self._client)

    def _read_fluent(self) -> Dict[str, Material]:
        return []
