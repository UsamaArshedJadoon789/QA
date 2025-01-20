import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Arc, Circle
from matplotlib import patches
import matplotlib.gridspec as gridspec

def set_engineering_style():
    """Configure matplotlib for engineering diagrams"""
    plt.style.use('default')  # Use default style as base
    
    # Figure size and resolution
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    
    # Font settings
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = ['DejaVu Sans']
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 16
    
    # Grid settings
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.5
    
    # Layout and spacing
    plt.rcParams['figure.constrained_layout.use'] = True
    plt.rcParams['figure.constrained_layout.h_pad'] = 0.4
    plt.rcParams['figure.constrained_layout.w_pad'] = 0.4
    plt.rcParams['figure.subplot.wspace'] = 0.3
    plt.rcParams['figure.subplot.hspace'] = 0.3
    
    # Save settings
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.pad_inches'] = 0.5
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.edgecolor'] = 'none'
    
    # Axes settings
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams['axes.facecolor'] = 'white'

def create_load_distribution_diagram():
    """Create load distribution diagram with forces"""
    set_engineering_style()
    fig, ax = plt.subplots()
    
    # Roof outline
    roof_points = np.array([
        [0, 2.5],
        [3.6, 2.65],
        [7.2, 2.5],
        [0, 2.5]
    ])
    
    # Plot roof outline
    ax.plot(roof_points[:, 0], roof_points[:, 1], 'k-', linewidth=2)
    
    # Add distributed loads
    x = np.linspace(0, 7.2, 50)
    y_roof = 2.5 + (0.15/7.2) * x
    
    # Snow load arrows
    arrow_spacing = 0.4
    for xi in np.arange(0, 7.2, arrow_spacing):
        yi = 2.5 + (0.15/7.2) * xi
        ax.arrow(float(xi), float(yi + 0.2), 0, -0.15, head_width=0.05, 
                head_length=0.05, fc='blue', ec='blue', alpha=0.5)
    
    # Wind load arrows
    for xi in np.arange(0, 7.2, arrow_spacing):
        yi = 2.5 + (0.15/7.2) * xi
        ax.arrow(float(xi - 0.2), float(yi), 0.15, 0, head_width=0.05,
                head_length=0.05, fc='red', ec='red', alpha=0.5)
    
    # Add labels
    ax.text(3.6, 3.0, 'Snow Load: 0.56 kN/m²', ha='center')
    ax.text(1.0, 2.7, 'Wind Load: 0.483 kN/m²', ha='left')
    
    ax.set_xlim(-0.5, 7.7)
    ax.set_ylim(2.0, 3.2)
    ax.set_aspect('equal')
    ax.set_title('Load Distribution Diagram')
    ax.set_xlabel('Width (m)')
    ax.set_ylabel('Height (m)')
    
    plt.tight_layout(pad=1.5)
    plt.savefig('output/figures/load_distribution.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_thermal_resistance_diagram():
    """Create comprehensive thermal resistance analysis with layer details"""
    set_engineering_style()
    fig = plt.figure(figsize=(20, 15))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # Wall assembly subplot
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Enhanced wall assembly with material properties
    layers_wall = [
        ('External Surface (Rse)', 0.04, 'lightgray', '-'),
        ('MAX 220 Block', 0.489, 'lightcoral', '0.45'),
        ('Mineral Wool', 3.750, 'lightyellow', '0.04'),
        ('Internal Surface (Rsi)', 0.13, 'lightgray', '-')
    ]
    
    # Plot enhanced wall assembly
    y_pos = np.arange(len(layers_wall))
    resistance_wall = [layer[1] for layer in layers_wall]
    colors_wall = [layer[2] for layer in layers_wall]
    
    bars_wall = ax1.barh(y_pos, resistance_wall, color=colors_wall)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([f"{layer[0]}\nλ = {layer[3]} W/(m·K)" for layer in layers_wall])
    ax1.set_xlabel('Thermal Resistance (m²K/W)')
    ax1.set_title('Wall Assembly Thermal Resistance\nU-value = 0.195 W/(m²·K)')
    
    # Add resistance values on bars
    for i, bar in enumerate(bars_wall):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2,
                f'R = {resistance_wall[i]:.3f} m²K/W',
                va='center', ha='left', fontsize=9)
    
    # Roof assembly subplot
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Enhanced roof assembly with material properties
    layers_roof = [
        ('External Surface (Rse)', 0.04, 'lightgray', '-'),
        ('Steel Tile 0.6mm', 0.001, 'silver', '50'),
        ('Ventilated Air Gap', 0.160, 'white', '-'),
        ('Mineral Wool', 5.000, 'lightyellow', '0.04'),
        ('C27 Timber', 0.769, 'burlywood', '0.13'),
        ('Internal Surface (Rsi)', 0.10, 'lightgray', '-')
    ]
    
    # Plot enhanced roof assembly
    y_pos = np.arange(len(layers_roof))
    resistance_roof = [layer[1] for layer in layers_roof]
    colors_roof = [layer[2] for layer in layers_roof]
    
    bars_roof = ax2.barh(y_pos, resistance_roof, color=colors_roof)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([f"{layer[0]}\nλ = {layer[3]} W/(m·K)" for layer in layers_roof])
    ax2.set_xlabel('Thermal Resistance (m²K/W)')
    ax2.set_title('Roof Assembly Thermal Resistance\nU-value = 0.166 W/(m²·K)')
    
    # Add resistance values on bars
    for i, bar in enumerate(bars_roof):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2,
                f'R = {resistance_roof[i]:.3f} m²K/W',
                va='center', ha='left', fontsize=9)
    
    # Temperature gradient subplot
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Create temperature gradient visualization
    x = np.linspace(0, 1, 100)
    layers_x = np.cumsum([0, 0.1, 0.3, 0.5, 0.1])  # Normalized layer thicknesses
    T_ext = -20  # External temperature (°C)
    T_int = 20   # Internal temperature (°C)
    
    # Calculate temperature at layer boundaries
    R_total_wall = sum(resistance_wall)
    T_layers = [T_int - (T_int - T_ext) * sum(resistance_wall[:i])/R_total_wall 
                for i in range(len(resistance_wall) + 1)]
    
    # Plot temperature gradient
    ax3.plot(layers_x, T_layers, 'r-', linewidth=2, label='Temperature')
    ax3.fill_between(layers_x, T_layers, T_ext, alpha=0.1, color='red')
    
    ax3.set_xlabel('Wall Thickness')
    ax3.set_ylabel('Temperature (°C)')
    ax3.set_title('Temperature Gradient Through Wall Assembly')
    ax3.grid(True)
    ax3.legend()
    
    # Heat flux subplot
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate heat flux
    q = (T_int - T_ext) / R_total_wall
    q_layers = [q] * len(layers_wall)  # Constant heat flux through layers
    
    # Plot heat flux
    ax4.bar(range(len(layers_wall)), q_layers, 
            color=[layer[2] for layer in layers_wall],
            alpha=0.7)
    ax4.set_xticks(range(len(layers_wall)))
    ax4.set_xticklabels([layer[0] for layer in layers_wall], rotation=45)
    ax4.set_ylabel('Heat Flux (W/m²)')
    ax4.set_title(f'Heat Flux Through Wall Assembly\nq = {q:.2f} W/m²')
    
    # Add equations and annotations
    fig.text(0.02, 0.02, 
             'Thermal Resistance Calculations:\n' +
             'R = d/λ  [m²·K/W]\n' +
             'U = 1/ΣR  [W/(m²·K)]\n' +
             'q = (Ti - Te)/ΣR  [W/m²]',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.savefig('output/figures/thermal_resistance.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_stress_analysis_diagram():
    """Create stress analysis visualization"""
    set_engineering_style()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Bending moment diagram
    x = np.linspace(0, 7.2, 100)
    moment = -(0.623 * x * (7.2 - x)) / 2  # Simplified moment equation
    
    ax1.plot(x, moment, 'b-', linewidth=2)
    ax1.fill_between(x, moment, alpha=0.2)
    ax1.set_title('Bending Moment Diagram')
    ax1.set_xlabel('Length (m)')
    ax1.set_ylabel('Moment (kNm)')
    ax1.grid(True)
    
    # Stress distribution
    def create_stress_distribution(ax, height, width, stress_max):
        # Cross-section outline
        rect = Rectangle((-width/2, -height/2), width, height,
                        fill=False, color='black')
        ax.add_patch(rect)
        
        # Stress distribution
        x_stress = np.linspace(-stress_max, stress_max, 100)
        y_stress = np.linspace(-height/2, height/2, 100)
        X, Y = np.meshgrid(x_stress, y_stress)
        
        # Plot stress contours
        levels = np.linspace(-stress_max, stress_max, 20)
        ax.contourf(X, Y, Y * stress_max/(height/2), levels=levels, cmap='RdYlBu_r')
        
        return ax
    
    # Create stress distribution for rafter
    create_stress_distribution(ax2, 0.2, 0.1, 9.18)  # 200mm x 100mm, max stress 9.18 N/mm²
    ax2.set_title('Stress Distribution (Rafter Cross-section)')
    ax2.set_xlabel('Width (m)')
    ax2.set_ylabel('Height (m)')
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.tight_layout(pad=1.5)
    plt.savefig('output/figures/stress_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_connection_detail_diagram():
    """Create detailed connection technical drawing with force transfer"""
    set_engineering_style()
    fig = plt.figure(figsize=(15, 15))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Main connection detail
    ax1 = fig.add_subplot(gs[0, :])
    
    # Rafter outline with material fill
    rafter = Rectangle((0, 0), 0.1, 0.2, fill=True, color='burlywood', alpha=0.3)
    ax1.add_patch(rafter)
    
    # Purlin outline with material fill
    purlin = Rectangle((0.1, 0.15), 0.16, 0.08, fill=True, color='burlywood', alpha=0.3)
    ax1.add_patch(purlin)
    
    # Steel plate
    plate = Rectangle((0.08, 0.12), 0.04, 0.1, fill=True, color='gray', alpha=0.3)
    ax1.add_patch(plate)
    
    # Bolt holes with specifications
    bolt_specs = "M12 Grade 8.8\nfyb = 640 MPa\nfub = 800 MPa"
    bolt1 = Circle((0.1, 0.19), 0.006, fill=True, color='black')
    bolt2 = Circle((0.1, 0.15), 0.006, fill=True, color='black')
    ax1.add_patch(bolt1)
    ax1.add_patch(bolt2)
    ax1.text(0.12, 0.17, bolt_specs, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))
    
    # Enhanced dimensions with proper engineering notation
    ax1.annotate('', xy=(0, -0.02), xytext=(0.1, -0.02),
                arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax1.text(0.05, -0.04, '100mm', ha='center', fontsize=10)
    
    ax1.annotate('', xy=(-0.02, 0), xytext=(-0.02, 0.2),
                arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax1.text(-0.04, 0.1, '200mm', va='center', rotation=90, fontsize=10)
    
    # Add force arrows
    arrow_style = dict(arrowstyle='->', color='red', linewidth=1.5)
    ax1.annotate('', xy=(0.1, 0.25), xytext=(0.1, 0.35),
                arrowprops=arrow_style)
    ax1.text(0.12, 0.3, 'F = 2.34 kN', fontsize=10)
    
    ax1.set_xlim(-0.1, 0.3)
    ax1.set_ylim(-0.1, 0.4)
    ax1.set_aspect('equal')
    ax1.set_title('Rafter-Purlin Connection Detail\nwith Force Transfer', pad=20)
    ax1.axis('off')
    
    # Bolt shear diagram
    ax2 = fig.add_subplot(gs[1, 0])
    bolt_circle = Circle((0, 0), 0.006, fill=True, color='black')
    ax2.add_patch(bolt_circle)
    
    # Add shear force arrows
    arrow_length = 0.05
    angles = [0, 90, 180, 270]
    for angle in angles:
        dx = arrow_length * np.cos(np.radians(angle))
        dy = arrow_length * np.sin(np.radians(angle))
        ax2.arrow(0, 0, dx, dy, head_width=0.01, head_length=0.01,
                 fc='red', ec='red', alpha=0.5)
    
    ax2.set_xlim(-0.1, 0.1)
    ax2.set_ylim(-0.1, 0.1)
    ax2.set_aspect('equal')
    ax2.set_title('Bolt Shear Force Distribution', pad=20)
    ax2.axis('off')
    
    # Connection specifications table
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.axis('off')
    
    specs_table = [
        ['Component', 'Specification'],
        ['Bolt Type', 'M12 Grade 8.8'],
        ['Bolt Spacing', '40mm'],
        ['Edge Distance', '20mm'],
        ['Plate Thickness', '6mm'],
        ['Design Shear', '1.655 kN/bolt']
    ]
    
    table = ax3.table(cellText=specs_table,
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.5, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Style the table
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('lightgray')
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
    
    ax3.set_title('Connection Specifications', pad=20)
    
    plt.savefig('output/figures/connection_detail.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_thermal_bridge_analysis():
    """Create comprehensive thermal bridge analysis with temperature distribution and heat flow"""
    set_engineering_style()
    
    # Create figure with 2x2 grid for detailed analysis
    fig = plt.figure(figsize=(20, 15))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Temperature distribution subplot
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Enhanced temperature gradient visualization
    x = np.linspace(0, 1, 200)
    y = np.linspace(0, 1, 200)
    X, Y = np.meshgrid(x, y)
    
    # More realistic temperature distribution with material properties
    def temp_distribution(X, Y):
        T_int = 20    # Internal temperature (°C)
        T_ext = -20   # External temperature (°C)
        
        # Material thermal conductivities
        k_wall = 0.45   # MAX 220 block
        k_ins = 0.04    # Mineral wool
        k_timber = 0.13 # C27 timber
        
        # Create temperature field with material properties
        T = np.ones_like(X) * T_ext
        
        # Wall region
        wall_mask = (X < 0.2)
        T[wall_mask] = T_ext + (T_int - T_ext) * (1 - np.exp(-k_wall * Y[wall_mask]))
        
        # Insulation region
        ins_mask = (X >= 0.15) & (X < 0.25)
        T[ins_mask] = T_ext + (T_int - T_ext) * (1 - np.exp(-k_ins * Y[ins_mask]))
        
        # Roof region
        roof_mask = (Y > 0.6)
        T[roof_mask] = T_ext + (T_int - T_ext) * (1 - np.exp(-k_timber * (1-X[roof_mask])))
        
        return T
    
    T = temp_distribution(X, Y)
    
    # Plot enhanced temperature contours
    levels = np.linspace(T.min(), T.max(), 40)
    im1 = ax1.contourf(X, Y, T, levels=levels, cmap='RdBu_r')
    ax1.set_title('Temperature Distribution\nat Wall-Roof Junction')
    
    # Add colorbar with proper spacing
    cbar1 = fig.colorbar(im1, ax=ax1, label='Temperature (°C)')
    
    # Add detailed construction elements
    wall = Rectangle((0, 0), 0.2, 0.8, fill=False, color='black', linewidth=1.5)
    roof = Rectangle((0.2, 0.6), 0.6, 0.2, fill=False, color='black', linewidth=1.5)
    insulation = Rectangle((0.15, 0), 0.1, 0.8, fill=True, color='yellow', alpha=0.3)
    timber = Rectangle((0.2, 0.6), 0.6, 0.2, fill=True, color='burlywood', alpha=0.3)
    
    for element in [wall, roof, insulation, timber]:
        ax1.add_patch(element)
    
    # Heat flux visualization subplot
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Calculate heat flux vectors
    U = -np.gradient(T, axis=1)
    V = -np.gradient(T, axis=0)
    magnitude = np.sqrt(U**2 + V**2)
    
    # Plot heat flux vectors with magnitude-based color
    quiver = ax2.quiver(X[::8, ::8], Y[::8, ::8], U[::8, ::8], V[::8, ::8],
                       magnitude[::8, ::8], cmap='hot', scale=50, width=0.003)
    ax2.set_title('Heat Flux Vectors\nand Flow Paths')
    
    # Add colorbar for heat flux magnitude
    cbar2 = fig.colorbar(quiver, ax=ax2, label='Heat Flux Magnitude (W/m²)')
    
    # Add construction elements to heat flux plot
    for element in [wall, roof, insulation, timber]:
        new_element = Rectangle(element.get_xy(), element.get_width(), element.get_height(),
                              fill=element.get_fill(), color=element.get_facecolor(),
                              alpha=element.get_alpha())
        ax2.add_patch(new_element)
    
    # Condensation risk analysis subplot
    ax3 = fig.add_subplot(gs[1, 0])
    
    # Calculate dewpoint temperature
    RH_int = 50  # Internal relative humidity (%)
    def dewpoint(T, RH):
        return T - ((100 - RH)/5)  # Simplified Magnus formula
    
    T_dp = dewpoint(T, RH_int)
    
    # Plot condensation risk
    risk = T <= T_dp
    extent = (0.0, 1.0, 0.0, 1.0)  # Define proper extent tuple
    im3 = ax3.imshow(risk, cmap='RdYlBu_r', extent=extent)
    ax3.set_title('Condensation Risk Analysis\n(Red indicates risk)')
    
    # Add construction elements to condensation plot
    for element in [wall, roof, insulation, timber]:
        new_element = Rectangle(element.get_xy(), element.get_width(), element.get_height(),
                              fill=element.get_fill(), color=element.get_facecolor(),
                              alpha=element.get_alpha())
        ax3.add_patch(new_element)
    
    # Thermal bridge effect subplot
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calculate and plot thermal bridge effect (Ψ-value)
    y_bridge = np.linspace(0, 0.8, 100)
    psi_value = 0.15  # Example Ψ-value (W/m·K)
    heat_loss = psi_value * y_bridge
    
    ax4.plot(y_bridge, heat_loss, 'r-', linewidth=2, label=f'Ψ = {psi_value} W/m·K')
    ax4.fill_between(y_bridge, heat_loss, alpha=0.2, color='red')
    ax4.set_xlabel('Junction Height (m)')
    ax4.set_ylabel('Additional Heat Loss (W/m)')
    ax4.set_title('Thermal Bridge Effect\n(Linear Thermal Transmittance)')
    ax4.grid(True)
    ax4.legend()
    
    # Add annotations explaining thermal bridge calculations
    fig.text(0.02, 0.02,
             'Thermal Bridge Calculations:\n' +
             'Ψ = L²D - ΣUi·li  [W/(m·K)]\n' +
             'where:\n' +
             'L²D = thermal coupling coefficient\n' +
             'Ui = U-value of adjacent elements\n' +
             'li = length of thermal bridge',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    # Use figure-level padding instead of tight_layout
    fig.savefig('output/figures/thermal_bridge_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_combined_load_analysis():
    """Create combined load analysis diagram"""
    set_engineering_style()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # Load combination diagram
    loads = ['Dead Load', 'Snow Load', 'Wind Load']
    values = [0.297, 0.56, 0.483]  # kN/m²
    colors = ['gray', 'lightblue', 'lightcoral']
    
    ax1.bar(loads, values, color=colors)
    ax1.set_ylabel('Load (kN/m²)')
    ax1.set_title('Individual Load Components')
    
    # Add value labels
    for i, v in enumerate(values):
        ax1.text(i, v + 0.05, f'{v} kN/m²', ha='center')
    
    # Combined load effects
    x = np.linspace(0, 7.2, 100)
    
    # Different load combinations
    combo1 = 1.35 * 0.297 + 1.5 * 0.56  # ULS1: 1.35G + 1.5S
    combo2 = 1.35 * 0.297 + 1.5 * 0.483  # ULS2: 1.35G + 1.5W
    combo3 = 1.35 * 0.297 + 1.05 * 0.56 + 0.9 * 0.483  # ULS3: 1.35G + 1.05S + 0.9W
    
    ax2.plot(x, np.ones_like(x) * combo1, 'b-', label='ULS1: 1.35G + 1.5S')
    ax2.plot(x, np.ones_like(x) * combo2, 'r-', label='ULS2: 1.35G + 1.5W')
    ax2.plot(x, np.ones_like(x) * combo3, 'g-', label='ULS3: 1.35G + 1.05S + 0.9W')
    
    ax2.set_xlabel('Position along Building Width (m)')
    ax2.set_ylabel('Combined Design Load (kN/m²)')
    ax2.set_title('Load Combinations (ULS)')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout(pad=1.5)
    plt.savefig('output/figures/combined_load_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_cross_section_analysis():
    """Create detailed cross-section analysis diagram with material properties"""
    set_engineering_style()
    fig = plt.figure(figsize=(20, 10))
    
    # Create a 2x2 grid for more detailed analysis
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])
    
    # Rafter cross-section with material properties
    rafter = Rectangle((-0.05, -0.1), 0.1, 0.2, fill=True, color='burlywood', alpha=0.3)
    ax1.add_patch(rafter)
    
    # Enhanced dimensions and labels for rafter
    ax1.annotate('', xy=(-0.06, -0.1), xytext=(-0.06, 0.1),
                 arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax1.text(-0.09, 0, '200mm', va='center', rotation=90, fontsize=10)
    
    ax1.annotate('', xy=(-0.05, -0.12), xytext=(0.05, -0.12),
                 arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax1.text(0, -0.14, '100mm', ha='center', fontsize=10)
    
    # Add material properties for rafter
    props_text = "C27 Timber\nfm,k = 27 MPa\nE0,mean = 11500 MPa\nρk = 370 kg/m³"
    ax1.text(0.07, 0.07, props_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))
    
    ax1.set_xlim(-0.15, 0.15)
    ax1.set_ylim(-0.15, 0.15)
    ax1.set_title('Rafter Cross-section\n(100×200mm)', pad=10)
    ax1.axis('off')
    ax1.set_aspect('equal')
    
    # Purlin cross-section with material properties
    purlin = Rectangle((-0.04, -0.08), 0.08, 0.16, fill=True, color='burlywood', alpha=0.3)
    ax2.add_patch(purlin)
    
    # Enhanced dimensions and labels for purlin
    ax2.annotate('', xy=(-0.05, -0.08), xytext=(-0.05, 0.08),
                 arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax2.text(-0.08, 0, '160mm', va='center', rotation=90, fontsize=10)
    
    ax2.annotate('', xy=(-0.04, -0.1), xytext=(0.04, -0.1),
                 arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax2.text(0, -0.12, '80mm', ha='center', fontsize=10)
    
    # Add material properties for purlin
    props_text = "C27 Timber\nfm,k = 27 MPa\nE0,mean = 11500 MPa\nρk = 370 kg/m³"
    ax2.text(0.06, 0.05, props_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))
    
    ax2.set_xlim(-0.15, 0.15)
    ax2.set_ylim(-0.15, 0.15)
    ax2.set_title('Purlin Cross-section\n(80×160mm)', pad=10)
    ax2.axis('off')
    ax2.set_aspect('equal')
    
    # Add section properties analysis
    ax3.axis('off')
    props_table = [
        ['Property', 'Rafter', 'Purlin'],
        ['Area (mm²)', '20,000', '12,800'],
        ['Moment of Inertia (mm⁴)', '66.67×10⁶', '27.31×10⁶'],
        ['Section Modulus (mm³)', '666,667', '341,333'],
        ['Radius of Gyration (mm)', '57.74', '46.19']
    ]
    
    table = ax3.table(cellText=props_table,
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.3, 0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Style the table
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('lightgray')
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
    
    ax3.set_title('Section Properties Analysis', pad=20)
    
    plt.tight_layout(pad=1.5)
    plt.savefig('output/figures/cross_sections.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_momentum_analysis():
    """Create comprehensive momentum and bending analysis visualization"""
    set_engineering_style()
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # Bending moment diagram
    ax1 = fig.add_subplot(gs[0, :])
    x = np.linspace(0, 7.2, 100)
    moment = -(1.401 * 1.1 * x * (7.2 - x)) / 8  # MEd calculation
    
    ax1.plot(x, moment, 'b-', linewidth=2)
    ax1.fill_between(x, moment, alpha=0.2)
    ax1.set_title('Bending Moment Diagram (MEd)')
    ax1.set_xlabel('Length (m)')
    ax1.set_ylabel('Moment (kNm)')
    ax1.grid(True)
    
    # Add maximum moment annotation
    max_moment_idx = np.argmin(moment)
    ax1.annotate(f'MEd,max = {abs(moment[max_moment_idx]):.2f} kNm',
                xy=(x[max_moment_idx], moment[max_moment_idx]),
                xytext=(x[max_moment_idx], moment[max_moment_idx]-2),
                ha='center', va='top',
                bbox=dict(facecolor='white', alpha=0.8))
    
    # Shear force diagram
    ax2 = fig.add_subplot(gs[1, 0])
    shear = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi < 7.2/2:
            shear[i] = 1.401 * 1.1 * xi
        else:
            shear[i] = 1.401 * 1.1 * (7.2 - xi)
    
    ax2.plot(x, shear, 'r-', linewidth=2)
    ax2.fill_between(x, shear, alpha=0.2)
    ax2.set_title('Shear Force Diagram')
    ax2.set_xlabel('Length (m)')
    ax2.set_ylabel('Shear Force (kN)')
    ax2.grid(True)
    
    # Normal force diagram
    ax3 = fig.add_subplot(gs[1, 1])
    angle_rad = np.radians(16)
    normal_force = -1.401 * 1.1 * x * np.cos(angle_rad)
    
    ax3.plot(x, normal_force, 'g-', linewidth=2)
    ax3.fill_between(x, normal_force, alpha=0.2)
    ax3.set_title('Normal Force Diagram')
    ax3.set_xlabel('Length (m)')
    ax3.set_ylabel('Normal Force (kN)')
    ax3.grid(True)
    
    # Add equations and annotations
    fig.text(0.02, 0.02,
             'Momentum Analysis Equations:\n' +
             'MEd = (qEd × L²) / 8\n' +
             'VEd = (qEd × L) / 2\n' +
             'NEd = qEd × L × cos(α)',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.savefig('output/figures/momentum_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_inertia_analysis():
    """Create comprehensive moment of inertia analysis visualization"""
    set_engineering_style()
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # Moment of inertia distribution for rafter
    ax1 = fig.add_subplot(gs[0, 0])
    height = 0.2  # 200mm
    width = 0.1   # 100mm
    y = np.linspace(-height/2, height/2, 100)
    I_rafter = (width * height**3) / 12  # m⁴
    dA = width * (height/100)
    I_local = width * y**2 * dA  # Local contribution to moment of inertia
    
    ax1.plot(I_local * 1e6, y * 1000, 'b-', linewidth=2)
    ax1.fill_betweenx(y * 1000, 0, I_local * 1e6, alpha=0.2)
    ax1.set_title('Rafter Section\nMoment of Inertia Distribution')
    ax1.set_xlabel('Local I Contribution (mm⁴)')
    ax1.set_ylabel('Distance from Neutral Axis (mm)')
    ax1.grid(True)
    ax1.text(0.5, 0.95, f'I = {I_rafter*1e6:.2e} mm⁴',
             transform=ax1.transAxes, ha='center', va='top',
             bbox=dict(facecolor='white', alpha=0.8))
    
    # Moment of inertia distribution for purlin
    ax2 = fig.add_subplot(gs[0, 1])
    height_p = 0.16  # 160mm
    width_p = 0.08   # 80mm
    y_p = np.linspace(-height_p/2, height_p/2, 100)
    I_purlin = (width_p * height_p**3) / 12  # m⁴
    dA_p = width_p * (height_p/100)
    I_local_p = width_p * y_p**2 * dA_p  # Local contribution to moment of inertia
    
    ax2.plot(I_local_p * 1e6, y_p * 1000, 'r-', linewidth=2)
    ax2.fill_betweenx(y_p * 1000, 0, I_local_p * 1e6, alpha=0.2)
    ax2.set_title('Purlin Section\nMoment of Inertia Distribution')
    ax2.set_xlabel('Local I Contribution (mm⁴)')
    ax2.set_ylabel('Distance from Neutral Axis (mm)')
    ax2.grid(True)
    ax2.text(0.5, 0.95, f'I = {I_purlin*1e6:.2e} mm⁴',
             transform=ax2.transAxes, ha='center', va='top',
             bbox=dict(facecolor='white', alpha=0.8))
    
    # Section comparison
    ax3 = fig.add_subplot(gs[1, :])
    sections = ['Rafter\n100×200mm', 'Purlin\n80×160mm']
    I_values = [I_rafter * 1e6, I_purlin * 1e6]
    
    bars = ax3.bar(sections, I_values)
    ax3.set_title('Section Moment of Inertia Comparison')
    ax3.set_ylabel('Moment of Inertia (mm⁴)')
    ax3.grid(True, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2e}',
                ha='center', va='bottom')
    
    # Add equations and annotations
    fig.text(0.02, 0.02,
             'Moment of Inertia Equations:\n' +
             'I = ∫y² dA\n' +
             'For rectangular section:\n' +
             'I = (b × h³)/12\n' +
             'where b = width, h = height',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.savefig('output/figures/inertia_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_uls_verification():
    """Create comprehensive ULS verification visualization"""
    set_engineering_style()
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # Combined stress ratio visualization
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Example stress ratios
    bending_ratio = 0.76  # σm,d/fm,d
    compression_ratio = 0.34  # σc,d/fc,0,d
    combined_ratio = bending_ratio + compression_ratio
    
    # Create stacked bar for combined ratio
    labels = ['Design\nRequirement', 'Combined\nStress Ratio']
    ax1.bar(labels[1], compression_ratio, label='Compression', color='lightblue')
    ax1.bar(labels[1], bending_ratio, bottom=compression_ratio, label='Bending', color='lightcoral')
    ax1.bar(labels[0], 1.0, color='gray', alpha=0.3, label='Limit')
    
    ax1.set_ylim(0, 1.2)
    ax1.set_title('Combined Stress Ratio Check')
    ax1.set_ylabel('Utilization Ratio')
    ax1.axhline(y=1.0, color='r', linestyle='--', alpha=0.5)
    ax1.legend()
    ax1.grid(True)
    
    # Add ratio values
    ax1.text(1, combined_ratio + 0.05, f'Total: {combined_ratio:.2f}',
             ha='center', va='bottom')
    
    # Stability verification
    ax2 = fig.add_subplot(gs[0, 1])
    
    # Example stability parameters
    kcrit = 1.0  # Lateral torsional buckling factor
    stability_ratio = 0.82  # Combined stability ratio
    
    # Create stability check visualization
    stability_labels = ['Lateral Torsional\nBuckling', 'Combined\nStability', 'Limit']
    stability_values = [kcrit, stability_ratio, 1.0]
    colors = ['lightblue', 'lightcoral', 'gray']
    
    x = range(len(stability_labels))
    ax2.bar(x, stability_values, color=colors)
    ax2.set_xticks(x)
    ax2.set_xticklabels(stability_labels)
    ax2.set_ylim(0, 1.2)
    ax2.set_title('Stability Verification')
    ax2.set_ylabel('Factor / Ratio')
    ax2.axhline(y=1.0, color='r', linestyle='--', alpha=0.5)
    ax2.grid(True)
    
    # Load factors visualization
    ax3 = fig.add_subplot(gs[1, :])
    
    # Example load combinations
    combination_labels = [
        'ULS 1\n1.35G + 1.5S',
        'ULS 2\n1.35G + 1.5W',
        'ULS 3\n1.35G + 1.05S + 0.9W'
    ]
    combination_values = [1.343, 1.287, 1.312]
    colors = ['lightblue', 'lightcoral', 'lightgreen']
    
    bars = ax3.bar(combination_labels, combination_values, color=colors)
    ax3.set_title('Design Load Combinations')
    ax3.set_ylabel('Combined Design Load (kN/m²)')
    ax3.grid(True)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    
    # Add verification equations
    fig.text(0.02, 0.02,
             'ULS Verification Equations (EN 1995-1-1):\n' +
             'Combined Stress: σm,d/fm,d + σc,d/fc,0,d ≤ 1.0\n' +
             'Stability: σm,d/(kcrit×fm,d) + σc,d/fc,0,d ≤ 1.0\n' +
             'Load Combinations (EN 1990):\n' +
             'ULS 1: 1.35G + 1.5S\n' +
             'ULS 2: 1.35G + 1.5W\n' +
             'ULS 3: 1.35G + 1.05S + 0.9W',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.savefig('output/figures/uls_verification.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_strength_analysis():
    """Create comprehensive strength calculation visualization"""
    set_engineering_style()
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # Material strength properties
    ax1 = fig.add_subplot(gs[0, 0])
    strength_types = ['fm,k', 'ft,0,k', 'fc,0,k']
    strength_values = [27, 16, 22]  # MPa
    
    bars = ax1.bar(strength_types, strength_values, color='lightblue')
    ax1.set_title('C27 Timber Characteristic Strengths')
    ax1.set_ylabel('Strength (MPa)')
    ax1.grid(True)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f} MPa',
                ha='center', va='bottom')
    
    # Design strength calculation
    ax2 = fig.add_subplot(gs[0, 1])
    kmod = 0.8
    gamma_M = 1.3
    design_strengths = [val * kmod / gamma_M for val in strength_values]
    
    bars = ax2.bar(strength_types, design_strengths, color='lightcoral')
    ax2.set_title('Design Strengths\n(kmod = 0.8, γM = 1.3)')
    ax2.set_ylabel('Design Strength (MPa)')
    ax2.grid(True)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} MPa',
                ha='center', va='bottom')
    
    # Strength modification factors
    ax3 = fig.add_subplot(gs[1, :])
    factors = ['kmod\n(Load duration)', 'kh\n(Size effect)', 'kcrit\n(Stability)',
              'kdef\n(Creep)', 'γM\n(Material)']
    factor_values = [0.8, 1.0, 1.0, 0.6, 1.3]
    colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightgray']
    
    bars = ax3.bar(factors, factor_values, color=colors)
    ax3.set_title('Strength Modification Factors')
    ax3.set_ylabel('Factor Value')
    ax3.grid(True)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')
    
    # Add equations and annotations
    fig.text(0.02, 0.02,
             'Design Strength Equations (EN 1995-1-1):\n' +
             'fd = kmod × fk / γM\n' +
             'where:\n' +
             'fd = design strength\n' +
             'fk = characteristic strength\n' +
             'kmod = modification factor for duration of load\n' +
             'γM = partial factor for material properties',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.savefig('output/figures/strength_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_layer_analysis():
    """Create comprehensive layer calculation visualization"""
    set_engineering_style()
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # Layer composition visualization
    ax1 = fig.add_subplot(gs[0, :])
    layers = [
        ('Steel Tile', 0.6, 50.0, 7850),
        ('Air Gap', 20, 0.024, 1.2),
        ('Mineral Wool', 150, 0.04, 20),
        ('MAX 220 Block', 220, 0.45, 1200)
    ]
    
    y_pos = 0
    colors = ['gray', 'lightblue', 'lightyellow', 'lightcoral']
    for i, (name, thickness, lambda_val, density) in enumerate(layers):
        rect = patches.Rectangle((0.2, y_pos), 0.6, thickness,
                                    facecolor=colors[i], edgecolor='black',
                                    alpha=0.7)
        ax1.add_patch(rect)
        # Add layer labels
        ax1.text(0.1, y_pos + thickness/2,
                f'{thickness}mm',
                va='center', ha='right')
        ax1.text(0.85, y_pos + thickness/2,
                f'{name}\nλ = {lambda_val} W/(m·K)\nρ = {density} kg/m³',
                va='center', ha='left')
        y_pos += thickness
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-10, y_pos + 10)
    ax1.set_title('Layer Composition Analysis')
    ax1.axis('off')
    
    # Thermal resistance calculation
    ax2 = fig.add_subplot(gs[1, 0])
    R_values = [
        ('Rsi', 0.13),
        ('Steel Tile', 0.6/50.0),
        ('Air Gap', 20/0.024),
        ('Mineral Wool', 150/0.04),
        ('MAX 220 Block', 220/0.45),
        ('Rse', 0.04)
    ]
    
    names = [r[0] for r in R_values]
    values = [r[1] for r in R_values]
    
    bars = ax2.bar(names, values, color='lightblue')
    ax2.set_title('Layer Thermal Resistances')
    ax2.set_ylabel('Thermal Resistance (m²K/W)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    
    # U-value calculation
    ax3 = fig.add_subplot(gs[1, 1])
    R_total = sum(values)
    U_value = 1/R_total
    
    # Create pie chart showing contribution to total resistance
    sizes = [v/R_total * 100 for v in values]
    plt.pie(sizes, labels=names, autopct='%1.1f%%',
            colors=['lightblue', 'gray', 'lightgreen', 'lightyellow',
                   'lightcoral', 'lightblue'])
    ax3.set_title(f'Thermal Resistance Distribution\nTotal R = {R_total:.3f} m²K/W\nU = {U_value:.3f} W/(m²K)')
    
    # Add equations and annotations
    fig.text(0.02, 0.02,
             'Thermal Resistance Calculations (EN ISO 6946):\n' +
             'R = d/λ  [m²K/W]\n' +
             'where:\n' +
             'd = layer thickness [m]\n' +
             'λ = thermal conductivity [W/(m·K)]\n' +
             'RT = Rsi + ΣR + Rse\n' +
             'U = 1/RT  [W/(m²K)]',
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.savefig('output/figures/layer_analysis.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_purlin_spacing_diagram():
    """Create detailed purlin spacing and load distribution diagram"""
    set_engineering_style()
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3)
    
    # Top view with purlin spacing
    ax1 = fig.add_subplot(gs[0])
    
    # Building outline
    rect = Rectangle((0, 0), 6.6, 7.2, fill=False, color='black', linewidth=2)
    ax1.add_patch(rect)
    
    # Add purlins
    spacing = 1.1  # meters
    num_purlins = int(7.2 / spacing) + 1
    for i in range(num_purlins):
        y = i * spacing
        if y <= 7.2:
            purlin = Rectangle((0, y), 6.6, 0.08, fill=True, color='burlywood', alpha=0.3)
            ax1.add_patch(purlin)
            # Add spacing dimension for first gap
            if i == 1:
                ax1.annotate('', xy=(-0.2, 0), xytext=(-0.2, spacing),
                            arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
                ax1.text(-0.4, spacing/2, '1100mm', rotation=90, ha='right', va='center')
    
    # Add dimensions
    ax1.annotate('', xy=(0, -0.2), xytext=(6.6, -0.2),
                arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax1.text(3.3, -0.4, '6600mm', ha='center')
    
    ax1.annotate('', xy=(-0.2, 0), xytext=(-0.2, 7.2),
                arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    ax1.text(-0.4, 3.6, '7200mm', rotation=90, ha='right', va='center')
    
    ax1.set_xlim(-1, 8)
    ax1.set_ylim(-1, 8)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Purlin Spacing Layout (Top View)', pad=20)
    
    # Load distribution diagram
    ax2 = fig.add_subplot(gs[1])
    
    # Create distributed load visualization
    x = np.linspace(0, 6.6, 100)
    y = np.zeros_like(x)
    ax2.plot(x, y, 'k-', linewidth=2)
    
    # Add distributed load arrows
    arrow_spacing = 0.3
    for xi in np.arange(0, 6.6, arrow_spacing):
        ax2.arrow(float(xi), 1.0, 0.0, -0.8, head_width=0.1, head_length=0.1,
                 fc='blue', ec='blue', alpha=0.5)
    
    # Add load values
    ax2.text(3.3, 1.2, 'Distributed Load: 1.343 kN/m²', ha='center')
    
    ax2.set_xlim(-0.5, 7.1)
    ax2.set_ylim(-0.5, 1.5)
    ax2.axis('off')
    ax2.set_title('Load Distribution on Purlins', pad=20)
    
    plt.savefig('output/figures/purlin_spacing.png',
                bbox_inches='tight',
                dpi=300,
                pad_inches=0.5,
                facecolor='white',
                edgecolor='none')
    plt.close()

if __name__ == "__main__":
    # Create output directory
    import os
    os.makedirs('output/figures', exist_ok=True)
    
    # Generate all diagrams
    create_load_distribution_diagram()
    create_thermal_resistance_diagram()
    create_stress_analysis_diagram()
    create_connection_detail_diagram()
    create_cross_section_analysis()
    create_thermal_bridge_analysis()
    create_combined_load_analysis()
    create_purlin_spacing_diagram()
    
    print("All technical diagrams generated successfully")
