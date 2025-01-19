#!/usr/bin/python3
import os
import sys
import math

# Set up FreeCAD environment
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['FREECAD_LIB'] = '/usr/lib/freecad/lib'
os.environ['PYTHONPATH'] = '/usr/lib/freecad-python3/lib'

# Add FreeCAD paths
freecad_paths = [
    '/usr/lib/freecad-python3/lib',
    '/usr/lib/freecad/lib',
    '/usr/share/freecad/Mod'
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

# Set environment for headless operation
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Initialize FreeCAD
try:
    import FreeCAD
    import Part
    print(f"FreeCAD Version: {FreeCAD.Version()}")
    print("Successfully imported FreeCAD modules")
except ImportError as e:
    print(f"Error importing FreeCAD: {e}")
    print("Python path:", sys.path)
    sys.exit(1)

print("Initializing in headless mode...")

# Configure FreeCAD for headless operation
if hasattr(FreeCAD, 'GuiUp') and FreeCAD.GuiUp:
    print("Warning: GUI mode detected, continuing anyway...")
    
# Create new document
doc = FreeCAD.newDocument('Dataset5_Building')

def init_environment():
    """Initialize the FreeCAD environment"""
    try:
        # Set up units and preferences
        FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part").SetFloat("MeshDeviation", 0.1)
        # Set up document units to millimeters
        FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").SetInt("UserSchema", 0)
        return True
    except Exception as e:
        print(f"Error initializing environment: {e}")
        return False

def create_walls():
    # Building dimensions from dataset 5
    width = 7200  # b=7.2m
    length1 = 6600  # L1=6.6m
    length2 = 10800  # L2=10.8m
    height1 = 2500  # h1=2.5m
    height2 = 2650  # h2=2.65m
    roof_angle = 16  # angle=16°
    ground_level = -1400  # -1.4 m.a.s.l
    
    # Create base walls with insulation
    def create_wall_with_insulation(width, thickness, height):
        # Block wall (220mm)
        wall = Part.makeBox(width, thickness, height)
        # Insulation layer (150mm mineral wool)
        insulation = Part.makeBox(width, 150, height)
        insulation.translate(FreeCAD.Vector(0, thickness, 0))
        return wall.fuse([insulation])
    
    # Front wall
    front_wall = create_wall_with_insulation(width, 220, height1)
    front_wall.translate(FreeCAD.Vector(0, 0, ground_level))
    
    # Side walls
    left_wall = create_wall_with_insulation(220, length2, height1)
    left_wall.translate(FreeCAD.Vector(0, 0, ground_level))
    
    right_wall = create_wall_with_insulation(220, length2, height1)
    right_wall.translate(FreeCAD.Vector(width-220, 0, ground_level))
    
    # Back wall
    back_wall = create_wall_with_insulation(width, 220, height1)
    back_wall.translate(FreeCAD.Vector(0, length2-220, ground_level))
    
    # Combine walls
    walls = front_wall.fuse([left_wall, right_wall, back_wall])
    
    # Create wall object
    wall_obj = doc.addObject("Part::Feature", "Walls")
    wall_obj.Shape = walls
    
def create_roof():
    # Roof dimensions
    width = 7200
    length2 = 10800
    height1 = 2500
    height2 = 2650
    angle = 16
    ground_level = -1400
    purlin_spacing = 1100  # s=1.1m
    
    # Calculate roof points
    peak_height = height2
    roof_rise = peak_height - height1
    roof_run = width/2
    
    # Create main roof structure
    p1 = FreeCAD.Vector(0, 0, height1 + ground_level)
    p2 = FreeCAD.Vector(width, 0, height1 + ground_level)
    p3 = FreeCAD.Vector(width/2, 0, peak_height + ground_level)
    
    # Create roof face
    roof_wire = Part.makePolygon([p1, p2, p3, p1])
    roof_face = Part.Face(roof_wire)
    
    # Extrude roof face
    roof = roof_face.extrude(FreeCAD.Vector(0, length2, 0))
    
    # Create purlins
    purlins = []
    purlin_width = 80  # 80mm width
    purlin_height = 160  # 160mm height
    
    # Calculate number of purlins needed on each side
    roof_length = math.sqrt((width/2)**2 + roof_rise**2)
    num_purlins = int(roof_length / purlin_spacing)
    
    # Create purlins for both sides of the roof
    for side in [-1, 1]:  # Left and right sides
        for i in range(num_purlins):
            # Calculate purlin position along roof slope
            pos = i * purlin_spacing
            x_offset = pos * math.cos(math.radians(angle)) * side
            z_offset = pos * math.sin(math.radians(angle))
            
            # Create purlin
            purlin = Part.makeBox(purlin_width, length2, purlin_height)
            
            # Position purlin
            base_x = width/2 + x_offset
            base_z = height1 + z_offset + ground_level
            purlin.translate(FreeCAD.Vector(base_x - purlin_width/2, 0, base_z))
            
            # Rotate purlin to match roof angle
            rotation = FreeCAD.Rotation(FreeCAD.Vector(0,1,0), angle * side)
            purlin.rotate(FreeCAD.Vector(base_x, 0, base_z), FreeCAD.Vector(0,1,0), angle * side)
            
            purlins.append(purlin)
    
    # Combine roof and purlins
    roof_structure = roof.fuse(purlins)
    
    # Create roof object
    roof_obj = doc.addObject("Part::Feature", "Roof")
    roof_obj.Shape = roof_structure

def create_columns():
    # Column dimensions (from calculations)
    column_size = 150  # 150mm x 150mm
    spacing = 1100  # s=1.1m
    ground_level = -1400  # -1.4 m.a.s.l
    
    columns = []
    
    # Create columns along the length
    for i in range(int(10800/spacing)):
        # Column extends 400mm into foundation
        column = Part.makeBox(column_size, column_size, 2900)  # Height + foundation depth
        column.translate(FreeCAD.Vector(3525, i*spacing, ground_level - 400))  # Start from foundation level
        columns.append(column)
    
    # Combine all columns
    all_columns = columns[0].multiFuse(columns[1:])
    
    # Create columns object
    columns_obj = doc.addObject("Part::Feature", "Columns")
    columns_obj.Shape = all_columns
    
def create_detail_drawings():
    # Column-Foundation Connection Detail
    def create_foundation_detail():
        # Foundation pad (600x600x400mm)
        foundation = Part.makeBox(600, 600, 400)
        foundation.translate(FreeCAD.Vector(-225, -225, -400))  # Centered under column
        
        # Column stub (150x150x500mm)
        column = Part.makeBox(150, 150, 500)
        
        # Anchor bolts (simplified representation)
        bolt_radius = 8
        bolt_height = 450
        bolt1 = Part.makeCylinder(bolt_radius, bolt_height)
        bolt2 = Part.makeCylinder(bolt_radius, bolt_height)
        bolt3 = Part.makeCylinder(bolt_radius, bolt_height)
        bolt4 = Part.makeCylinder(bolt_radius, bolt_height)
        
        # Position bolts at corners
        bolt1.translate(FreeCAD.Vector(25, 25, -350))
        bolt2.translate(FreeCAD.Vector(125, 25, -350))
        bolt3.translate(FreeCAD.Vector(25, 125, -350))
        bolt4.translate(FreeCAD.Vector(125, 125, -350))
        
        # Combine all parts
        foundation_detail = foundation.fuse([column, bolt1, bolt2, bolt3, bolt4])
        detail_obj = doc.addObject("Part::Feature", "FoundationDetail")
        detail_obj.Shape = foundation_detail
        return detail_obj
    
    # Roof-Column Connection Detail
    def create_roof_connection_detail():
        # Column top (150x150x200mm)
        column_top = Part.makeBox(150, 150, 200)
        
        # Roof beam (100x200x400mm)
        beam = Part.makeBox(400, 100, 200)
        beam.translate(FreeCAD.Vector(-125, 25, 150))
        
        # Steel plate (200x200x10mm)
        plate = Part.makeBox(200, 200, 10)
        plate.translate(FreeCAD.Vector(-25, -25, 140))
        
        # Bolts
        bolt_radius = 8
        bolt_height = 170
        bolts = []
        bolt_positions = [(25, 25), (125, 25), (25, 125), (125, 125)]
        for x, y in bolt_positions:
            bolt = Part.makeCylinder(bolt_radius, bolt_height)
            bolt.translate(FreeCAD.Vector(x, y, 0))
            bolts.append(bolt)
        
        # Combine all parts
        connection = column_top.fuse([beam, plate] + bolts)
        detail_obj = doc.addObject("Part::Feature", "RoofConnection")
        detail_obj.Shape = connection
        return detail_obj
    
    # Wall-Roof Junction Detail
    def create_wall_roof_junction():
        # Wall section (220mm block + 150mm insulation)
        wall = Part.makeBox(370, 200, 500)  # Total wall thickness
        
        # Roof section
        roof_angle = 16
        roof_length = 600
        roof_height = roof_length * math.tan(math.radians(roof_angle))
        
        # Create roof shape
        p1 = FreeCAD.Vector(0, 0, 500)
        p2 = FreeCAD.Vector(roof_length, 0, 500)
        p3 = FreeCAD.Vector(0, 0, 500 + roof_height)
        roof_wire = Part.makePolygon([p1, p2, p3, p1])
        roof_face = Part.Face(roof_wire)
        roof = roof_face.extrude(FreeCAD.Vector(0, 200, 0))
        
        # Insulation layers
        wall_insulation = Part.makeBox(150, 200, 500)
        wall_insulation.translate(FreeCAD.Vector(220, 0, 0))
        
        roof_insulation = Part.makeBox(600, 200, 200)
        roof_insulation.rotate(FreeCAD.Vector(0, 0, 500), FreeCAD.Vector(0, 1, 0), roof_angle)
        
        # Combine all parts
        junction = wall.fuse([roof, wall_insulation, roof_insulation])
        detail_obj = doc.addObject("Part::Feature", "WallRoofJunction")
        detail_obj.Shape = junction
        return detail_obj
    
    # Insulation Installation Detail
    def create_insulation_detail():
        # Wall section
        wall = Part.makeBox(220, 400, 400)  # MAX 220 block
        
        # Insulation layer with mounting points
        insulation = Part.makeBox(150, 400, 400)
        insulation.translate(FreeCAD.Vector(220, 0, 0))
        
        # Mounting anchors (simplified representation)
        anchors = []
        anchor_positions = [(110, 100), (110, 300), (295, 100), (295, 300)]
        for x, y in anchor_positions:
            anchor = Part.makeCylinder(5, 30)
            anchor.rotate(FreeCAD.Vector(x, y, 200), FreeCAD.Vector(0, 1, 0), 90)
            anchor.translate(FreeCAD.Vector(0, y, x))
            anchors.append(anchor)
        
        # Combine all parts
        installation = wall.fuse([insulation] + anchors)
        detail_obj = doc.addObject("Part::Feature", "InsulationDetail")
        detail_obj.Shape = installation
        return detail_obj
    
    # Create all details
    foundation_detail = create_foundation_detail()
    roof_connection = create_roof_connection_detail()
    wall_roof_junction = create_wall_roof_junction()
    insulation_detail = create_insulation_detail()
    
    return [foundation_detail, roof_connection, wall_roof_junction, insulation_detail]

def export_drawings():
    """Export drawings in required formats"""
    try:
        # Create export directory if it doesn't exist
        export_dir = "/home/ubuntu/cad_project/exports"
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Save native FreeCAD file without GUI dependencies
        print("Saving FreeCAD file...")
        fcstd_path = os.path.join(export_dir, "dataset5_building.FCStd")
        doc.saveAs(fcstd_path)  # Use saveAs() with full path
        
        # Export to DXF format using core functionality
        print("Exporting DXF files...")
        scale_main = 1.0/50.0  # 1:50 scale for main views
        scale_detail = 1.0/10.0  # 1:10 scale for detail drawings
        
        def export_to_dxf(objects, filename, scale):
            # Building dimensions in mm
            width = 7200      # b = 7.2m
            length1 = 6600    # L1 = 6.6m
            length2 = 10800   # L2 = 10.8m
            height1 = 2500    # h1 = 2.5m
            height2 = 2650    # h2 = 2.65m
            ground_level = -1400  # -1.4 m.a.s.l
            
            # Create a new document for export
            export_doc = FreeCAD.newDocument(f"Export_{filename}")
            
            # Copy and scale objects
            for obj in objects:
                scaled_shape = obj.Shape.copy()
                scaled_shape.scale(scale)
                new_obj = export_doc.addObject("Part::Feature", obj.Name)
                new_obj.Shape = scaled_shape
            
            # Export using basic DXF format
            export_doc.recompute()
            dxf_path = os.path.join(export_dir, filename)
            
            # Create DXF file with proper headers and layers
            with open(dxf_path, 'w') as f:
                # Header section
                f.write("0\nSECTION\n2\nHEADER\n")
                f.write("9\n$ACADVER\n1\nAC1014\n")  # AutoCAD 2000 format
                f.write("9\n$MEASUREMENT\n70\n1\n")  # Metric
                f.write("9\n$INSUNITS\n70\n4\n")    # Millimeters
                f.write("9\n$LUNITS\n70\n2\n")      # Decimal
                f.write("0\nENDSEC\n")
                
                # Tables section
                f.write("0\nSECTION\n2\nTABLES\n")
                # Layer table
                f.write("0\nTABLE\n2\nLAYER\n70\n3\n")
                f.write("0\nLAYER\n2\n0\n70\n0\n62\n7\n6\nCONTINUOUS\n")
                f.write("0\nLAYER\n2\nDIMENSIONS\n70\n0\n62\n1\n6\nCONTINUOUS\n")
                f.write("0\nLAYER\n2\nTEXT\n70\n0\n62\n3\n6\nCONTINUOUS\n")
                f.write("0\nENDTAB\n0\nENDSEC\n")
                
                # Entities section
                f.write("0\nSECTION\n2\nENTITIES\n")
                
                # Export geometry
                for obj in export_doc.Objects:
                    if hasattr(obj, 'Shape'):
                        edges = obj.Shape.Edges
                        for edge in edges:
                            if len(edge.Vertexes) >= 2:
                                start = edge.Vertexes[0].Point
                                end = edge.Vertexes[-1].Point
                                
                                # Write line entity
                                f.write("0\nLINE\n")
                                f.write("8\n0\n")  # Layer 0
                                f.write(f"10\n{start.x:.6f}\n20\n{start.y:.6f}\n30\n{start.z:.6f}\n")
                                f.write(f"11\n{end.x:.6f}\n21\n{end.y:.6f}\n31\n{end.z:.6f}\n")
                
                # Add annotations based on drawing type
                def add_text(x, y, text, height=2.5, layer="TEXT"):
                    f.write("0\nTEXT\n")
                    f.write(f"8\n{layer}\n")  # Layer name
                    f.write(f"10\n{x}\n20\n{y}\n30\n0\n")  # Position
                    f.write(f"40\n{height}\n")  # Text height
                    f.write(f"1\n{text}\n")  # Text content
                    f.write("7\nSTANDARD\n")  # Text style
                
                def add_dimension(x1, y1, x2, y2, text, offset=20):
                    """Add dimension line with text"""
                    # Dimension line
                    f.write("0\nLINE\n8\nDIMENSIONS\n")
                    f.write(f"10\n{x1}\n20\n{y1}\n30\n0\n")
                    f.write(f"11\n{x2}\n21\n{y2}\n31\n0\n")
                    # Extension lines
                    f.write("0\nLINE\n8\nDIMENSIONS\n")
                    f.write(f"10\n{x1}\n20\n{y1}\n30\n0\n")
                    f.write(f"11\n{x1}\n21\n{y1+offset}\n31\n0\n")
                    f.write("0\nLINE\n8\nDIMENSIONS\n")
                    f.write(f"10\n{x2}\n20\n{y2}\n30\n0\n")
                    f.write(f"11\n{x2}\n21\n{y2+offset}\n31\n0\n")
                    # Dimension text
                    text_x = (x1 + x2) / 2
                    text_y = y1 + offset + 5
                    add_text(text_x, text_y, text, layer="DIMENSIONS")

                # Add dimensions and annotations based on filename
                if "vertical" in filename.lower():
                    # Title and scale
                    add_text(-100, -50, "VERTICAL PROJECTION")
                    add_text(-100, -75, f"Scale 1:{int(1/scale)}")
                    
                    # Ground level and heights
                    add_text(-100, height1*scale/2, "Ground Level: -1.4 m.a.s.l")
                    add_dimension(0, 0, 0, height1*scale, "h1 = 2.5m")
                    add_dimension(width*scale, 0, width*scale, height1*scale, "h1 = 2.5m")
                    add_dimension(width*scale/2, height1*scale, width*scale/2, height2*scale, "h2 = 2.65m")
                    
                    # Roof angle
                    add_text(width*scale/4, height2*scale - 100, "Roof Angle: 16°")
                    
                    # Wall composition
                    add_text(-150, height1*scale/2, "Wall Section:")
                    add_text(-150, height1*scale/2 - 30, "- MAX 220 block")
                    add_text(-150, height1*scale/2 - 60, "- 150mm mineral wool")
                    
                elif "horizontal" in filename.lower():
                    # Title and scale
                    add_text(-100, -50, "HORIZONTAL PROJECTION")
                    add_text(-100, -75, f"Scale 1:{int(1/scale)}")
                    
                    # Building dimensions
                    add_dimension(0, 0, width*scale, 0, "b = 7.2m")
                    add_dimension(0, 0, 0, length2*scale, "L2 = 10.8m")
                    add_dimension(width*scale, 0, width*scale, length1*scale, "L1 = 6.6m")
                    
                    # Purlin spacing
                    for i in range(int(length2/1100)):
                        y = i * 1100 * scale
                        add_dimension(-50, y, -50, y + 1100*scale, "s = 1.1m")
                    
                    # Column grid
                    add_text(-100, -100, "Column Grid:")
                    add_text(-100, -125, "- C27 timber columns")
                    add_text(-100, -150, "- 150×150mm section")
                    add_text(-100, -175, "- 1.1m spacing")
                    
                elif "detail" in filename.lower():
                    add_text(-50, -25, f"DETAIL DRAWING - Scale 1:10")
                    if "foundation" in filename.lower():
                        add_text(-50, -50, "Foundation-Column Connection")
                        add_dimension(-225, -400, 375, -400, "600mm")
                        add_dimension(-225, -400, -225, 0, "400mm")
                        add_text(-50, -75, "Column: 150×150mm C27 timber")
                        add_text(-50, -100, "Foundation: 600×600×400mm concrete")
                    elif "roof" in filename.lower():
                        add_text(-50, -50, "Roof-Column Connection")
                        add_dimension(-125, 150, 275, 150, "400mm")
                        add_text(-50, -75, "Purlin: 80×160mm C27 timber")
                        add_text(-50, -100, "Steel plate: 200×200×10mm")
                    elif "insulation" in filename.lower():
                        add_text(-50, -50, "Wall-Insulation Detail")
                        add_dimension(0, 0, 220, 0, "220mm")
                        add_dimension(220, 0, 370, 0, "150mm")
                        add_text(-50, -75, "Wall: MAX 220 block")
                        add_text(-50, -100, "Insulation: 150mm mineral wool")
                        add_text(-50, -125, "U-value: 0.195 W/(m²K)")
                
                # Close DXF file
                f.write("0\nENDSEC\n0\nEOF\n")
            
            print(f"Exported {filename}")
            
            FreeCAD.closeDocument(export_doc.Name)
        
        # Export main views
        main_objects = [doc.getObject("Walls"),
                       doc.getObject("Roof"),
                       doc.getObject("Columns")]
        export_to_dxf(main_objects, "vertical_projection.dxf", scale_main)
        
        # Export horizontal projection (top view)
        # Create a copy of objects and rotate for top view
        top_doc = FreeCAD.newDocument("TopView")
        for obj in main_objects:
            copied_shape = obj.Shape.copy()
            copied_shape.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1,0,0), -90)
            new_obj = top_doc.addObject("Part::Feature", f"{obj.Name}_top")
            new_obj.Shape = copied_shape
        top_doc.recompute()
        export_to_dxf(top_doc.Objects, "horizontal_projection.dxf", scale_main)
        FreeCAD.closeDocument(top_doc.Name)
        
        # Create and export detail drawings
        print("Creating detail drawings...")
        details = create_detail_drawings()
        
        # Export detail drawings
        for detail in details:
            if detail and hasattr(detail, 'Name'):
                export_to_dxf([detail], f"{detail.Name.lower()}.dxf", scale_detail)
                print(f"Exported detail: {detail.Name}")
        
        print("Successfully exported all drawings")
        return True
    except Exception as e:
        print(f"Error exporting drawings: {e}")
        print(f"Exception details: {str(e)}")
        return False

def create_documentation():
    """Create documentation for the drawings"""
    doc_path = "/home/ubuntu/cad_project/drawing_documentation.md"
    try:
        with open(doc_path, "w") as f:
            f.write("""# Building Design Documentation - Dataset 5

## Drawing Specifications
1. Main Views (Scale 1:50)
   - Vertical projection (front elevation)
   - Horizontal projection (top view)

2. Detail Drawings (Scale 1:10)
   - Foundation-column connection
   - Roof-column connection
   - Wall-roof junction
   - Insulation installation detail

## Building Parameters
1. Dimensions:
   - Width (b) = 7.2m
   - Length 1 (L1) = 6.6m
   - Length 2 (L2) = 10.8m
   - Height 1 (h1) = 2.5m
   - Height 2 (h2) = 2.65m
   - Roof angle = 16°
   - Purlin spacing = 1.1m
   - Ground level = -1.4 m.a.s.l

2. Materials:
   - Walls: Max 220 block
   - Insulation: Mineral wool
   - Roofing: Steel tile 0.6mm
   - Structure: C27 timber class""")
        print(f"Documentation created at {doc_path}")
        return True
    except Exception as e:
        print(f"Error creating documentation: {e}")
        return False

def main():
    """Main execution function"""
    try:
        if not init_environment():
            raise Exception("Failed to initialize FreeCAD environment")
            
        print("Creating building elements...")
        create_walls()
        create_roof()
        create_columns()
        create_detail_drawings()
        
        print("Recomputing document...")
        doc.recompute()
        
        print("Exporting drawings...")
        if not export_drawings():
            raise Exception("Failed to export drawings")
            
        print("Creating documentation...")
        if not create_documentation():
            raise Exception("Failed to create documentation")
            
        print("Successfully completed all operations")
        return True
    except Exception as e:
        print(f"Error in main execution: {e}")
        return False

if __name__ == '__main__':
    print("Starting main execution...")
    main()
