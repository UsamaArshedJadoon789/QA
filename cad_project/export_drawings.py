#!/usr/bin/python3
import os
import sys
import subprocess

# Set up FreeCAD environment for headless operation
os.environ.update({
    'DISPLAY': '',
    'QT_QPA_PLATFORM': 'offscreen',  # Use offscreen platform
    'FREECAD_LIB': '/usr/lib/freecad/lib',
    'PYTHONPATH': '/usr/lib/freecad-python3/lib:/usr/lib/freecad/lib',
    'COIN_GL_NO_WINDOW': '1',
    'LIBGL_ALWAYS_SOFTWARE': '1',
    'QT_QPA_FONTDIR': '/usr/share/fonts/truetype',  # Specify TrueType fonts
    'QT_QPA_PLATFORM_PLUGIN_PATH': '/usr/lib/x86_64-linux-gnu/qt5/plugins',
    'QT_FONT_DPI': '96',
    'QT_XKB_CONFIG_ROOT': '/usr/share/X11/xkb',
    'FONTCONFIG_PATH': '/etc/fonts',
    'FREECAD_USER_DATA': '/home/ubuntu/.FreeCAD',
    'PYTHONPATH': '/usr/lib/freecad-python3/lib:/usr/lib/freecad/lib:/usr/lib/python3/dist-packages'
})

# Add FreeCAD paths
freecad_paths = [
    '/usr/lib/freecad-python3/lib',
    '/usr/lib/freecad/lib',
    '/usr/share/freecad/Mod',
    '/usr/lib/python3/dist-packages',  # System Python packages
    '/usr/share/freecad-python3',  # Additional FreeCAD modules
    '/usr/lib/freecad/Mod',  # FreeCAD workbenches
    '/usr/lib/freecad/Ext'  # FreeCAD extensions
]

# Add paths to Python path
for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

# Import core FreeCAD modules
try:
    # Import core modules only
    import FreeCAD
    import Part
    import Import
    
    # Configure FreeCAD for console operation
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part").SetFloat("MeshDeviation", 0.1)
    
    # Set up parameters for drawing export
    EXPORT_PARAMS = {
        'SCALE_MAIN': 1.0/50.0,  # 1:50 scale for main views
        'SCALE_DETAIL': 1.0/10.0,  # 1:10 scale for detail views
        'PNG_WIDTH': 2048,
        'PNG_HEIGHT': 1536,
        'DPI': 300
    }
    
    print(f"FreeCAD Version: {FreeCAD.Version()}")
    print("Successfully imported core modules and initialized GUI system")
except ImportError as e:
    print(f"Error importing FreeCAD modules: {e}")
    sys.exit(1)

# Create test document to verify TechDraw
test_doc = FreeCAD.newDocument("TestDoc")
try:
    page = test_doc.addObject('TechDraw::DrawPage', 'TestPage')
    template = test_doc.addObject('TechDraw::DrawSVGTemplate', 'TestTemplate')
    print("TechDraw objects created successfully")
    test_doc.recompute()
except Exception as e:
    print(f"Error creating TechDraw objects: {str(e)}")
    sys.exit(1)
finally:
    FreeCAD.closeDocument("TestDoc")

def create_drawing(doc, name, objects, scale):
    """Create a drawing view with given objects and scale"""
    try:
        print(f"\nCreating drawing: {name}")
        print(f"Scale: 1:{int(1/scale)}")
        print(f"Number of objects: {len(objects)}")
        
        # Create compound from objects
        shapes = []
        for obj in objects:
            if hasattr(obj, 'Shape'):
                shapes.append(obj.Shape)
        
        if not shapes:
            print("No valid shapes found")
            return None
            
        compound = Part.makeCompound(shapes)
        
        # Scale the compound
        scaled_shape = compound.copy()
        scaled_shape.scale(scale)
        
        # Create a new object to hold the scaled shape
        view = doc.addObject("Part::Feature", f"View_{name}")
        view.Shape = scaled_shape
        
        doc.recompute()
        return view
        
    except Exception as e:
        print(f"Error creating drawing: {str(e)}")
        return None

def export_drawings():
    """Export drawings using Part module"""
    try:
        print("\nStarting drawing export...")
        
        # Create export directories with full paths
        base_dir = "/home/ubuntu/cad_project"
        export_dir = os.path.join(base_dir, "exports")
        screenshot_dir = os.path.join(export_dir, "screenshots")
        temp_dir = os.path.join(export_dir, "temp")
        
        # Remove existing directories to ensure clean state
        import shutil
        for dir_path in [screenshot_dir, temp_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
        
        # Create fresh directories
        os.makedirs(screenshot_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        print(f"\nExport directories created:")
        print(f"Screenshot dir: {screenshot_dir}")
        print(f"Temp dir: {temp_dir}")
        
        # Load FCStd file
        doc_path = "/home/ubuntu/cad_project/dataset5_building.FCStd"
        if not os.path.exists(doc_path):
            print(f"Error: {doc_path} not found")
            return False
            
        # Open document
        doc = FreeCAD.openDocument(doc_path)
        FreeCAD.setActiveDocument(doc.Name)
            
        # Export vertical projection (1:50)
        print("\nExporting vertical projection...")
        try:
            vertical_objects = [obj for obj in doc.Objects if obj.Name.startswith(("Wall", "Column", "Roof"))]
            view = create_drawing(doc, "Vertical", vertical_objects, EXPORT_PARAMS['SCALE_MAIN'])
            if not view:
                print("Error: Failed to create vertical projection view")
                return False
                
            # Set up export paths
            png_path = os.path.join(screenshot_dir, "vertical_projection.png")
            brep_path = os.path.join(temp_dir, "vertical.brp")
            svg_path = png_path.replace('.png', '.svg')
        except Exception as e:
            print(f"Error setting up vertical projection: {str(e)}")
            return False
            
            doc.recompute()
            
            # Export directly to SVG using Part module
            svg_path = png_path.replace('.png', '.svg')
            print(f"Exporting vertical projection to SVG: {svg_path}")
            
            try:
                # Export shape directly to SVG using Part module
                import Part
                print(f"Shape type: {type(view.Shape)}")
                print(f"Shape valid: {view.Shape.isValid()}")
                print(f"Shape faces: {len(view.Shape.Faces)}")
                print(f"Shape edges: {len(view.Shape.Edges)}")
                
                # Create projection
                proj = Part.makeProjection(view.Shape.Edges, FreeCAD.Vector(0,0,1))
                if not proj:
                    print("Failed to create projection")
                    return False
                
                # Create a new document for the projection
                proj_doc = FreeCAD.newDocument("Projection")
                proj_obj = proj_doc.addObject("Part::Feature", "Projection")
                proj_obj.Shape = proj[0]
                proj_doc.recompute()
                
                # Export to SVG
                import importSVG
                importSVG.export([proj_obj], svg_path)
                print(f"SVG export completed: {svg_path}")
                
                # Close projection document
                FreeCAD.closeDocument("Projection")
                
            except Exception as e:
                print(f"Error exporting vertical projection to SVG: {str(e)}")
                print(f"Exception type: {type(e)}")
                import traceback
                traceback.print_exc()
                return False
            
            if not os.path.exists(svg_path):
                print("Failed to create SVG file")
                return False
                
            print(f"Successfully exported to SVG: {svg_path}")
            
            # Convert SVG to PNG using ImageMagick with high quality settings
            try:
                subprocess.run([
                    'convert',
                    '-density', '300',
                    '-resize', f"{EXPORT_PARAMS['PNG_WIDTH']}x{EXPORT_PARAMS['PNG_HEIGHT']}",
                    '-background', 'white',
                    '-flatten',
                    svg_path,
                    png_path
                ], check=True)
                
                # Verify PNG was created
                if not os.path.exists(png_path):
                    print(f"Error: Failed to create PNG file at {png_path}")
                    return False
                    
                size = os.path.getsize(png_path)
                if size < 1000:
                    print(f"Error: Generated PNG file is too small ({size} bytes)")
                    return False
                    
                print(f"Successfully exported vertical projection ({size} bytes)")
            except subprocess.CalledProcessError as e:
                print(f"Error converting SVG to PNG: {str(e)}")
                return False
            
            if not os.path.exists(svg_path):
                print("Failed to create SVG file")
                return False
                
            print(f"Successfully exported to SVG: {svg_path}")
            
            # Convert SVG to PNG using ImageMagick
            try:
                subprocess.run([
                    'convert',
                    '-density', '300',
                    '-resize', '2048x1536',
                    '-background', 'white',
                    '-flatten',
                    svg_path,
                    png_path
                ], check=True)
                
                # Clean up SVG file
                os.remove(svg_path)
                
                # Verify export
                if not os.path.exists(png_path):
                    print(f"Error: Failed to create PNG file at {png_path}")
                    return False
                
                size = os.path.getsize(png_path)
                if size < 1000:
                    print(f"Error: Generated PNG file is too small ({size} bytes)")
                    return False
                
                print(f"Successfully exported vertical projection ({size} bytes)")
                # Continue with next projection
            except subprocess.CalledProcessError as e:
                print(f"Error converting SVG to PNG: {str(e)}")
                return False
            except Exception as e:
                print(f"Error during vertical projection export: {str(e)}")
                return False
        
        # Export horizontal projection (1:50)
        print("\nExporting horizontal projection...")
        try:
            horizontal_objects = [obj for obj in doc.Objects if obj.Name.startswith(("Building", "Purlin"))]
            view = create_drawing(doc, "Horizontal", horizontal_objects, EXPORT_PARAMS['SCALE_MAIN'])
            if not view:
                print("Error: Failed to create horizontal projection view")
                return False
                
            # Set up export paths
            png_path = os.path.join(screenshot_dir, "horizontal_projection.png")
            brep_path = os.path.join(temp_dir, "horizontal.brp")
            svg_path = png_path.replace('.png', '.svg')
        except Exception as e:
            print(f"Error setting up horizontal projection: {str(e)}")
            return False
            
            doc.recompute()
            
            # Export directly to SVG using Part module
            svg_path = png_path.replace('.png', '.svg')
            print(f"Exporting horizontal projection to SVG: {svg_path}")
            
            try:
                # Export shape directly to SVG using Part module
                import Part
                print(f"Shape type: {type(view.Shape)}")
                print(f"Shape valid: {view.Shape.isValid()}")
                print(f"Shape faces: {len(view.Shape.Faces)}")
                print(f"Shape edges: {len(view.Shape.Edges)}")
                
                # Create projection
                proj = Part.makeProjection(view.Shape.Edges, FreeCAD.Vector(0,1,0))
                if not proj:
                    print("Failed to create projection")
                    return False
                
                # Create a new document for the projection
                proj_doc = FreeCAD.newDocument("Projection")
                proj_obj = proj_doc.addObject("Part::Feature", "Projection")
                proj_obj.Shape = proj[0]
                proj_doc.recompute()
                
                # Export to SVG
                import importSVG
                importSVG.export([proj_obj], svg_path)
                print(f"SVG export completed: {svg_path}")
                
                # Close projection document
                FreeCAD.closeDocument("Projection")
                
            except Exception as e:
                print(f"Error exporting horizontal projection to SVG: {str(e)}")
                print(f"Exception type: {type(e)}")
                import traceback
                traceback.print_exc()
                return False
            
            if not os.path.exists(svg_path):
                print("Failed to create SVG file")
                return False
                
            print(f"Successfully exported to SVG: {svg_path}")
            
            # Convert SVG to PNG using ImageMagick with high quality settings
            try:
                subprocess.run([
                    'convert',
                    '-density', '300',
                    '-resize', f"{EXPORT_PARAMS['PNG_WIDTH']}x{EXPORT_PARAMS['PNG_HEIGHT']}",
                    '-background', 'white',
                    '-flatten',
                    svg_path,
                    png_path
                ], check=True)
                
                # Verify PNG was created
                if not os.path.exists(png_path):
                    print(f"Error: Failed to create PNG file at {png_path}")
                    return False
                    
                size = os.path.getsize(png_path)
                if size < 1000:
                    print(f"Error: Generated PNG file is too small ({size} bytes)")
                    return False
                    
                print(f"Successfully exported horizontal projection ({size} bytes)")
            except subprocess.CalledProcessError as e:
                print(f"Error converting SVG to PNG: {str(e)}")
                return False
            
            if not os.path.exists(svg_path):
                print("Failed to create SVG file")
                return False
                
            print(f"Successfully exported to SVG: {svg_path}")
            
            # Convert SVG to PNG using ImageMagick
            try:
                subprocess.run([
                    'convert',
                    '-density', '300',
                    '-resize', '2048x1536',
                    '-background', 'white',
                    '-flatten',
                    svg_path,
                    png_path
                ], check=True)
                
                # Clean up SVG file
                os.remove(svg_path)
                
                # Verify export
                if not os.path.exists(png_path):
                    print(f"Error: Failed to create PNG file at {png_path}")
                    return False
                
                size = os.path.getsize(png_path)
                if size < 1000:
                    print(f"Error: Generated PNG file is too small ({size} bytes)")
                    return False
                
                print(f"Successfully exported horizontal projection ({size} bytes)")
                # Continue with next projection
            except subprocess.CalledProcessError as e:
                print(f"Error converting SVG to PNG: {str(e)}")
                return False
            except Exception as e:
                print(f"Error during horizontal projection export: {str(e)}")
                return False
        
        # Export detail drawings (1:10)
        print("\nExporting detail drawings...")
        try:
            detail_objects = [obj for obj in doc.Objects if "Detail" in obj.Name]
            view = create_drawing(doc, "Details", detail_objects, EXPORT_PARAMS['SCALE_DETAIL'])
            if not view:
                print("Error: Failed to create detail drawings view")
                return False
                
            # Set up export paths
            png_path = os.path.join(screenshot_dir, "detail_drawings.png")
            brep_path = os.path.join(temp_dir, "details.brp")
            svg_path = png_path.replace('.png', '.svg')
        except Exception as e:
            print(f"Error setting up detail drawings: {str(e)}")
            return False
            
            doc.recompute()
            
            # Export directly to SVG using Part module
            svg_path = png_path.replace('.png', '.svg')
            print(f"Exporting detail drawings to SVG: {svg_path}")
            
            try:
                # Export shape directly to SVG using Part module
                import Part
                print(f"Shape type: {type(view.Shape)}")
                print(f"Shape valid: {view.Shape.isValid()}")
                print(f"Shape faces: {len(view.Shape.Faces)}")
                print(f"Shape edges: {len(view.Shape.Edges)}")
                
                # Create projection
                proj = Part.makeProjection(view.Shape.Edges, FreeCAD.Vector(0,0,1))
                if not proj:
                    print("Failed to create projection")
                    return False
                
                # Create a new document for the projection
                proj_doc = FreeCAD.newDocument("Projection")
                proj_obj = proj_doc.addObject("Part::Feature", "Projection")
                proj_obj.Shape = proj[0]
                proj_doc.recompute()
                
                # Export to SVG
                import importSVG
                importSVG.export([proj_obj], svg_path)
                print(f"SVG export completed: {svg_path}")
                
                # Close projection document
                FreeCAD.closeDocument("Projection")
                
            except Exception as e:
                print(f"Error exporting detail drawings to SVG: {str(e)}")
                print(f"Exception type: {type(e)}")
                import traceback
                traceback.print_exc()
                return False
            
            if not os.path.exists(svg_path):
                print("Failed to create SVG file")
                return False
                
            print(f"Successfully exported to SVG: {svg_path}")
            
            # Convert SVG to PNG using ImageMagick with high quality settings
            try:
                subprocess.run([
                    'convert',
                    '-density', '300',
                    '-resize', f"{EXPORT_PARAMS['PNG_WIDTH']}x{EXPORT_PARAMS['PNG_HEIGHT']}",
                    '-background', 'white',
                    '-flatten',
                    svg_path,
                    png_path
                ], check=True)
                
                # Verify PNG was created
                if not os.path.exists(png_path):
                    print(f"Error: Failed to create PNG file at {png_path}")
                    return False
                    
                size = os.path.getsize(png_path)
                if size < 1000:
                    print(f"Error: Generated PNG file is too small ({size} bytes)")
                    return False
                    
                print(f"Successfully exported detail drawings ({size} bytes)")
            except subprocess.CalledProcessError as e:
                print(f"Error converting SVG to PNG: {str(e)}")
                return False
            
            if not os.path.exists(svg_path):
                print("Failed to create SVG file")
                return False
                
            print(f"Successfully exported to SVG: {svg_path}")
            
            # Convert SVG to PNG using ImageMagick
            try:
                subprocess.run([
                    'convert',
                    '-density', '300',
                    '-resize', '2048x1536',
                    '-background', 'white',
                    '-flatten',
                    svg_path,
                    png_path
                ], check=True)
                
                # Clean up SVG file
                os.remove(svg_path)
                
                # Verify export
                if not os.path.exists(png_path):
                    print(f"Error: Failed to create PNG file at {png_path}")
                    return False
                
                size = os.path.getsize(png_path)
                if size < 1000:
                    print(f"Error: Generated PNG file is too small ({size} bytes)")
                    return False
                
                print(f"Successfully exported detail drawings ({size} bytes)")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error converting SVG to PNG: {str(e)}")
                return False
            except Exception as e:
                print(f"Error during detail drawings export: {str(e)}")
                return False
        
        print("\nDrawings exported successfully")
        return True
        
    except Exception as e:
        print(f"Error exporting drawings: {str(e)}")
        return False

if __name__ == "__main__":
    if export_drawings():
        print("\nAll drawings exported successfully")
        sys.exit(0)
    else:
        print("\nError exporting drawings")
        sys.exit(1)
