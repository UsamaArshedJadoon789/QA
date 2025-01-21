import FreeCAD as App
import Draft
import Part
import importDXF

# Create new document
doc = App.newDocument()

# Dataset 5 specifications
width = 7200  # mm
length1 = 6600  # mm
length2 = 10800  # mm
height1 = 2500  # mm
height2 = 2650  # mm
angle = 16  # degrees
spacing = 1100  # mm

# Create horizontal projection (top view)
rect = Draft.makeRectangle(length1, width)
doc.recompute()

# Export to DXF
importDXF.export([rect], 'horizontal_projection.dxf')

# Create vertical projection (side view)
points = [
    App.Vector(0, 0, 0),
    App.Vector(0, height1, 0),
    App.Vector(width, height2, 0),
    App.Vector(width, 0, 0)
]
wire = Draft.makeWire(points, closed=True)
doc.recompute()

# Export to DXF
importDXF.export([wire], 'vertical_projection.dxf')

# Save document
doc.saveAs('building_drawings.FCStd')
