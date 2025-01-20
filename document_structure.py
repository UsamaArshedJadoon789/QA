import os
import json
from collections import OrderedDict

def create_document_structure():
    """Create structured representation of the document content"""
    document = OrderedDict({
        "title": "Civil Engineering Project - Dataset 5 Analysis",
        "sections": {
            "1_load_analysis": {
                "title": "Load Analysis",
                "type": "Load Analysis",
                "content": {
                    "load_distribution_calculations": {
                        "title": "Load Distribution Analysis",
                        "type": "Load Distribution",
                        "calculations": {
                            "characteristic_loads": {
                                "snow_load": "0.56 kN/m²",
                                "wind_pressure": "0.483 kN/m²",
                                "dead_load": "0.297 kN/m²"
                            },
                            "design_loads": {
                                "total_design_load": "1.343 kN/m²",
                                "load_combinations": {
                                    "ULS1": "1.35G + 1.5S",
                                    "ULS2": "1.35G + 1.5W",
                                    "ULS3": "1.35G + 1.05S + 0.9W"
                                }
                            },
                            "distributed_loads": {
                                "rafter": "1.477 kN/m",
                                "purlin": "1.624 kN/m"
                            }
                        }
                    },
                    "load_distribution": {
                        "image": "extracted_image_p8_1.png",
                        "description": "Comprehensive analysis of structural loads showing snow load distribution and wind pressure. The diagram illustrates the combined effect of vertical and horizontal forces on the building structure.",
                        "technical_details": "Load distribution diagram showing the application of combined loads (snow, wind, and dead loads) on the roof structure. The arrows indicate force directions and magnitudes, with special attention to the critical points at connections."
                    }
                }
            },
            "2_thermal_analysis": {
                "title": "Thermal Analysis",
                "type": "Thermal Analysis",
                "content": {
                    "thermal_performance_calculations": {
                        "title": "Thermal Performance Analysis",
                        "type": "Thermal Performance",
                        "calculations": {
                            "wall_assembly": {
                                "u_value": "0.195 W/m²K",
                                "total_resistance": "5.123 m²K/W",
                                "layer_analysis": {
                                    "block": {"thickness": "220mm", "λ": "0.45 W/(m·K)"},
                                    "insulation": {"thickness": "150mm", "λ": "0.04 W/(m·K)"},
                                    "surface_resistances": {"Rsi": "0.13", "Rse": "0.04"}
                                }
                            },
                            "roof_assembly": {
                                "u_value": "0.166 W/m²K",
                                "total_resistance": "6.014 m²K/W",
                                "layer_analysis": {
                                    "insulation": {"thickness": "200mm", "λ": "0.04 W/(m·K)"},
                                    "timber": {"thickness": "100mm", "λ": "0.13 W/(m·K)"},
                                    "surface_resistances": {"Rsi": "0.10", "Rse": "0.04"}
                                }
                            }
                        }
                    },
                    "thermal_bridging": {
                        "image": "extracted_image_p9_1.png",
                        "description": "Detailed analysis of thermal bridging at the wall-roof junction, showing temperature gradients and heat flow patterns through the building envelope.",
                        "technical_details": "Thermal bridge analysis showing heat flow paths and temperature distribution at critical junctions. The color gradient indicates temperature variation, with special focus on potential condensation risk areas."
                    }
                }
            },
            "3_technical_drawings": {
                "title": "Technical Drawings",
                "subsections": {
                    "specifications": {
                        "title": "Drawing Specifications",
                        "table": {
                            "headers": ["Drawing Type", "Scale", "Key Elements", "Format"],
                            "rows": [
                                ["Vertical Projection", "1:50", "Heights, angles, wall sections", "DXF/PNG"],
                                ["Horizontal Projection", "1:50", "Dimensions, layout, spacing", "DXF/PNG"],
                                ["Construction Details", "1:10", "Connections, assemblies", "DXF/PNG"]
                            ]
                        }
                    },
                    "projections": {
                        "title": "Building Projections",
                        "vertical": {
                            "title": "Vertical Projection (1:50)",
                            "image": "extracted_image_p10_1.png",
                            "description": "Vertical projection showing building elevations, heights, and roof angle.",
                            "technical_details": {
                                "heights": {"h1": "2.5m", "h2": "2.65m"},
                                "roof_angle": "16°",
                                "ground_level": "-1.4 m.a.s.l"
                            },
                            "key_elements": [
                                "Wall sections with MAX 220 block construction",
                                "Roof structure with 16° pitch",
                                "Column positions and heights",
                                "Thermal insulation layer details"
                            ]
                        },
                        "horizontal": {
                            "title": "Horizontal Projection (1:50)",
                            "image": "extracted_image_p11_1.png",
                            "description": "Horizontal projection showing building layout and dimensions.",
                            "technical_details": {
                                "width": "7.2m",
                                "lengths": {"L1": "6.6m", "L2": "10.8m"},
                                "spacing": "1.1m"
                            },
                            "key_elements": [
                                "Overall building dimensions",
                                "Purlin and rafter spacing",
                                "Column grid layout",
                                "Wall thickness details"
                            ]
                        }
                    },
                    "vertical_projection": {
                        "title": "Vertical Projection (1:50)",
                        "image": "extracted_image_p10_1.png",
                        "specifications": {
                            "heights": {"h1": "2.5m", "h2": "2.65m"},
                            "roof_angle": "16°",
                            "ground_level": "-1.4 m.a.s.l",
                            "wall_construction": "MAX 220 block with mineral wool insulation"
                        }
                    },
                    "horizontal_projection": {
                        "title": "Horizontal Projection (1:50)",
                        "image": "extracted_image_p11_1.png",
                        "specifications": {
                            "width": "7.2m",
                            "lengths": {"L1": "6.6m", "L2": "10.8m"},
                            "purlin_spacing": "1.1m"
                        }
                    }
                }
            },
            "4_structural_details": {
                "title": "Structural Details",
                "subsections": {
                    "construction": {
                        "title": "Construction Details (1:10)",
                        "image": "extracted_image_p12_1.png",
                        "description": "Detailed construction drawings showing component dimensions and assembly details.",
                        "components": {
                            "timber": "C27",
                            "columns": "150×150mm",
                            "purlins": "80×160mm",
                            "rafters": "100×200mm",
                            "wall": "MAX 220 block + 150mm mineral wool"
                        },
                        "technical_details": {
                            "connections": {
                                "column_base": "200×200×10mm steel plate with M16 grade 8.8 anchors",
                                "rafter_purlin": "M12 grade 8.8 bolts with steel plates",
                                "wall_column": "Embedded steel plates with anchor bolts"
                            },
                            "assembly_sequence": [
                                "Foundation preparation and anchor placement",
                                "Column erection and alignment",
                                "Rafter installation and connection",
                                "Purlin placement and fastening",
                                "Wall construction and insulation"
                            ]
                        }
                    },
                    "thermal_envelope": {
                        "title": "Thermal Envelope Details",
                        "image": "extracted_image_p13_1.png",
                        "specifications": {
                            "wall_assembly": {"U_value": "0.195 W/m²K"},
                            "roof_assembly": {"U_value": "0.166 W/m²K"}
                        }
                    },
                    "connections": {
                        "title": "Structural Connection Details",
                        "image": "extracted_image_p14_1.png",
                        "specifications": {
                            "column_foundation": {
                                "base_plate": "200×200×10mm",
                                "anchors": "M16 grade 8.8"
                            },
                            "roof_column": {
                                "plates": "6mm steel",
                                "bolts": "M12 grade 8.8"
                            }
                        }
                    }
                }
            },
            "5_calculations": {
                "title": "Calculations",
                "type": "Calculations",
                "subsections": {
                    "loads": {
                        "title": "Load and Momentum Analysis",
                        "type": "Momentum Analysis",
                        "design_loads": {
                            "dead_load": "0.297 kN/m²",
                            "snow_load": "0.56 kN/m²",
                            "wind_load": "0.483 kN/m²"
                        },
                        "momentum": {
                            "rafter": "MEd = 6.12 kNm",
                            "purlin": "MEd = 0.623 kNm"
                        },
                        "load_combinations": {
                            "ULS_1": "1.35 × G + 1.5 × S",
                            "ULS_2": "1.35 × G + 1.5 × W",
                            "ULS_3": "1.35 × G + 1.05 × S + 0.9 × W"
                        }
                    },
                    "stress": {
                        "title": "Building Stress Analysis",
                        "type": "Stress Analysis",
                        "results": {
                            "rafter": {
                                "bending_stress": "σm,d = 9.18 N/mm²",
                                "axial_stress": "σc,d = 2.34 N/mm²",
                                "shear_stress": "τd = 0.76 N/mm²"
                            },
                            "purlin": {
                                "bending_stress": "σm,d = 1.83 N/mm²",
                                "axial_stress": "σc,d = 0.45 N/mm²",
                                "shear_stress": "τd = 0.21 N/mm²"
                            }
                        },
                        "verification": {
                            "type": "ULS Verification",
                            "title": "Ultimate Limit State Verification",
                            "combined_stress_ratio": "0.76 ≤ 1.0",
                            "stability_check": "kc,y × σc,d / fc,d + km × σm,d / fm,d ≤ 1.0",
                            "verification_criteria": [
                                "Combined stress ratio must not exceed 1.0",
                                "Stability check must satisfy Eurocode 5 requirements",
                                "All component stresses within material limits"
                            ]
                        }
                    },
                    "thermal": {
                        "title": "Thermal Performance Results",
                        "type": "Thermal Performance",
                        "wall_assembly": {
                            "total_resistance": "5.123 m²K/W",
                            "U_value": "0.195 W/(m²K)",
                            "layer_analysis": {
                                "block": {"thickness": "220mm", "λ": "0.45 W/(m·K)"},
                                "insulation": {"thickness": "150mm", "λ": "0.04 W/(m·K)"},
                                "surface_resistances": {"Rsi": "0.13", "Rse": "0.04"}
                            }
                        },
                        "roof_assembly": {
                            "total_resistance": "6.014 m²K/W",
                            "U_value": "0.166 W/(m²K)",
                            "layer_analysis": {
                                "insulation": {"thickness": "200mm", "λ": "0.04 W/(m·K)"},
                                "timber": {"thickness": "100mm", "λ": "0.13 W/(m·K)"},
                                "surface_resistances": {"Rsi": "0.10", "Rse": "0.04"}
                            }
                        }
                    }
                }
            }
        }
    })
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save structure to JSON file
    output_path = os.path.join('output', 'document_structure.json')
    with open(output_path, 'w') as f:
        json.dump(document, f, indent=2)
    
    # Print structure overview
    print("Document structure created successfully")
    print(f"\nSaved to: {output_path}")
    print("\nStructure overview:")
    
    def print_section(section_data, indent=0):
        """Recursively print section structure"""
        if isinstance(section_data, dict):
            if 'title' in section_data:
                print("  " * indent + f"- {section_data['title']}")
            if 'subsections' in section_data:
                for _, subsection in section_data['subsections'].items():
                    print_section(subsection, indent + 1)
    
    # Print the structure
    sections = document.get('sections', {})
    if isinstance(sections, dict):
        for _, section in sections.items():
            print_section(section)
    
    return document

if __name__ == "__main__":
    document = create_document_structure()
