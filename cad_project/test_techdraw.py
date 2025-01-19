#!/usr/bin/env python3
import sys
import os

# Set up FreeCAD environment
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['FREECAD_LIB'] = '/usr/lib/freecad/lib'

try:
    import FreeCAD
    import TechDraw
    print('FreeCAD Version:', FreeCAD.Version())
    print('TechDraw module successfully loaded')
    sys.exit(0)
except ImportError as e:
    print('Error:', str(e))
    sys.exit(1)
