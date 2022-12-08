from ansys.materials.manager._models import Constant
import CoolProp.CoolProp as coolp


from ansys.materials.manager.material import Material
from ansys.materials.manager.serialize import serialize_material_to_file

name = "Air"
coolp_fluid = "Air"
ref_pressure = 101325.0
ref_temperature = 298.15
models = [
    Constant("Reference Pressure", ref_pressure),
    Constant(
        "Density",
        "ideal-gas",
    ),
    Constant(
        "Viscosity",
        coolp.PropsSI("V", "P", ref_pressure, "T", ref_temperature, coolp_fluid),
    ),
    Constant(
        "Specific Heat Capacity",
        coolp.PropsSI("C", "P", ref_pressure, "T", ref_temperature, coolp_fluid),
    ),
    Constant(
        "Thermal Conductivity (11-axis)",
        coolp.PropsSI("L", "P", ref_pressure, "T", ref_temperature, coolp_fluid),
    ),
    Constant(
        "Thermal Expansion Coefficient (11-axis)",
        coolp.PropsSI(
            "ISOBARIC_EXPANSION_COEFFICIENT",
            "P",
            ref_pressure,
            "T",
            ref_temperature,
            coolp_fluid,
        ),
    ),
    Constant(
        "Molar Mass",
        coolp.PropsSI("M", "P", ref_pressure, "T", ref_temperature, coolp_fluid) * 1000.0,
    ),
]
material = Material(
    material_name=name, models=models, reference_temperature=ref_temperature
)

serialize_material_to_file(material, "material.out")