import os
from create_technical_diagrams import *

def generate_all_diagrams():
    """Generate all missing technical diagrams"""
    print('Creating output directory...')
    os.makedirs('output/figures', exist_ok=True)
    
    print('\nGenerating momentum analysis...')
    create_momentum_analysis()
    
    print('\nGenerating inertia analysis...')
    create_inertia_analysis()
    
    print('\nGenerating strength analysis...')
    create_strength_analysis()
    
    print('\nGenerating layer analysis...')
    create_layer_analysis()
    
    print('\nGenerating ULS verification...')
    create_uls_verification()
    
    print('\nGenerating purlin spacing diagram...')
    create_purlin_spacing_diagram()
    
    print('\nAll diagrams generated successfully.')

if __name__ == '__main__':
    generate_all_diagrams()
