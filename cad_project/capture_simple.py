#!/usr/bin/env python3
import os
import sys

# Set environment
os.environ['DISPLAY'] = ':99'
os.environ['QT_QPA_PLATFORM'] = 'xcb'
os.environ['PYTHONPATH'] = '/usr/lib/freecad/lib'

import FreeCAD
import Import
import Part

def capture_drawing(dxf_path, output_name):
    """Capture a single drawing"""
    try:
        # Create new document
        doc = FreeCAD.newDocument(output_name)
        
        # Import DXF
        Import.insert(dxf_path, doc.Name)
        doc.recompute()
        
        # Create output directory
        output_dir = "exports/screenshots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{output_name}.png")
        
        print(f"Processing {output_name}...")
        return True
        
    except Exception as e:
        print(f"Error processing {output_name}: {str(e)}")
        return False

def main():
    # Test with vertical projection first
    dxf_path = "exports/dataset5_vertical.dxf"
    if os.path.exists(dxf_path):
        success = capture_drawing(dxf_path, "vertical_test")
        print("Test capture completed:", "Success" if success else "Failed")
    else:
        print(f"DXF file not found: {dxf_path}")

if __name__ == "__main__":
    main()
