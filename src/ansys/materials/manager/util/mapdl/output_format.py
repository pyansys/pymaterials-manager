from typing import Dict

from ansys.mapdl.core.mapdl import _MapdlCore

from ansys.materials.manager.util.common import INTEGER_VALUE_REGEX

STRING_PROP_MAP = {
    "OUTPUT DISPLAY TYPE": "ftype",
    "CHARACTERS PER OUTPUT FIELD": "nwidth",
    "SIGNIFICANT DIGITS": "dsignf",
}


def get_format(mapdl: _MapdlCore) -> Dict[str, int]:
    """
    Get the numerical display format for MAPDL.

    Parameters
    ----------
    mapdl: _MapdlCore
        MAPDL session

    Returns
    -------
    Dict[str, Union[str, int]]
        Numerical display options indexed by their option name.
    """
    output = {}
    format_data = mapdl.gformat("STAT")
    for line in format_data.splitlines():
        current_prop = None
        for k, v in STRING_PROP_MAP.items():
            if k in line:
                current_prop = v
                break
        if current_prop is None:
            continue
        match = INTEGER_VALUE_REGEX.search(line)
        val = None
        if match is not None:
            val = match.group(0)
        output[current_prop] = val
    return output


def set_format(mapdl: _MapdlCore, format_settings: Dict[str, int]) -> None:
    """
    Set the MAPDL numerical display format.

    Parameters
    ----------
    mapdl: _MapdlCore
        MAPDL session
    format_settings: Dict[str, Union[str, int]]
        Numerical display format options, indexed by option name.
    """
    mapdl.gformat(**format_settings)
