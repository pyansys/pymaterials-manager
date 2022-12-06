from enum import Enum, auto


class SupportedPackage(Enum):
    """Enum representing the packages supported by the Material Manager."""

    MAPDL = auto()
    FLUENT = auto()
