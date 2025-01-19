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

print('Python version:', sys.version)
print('Python path:', sys.path)

try:
    import FreeCAD
    print('\nFreeCAD imported successfully')
    print('FreeCAD version:', FreeCAD.Version())
    
    import FreeCADGui
    print('\nFreeCADGui imported successfully')
    FreeCADGui.showMainWindow()  # Required for TechDraw
    
    import TechDraw
    print('TechDraw module imported successfully')
    
    # Create test document
    doc = FreeCAD.newDocument('TestDoc')
    print('\nTest document created')
    
    # Try to create TechDraw page
    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    print('TechDraw objects created successfully')
    
    # Clean up
    FreeCAD.closeDocument('TestDoc')
    print('\nAll tests passed successfully')
    
except Exception as e:
    print('\nError:', str(e))
    print('Exception type:', type(e))
    sys.exit(1)
