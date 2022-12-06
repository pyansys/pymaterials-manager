from enum import Flag, auto


class SupportedPackage(Flag):
    """Enum representing the packages supported by the Material Manager."""

    MAPDL = auto()
    FLUENT = auto()
