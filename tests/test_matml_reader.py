
from ansys.materials.manager.matml_parser import MatmlReader
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class TestMatmlReader:

    def test_reader(self):
        """read a xml file with steel and e-glass UD"""
        xml_file_path = os.path.join(dir_path, "data", "steel_eglass_ud.xml")
        reader = MatmlReader(xml_file_path)
        num_materials = reader.parse_matml()
        assert num_materials == 2

        steel = reader.get_material("Structural Steel")

        ref_steel = {'Color': {'Red': 132.0, 'Green': 139.0, 'Blue': 179.0, 'Material Property': 'Appearance'},
            'Compressive Ultimate Strength': {'Compressive Ultimate Strength': 0.0},
            'Compressive Yield Strength': {'Compressive Yield Strength': 250000000.0},
            'Density': {'Options Variable': 'Interpolation Options', 'Density': 7850.0,
                        'Temperature': 7.88860905221012e-31},
            'Tensile Yield Strength': {'Tensile Yield Strength': 250000000.0},
            'Tensile Ultimate Strength': {'Tensile Ultimate Strength': 460000000.0},
            'Coefficient of Thermal Expansion': {'Options Variable': 'Interpolation Options',
                                                 'Coefficient of Thermal Expansion': 1.2e-05,
                                                 'Temperature': 7.88860905221012e-31},
            'Zero-Thermal-Strain Reference Temperature': {'Zero-Thermal-Strain Reference Temperature': 22.0,
                                                          'Material Property': 'Coefficient of Thermal Expansion'},
            'Specific Heat': {'Options Variable': 'Interpolation Options', 'Specific Heat': 434.0,
                              'Temperature': 7.88860905221012e-31},
            'Thermal Conductivity': {'Options Variable': 'Interpolation Options', 'Thermal Conductivity': 60.5,
                                     'Temperature': 21.0}, 'S-N Curve': {
               'Alternating Stress': [3999000000.0, 2827000000.0, 1896000000.0, 1413000000.0, 1069000000.0, 441000000.0,
                                      262000000.0, 214000000.0, 138000000.0, 114000000.0, 86200000.0],
               'Cycles': [10.0, 20.0, 50.0, 100.0, 200.0, 2000.0, 10000.0, 20000.0, 100000.0, 200000.0, 1000000.0],
               'Mean Stress': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
            'Strain-Life Parameters': {'Strength Coefficient': 920000000.0, 'Strength Exponent': -0.106,
                                       'Ductility Coefficient': 0.213, 'Ductility Exponent': -0.47,
                                       'Cyclic Strength Coefficient': 1000000000.0,
                                       'Cyclic Strain Hardening Exponent': 0.2},
            'Resistivity': {'Resistivity': 1.7e-07, 'Temperature': 7.88860905221012e-31},
            'Elasticity': {'Options Variable': 'Interpolation Options', "Young's Modulus": 200000000000.0,
                           "Poisson's Ratio": 0.3, 'Bulk Modulus': 166666666666.667, 'Shear Modulus': 76923076923.0769,
                           'Temperature': 7.88860905221012e-31},
            'Relative Permeability': {'Relative Permeability': 10000.0}, 'Material Unique Id': {}}

        assert steel == ref_steel

        e_glass_ud = reader.get_material("Epoxy E-Glass UD")

        ref_eglass = {'Density': {'Options Variable': 'Interpolation Options', 'Density': 2000.0},
                      'Ply Type': {},
                      'Elasticity': {'Options Variable': 'Interpolation Options',
                                     "Young's Modulus X direction": 45000000000.0,
                                     "Young's Modulus Y direction": 10000000000.0,
                                     "Young's Modulus Z direction": 10000000000.0,
                                     "Poisson's Ratio XY": 0.3, "Poisson's Ratio YZ": 0.4, "Poisson's Ratio XZ": 0.3,
                                     'Shear Modulus XY': 5000000000.0, 'Shear Modulus YZ': 3846150000.0,
                                     'Shear Modulus XZ': 5000000000.0},
                      'Strain Limits': {'Options Variable': 'Interpolation Options', 'Tensile X direction': 0.0244,
                                        'Tensile Y direction': 0.0035, 'Tensile Z direction': 0.0035,
                                        'Compressive X direction': -0.015, 'Compressive Y direction': -0.012,
                                        'Compressive Z direction': -0.012, 'Shear XY': 0.016, 'Shear YZ': 0.012,
                                        'Shear XZ': 0.016},
                      'Stress Limits': {'Options Variable': 'Interpolation Options',
                                        'Tensile X direction': 1100000000.0, 'Tensile Y direction': 35000000.0,
                                        'Tensile Z direction': 35000000.0, 'Compressive X direction': -675000000.0,
                                        'Compressive Y direction': -120000000.0,
                                        'Compressive Z direction': -120000000.0, 'Shear XY': 80000000.0,
                                        'Shear YZ': 46153800.0, 'Shear XZ': 80000000.0},
                      'Puck Constants': {'Options Variable': 'Interpolation Options',
                                         'Compressive Inclination XZ': 0.25, 'Compressive Inclination YZ': 0.2,
                                         'Tensile Inclination XZ': 0.3, 'Tensile Inclination YZ': 0.2},
                      'Additional Puck Constants': {'Interface Weakening Factor': 0.8, 'Degradation Parameter s': 0.5,
                                                    'Degradation Parameter M': 0.5},
                      'Tsai-Wu Constants': {'Coupling Coefficient XY': -1.0, 'Coupling Coefficient YZ': -1.0,
                                            'Coupling Coefficient XZ': -1.0, 'Temperature': 7.88860905221012e-31},
                      'Material Unique Id': {},
                      'Color': {'Red': 184.0, 'Green': 235.0, 'Blue': 197.0, 'Material Property': 'Appearance'}}

        assert e_glass_ud == ref_eglass

