#!/usr/bin/python3
import os
import sys
import subprocess

def setup_freecad_env():
    """Set up FreeCAD environment variables and paths"""
    # Get FreeCAD Python path from pkg-config if available
    try:
        cmd = ['pkg-config', '--variable=pythondir', 'freecad']
        freecad_python = subprocess.check_output(cmd).decode().strip()
        if freecad_python and freecad_python not in sys.path:
            sys.path.append(freecad_python)
    except:
        # Fallback paths
        paths = [
            '/usr/lib/freecad-python3/lib',
            '/usr/lib/freecad/lib',
            '/usr/share/freecad/Mod'
        ]
        for path in paths:
            if os.path.exists(path) and path not in sys.path:
                sys.path.append(path)
    
    # Set environment variables
    os.environ['DISPLAY'] = ''
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    os.environ['COIN_GL_NO_WINDOW'] = '1'

# Set up environment
setup_freecad_env()

try:
    print('Importing FreeCAD...')
    import FreeCAD
    print('FreeCAD Version:', FreeCAD.Version())
    
    print('Importing Draft...')
    import Draft
    print('Draft imported successfully')
    
    # Create a test document
    doc = FreeCAD.newDocument('TestDoc')
    print('Document created successfully')
    
    # Create a simple rectangle (2D)
    print('Creating rectangle...')
    rect = Draft.makeRectangle(length=100, height=50)
    print('Rectangle created successfully')
    
    # Create a line (2D)
    print('Creating line...')
    p1 = FreeCAD.Vector(0, 0, 0)
    p2 = FreeCAD.Vector(100, 100, 0)
    line = Draft.makeLine(p1, p2)
    print('Line created successfully')
    
    # Save as FCStd
    doc.recompute()
    doc.saveAs("/home/ubuntu/cad_project/test.FCStd")
    print('FCStd file saved successfully')
    
    # Export to DXF using Draft
    print('Exporting to DXF...')
    import importDXF
    importDXF.export([rect, line], "/home/ubuntu/cad_project/test.dxf")
    print('DXF file exported successfully')
    
except Exception as e:
    print('Error:', str(e))
    print('Exception type:', type(e))
    print('Python path:', sys.path)
    
print('Test completed')
