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
    "Coefficient of Thermal Expansion::Isotropic::Secant": {
        "properties": [],
        "mappings": {
            "Coefficient of Thermal Expansion": [
                "secant thermal expansion coefficient x direction",
                "secant thermal expansion coefficient y direction",
                "secant thermal expansion coefficient z direction",
            ]
        },
    },
    "Coefficient of Thermal Expansion::Isotropic::Instantaneous": {
        "properties": [],
        "mappings": {
            "Coefficient of Thermal Expansion": [
                "instantaneous thermal expansion coefficient x direction",
                "instantaneous thermal expansion coefficient y direction",
                "instantaneous thermal expansion coefficient z direction",
            ]
        },
    },
    "Coefficient of Thermal Expansion::Orthotropic::Secant": {
        "properties": [],
        "mappings": {
            "Coefficient of Thermal Expansion X direction": [
                "secant thermal expansion coefficient x direction"
            ],
            "Coefficient of Thermal Expansion Y direction": [
                "secant thermal expansion coefficient y direction"
            ],
            "Coefficient of Thermal Expansion Z direction": [
                "secant thermal expansion coefficient z direction"
            ],
        },
    },
    "Coefficient of Thermal Expansion::Orthotropic::Instantaneous": {
        "properties": [],
        "mappings": {
            "Coefficient of Thermal Expansion X direction": [
                "instantaneous thermal expansion coefficient x direction"
            ],
            "Coefficient of Thermal Expansion Y direction": [
                "instantaneous thermal expansion coefficient y direction"
            ],
            "Coefficient of Thermal Expansion Z direction": [
                "instantaneous thermal expansion coefficient z direction"
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
