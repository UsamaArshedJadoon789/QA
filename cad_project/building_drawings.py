#!/usr/bin/env python3
import os
import sys
import math
import traceback

print("\n=== Starting FreeCAD Drawing Generation Script ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

# Set environment variables
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['FREECAD_LIB'] = '/usr/lib/freecad/lib'

# Add FreeCAD paths
freecad_paths = [
    '/usr/lib/freecad-python3/lib',
    '/usr/lib/freecad/lib',
    '/usr/share/freecad/Mod'
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

print("Python path:", sys.path)

try:
    import FreeCAD
    print("FreeCAD imported successfully")
    print("FreeCAD version:", FreeCAD.Version())
    
    # Import required modules
    import Part
    print("Part workbench imported")
    
    import Draft
    print("Draft workbench imported")
    
    # Create alias for FreeCAD
    App = FreeCAD
    
    print("\nFreeCAD environment initialized successfully")
    
except Exception as e:
    print(f"\nError during initialization: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

# FreeCAD and Draft are already imported as App and Draft

# Dataset 5 specifications
SPECS = {
    'width': 7200,  # b=7.2m in mm
    'length1': 6600,  # L1=6.6m in mm
    'length2': 10800,  # L2=10.8m in mm
    'height1': 2500,  # h1=2.5m in mm
    'height2': 2650,  # h2=2.65m in mm
    'roof_angle': 16,  # degrees
    'purlin_spacing': 1100,  # s=1.1m in mm
    'ground_level': -1400,  # -1.4 m.a.s.l in mm
    'wall_thickness': 220,  # Max 220 block in mm
    'insulation_thickness': 150,  # Mineral wool in mm
    'column_size': 150,  # 150x150mm
}

def create_vertical_projection(doc):
    """Create vertical projection at 1:50 scale"""
    # Draft is already imported at module level
    
    # Create foundation level
    p_found1 = App.Vector(-500, SPECS['ground_level'], 0)
    p_found2 = App.Vector(SPECS['width'] + 500, SPECS['ground_level'], 0)
    foundation = doc.addObject("Part::Feature", "Foundation_Level")
    foundation.Shape = Part.LineSegment(p_found1, p_found2).toShape()
    
    # Create walls with thickness
    # Left wall
    # Create left wall face
    wall_points = [
        App.Vector(0, SPECS['ground_level'], 0),
        App.Vector(0, SPECS['height1'], 0),
        App.Vector(SPECS['wall_thickness'], SPECS['height1'], 0),
        App.Vector(SPECS['wall_thickness'], SPECS['ground_level'], 0)
    ]
    # Create wire and force it to be closed
    wall_wire = Part.makePolygon(wall_points + [wall_points[0]])
    # Create face from wire
    wall_face = Part.Face(wall_wire)
    # Create shape
    wall_left = doc.addObject("Part::Feature", "Wall_Left")
    wall_left.Shape = wall_face
    # Verify face was created
    if len(wall_left.Shape.Faces) == 0:
        print("Warning: Failed to create face for left wall")
    
    # Right wall
    # Create right wall face
    wall_points = [
        App.Vector(SPECS['width'] - SPECS['wall_thickness'], SPECS['ground_level'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'], SPECS['height1'], 0),
        App.Vector(SPECS['width'], SPECS['height1'], 0),
        App.Vector(SPECS['width'], SPECS['ground_level'], 0)
    ]
    # Create wire and force it to be closed
    wall_wire = Part.makePolygon(wall_points + [wall_points[0]])
    # Create face from wire
    wall_face = Part.Face(wall_wire)
    # Create shape
    wall_right = doc.addObject("Part::Feature", "Wall_Right")
    wall_right.Shape = wall_face
    # Verify face was created
    if len(wall_right.Shape.Faces) == 0:
        print("Warning: Failed to create face for right wall")
    
    # Create insulation layers
    # Create left insulation face
    insul_points = [
        App.Vector(SPECS['wall_thickness'], SPECS['ground_level'], 0),
        App.Vector(SPECS['wall_thickness'], SPECS['height1'], 0),
        App.Vector(SPECS['wall_thickness'] + SPECS['insulation_thickness'], SPECS['height1'], 0),
        App.Vector(SPECS['wall_thickness'] + SPECS['insulation_thickness'], SPECS['ground_level'], 0)
    ]
    # Create wire and force it to be closed
    insul_wire = Part.makePolygon(insul_points + [insul_points[0]])
    # Create face from wire
    insul_face = Part.Face(insul_wire)
    # Create shape
    insul_left = doc.addObject("Part::Feature", "Insulation_Left")
    insul_left.Shape = insul_face
    # Verify face was created
    if len(insul_left.Shape.Faces) == 0:
        print("Warning: Failed to create face for left insulation")
    
    # Create right insulation face
    insul_points = [
        App.Vector(SPECS['width'] - SPECS['wall_thickness'] - SPECS['insulation_thickness'], SPECS['ground_level'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'] - SPECS['insulation_thickness'], SPECS['height1'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'], SPECS['height1'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'], SPECS['ground_level'], 0)
    ]
    # Create wire and force it to be closed
    insul_wire = Part.makePolygon(insul_points + [insul_points[0]])
    # Create face from wire
    insul_face = Part.Face(insul_wire)
    # Create shape
    insul_right = doc.addObject("Part::Feature", "Insulation_Right")
    insul_right.Shape = insul_face
    # Verify face was created
    if len(insul_right.Shape.Faces) == 0:
        print("Warning: Failed to create face for right insulation")
    
    # Create roof structure
    angle_rad = math.radians(SPECS['roof_angle'])
    roof_rise = SPECS['width'] * math.tan(angle_rad) / 2
    peak_height = SPECS['height1'] + roof_rise
    
    # Roof outline
    # Create roof face
    roof_points = [
        App.Vector(0, SPECS['height1'], 0),
        App.Vector(SPECS['width']/2, peak_height, 0),
        App.Vector(SPECS['width'], SPECS['height1'], 0)
    ]
    # Create wire and force it to be closed
    roof_wire = Part.makePolygon(roof_points + [roof_points[0]])
    # Create face from wire
    try:
        roof_face = Part.Face(roof_wire)
        # Create shape
        roof = doc.addObject("Part::Feature", "Roof")
        roof.Shape = roof_face
        # Verify face was created
        if len(roof.Shape.Faces) == 0:
            print("Warning: Failed to create face for roof")
    except Part.OCCError as e:
        print(f"Error creating roof face: {str(e)}")
        # Fallback to wire if face creation fails
        roof = doc.addObject("Part::Feature", "Roof")
        roof.Shape = roof_wire
    
    # Add dimensions
    def add_dimension(p1, p2, offset, text):
        # Create dimension line
        dim_line = doc.addObject("Part::Feature", f"Dim_{text}")
        dim_line.Shape = Part.LineSegment(p1 + offset, p2 + offset).toShape()
        
        # Add dimension text
        text_pos = p1 + offset + (p2 - p1).multiply(0.5)
        text_obj = doc.addObject("App::AnnotationLabel", f"DimText_{text}")
        text_obj.BasePosition = text_pos
        text_obj.LabelText = text
        
        return [dim_line, text_obj]
    
    # Height dimensions
    h1_dim = add_dimension(
        App.Vector(-500, SPECS['ground_level'], 0),
        App.Vector(-500, SPECS['height1'], 0),
        App.Vector(-1000, 0, 0),
        "h1=2.5m"
    )
    
    h2_dim = add_dimension(
        App.Vector(-500, SPECS['height1'], 0),
        App.Vector(-500, peak_height, 0),
        App.Vector(-1000, 0, 0),
        "h2=2.65m"
    )
    
    # Add annotations
    def add_text(pos, text, size=200):
        text_obj = doc.addObject("App::AnnotationLabel", f"Anno_{text}")
        text_obj.BasePosition = pos
        text_obj.LabelText = text
        return text_obj
    
    # Add ground level annotation
    ground_anno = add_text(
        App.Vector(-2000, SPECS['ground_level'], 0),
        "Ground Level: -1.4 m.a.s.l"
    )
    
    # Add roof angle annotation
    angle_anno = add_text(
        App.Vector(SPECS['width']/4, peak_height + 500, 0),
        "Roof Angle: 16°"
    )
    
    # Add columns
    col_width = SPECS['column_size']
    # Left column
    # Create left column face
    col_points = [
        App.Vector(SPECS['wall_thickness'] + 100, SPECS['ground_level'], 0),
        App.Vector(SPECS['wall_thickness'] + 100, SPECS['height1'], 0),
        App.Vector(SPECS['wall_thickness'] + 100 + col_width, SPECS['height1'], 0),
        App.Vector(SPECS['wall_thickness'] + 100 + col_width, SPECS['ground_level'], 0)
    ]
    col_wire = Part.makePolygon(col_points + [col_points[0]])
    col_left = doc.addObject("Part::Feature", "Column_Left")
    col_left.Shape = Part.Face(col_wire)
    
    # Right column
    # Create right column face
    col_points = [
        App.Vector(SPECS['width'] - SPECS['wall_thickness'] - 100 - col_width, SPECS['ground_level'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'] - 100 - col_width, SPECS['height1'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'] - 100, SPECS['height1'], 0),
        App.Vector(SPECS['width'] - SPECS['wall_thickness'] - 100, SPECS['ground_level'], 0)
    ]
    col_wire = Part.makePolygon(col_points + [col_points[0]])
    col_right = doc.addObject("Part::Feature", "Column_Right")
    col_right.Shape = Part.Face(col_wire)
    
    # Add wall thickness annotation
    wall_dim = add_dimension(
        App.Vector(0, SPECS['height1'] - 500, 0),
        App.Vector(SPECS['wall_thickness'], SPECS['height1'] - 500, 0),
        App.Vector(0, 100, 0),
        "Wall: 220mm"
    )
    
    # Add insulation thickness annotation
    insul_dim = add_dimension(
        App.Vector(SPECS['wall_thickness'], SPECS['height1'] - 800, 0),
        App.Vector(SPECS['wall_thickness'] + SPECS['insulation_thickness'], SPECS['height1'] - 800, 0),
        App.Vector(0, 100, 0),
        "Insulation: 150mm"
    )
    
    # Flatten lists of objects returned by add_dimension
    objects = [
        foundation,
        wall_left, wall_right,
        insul_left, insul_right,
        roof,
        col_left, col_right
    ]
    objects.extend(h1_dim)  # h1_dim returns [line, text]
    objects.extend(h2_dim)  # h2_dim returns [line, text]
    objects.extend(wall_dim)  # wall_dim returns [line, text]
    objects.extend(insul_dim)  # insul_dim returns [line, text]
    objects.extend([ground_anno, angle_anno])
    return objects

def create_horizontal_projection(doc):
    """Create horizontal projection at 1:50 scale"""
    # Draft is already imported at module level
    
    # Create outline
    points = [
        App.Vector(0, 0, 0),
        App.Vector(SPECS['width'], 0, 0),
        App.Vector(SPECS['width'], SPECS['length2'], 0),
        App.Vector(0, SPECS['length2'], 0),
        App.Vector(0, 0, 0)
    ]
    # Create building outline face
    outline_wire = Part.makePolygon(points + [points[0]])
    outline_face = Part.Face(outline_wire)
    outline = doc.addObject("Part::Feature", "Building_Outline")
    outline.Shape = outline_face
    # Verify face was created
    if len(outline.Shape.Faces) == 0:
        print("Warning: Failed to create face for building outline")
    
    # Add purlins
    purlins = []
    current_pos = 0
    while current_pos < SPECS['length2']:
        p1 = App.Vector(0, current_pos, 0)
        p2 = App.Vector(SPECS['width'], current_pos, 0)
        purlin = doc.addObject("Part::Feature", f"Purlin_{len(purlins)}")
        purlin.Shape = Part.LineSegment(p1, p2).toShape()
        purlins.append(purlin)
        current_pos += SPECS['purlin_spacing']
    
    # Add dimensions
    def add_dimension(p1, p2, offset, text):
        # Create dimension line
        dim_line = doc.addObject("Part::Feature", f"Dim_{text}")
        dim_line.Shape = Part.LineSegment(p1 + offset, p2 + offset).toShape()
        
        # Add dimension text
        text_pos = p1 + offset + (p2 - p1).multiply(0.5)
        text_obj = doc.addObject("App::AnnotationLabel", f"DimText_{text}")
        text_obj.BasePosition = text_pos
        text_obj.LabelText = text
        
        return [dim_line, text_obj]
    
    # Width dimension
    width_dim = add_dimension(
        App.Vector(0, -500, 0),
        App.Vector(SPECS['width'], -500, 0),
        App.Vector(0, -1000, 0),
        "b=7.2m"
    )
    
    # Length dimensions
    l1_dim = add_dimension(
        App.Vector(-500, 0, 0),
        App.Vector(-500, SPECS['length1'], 0),
        App.Vector(-1000, 0, 0),
        "L1=6.6m"
    )
    
    l2_dim = add_dimension(
        App.Vector(-500, 0, 0),
        App.Vector(-500, SPECS['length2'], 0),
        App.Vector(-1500, 0, 0),
        "L2=10.8m"
    )
    
    # Add purlin spacing annotation
    spacing_anno = doc.addObject("App::AnnotationLabel", "Anno_PurlinSpacing")
    spacing_anno.BasePosition = App.Vector(SPECS['width'] + 500, SPECS['length2']/2, 0)
    spacing_anno.LabelText = "Purlin Spacing: 1.1m"
    
    # Flatten lists of objects returned by add_dimension
    objects = [outline] + purlins
    objects.extend(width_dim)  # width_dim returns [line, text]
    objects.extend(l1_dim)     # l1_dim returns [line, text]
    objects.extend(l2_dim)     # l2_dim returns [line, text]
    objects.append(spacing_anno)
    return objects

def create_detail_drawings(doc):
    """Create detail drawings at 1:10 scale"""
    # Draft is already imported at module level
    
    details = []
    
    # Column-foundation connection
    def create_foundation_detail():
        foundation_group = []
        
        def add_dimension(p1, p2, offset, text):
            # Create dimension line
            dim_line = doc.addObject("Part::Feature", f"DetailDim_{text}")
            dim_line.Shape = Part.LineSegment(p1 + offset, p2 + offset).toShape()
            
            # Add dimension text
            text_pos = p1 + offset + (p2 - p1).multiply(0.5)
            text_obj = doc.addObject("App::AnnotationLabel", f"DetailDimText_{text}")
            text_obj.BasePosition = text_pos
            text_obj.LabelText = text
            
            return [dim_line, text_obj]
        
        # Column
        p1 = App.Vector(0, 0, 0)
        p2 = App.Vector(SPECS['column_size'], 0, 0)
        p3 = App.Vector(SPECS['column_size'], SPECS['column_size'], 0)
        p4 = App.Vector(0, SPECS['column_size'], 0)
        column = doc.addObject("Part::Feature", "Column_Section")
        column.Shape = Part.makePolygon([p1, p2, p3, p4, p1])
        foundation_group.append(column)
        
        # Foundation
        f1 = App.Vector(-200, -400, 0)
        f2 = App.Vector(SPECS['column_size'] + 200, -400, 0)
        f3 = App.Vector(SPECS['column_size'] + 200, 0, 0)
        f4 = App.Vector(-200, 0, 0)
        foundation = doc.addObject("Part::Feature", "Foundation")
        foundation.Shape = Part.makePolygon([f1, f2, f3, f4, f1])
        foundation_group.append(foundation)
        
        # Dimensions
        dim1 = add_dimension(
            p1, p2,
            App.Vector(0, SPECS['column_size'] + 100, 0),
            "150mm"
        )
        foundation_group.extend(dim1)  # dim1 returns [line, text]
        
        return foundation_group
    
    # Wall-roof junction detail
    def create_wall_roof_detail():
        wall_roof_group = []
        
        # Wall section
        wall_points = [
            App.Vector(0, 0, 0),
            App.Vector(SPECS['wall_thickness'], 0, 0),
            App.Vector(SPECS['wall_thickness'], 500, 0),
            App.Vector(0, 500, 0),
            App.Vector(0, 0, 0)
        ]
        wall = doc.addObject("Part::Feature", "Wall_Section")
        wall.Shape = Part.makePolygon(wall_points)
        wall_roof_group.append(wall)
        
        # Insulation layer
        insulation_points = [
            App.Vector(SPECS['wall_thickness'], 0, 0),
            App.Vector(SPECS['wall_thickness'] + SPECS['insulation_thickness'], 0, 0),
            App.Vector(SPECS['wall_thickness'] + SPECS['insulation_thickness'], 500, 0),
            App.Vector(SPECS['wall_thickness'], 500, 0),
            App.Vector(SPECS['wall_thickness'], 0, 0)
        ]
        insulation = doc.addObject("Part::Feature", "Insulation")
        insulation.Shape = Part.makePolygon(insulation_points)
        wall_roof_group.append(insulation)
        
        # Annotations
        text1 = doc.addObject("App::AnnotationLabel", "Anno_WallBlock")
        text1.BasePosition = App.Vector(0, -100, 0)
        text1.LabelText = "MAX 220 Block"
        
        text2 = doc.addObject("App::AnnotationLabel", "Anno_Insulation")
        text2.BasePosition = App.Vector(SPECS['wall_thickness'], -100, 0)
        text2.LabelText = "150mm Mineral Wool"
        wall_roof_group.extend([text1, text2])
        
        return wall_roof_group
    
    def create_rafter_purlin_detail():
        rafter_purlin_group = []
        
        # Create rafter section (rotated to show connection)
        rafter_points = [
            App.Vector(0, 0, 0),
            App.Vector(200, 0, 0),  # 200mm height
            App.Vector(200, 100, 0), # 100mm width
            App.Vector(0, 100, 0),
            App.Vector(0, 0, 0)
        ]
        rafter = doc.addObject("Part::Feature", "Rafter_Section")
        rafter.Shape = Part.makePolygon(rafter_points)
        rafter_purlin_group.append(rafter)
        
        # Create purlin section
        purlin_points = [
            App.Vector(50, -80, 0),  # Offset from rafter
            App.Vector(130, -80, 0),  # 80mm width
            App.Vector(130, -240, 0), # 160mm height
            App.Vector(50, -240, 0),
            App.Vector(50, -80, 0)
        ]
        purlin = doc.addObject("Part::Feature", "Purlin_Section")
        purlin.Shape = Part.makePolygon(purlin_points)
        rafter_purlin_group.append(purlin)
        
        # Add annotations
        text1 = doc.addObject("App::AnnotationLabel", "Anno_RafterPurlin")
        text1.BasePosition = App.Vector(0, -300, 0)
        text1.LabelText = "Purlin: 80×160mm C27"
        rafter_purlin_group.append(text1)
        
        return rafter_purlin_group
        
    def create_column_roof_detail():
        column_roof_group = []
        
        # Create column top section
        column_points = [
            App.Vector(0, 0, 0),
            App.Vector(SPECS['column_size'], 0, 0),
            App.Vector(SPECS['column_size'], SPECS['column_size'], 0),
            App.Vector(0, SPECS['column_size'], 0),
            App.Vector(0, 0, 0)
        ]
        column = doc.addObject("Part::Feature", "Column_Top")
        column.Shape = Part.makePolygon(column_points)
        column_roof_group.append(column)
        
        # Create rafter connection
        angle_rad = math.radians(SPECS['roof_angle'])
        rafter_points = [
            App.Vector(-50, SPECS['column_size'], 0),
            App.Vector(SPECS['column_size'] + 50, SPECS['column_size'], 0),
            App.Vector(SPECS['column_size'] + 50, SPECS['column_size'] + 100, 0),
            App.Vector(-50, SPECS['column_size'] + 100, 0),
            App.Vector(-50, SPECS['column_size'], 0)
        ]
        rafter = doc.addObject("Part::Feature", "Rafter_Connection")
        rafter.Shape = Part.makePolygon(rafter_points)
        column_roof_group.append(rafter)
        
        # Add annotations
        text1 = doc.addObject("App::AnnotationLabel", "Anno_ColumnRoof")
        text1.BasePosition = App.Vector(0, -50, 0)
        text1.LabelText = "Column-Roof Connection"
        column_roof_group.append(text1)
        
        return column_roof_group
    
    # Create and collect all details
    details.extend(create_foundation_detail())
    details.extend(create_wall_roof_detail())
    details.extend(create_rafter_purlin_detail())
    details.extend(create_column_roof_detail())
    
    return details

def main():
    print("\n=== Starting Drawing Generation ===")
    print("Python version:", sys.version)
    print("Python path:", sys.path)
    
    try:
        # Create new document
        print("\nCreating new document...")
        doc = App.newDocument("Dataset5_Building")
        print("Document created successfully")
        
        try:
            # Create vertical projection
            print("\nCreating vertical projection...")
            vertical_objects = create_vertical_projection(doc)
            print(f"Created {len(vertical_objects)} objects for vertical projection")
            
            # Create horizontal projection
            print("\nCreating horizontal projection...")
            horizontal_objects = create_horizontal_projection(doc)
            print(f"Created {len(horizontal_objects)} objects for horizontal projection")
            
            # Create detail drawings
            print("\nCreating detail drawings...")
            detail_objects = create_detail_drawings(doc)
            print(f"Created {len(detail_objects)} objects for detail drawings")
            
            # Save document
            print("\nSaving FreeCAD document...")
            doc.recompute()
            fcstd_path = "/home/ubuntu/cad_project/dataset5_building.FCStd"
            doc.saveAs(fcstd_path)
            print(f"Saved FreeCAD file to: {fcstd_path}")
            
            # Export to DXF
            print("\nExporting to DXF format...")
            try:
                import Draft
                
                # Create export directory if it doesn't exist
                export_dir = "/home/ubuntu/cad_project/exports"
                os.makedirs(export_dir, exist_ok=True)
                
                def export_to_dxf(objects, filename, scale=1.0):
                    """Export objects to DXF with proper scaling"""
                    # Create a new document for scaled export
                    export_doc = App.newDocument(f"Export_{os.path.splitext(filename)[0]}")
                    
                    # Copy and scale objects
                    export_objects = []
                    for obj in objects:
                        if hasattr(obj, 'Shape'):
                            new_obj = export_doc.addObject("Part::Feature", obj.Name)
                            scaled_shape = obj.Shape.copy()
                            scaled_shape.scale(scale)
                            new_obj.Shape = scaled_shape
                            export_objects.append(new_obj)
                        elif hasattr(obj, 'LabelText'):  # Handle annotations
                            new_obj = export_doc.addObject("App::AnnotationLabel", obj.Name)
                            new_obj.LabelText = obj.LabelText
                            new_obj.BasePosition = App.Vector(
                                obj.BasePosition.x * scale,
                                obj.BasePosition.y * scale,
                                obj.BasePosition.z * scale
                            )
                            export_objects.append(new_obj)
                    
                    export_doc.recompute()
                    
                    # Export using Draft workbench
                    filepath = os.path.join(export_dir, filename)
                    
                    # Create scaled objects for export
                    scaled_objects = []
                    for obj in export_objects:
                        if hasattr(obj, 'Shape'):
                            # Create a new object with scaled shape
                            new_obj = export_doc.addObject("Part::Feature", f"Scaled_{obj.Name}")
                            scaled_shape = obj.Shape.copy()
                            scaled_shape.scale(scale)
                            new_obj.Shape = scaled_shape
                            scaled_objects.append(new_obj)
                        elif hasattr(obj, 'LabelText'):
                            # Create text as annotation
                            pos = obj.BasePosition
                            anno = export_doc.addObject("App::AnnotationLabel", f"Text_{obj.Name}")
                            anno.BasePosition = App.Vector(pos.x * scale, pos.y * scale, 0)
                            anno.LabelText = str(obj.LabelText)
                            scaled_objects.append(anno)
                    
                    export_doc.recompute()
                    
                    # Export to DXF using enhanced DXF writer
                    try:
                        # Convert mm to drawing units based on scale
                        drawing_scale = 1.0 if "detail" in filename.lower() else 50.0
                        unit_scale = 1.0  # 1 drawing unit = 1 mm
                        
                        with open(filepath, 'w') as f:
                            # Write DXF header
                            f.write("0\nSECTION\n2\nHEADER\n")
                            f.write("9\n$ACADVER\n1\nAC1014\n")  # AutoCAD 2000
                            f.write("9\n$MEASUREMENT\n70\n1\n")  # Metric
                            f.write("9\n$INSUNITS\n70\n4\n")    # Millimeters
                            f.write("9\n$LUNITS\n70\n2\n")      # Decimal
                            f.write("9\n$DIMSCALE\n40\n1.0\n")  # Dimension scale
                            f.write("9\n$DIMTXT\n40\n2.5\n")    # Dimension text height
                            f.write("9\n$DIMASZ\n40\n2.5\n")    # Arrow size
                            f.write("9\n$DIMEXE\n40\n1.25\n")   # Extension line extension
                            f.write("9\n$DIMEXO\n40\n0.625\n")  # Extension line offset
                            f.write("9\n$DIMGAP\n40\n0.625\n")  # Dimension line gap
                            f.write("9\n$DIMTIH\n70\n1\n")      # Text inside horizontal
                            f.write("9\n$DIMTOH\n70\n1\n")      # Text outside horizontal
                            f.write("0\nENDSEC\n")
                            
                            # Write tables section
                            f.write("0\nSECTION\n2\nTABLES\n")
                            # Layer table
                            f.write("0\nTABLE\n2\nLAYER\n70\n3\n")
                            f.write("0\nLAYER\n2\n0\n70\n0\n62\n7\n6\nCONTINUOUS\n")
                            f.write("0\nLAYER\n2\nDIMENSIONS\n70\n0\n62\n1\n6\nCONTINUOUS\n")
                            f.write("0\nLAYER\n2\nTEXT\n70\n0\n62\n3\n6\nCONTINUOUS\n")
                            f.write("0\nENDTAB\n0\nENDSEC\n")
                            
                            # Write entities section
                            f.write("0\nSECTION\n2\nENTITIES\n")
                            
                            # Write geometry
                            for obj in scaled_objects:
                                if hasattr(obj, 'Shape'):
                                    for edge in obj.Shape.Edges:
                                        if len(edge.Vertexes) >= 2:
                                            v1 = edge.Vertexes[0].Point
                                            v2 = edge.Vertexes[-1].Point
                                            # Scale coordinates
                                            x1 = v1.x * unit_scale / drawing_scale
                                            y1 = v1.y * unit_scale / drawing_scale
                                            x2 = v2.x * unit_scale / drawing_scale
                                            y2 = v2.y * unit_scale / drawing_scale
                                            
                                            f.write("0\nLINE\n")
                                            f.write("8\n0\n")  # Layer 0
                                            f.write(f"10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0\n")
                                            f.write(f"11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0\n")
                                
                                elif hasattr(obj, 'LabelText'):
                                    pos = obj.BasePosition
                                    # Scale text position
                                    x = pos.x * unit_scale / drawing_scale
                                    y = pos.y * unit_scale / drawing_scale
                                    
                                    f.write("0\nTEXT\n")
                                    f.write("8\nTEXT\n")  # TEXT layer
                                    f.write(f"10\n{x:.3f}\n20\n{y:.3f}\n30\n0\n")
                                    # Adjust text height based on drawing scale
                                    text_height = 2.5 * drawing_scale if "detail" not in filename.lower() else 25
                                    f.write(f"40\n{text_height}\n")  # Text height in drawing units
                                    f.write(f"1\n{obj.LabelText}\n")
                                    f.write("7\nSTANDARD\n")  # Text style
                                    f.write("72\n0\n")  # Left-aligned text
                            
                            # Add scale annotation and title
                            title = "VERTICAL PROJECTION" if "vertical" in filename.lower() else \
                                   "HORIZONTAL PROJECTION" if "horizontal" in filename.lower() else \
                                   "DETAIL DRAWINGS"
                            
                            # Title
                            f.write("0\nTEXT\n")
                            f.write("8\nTEXT\n")
                            f.write("10\n0\n20\n-250\n30\n0\n")
                            f.write(f"40\n{text_height * 1.5}\n")
                            f.write(f"1\n{title}\n")
                            f.write("7\nSTANDARD\n")
                            f.write("72\n1\n")  # Center-aligned
                            
                            # Scale annotation
                            scale_text = f"Scale 1:{int(drawing_scale)}"
                            f.write("0\nTEXT\n")
                            f.write("8\nTEXT\n")
                            f.write("10\n0\n20\n-500\n30\n0\n")
                            f.write(f"40\n{text_height}\n")
                            f.write(f"1\n{scale_text}\n")
                            f.write("7\nSTANDARD\n")
                            f.write("72\n0\n")  # Left-aligned
                            
                            # Close DXF file
                            f.write("0\nENDSEC\n0\nEOF\n")
                            
                        print(f"Exported {filename} with scale 1:{int(drawing_scale)}")
                        
                    except Exception as e:
                        print(f"Error exporting {filename}: {str(e)}")
                        raise
                        print(f"Exported {filename} using fallback method")
                    
                    App.closeDocument(export_doc.Name)
                
                # Export vertical projection (1:50)
                print(f"\nExporting vertical projection...")
                export_to_dxf(vertical_objects, "dataset5_vertical.dxf", scale=1/50)
                
                # Export horizontal projection (1:50)
                print(f"Exporting horizontal projection...")
                export_to_dxf(horizontal_objects, "dataset5_horizontal.dxf", scale=1/50)
                
                # Export details (1:10)
                print(f"Exporting detail drawings...")
                export_to_dxf(detail_objects, "dataset5_details.dxf", scale=1/10)
                
                print("\nSuccessfully exported all DXF files")
            except Exception as export_error:
                print(f"\nError during DXF export: {str(export_error)}")
                print(f"Exception type: {type(export_error)}")
                raise
            
            print("\n=== Drawing Generation Complete ===")
            return True
            
        except Exception as draw_error:
            print(f"\nError during drawing creation: {str(draw_error)}")
            print(f"Exception type: {type(draw_error)}")
            raise
            
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        print(f"Exception type: {type(e)}")
        return False

def run():
    """Wrapper function to ensure proper execution"""
    try:
        print("\n=== Starting Drawing Generation ===")
        print(f"FreeCAD Version: {App.Version()}")
        print(f"Python Path: {sys.path}")
        
        result = main()
        
        if result:
            print("\n=== Drawing Generation Completed Successfully ===")
            print("Generated files:")
            print("- dataset5_building.FCStd")
            print("- dataset5_vertical.dxf")
            print("- dataset5_horizontal.dxf")
            print("- dataset5_details.dxf")
        else:
            print("\n=== Drawing Generation Failed ===")
        
        return result
        
    except Exception as e:
        print(f"\nFatal error in run(): {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if run() else 1)
