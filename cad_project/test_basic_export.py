#!/usr/bin/python3
import os
import sys

# Add FreeCAD paths
freecad_paths = [
    '/usr/lib/freecad-python3/lib',
    '/usr/lib/freecad/lib',
    '/usr/share/freecad/Mod',
    '/usr/lib/python3/dist-packages'
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

# Set environment variables
os.environ.update({
    'DISPLAY': '',
    'QT_QPA_PLATFORM': 'offscreen',
    'FREECAD_LIB': '/usr/lib/freecad/lib',
    'PYTHONPATH': '/usr/lib/freecad-python3/lib:/usr/lib/freecad/lib',
    'COIN_GL_NO_WINDOW': '1'
})

import FreeCAD
import Part

# Set up environment
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

print("FreeCAD Version:", FreeCAD.Version())

# Create export directories
export_dir = "/home/ubuntu/cad_project/exports"
screenshot_dir = os.path.join(export_dir, "screenshots")
temp_dir = os.path.join(export_dir, "temp")
os.makedirs(screenshot_dir, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

# Create new document
doc = FreeCAD.newDocument("TestExport")

try:
    # Create a simple rectangle
    print("\nCreating test shape...")
    rect = Part.makeBox(100, 50, 0.1)  # Very thin box to appear as 2D
    obj = doc.addObject("Part::Feature", "Rectangle")
    obj.Shape = rect
    doc.recompute()
    
    # Create SVG directly
    svg_path = os.path.join(temp_dir, "test.svg")
    print(f"\nCreating SVG at: {svg_path}")
    
    svg_content = ['<?xml version="1.0" encoding="UTF-8"?>',
                  '<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="1536">']
    
    # Add rectangle edges as paths
    for edge in obj.Shape.Edges:
        if len(edge.Vertexes) >= 2:
            v1, v2 = edge.Vertexes[0].Point, edge.Vertexes[-1].Point
            path = f'<path d="M {v1.x},{v1.y} L {v2.x},{v2.y}" stroke="black" fill="none"/>'
            svg_content.append(path)
    
    svg_content.append('</svg>')
    
    # Write SVG file
    with open(svg_path, 'w') as f:
        f.write('\n'.join(svg_content))
    
    if os.path.exists(svg_path):
        size = os.path.getsize(svg_path)
        print(f"SVG file created successfully: {size} bytes")
        
        # Convert to PNG using ImageMagick
        png_path = os.path.join(screenshot_dir, "test.png")
        print(f"\nConverting to PNG: {png_path}")
        
        import subprocess
        result = subprocess.run([
            'convert',
            '-density', '300',
            '-resize', '2048x1536',
            '-background', 'white',
            '-flatten',
            svg_path,
            png_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(png_path):
            print(f"PNG file created successfully: {os.path.getsize(png_path)} bytes")
        else:
            print("Error converting to PNG:")
            print(result.stderr)
    else:
        print("Failed to create SVG file")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    print(f"Exception type: {type(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTest completed")
