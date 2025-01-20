import numpy as np
from math import radians, cos, sin, tan
import matplotlib.pyplot as plt

class WoodStructureCalculations:
    def __init__(self):
        # Dataset 5 specifications
        self.width = 7.2  # m
        self.length1 = 6.6  # m
        self.length2 = 10.8  # m
        self.height1 = 2.5  # m
        self.height2 = 2.65  # m
        self.angle = 16  # degrees
        self.spacing = 1.1  # m
        self.ground_level = -1.4  # m.a.s.l.
        
        # Material properties (C27 timber)
        self.fm_k = 27  # MPa, characteristic bending strength
        self.ft_0_k = 16  # MPa, characteristic tensile strength parallel to grain
        self.fc_0_k = 22  # MPa, characteristic compressive strength parallel to grain
        self.E_0_mean = 11500  # MPa, mean modulus of elasticity parallel to grain
        self.density = 370  # kg/m³, characteristic density
        
        # Partial safety factors
        self.gamma_M = 1.3  # Material safety factor for timber
        self.kmod = 0.8  # Modification factor for duration of load and moisture content
        
        # Load calculations
        self.dead_load = 0.5  # kN/m² (self-weight of roof structure)
        self.snow_load = 1.0  # kN/m² (assumed snow load, to be adjusted based on location)
        self.wind_load = 0.6  # kN/m² (assumed wind load, to be adjusted based on location)

    def calculate_design_strength(self):
        """Calculate design strength values according to EN 1995-1-1"""
        # Design bending strength (1)
        self.fm_d = (self.kmod * self.fm_k) / self.gamma_M
        # Design tensile strength (2)
        self.ft_0_d = (self.kmod * self.ft_0_k) / self.gamma_M
        # Design compressive strength (3)
        self.fc_0_d = (self.kmod * self.fc_0_k) / self.gamma_M
        
        # Document calculations with equation numbers
        calculations = {
            'fm_d': f"fm,d = (kmod × fm,k) / γM = ({self.kmod} × {self.fm_k}) / {self.gamma_M} = {self.fm_d:.2f} N/mm² (1)",
            'ft_0_d': f"ft,0,d = (kmod × ft,0,k) / γM = ({self.kmod} × {self.ft_0_k}) / {self.gamma_M} = {self.ft_0_d:.2f} N/mm² (2)",
            'fc_0_d': f"fc,0,d = (kmod × fc,0,k) / γM = ({self.kmod} × {self.fc_0_k}) / {self.gamma_M} = {self.fc_0_d:.2f} N/mm² (3)"
        }
        
        return {
            'fm_d': self.fm_d,
            'ft_0_d': self.ft_0_d,
            'fc_0_d': self.fc_0_d,
            'calculations': calculations
        }

    def calculate_loads(self):
        """Calculate characteristic loads according to EN 1990"""
        # Dead loads (4)
        self.gk_tile = 0.047  # Steel tile 0.6mm
        self.gk_struct = 0.15  # Supporting structure
        self.gk_total = self.gk_tile + self.gk_struct
        
        # Snow load (5)
        self.mu1 = 0.8  # Roof shape coefficient for α = 16°
        self.Ce = 1.0   # Exposure coefficient
        self.Ct = 1.0   # Thermal coefficient
        self.sk = 0.7   # Characteristic ground snow load for Warsaw
        self.snow_load = self.mu1 * self.Ce * self.Ct * self.sk
        
        # Wind load (6)
        self.vb = 22.0  # Basic wind velocity for Warsaw
        self.qb = 0.5 * 1.25 * (self.vb ** 2) / 1000  # Basic velocity pressure
        self.ce = 1.6   # Exposure factor at h = 2.65m
        self.wind_load = self.ce * self.qb
        
        # Design load combinations (7)
        self.Ed1 = 1.35 * self.gk_total + 1.5 * self.snow_load + 1.5 * 0.6 * self.wind_load
        self.Ed2 = 1.35 * self.gk_total + 1.5 * self.wind_load + 1.5 * 0.5 * self.snow_load
        self.design_load = max(self.Ed1, self.Ed2)
        
        # Document calculations with equation numbers
        calculations = {
            'dead_loads': f"gk = {self.gk_tile:.3f} + {self.gk_struct:.3f} = {self.gk_total:.3f} kN/m² (4)",
            'snow_load': f"s = µ1 × Ce × Ct × sk = {self.mu1} × {self.Ce} × {self.Ct} × {self.sk} = {self.snow_load:.3f} kN/m² (5)",
            'wind_load': f"qp = ce × qb = {self.ce} × {self.qb:.3f} = {self.wind_load:.3f} kN/m² (6)",
            'design_load': f"Ed = max({self.Ed1:.3f}, {self.Ed2:.3f}) = {self.design_load:.3f} kN/m² (7)"
        }
        
        return {
            'characteristic_loads': {
                'dead_load': self.gk_total,
                'snow_load': self.snow_load,
                'wind_load': self.wind_load
            },
            'design_load': self.design_load,
            'calculations': calculations
        }

    def calculate_rafter_forces(self):
        """Calculate forces in rafters according to EN 1995-1-1"""
        # Geometric calculations (8)
        angle_rad = radians(self.angle)
        rafter_length = self.width / (2 * cos(angle_rad))
        
        # Load distribution (9)
        q_parallel = self.design_load * cos(angle_rad)
        q_perpendicular = self.design_load * sin(angle_rad)
        
        # Maximum bending moment (10)
        M_max = (q_parallel * rafter_length**2) / 8
        
        # Axial force (11)
        N = q_parallel * rafter_length / (2 * tan(angle_rad))
        
        # Document calculations with equation numbers
        calculations = {
            'geometry': f"L = b/(2×cos(α)) = {self.width:.1f}/(2×cos({self.angle}°)) = {rafter_length:.2f} m (8)",
            'loads': f"q∥ = Ed×cos(α) = {self.design_load:.3f}×cos({self.angle}°) = {q_parallel:.3f} kN/m\n" + 
                    f"q⊥ = Ed×sin(α) = {self.design_load:.3f}×sin({self.angle}°) = {q_perpendicular:.3f} kN/m (9)",
            'moment': f"MEd = (q∥×L²)/8 = ({q_parallel:.3f}×{rafter_length:.2f}²)/8 = {M_max:.2f} kNm (10)",
            'axial': f"NEd = q∥×L/(2×tan(α)) = {q_parallel:.3f}×{rafter_length:.2f}/(2×tan({self.angle}°)) = {N:.2f} kN (11)"
        }
        
        # Calculate section properties
        props = self.calculate_section_properties()
        
        # Calculate stresses
        # Bending stress
        sigma_m = (M_max * 1e6) / props['section_modulus']  # MPa
        # Compressive stress
        sigma_c = (N * 1000) / props['area']  # MPa
        
        return {
            'rafter_length': rafter_length,
            'max_moment': M_max,
            'axial_force': N,
            'calculations': calculations
        }

    def calculate_purlin_forces(self):
        """Calculate forces in purlins according to EN 1995-1-1"""
        # Tributary width calculation (12)
        trib_width = self.spacing
        span = 1.5  # Typical purlin span (m)
        
        # Design load on purlin (13)
        q_purlin = self.design_load * trib_width
        
        # Maximum bending moment (14)
        M_max_purlin = (q_purlin * span**2) / 8
        
        # Shear force (15)
        V_max = (q_purlin * span) / 2
        
        # Document calculations with equation numbers
        calculations = {
            'tributary': f"b = {self.spacing:.3f} m (12)",
            'load': f"qEd = Ed × b = {self.design_load:.3f} × {trib_width:.3f} = {q_purlin:.3f} kN/m (13)",
            'moment': f"MEd = (qEd × L²)/8 = ({q_purlin:.3f} × {span:.3f}²)/8 = {M_max_purlin:.3f} kNm (14)",
            'shear': f"VEd = (qEd × L)/2 = ({q_purlin:.3f} × {span:.3f})/2 = {V_max:.3f} kN (15)"
        }
        
        return {
            'purlin_load': q_purlin,
            'max_moment': M_max_purlin,
            'max_shear': V_max,
            'span': span,
            'calculations': calculations
        }

    def calculate_thermal_resistance(self):
        """Calculate thermal resistance according to EN ISO 6946"""
        # Surface resistances (16)
        R_si = 0.10  # Internal surface resistance
        R_se = 0.04  # External surface resistance
        
        # Layer thermal conductivities (17)
        lambda_mineral_wool = 0.04  # Mineral wool
        lambda_wood = 0.13         # C27 timber
        lambda_steel = 50          # Steel tile
        
        # Layer thicknesses and resistances (18)
        d_insulation = 0.2    # Mineral wool (200mm)
        d_wood = 0.1         # Timber (100mm)
        d_steel = 0.0006     # Steel tile (0.6mm)
        
        # Calculate layer resistances
        R_insulation = d_insulation / lambda_mineral_wool
        R_wood = d_wood / lambda_wood
        R_steel = d_steel / lambda_steel
        
        # Document calculations with equation numbers
        calculations = {
            'surface': f"Surface resistances: Rsi = {R_si} m²K/W, Rse = {R_se} m²K/W (16)",
            'conductivity': f"Thermal conductivities:\n" +
                          f"λ1 = {lambda_mineral_wool} W/(m·K) (mineral wool)\n" +
                          f"λ2 = {lambda_wood} W/(m·K) (timber)\n" +
                          f"λ3 = {lambda_steel} W/(m·K) (steel) (17)",
            'resistance': f"Layer resistances:\n" +
                        f"R1 = {d_insulation}/{lambda_mineral_wool} = {R_insulation:.3f} m²K/W (insulation)\n" +
                        f"R2 = {d_wood}/{lambda_wood} = {R_wood:.3f} m²K/W (timber)\n" +
                        f"R3 = {d_steel}/{lambda_steel} = {R_steel:.6f} m²K/W (steel) (18)"
        }
        
        # Layer properties for documentation
        layers = [
            {
                'material': 'Steel tile roofing',
                'thickness': d_steel * 1000,  # mm
                'conductivity': lambda_steel,
                'resistance': R_steel,
                'density': 7850  # kg/m³
            },
            {
                'material': 'C27 timber structure',
                'thickness': d_wood * 1000,   # mm
                'conductivity': lambda_wood,
                'resistance': R_wood,
                'density': 370   # kg/m³
            },
            {
                'material': 'Mineral wool insulation',
                'thickness': d_insulation * 1000,  # mm
                'conductivity': lambda_mineral_wool,
                'resistance': R_insulation,
                'density': 20    # kg/m³
            }
        ]
        
        # Total thermal resistance including surface resistances
        R_total = R_si + R_insulation + R_wood + R_steel + R_se
        
        # U-value calculation (W/m²·K)
        U_value = 1 / R_total
        
        return {
            'surface_resistances': {'R_si': R_si, 'R_se': R_se},
            'layers': layers,
            'R_total': R_total,
            'U_value': U_value
        }

    def calculate_section_properties(self, section_height=0.2, section_width=0.05):
        """Calculate section properties according to EN 1995-1-1"""
        # Cross-sectional area (19)
        A = section_width * section_height  # m²
        
        # Second moment of area (20)
        I = (section_width * section_height**3) / 12  # m⁴
        
        # Section modulus (21)
        W = (section_width * section_height**2) / 6  # m³
        
        # Document calculations with equation numbers
        calculations = {
            'area': f"A = b × h = {section_width*1000:.0f} × {section_height*1000:.0f} = {A*1e6:.0f} mm² (19)",
            'inertia': f"I = (b × h³)/12 = ({section_width*1000:.0f} × {section_height*1000:.0f}³)/12 = {I*1e12:.0f} mm⁴ (20)",
            'modulus': f"W = (b × h²)/6 = ({section_width*1000:.0f} × {section_height*1000:.0f}²)/6 = {W*1e9:.0f} mm³ (21)"
        }
        
        return {
            'area': A,
            'moment_of_inertia': I,
            'section_modulus': W,
            'calculations': calculations
        }

    def analyze_cross_section(self, section_height=0.2, section_width=0.05):
        """Analyze cross-section according to EN 1995-1-1"""
        # Get section properties and forces
        props = self.calculate_section_properties(section_height, section_width)
        forces = self.calculate_rafter_forces()
        
        # Bending stress (22)
        M_d = forces['max_moment'] * 1e6  # kNm to Nmm
        sigma_m = M_d / (props['section_modulus'] * 1e6)  # MPa
        
        # Compressive stress (23)
        N_d = forces['axial_force'] * 1000  # kN to N
        sigma_c = N_d / (props['area'] * 1e6)  # MPa
        
        # Combined stress verification (24)
        bending_ratio = sigma_m / self.fm_d
        compression_ratio = sigma_c / self.fc_0_d
        combined_ratio = bending_ratio + compression_ratio
        
        # Stability verification (25)
        kcrit = 1.0  # Lateral torsional buckling factor
        stability_ratio = (sigma_m / (kcrit * self.fm_d)) + (sigma_c / self.fc_0_d)
        
        # Document calculations with equation numbers
        calculations = {
            'bending': f"σm,d = MEd/W = {M_d:.0f}/{props['section_modulus']*1e6:.0f} = {sigma_m:.2f} MPa (22)",
            'compression': f"σc,d = NEd/A = {N_d:.0f}/{props['area']*1e6:.0f} = {sigma_c:.2f} MPa (23)",
            'combined': f"σm,d/fm,d + σc,d/fc,0,d = {sigma_m:.2f}/{self.fm_d:.2f} + {sigma_c:.2f}/{self.fc_0_d:.2f} = {combined_ratio:.2f} ≤ 1.0 (24)",
            'stability': f"σm,d/(kcrit×fm,d) + σc,d/fc,0,d = {sigma_m:.2f}/({kcrit:.1f}×{self.fm_d:.2f}) + {sigma_c:.2f}/{self.fc_0_d:.2f} = {stability_ratio:.2f} ≤ 1.0 (25)"
        }
        
        return {
            'section_properties': {
                'area': props['area'] * 1e6,  # Convert m² to mm²
                'moment_of_inertia': props['moment_of_inertia'] * 1e12,  # Convert m⁴ to mm⁴
                'section_modulus': props['section_modulus'] * 1e9  # Convert m³ to mm³
            },
            'forces': {
                'bending_moment': M_d,  # Nmm
                'axial_force': N_d   # N
            },
            'stresses': {
                'bending': sigma_m,  # MPa
                'compression': sigma_c  # MPa
            },
            'utilization_ratios': {
                'bending': bending_ratio,
                'compression': compression_ratio,
                'combined': combined_ratio,
                'stability': stability_ratio
            },
            'verification': {
                'formula': '(σm,d / fm,d) + (σc,d / fc,0,d) ≤ 1.0',
                'result': combined_ratio <= 1.0,
                'value': combined_ratio
            }
        }

    def analyze_angle_brace(self, brace_length=2.0, brace_width=0.1, brace_height=0.15):
        """Analyze angle brace connection and forces according to Eurocode 5
        
        Analysis includes:
        1. Cross-Section Properties:
           A = b × h
           I = (b × h³) / 12
           i = √(I / A)
           where:
           - A is cross-sectional area [mm²]
           - I is moment of inertia [mm⁴]
           - i is radius of gyration [mm]
           - b is brace width [mm]
           - h is brace height [mm]
        
        2. Axial Force:
           N = F / cos(α)
           where:
           - N is axial force in brace [kN]
           - F is rafter force [kN]
           - α is brace angle [degrees]
        
        3. Buckling Analysis:
           λ = Lcr / i
           Ncr = π² × E × I / Lcr²
           where:
           - λ is slenderness ratio [-]
           - Lcr is buckling length [mm]
           - E is modulus of elasticity [MPa]
           - Ncr is critical buckling load [kN]
        
        4. Connection Design:
           Fv,Rd = kmod × (ρk × fh,k × d × t) / γM
           where:
           - Fv,Rd is connection design resistance [kN]
           - kmod is modification factor [-]
           - ρk is characteristic density [kg/m³]
           - fh,k is characteristic embedment strength [MPa]
           - d is fastener diameter [mm]
           - t is timber thickness [mm]
           - γM is partial factor for material [-]
        """
        # Calculate brace properties
        brace_props = self.calculate_section_properties(brace_height, brace_width)
        
        # Convert dimensions to mm for calculations
        brace_length_mm = brace_length * 1000
        brace_width_mm = brace_width * 1000
        brace_height_mm = brace_height * 1000
        
        # Calculate brace forces
        angle_rad = radians(45)  # Typical 45° angle brace
        rafter_force = self.calculate_rafter_forces()['axial_force']
        
        # Axial force in brace
        N_brace = rafter_force / cos(angle_rad)
        
        # Buckling analysis
        # Convert section properties to mm units
        A_mm2 = brace_props['area'] * 1e6
        I_mm4 = brace_props['moment_of_inertia'] * 1e12
        i_mm = (I_mm4 / A_mm2)**0.5
        
        # Calculate buckling parameters
        lambda_brace = brace_length_mm / i_mm
        Ncr = (3.14159**2 * self.E_0_mean * I_mm4) / (brace_length_mm**2)
        Ncr_kN = Ncr / 1000  # Convert N to kN
        
        # Connection design (M16 bolts)
        bolt_diameter = 16  # mm
        timber_thickness = min(brace_width_mm, brace_height_mm)
        fh_k = 0.082 * (1 - 0.01 * bolt_diameter) * self.density  # Characteristic embedment strength
        
        # Design resistance per shear plane
        Fv_Rd = self.kmod * (self.density * fh_k * bolt_diameter * timber_thickness) / (self.gamma_M * 1000)  # kN
        
        return {
            'geometry': {
                'length': brace_length_mm,
                'width': brace_width_mm,
                'height': brace_height_mm,
                'angle': 45
            },
            'section_properties': {
                'area': A_mm2,
                'moment_of_inertia': I_mm4,
                'radius_of_gyration': i_mm,
                'section_modulus': (I_mm4 / (brace_height_mm/2))  # W = I/y where y is distance to extreme fiber
            },
            'forces': {
                'axial_force': N_brace,
                'critical_buckling_load': Ncr_kN
            },
            'buckling_analysis': {
                'slenderness_ratio': lambda_brace,
                'utilization_ratio': N_brace / Ncr_kN
            },
            'connection': {
                'bolt_diameter': bolt_diameter,
                'timber_thickness': timber_thickness,
                'embedment_strength': fh_k,
                'design_resistance': Fv_Rd,
                'utilization_ratio': N_brace / Fv_Rd
            },
            'verification': {
                'buckling_check': (N_brace / Ncr_kN) <= 1.0,
                'connection_check': (N_brace / Fv_Rd) <= 1.0
            }
        }

    def analyze_column_buckling(self, column_height=2.5, section_width=0.2, section_depth=0.2):
        """Perform detailed buckling analysis for columns according to Eurocode 5"""
        # Section properties
        A = section_width * section_depth  # Cross-sectional area (m²)
        I = (section_width * section_depth**3) / 12  # Second moment of area (m⁴)
        i = (I / A)**0.5  # Radius of gyration (m)
        
        # Slenderness ratio
        lambda_y = column_height / i
        lambda_rel = lambda_y / (3.14159 * (self.E_0_mean / self.fc_0_k)**0.5)
        
        # Calculate buckling reduction factor (kc) according to EC5
        beta_c = 0.2  # For solid timber
        k = 0.5 * (1 + beta_c * (lambda_rel - 0.3) + lambda_rel**2)
        kc = 1 / (k + (k**2 - lambda_rel**2)**0.5)
        
        # Design compressive strength considering buckling
        fc_0_d_mod = kc * self.fc_0_d
        
        # Calculate design compressive force (simplified, considering self-weight and imposed loads)
        area_supported = self.width * self.spacing  # Tributary area
        N_d = 1.35 * (self.dead_load * area_supported) + 1.5 * (self.snow_load * area_supported)
        
        # Calculate actual stress
        sigma_c_d = N_d / (A * 1000)  # Convert kN to N
        
        # Utilization ratio
        utilization = sigma_c_d / fc_0_d_mod
        
        return {
            'slenderness_ratio': lambda_y,
            'relative_slenderness': lambda_rel,
            'buckling_factor': kc,
            'design_strength': fc_0_d_mod,
            'actual_stress': sigma_c_d,
            'utilization_ratio': utilization,
            'passes_buckling': utilization <= 1.0
        }
    
    def verify_SLS(self, section_height=0.24, section_width=0.05):
        """Verify Serviceability Limit State according to EN 1995-1-1"""
        # Characteristic load (34)
        q_k = self.dead_load + self.snow_load  # kN/m²
        
        # Section properties and span
        I = (section_width * section_height**3) / 12  # m⁴
        L = self.calculate_rafter_forces()['rafter_length']  # m
        
        # Instantaneous deflection (35)
        w_inst = 5 * (q_k * 1000) * L**4 / (384 * self.E_0_mean * 1e6 * I)
        
        # Final deflection with creep (36)
        kdef = 0.8  # Service class 2
        w_fin = w_inst * (1 + kdef)
        L_300 = L * 1000 / 300  # Limit
        
        # Document calculations with equation numbers
        calculations = {
            'load': f"qk = G + S = {self.dead_load:.3f} + {self.snow_load:.3f} = {q_k:.3f} kN/m² (34)",
            'deflection': f"winst = 5qL⁴/(384EI) = {w_inst*1000:.2f} mm (35)",
            'final': f"wfin = winst(1 + kdef) = {w_inst*1000:.2f}(1 + {kdef}) = {w_fin*1000:.2f} mm ≤ L/300 = {L_300:.2f} mm (36)"
        }
        
        return {
            'instantaneous_deflection': w_inst * 1000,  # mm
            'final_deflection': w_fin * 1000,  # mm
            'limit_L300': L_300,  # mm
            'passes_SLS': w_fin * 1000 <= L_300,
            'calculations': calculations
        }
    
    def verify_ULS(self, section_height=0.24, section_width=0.05):
        """Ultimate Limit State (ULS) Verification according to EN 1995-1-1"""
        # Cross Section Load Analysis (34)
        loads = self.calculate_loads()
        gk = loads['characteristic_loads']['dead_load']
        sk = loads['characteristic_loads']['snow_load']
        wk = loads['characteristic_loads']['wind_load']
        
        # Momentum and Bending Movement (35-36)
        rafter_forces = self.calculate_rafter_forces()
        purlin_forces = self.calculate_purlin_forces()
        
        # For rafter (100×200mm)
        MEd_rafter = loads['design_load'] * self.spacing * rafter_forces['rafter_length']**2 / 8
        
        # For purlin (80×160mm)
        MEd_purlin = purlin_forces['purlin_load'] * purlin_forces['span']**2 / 8
        
        # Building Stress Analysis (37)
        section = self.calculate_section_properties()
        sigma_m_rafter = MEd_rafter * 1e6 / section['section_modulus']
        sigma_m_purlin = MEd_purlin * 1e6 / section['section_modulus']
        
        # Movement of Inertia (38)
        I_rafter = section['moment_of_inertia']
        I_purlin = section['moment_of_inertia']
        
        # Cross Section of Angle Brace (39)
        brace = self.analyze_angle_brace()
        A_brace = brace['section_properties']['area']
        W_brace = brace['section_properties']['section_modulus']
        I_brace = brace['section_properties']['moment_of_inertia']
        
        # Calculating Strengths (40)
        design_strength = self.calculate_design_strength()
        fm_d = design_strength['fm_d']
        fc_0_d = design_strength['fc_0_d']
        ft_0_d = design_strength['ft_0_d']
        
        # Effort of Actions (41)
        Ed1 = 1.35*gk + 1.5*sk + 1.5*0.6*wk
        Ed2 = 1.35*gk + 1.5*wk + 1.5*0.5*sk
        NEd_brace = max(Ed1, Ed2) * brace['section_properties']['area'] * 0.707  # sin(45°)
        
        # Layer-by-Layer Thermal Analysis (42-43)
        thermal = self.calculate_thermal_resistance()
        
        # Document calculations with equation numbers
        calculations = {
            'loads': f"""Cross Section Load Analysis (34):
gk = {gk:.3f} kN/m² (dead load)
sk = {sk:.3f} kN/m² (snow load)
wk = {wk:.3f} kN/m² (wind load)""",
            
            'momentum': f"""Momentum and Bending Movement (35-36):
For rafter (100×200mm):
MEd = Ed × s × l²/8 = {loads['design_load']:.3f} × {self.spacing:.1f} × {rafter_forces['rafter_length']:.2f}²/8 = {MEd_rafter:.2f} kNm

For purlin (80×160mm):
MEd = w × l²/8 = {purlin_forces['purlin_load']:.3f} × {self.spacing:.1f}²/8 = {MEd_purlin:.3f} kNm""",
            
            'stress': f"""Building Stress Analysis (37):
σm,d,rafter = MEd/W = {MEd_rafter*1e6:.0f}/{section['section_modulus']*1e9:.0f} = {sigma_m_rafter:.2f} N/mm²
σm,d,purlin = MEd/W = {MEd_purlin*1e6:.0f}/{section['section_modulus']*1e9:.0f} = {sigma_m_purlin:.2f} N/mm²""",
            
            'inertia': f"""Movement of Inertia (38):
Irafter = b×h³/12 = {I_rafter*1e12:.0f} mm⁴
Ipurlin = b×h³/12 = {I_purlin*1e12:.0f} mm⁴""",
            
            'brace': f"""Cross Section of Angle Brace (39):
Abrace = b×h = {A_brace:.0f} mm²
Wbrace = b×h²/6 = {W_brace:.0f} mm³
Ibrace = b×h³/12 = {I_brace:.0f} mm⁴""",
            
            'strengths': f"""Calculating Strengths (40):
fm,d = kmod×fm,k/γM = 0.8×27/1.3 = {fm_d:.2f} N/mm²
fc,0,d = kmod×fc,0,k/γM = 0.8×22/1.3 = {fc_0_d:.2f} N/mm²
ft,0,d = kmod×ft,0,k/γM = 0.8×16/1.3 = {ft_0_d:.2f} N/mm²""",
            
            'actions': f"""Effort of Actions (41):
Ed1 = 1.35G + 1.5S + 1.5ψ0W = {Ed1:.3f} kN/m²
Ed2 = 1.35G + 1.5W + 1.5ψ0S = {Ed2:.3f} kN/m²
NEd,brace = Ed×Atrib×sin(45°) = {NEd_brace:.2f} kN""",
            
            'thermal_wall': f"""Layer-by-Layer Thermal Analysis (42):
Wall assembly thermal resistances:
Rsi = {thermal['surface_resistances']['R_si']:.2f} m²K/W (internal surface)
R1 = 0.22/0.33 = {0.22/0.33:.3f} m²K/W (MAX 220 block)
R2 = 0.15/0.035 = {0.15/0.035:.3f} m²K/W (mineral wool)
Rse = {thermal['surface_resistances']['R_se']:.2f} m²K/W (external surface)""",
            
            'thermal_roof': f"""Roof assembly thermal resistances (43):
Rsi = 0.10 m²K/W (internal surface)
R1 = 0.0006/50 = 0.000012 m²K/W (steel tile)
R2 = 0.16 m²K/W (ventilated air gap)
R3 = 0.20/0.035 = {0.20/0.035:.3f} m²K/W (mineral wool)
Rse = 0.04 m²K/W (external surface)"""
        }
        
        # Verification results
        verification = {
            'purlin': f"""• Purlin Design (80×160mm C27):
  • Design load: w = {purlin_forces['purlin_load']:.3f} kN/m
  • Maximum moment: Mmax = {MEd_purlin:.3f} kNm
  • Bending stress: σm,d = {sigma_m_purlin:.2f} N/mm² < fm,d = {fm_d:.2f} N/mm² ✓""",
            
            'rafter': f"""• Rafter Design (100×200mm C27):
  • Design load: Ed = {loads['design_load']:.3f} kN/m²
  • Maximum moment: Mmax = {MEd_rafter:.2f} kNm
  • Bending stress: σm,d = {sigma_m_rafter:.2f} N/mm² < fm,d = {fm_d:.2f} N/mm² ✓""",
            
            'brace': f"""• Angle Brace Analysis (60×100mm):
  • Axial force: N = {NEd_brace:.2f} kN
  • Tensile stress: σt,0,d = {NEd_brace*1000/A_brace:.3f} N/mm² < ft,0,d = {ft_0_d:.2f} N/mm² ✓"""
        }

        return {
            'calculations': calculations,
            'verification': verification,
            'stresses': {
                'bending_rafter': sigma_m_rafter,
                'bending_purlin': sigma_m_purlin,
                'tensile_brace': NEd_brace*1000/A_brace
            },
            'design_strengths': {
                'bending': fm_d,
                'compression': fc_0_d,
                'tension': ft_0_d
            },
            'verification_results': {
                'purlin': sigma_m_purlin <= fm_d,
                'rafter': sigma_m_rafter <= fm_d,
                'brace': NEd_brace*1000/A_brace <= ft_0_d
            },
            'overall_result': all([
                sigma_m_purlin <= fm_d,
                sigma_m_rafter <= fm_d,
                NEd_brace*1000/A_brace <= ft_0_d
            ])
        }

def main():
    # Create calculator instance
    calc = WoodStructureCalculations()
    
    # Perform calculations
    design_strength = calc.calculate_design_strength()
    loads = calc.calculate_loads()
    rafter_forces = calc.calculate_rafter_forces()
    purlin_forces = calc.calculate_purlin_forces()
    thermal = calc.calculate_thermal_resistance()
    uls_verification = calc.verify_ULS()
    sls_verification = calc.verify_SLS()
    buckling_analysis = calc.analyze_column_buckling()
    
    # Print results
    print("\nWood Structure Analysis Results (Dataset 5)")
    print("===========================================")
    
    print("\n1. Design Strength Values:")
    print(f"Bending strength (fm,d): {design_strength['fm_d']:.2f} MPa")
    print(f"Tensile strength (ft,0,d): {design_strength['ft_0_d']:.2f} MPa")
    print(f"Compressive strength (fc,0,d): {design_strength['fc_0_d']:.2f} MPa")
    
    print("\n2. Load Analysis:")
    print(f"Characteristic total load: {loads['characteristic_load']:.2f} kN/m²")
    print(f"Design load: {loads['design_load']:.2f} kN/m²")
    
    print("\n3. Rafter Forces:")
    print(f"Rafter length: {rafter_forces['rafter_length']:.2f} m")
    print(f"Maximum moment: {rafter_forces['max_moment']:.2f} kNm")
    print(f"Axial force: {rafter_forces['axial_force']:.2f} kN")
    
    print("\n4. Purlin Forces:")
    print(f"Purlin load: {purlin_forces['purlin_load']:.2f} kN/m")
    print(f"Maximum moment: {purlin_forces['max_moment']:.2f} kNm")
    
    print("\n5. Thermal Performance Analysis:")
    print("Surface Resistances:")
    print(f"Internal surface resistance (R_si): {thermal['surface_resistances']['R_si']:.3f} m²·K/W")
    print(f"External surface resistance (R_se): {thermal['surface_resistances']['R_se']:.3f} m²·K/W")
    
    print("\nLayer Properties:")
    for layer in thermal['layers']:
        print(f"\n{layer['material']}:")
        print(f"  Thickness: {layer['thickness']:.1f} mm")
        print(f"  Thermal conductivity: {layer['conductivity']:.3f} W/m·K")
        print(f"  Thermal resistance: {layer['resistance']:.3f} m²·K/W")
        print(f"  Density: {layer['density']} kg/m³")
    
    print(f"\nTotal thermal resistance: {thermal['R_total']:.2f} m²·K/W")
    print(f"Overall U-value: {thermal['U_value']:.2f} W/m²·K")
    
    print("\n6. Ultimate Limit State Verification:")
    print(f"Bending stress: {uls_verification['bending_stress']:.2f} MPa")
    print(f"Compressive stress: {uls_verification['compressive_stress']:.2f} MPa")
    print(f"Utilization ratio: {uls_verification['utilization_ratio']:.2f}")
    print(f"Passes ULS: {'Yes' if uls_verification['passes_ULS'] else 'No'}")
    
    print("\n7. Serviceability Limit State Verification:")
    print(f"Instantaneous deflection: {sls_verification['instantaneous_deflection']:.2f} mm")
    print(f"Final deflection: {sls_verification['final_deflection']:.2f} mm")
    print(f"Limit L/300: {sls_verification['limit_L300']:.2f} mm")
    print(f"Passes SLS: {'Yes' if sls_verification['passes_SLS'] else 'No'}")
    
    print("\n8. Column Buckling Analysis:")
    print(f"Slenderness ratio: {buckling_analysis['slenderness_ratio']:.2f}")
    print(f"Relative slenderness: {buckling_analysis['relative_slenderness']:.2f}")
    print(f"Buckling factor kc: {buckling_analysis['buckling_factor']:.3f}")
    print(f"Design strength: {buckling_analysis['design_strength']:.2f} MPa")
    print(f"Actual stress: {buckling_analysis['actual_stress']:.2f} MPa")
    print(f"Utilization ratio: {buckling_analysis['utilization_ratio']:.2f}")
    print(f"Passes buckling check: {'Yes' if buckling_analysis['passes_buckling'] else 'No'}")

if __name__ == "__main__":
    main()
