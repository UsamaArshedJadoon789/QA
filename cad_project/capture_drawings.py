#!/usr/bin/env python3
import os
import sys
import time

# Set up FreeCAD environment
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

import FreeCAD as App
import FreeCADGui as Gui
import importDXF

def capture_view(filepath, output_name, scale):
    """Open DXF and capture view"""
    try:
        # Create new document
        doc = App.newDocument(output_name)
        
        # Import DXF
        importDXF.open(filepath)
        
        # Set up view
        Gui.activeDocument().activeView().viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
        
        # Save screenshot
        output_dir = "exports/screenshots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{output_name}.png")
        
        Gui.activeDocument().activeView().saveImage(output_path, 2048, 1536)
        print(f"Captured {output_name}")
        
        # Close document
        App.closeDocument(doc.Name)
        
    except Exception as e:
        print(f"Error capturing {output_name}: {str(e)}")

def main():
    # Create screenshots directory
    os.makedirs("exports/screenshots", exist_ok=True)
    
    # Capture each drawing
    drawings = [
        ("exports/dataset5_vertical.dxf", "vertical_projection", "1:50"),
        ("exports/dataset5_horizontal.dxf", "horizontal_projection", "1:50"),
        ("exports/dataset5_details.dxf", "detail_drawings", "1:10")
    ]
    
    for filepath, name, scale in drawings:
        if os.path.exists(filepath):
            capture_view(filepath, name, scale)
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
