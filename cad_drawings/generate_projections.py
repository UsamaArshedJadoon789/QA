import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import math
import os
import traceback
from ezdxf.math import BoundingBox, Vec3

def set_viewport_bounds(msp, points, margin=500):
    """Set viewport bounds based on geometry with margin"""
    try:
        if not points:
            raise ValueError("No points provided")
            
        # Extract x and y coordinates
        xs = []
        ys = []
        for point in points:
            if isinstance(point, (list, tuple)) and len(point) >= 2:
                try:
                    xs.append(float(point[0]))
                    ys.append(float(point[1]))
                except (ValueError, TypeError):
                    print(f"Warning: Invalid point coordinates: {point}")
                    continue
            else:
                print(f"Warning: Invalid point format: {point}")
                continue
                
        if not xs or not ys:
            raise ValueError("No valid points for bounds calculation")
            
        # Calculate bounds
        min_x = min(xs) - margin
        max_x = max(xs) + margin
        min_y = min(ys) - margin
        max_y = max(ys) + margin
        
        print(f"Debug: Setting viewport bounds to ({min_x}, {min_y}) -> ({max_x}, {max_y})")
        
        # Set modelspace extents and limits
        msp.doc.header['$EXTMIN'] = (min_x, min_y, 0)
        msp.doc.header['$EXTMAX'] = (max_x, max_y, 0)
        msp.doc.header['$LIMMIN'] = (min_x, min_y)
        msp.doc.header['$LIMMAX'] = (max_x, max_y)
        
        # Return bounds as a simple tuple
        return ((min_x, min_y), (max_x, max_y))
        
    except Exception as e:
        print(f"Error setting viewport bounds: {str(e)}")
        raise

def create_dimension_style(doc, name='50', scale=50.0):
    """Create a standardized dimension style"""
    dimstyle = doc.dimstyles.new(name)
    dimstyle.dxf.dimscale = scale
    dimstyle.dxf.dimlfac = scale
    dimstyle.dxf.dimrnd = 1
    dimstyle.dxf.dimpost = '<>'  # Standard dimension text format
    dimstyle.dxf.dimtxt = 100    # Text size
    dimstyle.dxf.dimasz = 100    # Arrow size
    dimstyle.dxf.dimclrd = 256   # Dimension line color (black)
    dimstyle.dxf.dimclre = 256   # Extension line color (black)
    dimstyle.dxf.dimgap = 25     # Gap from dimension line to text
    dimstyle.dxf.dimexe = 50     # Extension line extension
    dimstyle.dxf.dimexo = 25     # Extension line offset
    dimstyle.dxf.dimtad = 1      # Text above dimension line
    dimstyle.dxf.dimzin = 8      # Suppress trailing zeros
    dimstyle.dxf.dimblk = ''     # Use default arrow
    dimstyle.dxf.dimblk1 = ''    # First arrow
    dimstyle.dxf.dimblk2 = ''    # Second arrow
    dimstyle.dxf.dimtofl = 1     # Force dimension line between extensions
    dimstyle.dxf.dimtix = 0      # Force text inside extensions
    dimstyle.dxf.dimatfit = 3    # Force text and arrows outside
    dimstyle.dxf.dimtmove = 0    # Keep text position
    return dimstyle

def create_horizontal_projection(width, length1, spacing):
    """Create horizontal projection DXF"""
    doc = ezdxf.new('R2010')
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Create or modify text style
    try:
        style = doc.styles.new('CustomStyle', dxfattribs={
            'font': 'arial.ttf',
            'width': 1.0,
            'height': 100.0
        })
    except:
        style = doc.styles.get('Standard')
        style.dxf.font = 'arial.ttf'
        style.dxf.width = 1.0
        style.dxf.height = 100.0
    
    # Create dimension style
    create_dimension_style(doc)
    
    # Main outline
    points = [(0, 0), (length1, 0), (length1, width), (0, width), (0, 0)]
    outline = msp.add_lwpolyline(points)
    outline.dxf.lineweight = 35
    outline.dxf.color = 256
    
    # Set viewport bounds
    bounds = set_viewport_bounds(msp, points)
    min_bound, max_bound = bounds
    print(f"Horizontal projection bounds: {min_bound} to {max_bound}")
    
    # Add dimensions
    msp.add_linear_dim(
        base=(0, -300),
        p1=(0, 0),
        p2=(length1, 0),
        dimstyle='50',
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    msp.add_linear_dim(
        base=(-300, 0),
        p1=(0, 0),
        p2=(0, width),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    # Add grid lines
    grid_spacing = 1000
    for x in range(0, int(length1) + grid_spacing, grid_spacing):
        grid = msp.add_line((x, 0), (x, width))
        grid.dxf.color = 8
        grid.dxf.lineweight = 13
    for y in range(0, int(width) + grid_spacing, grid_spacing):
        grid = msp.add_line((0, y), (length1, y))
        grid.dxf.color = 8
        grid.dxf.lineweight = 13
    
    # Add rafters
    rafter_count = int(length1 / spacing) + 1
    for i in range(rafter_count):
        pos = i * spacing
        if pos <= length1:
            points = [(pos, 0), (pos+200, 0), (pos+200, width), (pos, width), (pos, 0)]
            msp.add_lwpolyline(points)
    
    return doc

def create_floor_plan(width=7200, length1=6600):
    """Create floor plan DXF at 1:50 scale"""
    doc = ezdxf.new('R2010')
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Create dimension style
    create_dimension_style(doc)
    
    # Create or modify text style
    try:
        style = doc.styles.new('CustomStyle', dxfattribs={
            'font': 'arial.ttf',
            'width': 1.0,
            'height': 100.0
        })
    except:
        style = doc.styles.get('Standard')
        style.dxf.font = 'arial.ttf'
        style.dxf.width = 1.0
        style.dxf.height = 100.0
    
    # Main outline
    points = [(0, 0), (length1, 0), (length1, width), (0, width), (0, 0)]
    outline = msp.add_lwpolyline(points)
    outline.dxf.lineweight = 35
    outline.dxf.color = 256
    
    # Add grid lines
    grid_spacing = 1000  # 1m grid
    for x in range(0, int(length1) + grid_spacing, grid_spacing):
        grid = msp.add_line((x, 0), (x, width))
        grid.dxf.color = 8
        grid.dxf.lineweight = 13
    for y in range(0, int(width) + grid_spacing, grid_spacing):
        grid = msp.add_line((0, y), (length1, y))
        grid.dxf.color = 8
        grid.dxf.lineweight = 13
    
    # Add dimensions
    msp.add_linear_dim(
        base=(0, -300),
        p1=(0, 0),
        p2=(length1, 0),
        dimstyle='50',
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    msp.add_linear_dim(
        base=(-300, 0),
        p1=(0, 0),
        p2=(0, width),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    # Add room divisions (based on typical layout)
    # Main area divisions at 1/3 and 2/3 points
    div1_x = length1 / 3
    div2_x = 2 * length1 / 3
    
    # Add vertical division lines
    div_line1 = msp.add_line((div1_x, 0), (div1_x, width))
    div_line1.dxf.color = 256
    div_line1.dxf.lineweight = 35
    
    div_line2 = msp.add_line((div2_x, 0), (div2_x, width))
    div_line2.dxf.color = 256
    div_line2.dxf.lineweight = 35
    
    # Add horizontal division line
    div_y = width / 2
    div_line_h = msp.add_line((0, div_y), (length1, div_y))
    div_line_h.dxf.color = 256
    div_line_h.dxf.lineweight = 35
    
    # Add room labels
    room_labels = [
        ('Room 1', div1_x/2, width*3/4),
        ('Room 2', (div1_x + div2_x)/2, width*3/4),
        ('Room 3', (div2_x + length1)/2, width*3/4),
        ('Room 4', div1_x/2, width/4),
        ('Room 5', (div1_x + div2_x)/2, width/4),
        ('Room 6', (div2_x + length1)/2, width/4)
    ]
    
    for label, x, y in room_labels:
        text = msp.add_text(
            label,
            dxfattribs={'height': 100, 'style': 'Standard'}
        )
        text.set_placement((x, y), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # Add annotations
    text = msp.add_text(
        'Floor Plan (Scale 1:50)',
        dxfattribs={'height': 150, 'style': 'Standard'}
    )
    text.set_placement((length1/2, -600), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # Add dimensions for room sizes
    room_width = width/2
    room_length = length1/3
    
    # Set viewport bounds
    set_viewport_bounds(msp, points)
    
    return doc

def create_vertical_projection(width, height1, height2, ground_level, angle):
    """Create vertical projection DXF"""
    doc = ezdxf.new('R2010')
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Create or modify text style
    try:
        style = doc.styles.new('CustomStyle', dxfattribs={
            'font': 'arial.ttf',
            'width': 1.0,
            'height': 100.0
        })
    except:
        style = doc.styles.get('Standard')
        style.dxf.font = 'arial.ttf'
        style.dxf.width = 1.0
        style.dxf.height = 100.0
    
    # Create dimension style
    create_dimension_style(doc)
    
    # Main outline
    points = [
        (0, ground_level),
        (0, height1),
        (width, height2),
        (width, ground_level),
        (0, ground_level)
    ]
    outline = msp.add_lwpolyline(points)
    outline.dxf.lineweight = 35
    outline.dxf.color = 256
    
    # Set viewport bounds
    bounds = set_viewport_bounds(msp, points)
    min_bound, max_bound = bounds
    print(f"Vertical projection bounds: {min_bound} to {max_bound}")
    
    # Add dimensions
    msp.add_linear_dim(
        base=(-300, ground_level),
        p1=(0, ground_level),
        p2=(0, height1),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    msp.add_linear_dim(
        base=(width+300, ground_level),
        p1=(width, ground_level),
        p2=(width, height2),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    # Add grid lines
    grid_spacing = 1000
    for x in range(0, int(width) + grid_spacing, grid_spacing):
        grid = msp.add_line((x, ground_level), (x, max(height1, height2)))
        grid.dxf.color = 8
        grid.dxf.lineweight = 13
    for y in range(int(ground_level), int(max(height1, height2)) + grid_spacing, grid_spacing):
        grid = msp.add_line((0, y), (width, y))
        grid.dxf.color = 8
        grid.dxf.lineweight = 13
    
    # Add annotations
    angle_text = f'Roof angle: {angle}°'
    text = msp.add_text(
        angle_text,
        dxfattribs={'height': 100, 'style': 'Standard'}
    )
    text.set_placement((width/2, height2+200), align=TextEntityAlignment.MIDDLE_CENTER)
    
    ground_text = 'Ground level: -1.4 m.a.s.l'
    text = msp.add_text(
        ground_text,
        dxfattribs={'height': 100, 'style': 'Standard'}
    )
    text.set_placement((0, ground_level-200), align=TextEntityAlignment.LEFT)
    
    return doc

def create_projections():
    """Create DXF files with vertical and horizontal projections at 1:50 scale"""
    try:
        print("\nGenerating projections...")
        
        # Create all required output directories
        os.makedirs('dist/drawings/projections', exist_ok=True)
        os.makedirs('dist/drawings/floor_plan', exist_ok=True)
        os.makedirs('output/figures', exist_ok=True)
        
        # Dataset 5 specifications (all dimensions in mm)
        width = 7200      # 7.2m
        length1 = 6600    # 6.6m
        length2 = 10800   # 10.8m
        height1 = 2500    # 2.5m
        height2 = 2650    # 2.65m
        angle = 16        # degrees
        spacing = 1100    # 1.1m
        ground_level = -1400  # -1.4m
        
        print("\nVerifying output directories...")
        for dir_path in ['dist/drawings/projections', 'dist/drawings/floor_plan', 'output/figures']:
            if not os.path.exists(dir_path):
                raise Exception(f"Failed to create directory: {dir_path}")
        
        # Print specifications
        print("\nCreating drawings with specifications:")
        print(f"Width: {width}mm ({width/1000}m)")
        print(f"Length 1: {length1}mm ({length1/1000}m)")
        print(f"Length 2: {length2}mm ({length2/1000}m)")
        print(f"Height 1: {height1}mm ({height1/1000}m)")
        print(f"Height 2: {height2}mm ({height2/1000}m)")
        print(f"Roof angle: {angle}°")
        print(f"Rafter spacing: {spacing}mm ({spacing/1000}m)")
        print(f"Ground level: {ground_level}mm ({ground_level/1000}m)")
        
        # Create and save floor plan
        print("\nCreating floor plan...")
        try:
            doc_f = create_floor_plan(width, length1)
            if doc_f:
                print("Saving floor plan...")
                f_path = 'dist/drawings/floor_plan/floor_plan.dxf'
                doc_f.saveas(f_path)
                if os.path.exists(f_path):
                    print("Floor plan saved successfully.")
                else:
                    raise Exception("Failed to save floor plan")
            else:
                raise Exception("Failed to create floor plan")
        except Exception as e:
            print(f"Error creating floor plan: {str(e)}")
            raise
        
        # Dataset 5 specifications (all dimensions in mm)
        width = 7200      # 7.2m
        length1 = 6600    # 6.6m
        length2 = 10800   # 10.8m
        height1 = 2500    # 2.5m
        height2 = 2650    # 2.65m
        angle = 16        # degrees
        spacing = 1100    # 1.1m
        ground_level = -1400  # -1.4m
        
        print("\nVerifying output directories...")
        for dir_path in ['dist/drawings/projections', 'output/figures']:
            if not os.path.exists(dir_path):
                raise Exception(f"Failed to create directory: {dir_path}")
        
        # Print specifications
        print("\nCreating drawings with specifications:")
        print(f"Width: {width}mm ({width/1000}m)")
        print(f"Length 1: {length1}mm ({length1/1000}m)")
        print(f"Length 2: {length2}mm ({length2/1000}m)")
        print(f"Height 1: {height1}mm ({height1/1000}m)")
        print(f"Height 2: {height2}mm ({height2/1000}m)")
        print(f"Roof angle: {angle}°")
        print(f"Rafter spacing: {spacing}mm ({spacing/1000}m)")
        print(f"Ground level: {ground_level}mm ({ground_level/1000}m)")
        
        # Create and save horizontal projection
        print("\nCreating horizontal projection...")
        try:
            doc_h = create_horizontal_projection(width, length1, spacing)
            if doc_h:
                print("Saving horizontal projection...")
                h_path = 'dist/drawings/projections/horizontal_projection.dxf'
                doc_h.saveas(h_path)
                if os.path.exists(h_path):
                    print("Horizontal projection saved successfully.")
                else:
                    raise Exception("Failed to save horizontal projection")
            else:
                raise Exception("Failed to create horizontal projection")
        except Exception as e:
            print(f"Error creating horizontal projection: {str(e)}")
            raise
        
        # Create and save vertical projection
        print("\nCreating vertical projection...")
        try:
            doc_v = create_vertical_projection(width, height1, height2, ground_level, angle)
            if doc_v:
                print("Saving vertical projection...")
                v_path = 'dist/drawings/projections/vertical_projection.dxf'
                doc_v.saveas(v_path)
                if os.path.exists(v_path):
                    print("Vertical projection saved successfully.")
                else:
                    raise Exception("Failed to save vertical projection")
            else:
                raise Exception("Failed to create vertical projection")
        except Exception as e:
            print(f"Error creating vertical projection: {str(e)}")
            raise
        
        # Verify files were created
        h_path = 'dist/drawings/projections/horizontal_projection.dxf'
        v_path = 'dist/drawings/projections/vertical_projection.dxf'
        if not os.path.exists(h_path) or not os.path.exists(v_path):
            raise Exception("Failed to create DXF files")
        
        print("\nAll projections generated successfully.")
        return True
        
    except Exception as e:
        print(f"\nError generating projections: {str(e)}")
        traceback.print_exc()
        return False
