import os
import matplotlib
matplotlib.use('Agg')
from create_technical_diagrams import (
    create_load_distribution_diagram,
    create_thermal_resistance_diagram,
    create_stress_analysis_diagram,
    create_vertical_projection,
    create_horizontal_projection,
    create_construction_details,
    create_connection_detail_diagram,
    create_thermal_bridge_analysis,
    create_combined_load_analysis,
    create_cross_sections_diagram,
    create_momentum_analysis,
    create_inertia_analysis,
    create_uls_verification,
    create_strength_analysis,
    create_layer_analysis,
    create_purlin_spacing_diagram
)

def generate_all_diagrams():
    """Generate all required technical diagrams"""
    print('Creating output directories...')
    os.makedirs('output/figures', exist_ok=True)
    os.makedirs('output/documentation', exist_ok=True)
    os.makedirs('dist/drawings/projections', exist_ok=True)
    os.makedirs('dist/drawings/details', exist_ok=True)
    
    # Store current directory
    original_dir = os.getcwd()
    figures_dir = os.path.join(original_dir, 'output', 'figures')
    
    try:
        # Change to output/figures directory for saving
        os.chdir(figures_dir)
        print(f'\nChanged to directory: {figures_dir}')
        
        # Generate all diagrams
        diagrams = [
            ('load distribution', create_load_distribution_diagram),
            ('thermal resistance', create_thermal_resistance_diagram),
            ('stress analysis', create_stress_analysis_diagram),
            ('vertical projection', create_vertical_projection),
            ('horizontal projection', create_horizontal_projection),
            ('construction details', create_construction_details),
            ('connection detail', create_connection_detail_diagram),
            ('thermal bridge analysis', create_thermal_bridge_analysis),
            ('combined load analysis', create_combined_load_analysis),
            ('cross sections', create_cross_sections_diagram),
            ('momentum analysis', create_momentum_analysis),
            ('inertia analysis', create_inertia_analysis),
            ('ULS verification', create_uls_verification),
            ('strength analysis', create_strength_analysis),
            ('layer analysis', create_layer_analysis),
            ('purlin spacing', create_purlin_spacing_diagram)
        ]
        
        for name, func in diagrams:
            try:
                print(f'\nGenerating {name} diagram...')
                func()
                print(f'{name} diagram generated successfully.')
            except Exception as e:
                print(f'Error generating {name} diagram: {str(e)}')
                raise
        
        print('\nAll diagrams generated successfully.')
    
    finally:
        # Change back to original directory
        os.chdir(original_dir)
        print(f'\nChanged back to directory: {original_dir}')

if __name__ == '__main__':
    generate_all_diagrams()
