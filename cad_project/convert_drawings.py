#!/usr/bin/python3
import os
import sys
import subprocess

# Set up FreeCAD environment
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['FREECAD_LIB'] = '/usr/lib/freecad/lib'
os.environ['PYTHONPATH'] = '/usr/lib/freecad-python3/lib'

# Add FreeCAD paths
freecad_paths = [
    '/usr/lib/freecad-python3/lib',
    '/usr/lib/freecad/lib',
    '/usr/share/freecad/Mod'
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

try:
    import FreeCAD
    import Import
    import TechDraw
    import Part
except ImportError as e:
    print(f"Error importing FreeCAD modules: {e}")
    sys.exit(1)

# Set up FreeCAD environment
os.environ['DISPLAY'] = ''
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['FREECAD_LIB'] = '/usr/lib/freecad/lib'

def convert_dxf_to_png(dxf_path, output_name, scale=1.0):
    """Convert DXF directly to PNG using FreeCAD's TechDraw"""
    try:
        # Create output directories
        os.makedirs("exports/screenshots", exist_ok=True)
        
        # Create new document
        doc = FreeCAD.newDocument(output_name)
        
        # Import DXF as a new object
        import_obj = doc.addObject("Part::Feature", "ImportedDXF")
        
        # Read DXF and create shapes
        shapes = Import.readDXF(dxf_path)
        if not shapes:
            print(f"No shapes found in {dxf_path}")
            return None
            
        # Create compound from imported shapes
        compound = Part.makeCompound(shapes)
        import_obj.Shape = compound
        doc.recompute()
        
        # Create TechDraw page
        page = doc.addObject('TechDraw::DrawPage', 'Page')
        template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
        
        # Use a blank template
        template.Template = os.path.join(os.path.dirname(FreeCAD.getResourceDir()), 
                                       "Mod", "TechDraw", "Templates", "A3_Landscape_blank.svg")
        page.Template = template
        
        # Create view
        view = doc.addObject('TechDraw::DrawViewPart', 'View')
        page.addView(view)
        view.Source = import_obj  # Set source to the imported object
        view.Scale = scale
        view.X = 200  # Position on page
        view.Y = 200
        
        # Add dimensions and annotations based on drawing type
        if "vertical" in output_name:
            # Add height dimensions
            dim1 = doc.addObject('TechDraw::DrawViewDimension', 'Height1')
            dim1.Type = 'Distance'
            dim1.References2D = [(view, 'h1')]
            page.addView(dim1)
            
            # Add angle dimension
            dim2 = doc.addObject('TechDraw::DrawViewDimension', 'RoofAngle')
            dim2.Type = 'Angle'
            dim2.References2D = [(view, 'angle')]
            page.addView(dim2)
            
        elif "horizontal" in output_name:
            # Add width and length dimensions
            dim1 = doc.addObject('TechDraw::DrawViewDimension', 'Width')
            dim1.Type = 'Distance'
            dim1.References2D = [(view, 'b')]
            page.addView(dim1)
            
            dim2 = doc.addObject('TechDraw::DrawViewDimension', 'Length')
            dim2.Type = 'Distance'
            dim2.References2D = [(view, 'L1')]
            page.addView(dim2)
        
        doc.recompute()
        
        # Export to PNG
        png_path = f"exports/screenshots/{output_name}.png"
        page.ViewObject.save(png_path, 2048, 1536)  # HD resolution
        
        FreeCAD.closeDocument(doc.Name)
        return png_path
            
    except Exception as e:
        print(f"Error converting DXF to PNG: {str(e)}")
        print(f"Exception details: {str(e.__dict__)}")
        return None

def add_technical_description(png_path, drawing_type):
    """Add technical description to PNG using ImageMagick"""
    try:
        temp_png = png_path.replace('.png', '_temp.png')
        os.rename(png_path, temp_png)
        
        # Get description based on drawing type
        description = ""
        if "vertical" in drawing_type:
            description = (
                "Vertical Projection (Scale 1:50)\n"
                "Building heights: h1=2.5m, h2=2.65m\n"
                "Roof angle: 16°, Ground level: -1.4 m.a.s.l\n"
                "Wall construction: MAX 220 block with mineral wool insulation"
            )
        elif "horizontal" in drawing_type:
            description = (
                "Horizontal Projection (Scale 1:50)\n"
                "Building dimensions: b=7.2m, L1=6.6m, L2=10.8m\n"
                "Purlin spacing: s=1.1m\n"
                "Structure: C27 timber class, Steel tile roofing 0.6mm"
            )
        else:
            description = (
                "Detail Drawings (Scale 1:10)\n"
                "Structural connections and thermal envelope details\n"
                "Wall: MAX 220 block with 150mm mineral wool insulation\n"
                "Roof: C27 timber rafters and purlins, Steel tile 0.6mm"
            )
        
        # Add annotations using ImageMagick
        cmd = [
            'convert', temp_png,
            '-gravity', 'south',
            '-background', 'white',
            '-splice', '0x150',
            '-pointsize', '40',
            '-fill', 'black',
            '-annotate', '+0+20',
            description,
            png_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error adding annotations: {result.stderr}")
            return False
            
        # Clean up temporary file
        os.remove(temp_png)
        return True
        
    except Exception as e:
        print(f"Error adding technical description: {str(e)}")
        return False

def main():
    # Drawing specifications with proper scaling
    drawings = [
        ("dataset5_vertical.dxf", "vertical_projection", 1/50),  # 1:50 scale
        ("dataset5_horizontal.dxf", "horizontal_projection", 1/50),  # 1:50 scale
        ("dataset5_details.dxf", "detail_drawings", 1/10)  # 1:10 scale for details
    ]
    
    success = True
    for dxf_path, name, scale in drawings:
        full_path = os.path.join("exports", dxf_path)
        if os.path.exists(full_path):
            print(f"\nProcessing: {name}")
            png_path = convert_dxf_to_png(full_path, name, scale)
            
            if png_path and os.path.exists(png_path):
                # Verify image quality
                size = os.path.getsize(png_path)
                if size < 50000:  # Minimum size threshold for HD quality
                    print(f"Warning: Generated PNG size ({size} bytes) may be too small for HD quality")
                    success = False
                else:
                    # Add technical description
                    if add_technical_description(png_path, name):
                        print(f"Successfully converted {name}")
                    else:
                        success = False
                        print(f"Failed to add technical description to {name}")
            else:
                success = False
                print(f"Failed to convert {name}")
        else:
            print(f"DXF file not found: {full_path}")
            success = False
    
    return success

if __name__ == "__main__":
    print("FreeCAD Version:", FreeCAD.Version())
    if main():
        print("\nAll drawings converted successfully")
    else:
        print("\nSome drawings failed to convert")
        sys.exit(1)
