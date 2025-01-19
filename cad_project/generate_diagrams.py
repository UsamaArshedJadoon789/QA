#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Arrow, Arc
from matplotlib.lines import Line2D
from PIL import Image

def create_thermal_envelope_diagram():
    """Create detailed thermal envelope diagram showing wall and roof assemblies"""
    # Set exact figure dimensions for HD resolution
    plt.rcParams['figure.dpi'] = 300.0
    plt.rcParams['savefig.dpi'] = 300.0
    plt.rcParams['figure.figsize'] = [6.827, 5.12]  # 2048/300, 1536/300
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # Create figure with exact dimensions and force DPI
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_dpi(300.0)
    fig.set_size_inches(6.827, 5.12, forward=True)
    
    # Wall Assembly
    ax1.set_title('Wall Assembly Thermal Layers', pad=20, fontsize=14)
    layers = [
        ('External Surface (Rse = 0.04)', 10),
        ('Mineral Wool\n150mm\nλ = 0.035 W/(m·K)', 150),
        ('MAX 220 Block\n220mm\nλ = 0.33 W/(m·K)', 220),
        ('Internal Surface (Rsi = 0.13)', 10)
    ]
    
    y = 0
    for name, thickness in layers:
        rect = Rectangle((0, y), 300, thickness, 
                        facecolor='lightgray', edgecolor='black')
        ax1.add_patch(rect)
        ax1.text(310, y + thickness/2, name, 
                verticalalignment='center', fontsize=10)
        y += thickness
    
    ax1.set_xlim(-50, 600)
    ax1.set_ylim(-20, 450)
    ax1.set_xlabel('Width (mm)')
    ax1.set_ylabel('Height (mm)')
    
    # Roof Assembly
    ax2.set_title('Roof Assembly Thermal Layers', pad=20, fontsize=14)
    roof_layers = [
        ('External Surface (Rse = 0.04)', 10),
        ('Steel Tile 0.6mm\nλ = 50 W/(m·K)', 0.6),
        ('Ventilated Air Gap\nR = 0.16 m²K/W', 50),
        ('Mineral Wool\n200mm\nλ = 0.035 W/(m·K)', 200),
        ('Internal Surface (Rsi = 0.10)', 10)
    ]
    
    y = 0
    scale = 2  # Scale up thin layers for visibility
    for name, thickness in roof_layers:
        rect = Rectangle((0, y), 300, thickness * scale,
                        facecolor='lightgray', edgecolor='black')
        ax2.add_patch(rect)
        ax2.text(310, y + (thickness * scale)/2, name,
                verticalalignment='center', fontsize=10)
        y += thickness * scale
    
    ax2.set_xlim(-50, 600)
    ax2.set_ylim(-20, 600)
    ax2.set_xlabel('Width (mm)')
    
    plt.tight_layout()
    # Save with explicit resolution metadata
    from PIL import Image
    fig.savefig('enhanced_exports/screenshots/thermal_details.png',
                dpi=300.0, bbox_inches=None)
    # Update DPI metadata
    img = Image.open('enhanced_exports/screenshots/thermal_details.png')
    img.info['dpi'] = (300, 300)
    img.save('enhanced_exports/screenshots/thermal_details.png', dpi=(300, 300))
    plt.close()

def create_structural_connections_diagram():
    """Create detailed structural connection diagrams"""
    # Set exact figure dimensions for HD resolution
    plt.rcParams['figure.dpi'] = 300.0
    plt.rcParams['savefig.dpi'] = 300.0
    plt.rcParams['figure.figsize'] = [6.827, 5.12]  # 2048/300, 1536/300
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # Create figure with exact dimensions and force DPI
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_dpi(300.0)
    fig.set_size_inches(6.827, 5.12, forward=True)
    
    # Column-Foundation Connection
    ax1.set_title('Column-Foundation Connection Detail', pad=20, fontsize=14)
    
    # Foundation
    foundation = Rectangle((-200, -400), 400, 400,
                         facecolor='lightgray', edgecolor='black')
    ax1.add_patch(foundation)
    
    # Column
    column = Rectangle((-75, 0), 150, 300,
                      facecolor='wheat', edgecolor='black')
    ax1.add_patch(column)
    
    # Base plate
    plate = Rectangle((-100, -20), 200, 20,
                     facecolor='silver', edgecolor='black')
    ax1.add_patch(plate)
    
    # Anchor bolts
    for x in [-75, 75]:
        ax1.plot([x, x], [-20, -200], 'k-', linewidth=2)
        ax1.plot([x-10, x+10], [-200, -200], 'k-', linewidth=2)
    
    # Dimensions
    ax1.annotate('', xy=(-75, -300), xytext=(75, -300),
                arrowprops=dict(arrowstyle='<->'))
    ax1.text(0, -330, '150mm', ha='center')
    
    ax1.set_xlim(-250, 250)
    ax1.set_ylim(-450, 350)
    ax1.set_xlabel('Width (mm)')
    ax1.set_ylabel('Height (mm)')
    
    # Roof-Column Connection
    ax2.set_title('Roof-Column Connection Detail', pad=20, fontsize=14)
    
    # Column top
    column_top = Rectangle((-75, 0), 150, 150,
                         facecolor='wheat', edgecolor='black')
    ax2.add_patch(column_top)
    
    # Rafter
    rafter_points = np.array([
        [-200, 150],
        [200, 150 + np.tan(np.radians(16)) * 400],
        [200, 150 + np.tan(np.radians(16)) * 400 - 100],
        [-200, 50]
    ])
    ax2.fill(rafter_points[:, 0], rafter_points[:, 1],
             facecolor='wheat', edgecolor='black')
    
    # Steel plates
    plate1 = Rectangle((-100, 130), 200, 6,
                      facecolor='silver', edgecolor='black')
    ax2.add_patch(plate1)
    
    # Bolts
    for x in [-50, 50]:
        ax2.plot([x, x], [130, 136], 'k-', linewidth=2)
        ax2.plot([x-5, x+5], [133, 133], 'ko', markersize=3)
    
    # Dimensions
    ax2.annotate('', xy=(-100, 100), xytext=(100, 100),
                arrowprops=dict(arrowstyle='<->'))
    ax2.text(0, 80, '200mm', ha='center')
    
    # Angle notation
    arc = Arc((0, 150), 100, 100, theta1=0, theta2=16,
              edgecolor='black', linestyle='--')
    ax2.add_patch(arc)
    ax2.text(30, 170, '16°', ha='left')
    
    ax2.set_xlim(-250, 250)
    ax2.set_ylim(-50, 400)
    ax2.set_xlabel('Width (mm)')
    
    plt.tight_layout()
    # Save with explicit resolution metadata
    from PIL import Image
    fig.savefig('enhanced_exports/screenshots/connection_details.png',
                dpi=300.0, bbox_inches=None)
    # Update DPI metadata
    img = Image.open('enhanced_exports/screenshots/connection_details.png')
    img.info['dpi'] = (300, 300)
    img.save('enhanced_exports/screenshots/connection_details.png', dpi=(300, 300))
    plt.close()

def create_load_distribution_diagram():
    """Create diagram showing load distribution and force analysis"""
    # Set exact figure dimensions for HD resolution
    plt.rcParams['figure.dpi'] = 300.0
    plt.rcParams['savefig.dpi'] = 300.0
    plt.rcParams['figure.figsize'] = [6.827, 5.12]  # 2048/300, 1536/300
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # Create figure with exact dimensions and force DPI
    fig, ax = plt.subplots()
    fig.set_dpi(300.0)
    fig.set_size_inches(6.827, 5.12, forward=True)
    
    # Building outline
    building_points = np.array([
        [-360, 0],    # Base left
        [360, 0],     # Base right
        [360, 250],   # Wall right
        [360, 265],   # Top right
        [0, 330],     # Ridge
        [-360, 265],  # Top left
        [-360, 250],  # Wall left
        [-360, 0]     # Back to start
    ])
    
    # Draw building outline
    ax.plot(building_points[:, 0], building_points[:, 1], 'k-', linewidth=2)
    
    # Add roof angle
    arc = Arc((360, 265), 100, 100, theta1=180, theta2=196,
              edgecolor='black', linestyle='--')
    ax.add_patch(arc)
    ax.text(380, 280, '16°', ha='left')
    
    # Add loads
    # Snow load
    snow_spacing = 50.0
    snow_positions = np.arange(-350.0, 351.0, snow_spacing)
    for x in snow_positions:
        if x < 0:
            y = 265.0 + (x + 360.0) * np.tan(np.radians(16.0))
        else:
            y = 265.0 + (360.0 - x) * np.tan(np.radians(16.0))
        ax.arrow(float(x), float(y + 30), 0.0, -20.0, head_width=10.0, head_length=10.0,
                fc='blue', ec='blue', alpha=0.5)
        
    # Wind load
    wind_spacing = 100.0
    wind_positions = np.arange(0.0, 251.0, wind_spacing)
    for y in wind_positions:
        ax.arrow(-400.0, float(y), 30.0, 0.0, head_width=10.0, head_length=10.0,
                fc='red', ec='red', alpha=0.5)
    
    # Add legend and labels
    ax.text(-400, 350, 'Design Loads:', fontsize=12)
    ax.plot([-350, -300], [350, 350], 'b-', alpha=0.5, label='Snow Load (0.56 kN/m²)')
    ax.plot([-350, -300], [330, 330], 'r-', alpha=0.5, label='Wind Load (0.483 kN/m²)')
    ax.legend(loc='upper left')
    
    # Add dimensions
    ax.annotate('', xy=(-360, -20), xytext=(360, -20),
                arrowprops=dict(arrowstyle='<->'))
    ax.text(0, -40, 'b = 7.2m', ha='center')
    
    ax.annotate('', xy=(-380, 0), xytext=(-380, 265),
                arrowprops=dict(arrowstyle='<->'))
    ax.text(-400, 130, 'h1 = 2.5m', va='center', rotation=90)
    
    # Set limits and labels
    ax.set_xlim(-450, 450)
    ax.set_ylim(-50, 400)
    ax.set_xlabel('Width (mm)')
    ax.set_ylabel('Height (mm)')
    ax.set_title('Load Distribution Analysis', pad=20, fontsize=14)
    
    plt.tight_layout()
    # Save with explicit resolution metadata
    from PIL import Image
    fig.savefig('enhanced_exports/screenshots/load_distribution.png',
                dpi=300.0, bbox_inches=None)
    # Update DPI metadata
    img = Image.open('enhanced_exports/screenshots/load_distribution.png')
    img.info['dpi'] = (300, 300)
    img.save('enhanced_exports/screenshots/load_distribution.png', dpi=(300, 300))
    plt.close()

def create_thermal_bridge_diagram():
    """Create detailed thermal bridge analysis diagram"""
    # Set exact figure dimensions for HD resolution
    plt.rcParams['figure.dpi'] = 300.0
    plt.rcParams['savefig.dpi'] = 300.0
    plt.rcParams['figure.figsize'] = [6.827, 5.12]  # 2048/300, 1536/300
    plt.rcParams['figure.constrained_layout.use'] = True
    
    # Create figure with exact dimensions and force DPI
    fig, ax = plt.subplots()
    fig.set_dpi(300.0)
    fig.set_size_inches(6.827, 5.12, forward=True)
    
    # Wall-roof junction detail
    wall_points = np.array([
        [0, 0],      # Base
        [220, 0],    # Wall width
        [220, 400],  # Wall height
        [0, 400],    # Top
        [0, 0]       # Close polygon
    ])
    
    # Draw wall
    ax.fill(wall_points[:, 0], wall_points[:, 1],
            facecolor='lightgray', edgecolor='black', alpha=0.5,
            label='MAX 220 Block')
    
    # Add insulation layer
    insulation_points = np.array([
        [220, 0],
        [370, 0],    # 150mm insulation
        [370, 400],
        [220, 400],
        [220, 0]
    ])
    ax.fill(insulation_points[:, 0], insulation_points[:, 1],
            facecolor='yellow', edgecolor='black', alpha=0.3,
            label='Mineral Wool 150mm')
    
    # Add roof structure
    rafter_points = np.array([
        [0, 400],
        [370, 400],
        [370, 600],
        [0, 600],
        [0, 400]
    ])
    ax.fill(rafter_points[:, 0], rafter_points[:, 1],
            facecolor='wheat', edgecolor='black', alpha=0.5,
            label='Timber Rafter')
    
    # Add thermal bridge indicators
    # Heat flow arrows
    arrow_props = dict(arrowstyle='->',
                      linewidth=2,
                      color='red',
                      alpha=0.6)
    
    # Major thermal bridge at junction
    ax.annotate('', xy=(200, 420), xytext=(50, 420),
                arrowprops=arrow_props)
    ax.annotate('Heat Flow', xy=(100, 440),
                ha='center', color='red')
    
    # Temperature gradient indicators
    temps = ['20°C', '18°C', '15°C', '12°C', '8°C', '5°C', '0°C']
    x_positions = np.linspace(0, 370, len(temps))
    for x, temp in zip(x_positions, temps):
        ax.text(x, -30, temp, ha='center')
    
    # Add legend and labels
    ax.legend(loc='upper right')
    ax.set_title('Thermal Bridge Analysis - Wall-Roof Junction',
                pad=20, fontsize=14)
    
    # Set limits and labels
    ax.set_xlim(-50, 420)
    ax.set_ylim(-50, 650)
    ax.set_xlabel('Width (mm)')
    ax.set_ylabel('Height (mm)')
    
    plt.tight_layout()
    # Save with explicit resolution metadata
    from PIL import Image
    fig.savefig('enhanced_exports/screenshots/thermal_bridge.png',
                dpi=300.0, bbox_inches=None)
    # Update DPI metadata
    img = Image.open('enhanced_exports/screenshots/thermal_bridge.png')
    img.info['dpi'] = (300, 300)
    img.save('enhanced_exports/screenshots/thermal_bridge.png', dpi=(300, 300))
    plt.close()

if __name__ == "__main__":
    create_thermal_envelope_diagram()
    create_structural_connections_diagram()
    create_load_distribution_diagram()
    create_thermal_bridge_diagram()
