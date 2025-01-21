import os
import matplotlib
matplotlib.use('Agg')
from create_technical_diagrams import *
from generate_report import (
    create_force_diagram,
    save_high_dpi_image,
    create_brace_diagram,
    create_thermal_diagram,
    create_section_diagram
)

def generate_all_diagrams():
    """Generate all required technical diagrams"""
    print('Creating output directories...')
    os.makedirs('output/figures', exist_ok=True)
    os.makedirs('output/documentation', exist_ok=True)
    
    # Store current directory
    original_dir = os.getcwd()
    figures_dir = os.path.join(original_dir, 'output', 'figures')
    
    try:
        # Change to output/figures directory for saving
        os.chdir(figures_dir)
        print(f'\nChanged to directory: {figures_dir}')
        
        print('\nGenerating floor plan...')
        create_floor_plan()
        
        print('\nGenerating force diagram...')
        create_force_diagram()
        
        print('\nGenerating load distribution diagram...')
        create_load_distribution_diagram()
        
        print('\nGenerating thermal resistance diagram...')
        create_thermal_resistance_diagram()
        
        print('\nGenerating stress analysis diagram...')
        create_stress_analysis_diagram()
        
        print('\nGenerating vertical projection...')
        create_vertical_projection()
        
        print('\nGenerating horizontal projection...')
        create_horizontal_projection()
        
        print('\nGenerating construction details...')
        create_construction_details()
        
        print('\nGenerating connection detail diagram...')
        create_connection_detail_diagram()
        
        print('\nGenerating thermal bridge analysis...')
        create_thermal_bridge_analysis()
        
        print('\nGenerating combined load analysis...')
        create_combined_load_analysis()
        
        print('\nGenerating cross sections diagram...')
        create_cross_sections_diagram()
        
        print('\nGenerating momentum analysis...')
        create_momentum_analysis()
        
        print('\nGenerating inertia analysis...')
        create_inertia_analysis()
        
        print('\nGenerating ULS verification...')
        create_uls_verification()
        
        print('\nGenerating strength analysis...')
        create_strength_analysis()
        
        print('\nGenerating layer analysis...')
        create_layer_analysis()
        
        print('\nGenerating purlin spacing diagram...')
        create_purlin_spacing_diagram()
        
        print('\nGenerating brace diagram...')
        create_brace_diagram()
        
        print('\nGenerating thermal diagram...')
        create_thermal_diagram()
        
        print('\nGenerating section diagram...')
        create_section_diagram()
        
        print('\nAll diagrams generated successfully.')
    
    finally:
        # Change back to original directory
        os.chdir(original_dir)
        print(f'\nChanged back to directory: {original_dir}')

if __name__ == '__main__':
    generate_all_diagrams()
