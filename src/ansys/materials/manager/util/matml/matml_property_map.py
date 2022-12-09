"""Define a map between MAPDL and MATLM material properties."""

# todo: add more property sets and parameters to the map

# either define properties or mappings, but not both
MATML_PROPERTY_MAP = {
    "Density": {"properties": ["Density"], "mappings": {}},
    "Elasticity::Isotropic": {
        "properties": [],
        "mappings": {
            "Young's Modulus": [
                "Young's Modulus X direction",
                "Young's Modulus Y direction",
                "Young's Modulus Z direction",
            ],
            "Shear Modulus": [
                "Shear Modulus XY",
                "Shear Modulus XZ",
                "Shear Modulus YZ",
            ],
            "Poisson's Ratio": [
                "Poisson's Ratio XY",
                "Poisson's Ratio XZ",
                "Poisson's Ratio YZ",
            ],
        },
    },
    "Elasticity::Orthotropic": {
        "properties": [
            "Young's Modulus X direction",
            "Young's Modulus Y direction",
            "Young's Modulus Z direction",
            "Shear Modulus XY",
            "Shear Modulus XZ",
            "Shear Modulus YZ",
            "Poisson's Ratio XY",
            "Poisson's Ratio XZ",
            "Poisson's Ratio YZ",
        ],
        "mappings": {},
    },
    "Coefficient of Thermal Expansion::Isotropic": {
        "properties": [],
        "mappings": {
            "Coefficient of Thermal Expansion": [
                "thermal expansion coefficient x direction",
                "thermal expansion coefficient y direction",
                "thermal expansion coefficient z direction",
            ]
        },
    },
    "Coefficient of Thermal Expansion::Orthotropic": {
        "properties": [],
        "mappings": {
            "Coefficient of Thermal Expansion X direction": [
                "thermal expansion coefficient x direction"
            ],
            "Coefficient of Thermal Expansion Y direction": [
                "thermal expansion coefficient y direction"
            ],
            "Coefficient of Thermal Expansion Z direction": [
                "thermal expansion coefficient z direction"
            ],
        },
    },
    "Specific Heat": {"properties": [], "mappings": {"Specific Heat": ["Specific Heat Capacity"]}},
    "Thermal Conductivity::Isotropic": {
        "properties": [],
        "mappings": {
            "Thermal Conductivity": [
                "Thermal Conductivity X direction",
                "Thermal Conductivity Y direction",
                "Thermal Conductivity Z direction",
            ]
        },
    },
    "Thermal Conductivity::Orthotropic": {
        "properties": [
            "Thermal Conductivity X direction",
            "Thermal Conductivity Y direction",
            "Thermal Conductivity Z direction",
        ],
        "mappings": {},
    },
    "Viscosity": {"properties": ["Viscosity"], "mappings": {}},
    "Speed of Sound": {"properties": ["Speed of Sound"], "mappings": {}},
}
