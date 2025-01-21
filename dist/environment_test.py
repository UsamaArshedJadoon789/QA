import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import shapely.geometry as sg

# Test drawing capabilities with dataset 5 specifications
def test_drawing_capabilities():
    # Create a matplotlib figure at 1:50 scale
    # 1 meter = 20 pixels at 1:50 scale
    scale_factor = 20
    
    # Building dimensions from dataset 5
    width = 7.2 * scale_factor  # 7.2m
    length1 = 6.6 * scale_factor  # 6.6m
    length2 = 10.8 * scale_factor  # 10.8m
    height1 = 2.5 * scale_factor  # 2.5m
    height2 = 2.65 * scale_factor  # 2.65m
    angle = 16  # degrees
    
    # Create test figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    
    # Horizontal projection (top view)
    ax1.add_patch(Rectangle((0, 0), width, length1, fill=False))
    ax1.set_title('Horizontal Projection (1:50)')
    ax1.set_aspect('equal')
    
    # Vertical projection (side view)
    wall_points = [(0, 0), (0, height1), (width, height2), (width, 0)]
    ax2.add_patch(Polygon(wall_points, fill=False))
    ax2.set_title('Vertical Projection (1:50)')
    ax2.set_aspect('equal')
    
    plt.savefig('test_drawing.pdf')
    plt.close()

    return True

# Test geometric calculations
def test_calculations():
    # Basic structural calculations test
    angle_rad = np.radians(16)
    span = 7.2  # meters
    
    # Test moment calculation
    distributed_load = 1.0  # kN/m
    max_moment = (distributed_load * span**2) / 8  # kNm
    
    # Test thermal resistance calculation
    mineral_wool_thickness = 0.15  # m
    mineral_wool_lambda = 0.04  # W/(m·K)
    R_insulation = mineral_wool_thickness / mineral_wool_lambda
    
    return True

if __name__ == "__main__":
    drawing_test = test_drawing_capabilities()
    calc_test = test_calculations()
    print("Environment Test Results:")
    print(f"Drawing capabilities: {'OK' if drawing_test else 'FAILED'}")
    print(f"Calculation capabilities: {'OK' if calc_test else 'FAILED'}")
