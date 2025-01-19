#!/usr/bin/env python3
import os
import sys

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

print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    import FreeCAD
    print("FreeCAD imported successfully")
    print("FreeCAD version:", FreeCAD.Version())
    
    # Create a new document
    doc = FreeCAD.newDocument()
    print("Document created successfully")
    
    # Try to create a simple line
    import Part
    line = Part.makeLine((0,0,0), (10,0,0))
    doc.addObject("Part::Feature", "Line").Shape = line
    print("Line created successfully")
    
    # Save document
    doc.saveAs("/home/ubuntu/cad_project/test.FCStd")
    print("Document saved successfully")
    
except Exception as e:
    print("Error:", str(e))
    print("Exception type:", type(e))
    sys.exit(1)
