#!/usr/bin/env python3
import os
import sys

# Set FreeCAD environment
os.environ['FREECAD_LIB'] = '/usr/lib/freecad/lib'
os.environ['PYTHONPATH'] = '/usr/lib/freecad/lib'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

try:
    print("Python version:", sys.version)
    print("Python path:", sys.path)
    
    import FreeCAD
    print("FreeCAD imported successfully")
    print("FreeCAD version:", FreeCAD.Version())
    
    # Create new document
    doc = FreeCAD.newDocument()
    print("Document created successfully")
    
    # Try to import Draft workbench
    import Draft
    print("Draft workbench imported successfully")
    
    # Create a simple line
    p1 = FreeCAD.Vector(0, 0, 0)
    p2 = FreeCAD.Vector(100, 100, 0)
    line = Draft.makeLine(p1, p2)
    print("Line created successfully")
    
    # Save document
    doc.saveAs("/home/ubuntu/cad_project/test.FCStd")
    print("Document saved successfully")
    
except Exception as e:
    print("Error occurred:", str(e))
    print("Exception type:", type(e))
    sys.exit(1)
