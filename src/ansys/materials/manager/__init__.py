"""Provides a helper to manage materials in the Ansys ecosystem."""
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as metadata

    __version__ = metadata.version("ansys-materials-manager")

else:
    from importlib_metadata import metadata as metadata_backport

    __version__ = metadata_backport("ansys-materials-manager")["version"]
