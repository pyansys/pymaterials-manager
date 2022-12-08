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
}
