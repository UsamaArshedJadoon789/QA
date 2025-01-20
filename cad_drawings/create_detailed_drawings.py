import FreeCAD as App
import Draft
import Part
import importDXF
import math

# Create new document
doc = App.newDocument()

# Dataset 5 specifications (all dimensions in mm)
width = 7200
length1 = 6600
length2 = 10800
height1 = 2500
height2 = 2650
angle = 16  # degrees
spacing = 1100
ground_level = -1400

def create_horizontal_projection():
    """Create top view with rafters and purlins"""
    # Main building outline
    rect = Draft.makeRectangle(length1, width)
    
    # Add rafters (at 1100mm spacing)
    rafter_count = int(length1 / spacing) + 1
    rafters = []
    for i in range(rafter_count):
        pos = i * spacing
        if pos <= length1:
            rafter = Draft.makeRectangle(200, width)  # 200mm wide rafters
            Draft.move(rafter, App.Vector(pos, 0, 0))
            rafters.append(rafter)
    
    # Add purlins
    purlin_spacing = 1500  # 1.5m spacing for purlins
    purlin_count = int(width / purlin_spacing) + 1
    purlins = []
    for i in range(purlin_count):
        pos = i * purlin_spacing
        if pos <= width:
            purlin = Draft.makeRectangle(length1, 150)  # 150mm wide purlins
            Draft.move(purlin, App.Vector(0, pos, 0))
            purlins.append(purlin)
    
    # Group all elements
    horizontal_group = doc.addObject("App::DocumentObjectGroup", "HorizontalProjection")
    horizontal_group.addObject(rect)
    for r in rafters:
        horizontal_group.addObject(r)
    for p in purlins:
        horizontal_group.addObject(p)
    
    return [rect] + rafters + purlins

def create_vertical_projection():
    """Create side view with structural details"""
    # Main outline
    points = [
        App.Vector(0, ground_level, 0),
        App.Vector(0, height1, 0),
        App.Vector(width, height2, 0),
        App.Vector(width, ground_level, 0)
    ]
    outline = Draft.makeWire(points, closed=True)
    
    # Add roof structure
    angle_rad = math.radians(angle)
    roof_height = width * math.tan(angle_rad)
    
    # Rafters
    rafter_count = int(width / spacing) + 1
    rafters = []
    for i in range(rafter_count):
        pos = i * spacing
        if pos <= width:
            rafter_points = [
                App.Vector(pos, height1 + (pos/width)*roof_height, 0),
                App.Vector(pos, height1 + (pos/width)*roof_height - 200, 0)  # 200mm deep rafters
            ]
            rafter = Draft.makeWire(rafter_points)
            rafters.append(rafter)
    
    # Thermal insulation layer (simplified representation)
    insulation_points = [
        App.Vector(0, height1, 0),
        App.Vector(width, height2, 0),
        App.Vector(width, height2 - 200, 0),  # 200mm insulation thickness
        App.Vector(0, height1 - 200, 0)
    ]
    insulation = Draft.makeWire(insulation_points, closed=True)
    
    # Columns
    column_spacing = 2000  # 2m spacing for columns
    column_count = int(width / column_spacing) + 1
    columns = []
    for i in range(column_count):
        pos = i * column_spacing
        if pos <= width:
            column_points = [
                App.Vector(pos, ground_level, 0),
                App.Vector(pos, height1 + (pos/width)*(height2-height1), 0)
            ]
            column = Draft.makeWire(column_points)
            columns.append(column)
    
    # Group all elements
    vertical_group = doc.addObject("App::DocumentObjectGroup", "VerticalProjection")
    vertical_group.addObject(outline)
    vertical_group.addObject(insulation)
    for r in rafters:
        vertical_group.addObject(r)
    for c in columns:
        vertical_group.addObject(c)
    
    return [outline, insulation] + rafters + columns

# Create projections
horizontal_elements = create_horizontal_projection()
doc.recompute()
importDXF.export(horizontal_elements, 'horizontal_projection.dxf')

vertical_elements = create_vertical_projection()
doc.recompute()
importDXF.export(vertical_elements, 'vertical_projection.dxf')

# Save FreeCAD document
doc.saveAs('building_drawings.FCStd')
