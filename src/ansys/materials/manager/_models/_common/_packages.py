from enum import Flag, auto


class SupportedPackage(Flag):
    """Provides the enum representing the packages supported by the Material Manager."""

    MAPDL = auto()
    FLUENT = auto()
