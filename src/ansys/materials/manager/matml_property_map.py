from .property_codes import PropertyCode

"""Define a map between MAPDL and MATLM material properties"""
# todo: add more property sets and parameters to the map
MATML_PROPERTY_MAP = {
    "Density": {"Density": [PropertyCode.DENS]},
    "Elasticity::Isotropic": {
        "Young's Modulus": [PropertyCode.EX, PropertyCode.EY, PropertyCode.EZ],
        "Shear Modulus": [PropertyCode.GXY, PropertyCode.GXZ, PropertyCode.GYZ],
        "Poisson's Ratio": [PropertyCode.PRXY, PropertyCode.PRXZ, PropertyCode.PRYZ],
    },
    "Elasticity::Orthotropic": {
        "Young's Modulus X direction": [PropertyCode.EX],
        "Young's Modulus Y direction": [PropertyCode.EY],
        "Young's Modulus Z direction": [PropertyCode.EZ],
        "Shear Modulus XY": [PropertyCode.GXY],
        "Shear Modulus XZ": [PropertyCode.GXZ],
        "Shear Modulus YZ": [PropertyCode.GYZ],
        "Poisson's Ratio XY": [PropertyCode.PRXY],
        "Poisson's Ratio XZ": [PropertyCode.PRXZ],
        "Poisson's Ratio YZ": [PropertyCode.PRYZ],
    },
}
