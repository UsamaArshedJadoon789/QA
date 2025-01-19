#!/usr/bin/python3
import os
import sys
import subprocess
import math

# Set up FreeCAD environment for headless operation
os.environ.update({
    'DISPLAY': '',
    'QT_QPA_PLATFORM': 'offscreen',
    'FREECAD_LIB': '/usr/lib/freecad/lib',
    'PYTHONPATH': '/usr/lib/freecad-python3/lib:/usr/lib/freecad/lib:/usr/lib/python3/dist-packages',
    'COIN_GL_NO_WINDOW': '1',
    'LIBGL_ALWAYS_SOFTWARE': '1',
    'GALLIUM_DRIVER': 'llvmpipe',
    'MESA_GL_VERSION_OVERRIDE': '3.3',
    'MESA_GLSL_VERSION_OVERRIDE': '330',
    'QT_QPA_FONTDIR': '/usr/share/fonts/truetype',
    'QT_QPA_PLATFORM_PLUGIN_PATH': '/usr/lib/x86_64-linux-gnu/qt5/plugins',
    'FREECAD_USER_DATA': '/home/ubuntu/.FreeCAD',
    'PYTHONPATH': '/usr/lib/freecad-python3/lib:/usr/lib/freecad/lib:/usr/lib/python3/dist-packages:/usr/share/freecad-python3:/usr/lib/freecad/Mod',
    'FREECAD_ALLOW_OPENGL_RENDER': '1'
})

# Add FreeCAD paths
freecad_paths = [
    '/usr/lib/freecad-python3/lib',
    '/usr/lib/freecad/lib',
    '/usr/share/freecad/Mod',
    '/usr/lib/python3/dist-packages',
    '/usr/share/freecad-python3',
    '/usr/lib/freecad/Mod',
    '/usr/lib/freecad/Ext',
    '/usr/share/freecad-python3/Mod',
    '/usr/lib/freecad-python3/Ext'
]

for path in freecad_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

print("\nImporting FreeCAD modules...")

try:
    # Import core modules
    import FreeCAD
    print("FreeCAD Version:", FreeCAD.Version())
    
    # Import and initialize GUI
    try:
        import FreeCADGui
        FreeCADGui.showMainWindow()
        FreeCADGui.activateWorkbench("DraftWorkbench")
        print("GUI system initialized")
    except Exception as e:
        print(f"Warning: GUI initialization failed: {str(e)}")
        print("Continuing without GUI...")
        
    # Initialize Draft workbench
    try:
        import Draft
        Draft.init()
        print("Draft workbench initialized")
    except Exception as e:
        print(f"Warning: Draft initialization failed: {str(e)}")
    
    # Add module paths
    additional_paths = [
        '/usr/lib/freecad/Mod/AttachmentEditor',
        '/usr/share/freecad/Mod/AttachmentEditor',
        '/usr/lib/freecad-python3/Mod/AttachmentEditor',
        '/usr/lib/freecad/Mod/TechDraw',
        '/usr/share/freecad/Mod/TechDraw',
        '/usr/lib/freecad-python3/Mod/TechDraw',
        '/usr/lib/freecad/Mod/Import',
        '/usr/share/freecad/Mod/Import',
        '/usr/lib/freecad-python3/Mod/Import',
        '/usr/lib/freecad/Mod/Draft',
        '/usr/share/freecad/Mod/Draft',
        '/usr/lib/freecad-python3/Mod/Draft'
    ]
    
    for path in additional_paths:
        if os.path.exists(path) and path not in sys.path:
            sys.path.append(path)
            print(f"Added path: {path}")
            
    # Try importing required modules
    try:
        import Draft
        print("Draft module imported")
    except Exception as e:
        print(f"Warning: Draft import failed: {str(e)}")
        
    try:
        import TechDraw
        print("TechDraw module imported")
    except Exception as e:
        print(f"Warning: TechDraw import failed: {str(e)}")
        
    print("Module initialization completed")
    
    # Import Part module
    import Part
    print("Part module imported")
    
    # Import TechDraw
    import TechDraw
    print("TechDraw module imported")
    
    # Test Part functionality
    test_doc = FreeCAD.newDocument("PartTest")
    box = Part.makeBox(10, 10, 10)
    if box.isValid():
        print("Part functionality verified")
    FreeCAD.closeDocument("PartTest")
    
    # Configure parameters
    print("\nConfiguring FreeCAD parameters...")
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part").SetFloat("MeshDeviation", 0.1)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw").SetBool("ShowUnits", True)
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw").SetBool("HiddenLineStyle", 1)
    
    print("FreeCAD environment initialized successfully\n")
    
    print("Imported modules:", ['FreeCAD', 'FreeCADGui', 'Part', 'TechDraw'])
    
except ImportError as e:
    print(f"\nError importing FreeCAD modules: {e}")
    print("Python path:", sys.path)
    sys.exit(1)
except Exception as e:
    print(f"\nError during initialization: {e}")
    print("Python path:", sys.path)
    sys.exit(1)

import Part  # Add Part import at module level

def create_svg_from_shape(doc, shape, svg_path, scale=1.0, projection_vector=FreeCAD.Vector(0,0,1)):
    """Create SVG file using Part projection and direct SVG generation"""
    try:
        # Get shape for projection
        working_shape = shape.Shape if hasattr(shape, 'Shape') else shape
        
        print("\nChecking source shape...")
        print(f"Shape type: {type(working_shape)}")
        print(f"Shape valid: {working_shape.isValid()}")
        print(f"Shape faces: {len(working_shape.Faces)}")
        print(f"Shape edges: {len(working_shape.Edges)}")
        
        # Create TechDraw page and template
        print("\nCreating TechDraw page...")
        page = doc.addObject('TechDraw::DrawPage', 'Page')
        template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
        
        # Set up template
        template_path = os.path.join(os.path.dirname(FreeCAD.getResourceDir()),
                                   "Mod", "TechDraw", "Templates", "A3_Landscape_blank.svg")
        if not os.path.exists(template_path):
            template_path = "/usr/share/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg"
        template.Template = template_path
        page.Template = template
        
        # Create source shape
        print("Creating source shape...")
        shape_obj = doc.addObject("Part::Feature", "SourceShape")
        shape_obj.Shape = working_shape
        doc.recompute()
        
        # Create TechDraw view
        print("Creating TechDraw view...")
        view = doc.addObject('TechDraw::DrawViewPart', 'View')
        page.addView(view)
        
        # Set view properties
        view.Source = shape_obj
        view.Direction = projection_vector
        view.Scale = scale
        view.ScaleType = "Custom"
        view.Perspective = False
        view.Focus = 0
        view.IsoCount = 0
        view.SmoothVisible = False
        view.SeamVisible = True
        view.HardHidden = False
        
        # Position view on page
        view.X = 148.5  # Half of A3 width
        view.Y = 210.0  # Half of A3 height
        
        doc.recompute()
        
        # Export using Part module directly
        print("\nExporting using Part module...")
        try:
            # Set up view properties
            view.Source = shape  # Direct shape assignment
            view.Direction = FreeCAD.Vector(0,0,1)  # Top view
            view.Scale = scale
            view.ScaleType = "Custom"
            view.Perspective = False
            
            # Force view update
            print("Computing view...")
            doc.recompute()
            view.recompute()
            
            # Wait for view to be ready
            import time
            max_attempts = 5
            for attempt in range(max_attempts):
                if hasattr(view, 'Shape') and view.Shape and view.Shape.Edges:
                    print(f"View ready after {attempt + 1} attempts")
                    break
                print(f"Waiting for view to compute (attempt {attempt + 1}/{max_attempts})...")
                time.sleep(1)
                doc.recompute()
                view.recompute()
            
            # Get edges from view
            visible_edges = []
            if hasattr(view, 'Shape') and view.Shape:
                print("Using view's computed shape")
                visible_edges.extend(view.Shape.Edges)
            else:
                print("Falling back to direct shape projection")
                # Get the actual shape geometry
                working_shape = shape.Shape if hasattr(shape, 'Shape') else shape
                print(f"Working shape type: {type(working_shape)}")
                print(f"Working shape faces: {len(working_shape.Faces)}")
                
                # Create 2D projection using Part.Section
                try:
                    print("\nCreating 2D projection using Part.Section...")
                    
                    # Create an infinite plane at z=0
                    plane = Part.makePlane(1000, 1000,  # Large enough to cover the shape
                                         FreeCAD.Vector(-500, -500, 0),  # Centered at origin
                                         FreeCAD.Vector(0, 0, 1))  # Normal vector
                    
                    # Create section
                    section = working_shape.section(plane)
                    if section and section.Edges:
                        visible_edges.extend(section.Edges)
                        print(f"Added {len(section.Edges)} edges from section")
                        
                        # Scale edges if needed
                        if scale != 1.0:
                            scaled_edges = []
                            for edge in visible_edges:
                                scaled = edge.copy()
                                scaled.scale(scale)
                                scaled_edges.append(scaled)
                            visible_edges = scaled_edges
                            print(f"Scaled {len(visible_edges)} edges by factor {scale}")
                    else:
                        print("No edges found in section")
                        print(f"Section type: {type(section)}")
                        print(f"Section properties: {dir(section)}")
                    
                except Exception as e:
                    print(f"Error during section creation: {str(e)}")
                    print("Exception details:")
                    import traceback
                    traceback.print_exc()
                        
                print(f"Collected {len(visible_edges)} edges from projection")
            
            if not visible_edges:
                print("Error: No visible edges found in view")
                return False
            
            # Create document for export
            print(f"\nCreating document for {len(visible_edges)} edges...")
            export_doc = FreeCAD.newDocument("ExportDoc")
            
            try:
                # Create compound and add to document
                compound = Part.makeCompound(visible_edges)
                obj = export_doc.addObject("Part::Feature", "Projection")
                obj.Shape = compound
                obj.Label = "2D Projection"
                export_doc.recompute()
                
                # Export to SVG using Part module directly
                print(f"Exporting to SVG: {svg_path}")
                try:
                    # Get edges from shape
                    edges = obj.Shape.Edges
                    
                    # Calculate bounding box for scaling
                    bbox = obj.Shape.BoundBox
                    margin = 50  # pixels
                    width, height = 2048, 1536
                    
                    # Calculate scale to fit drawing in viewBox with margins
                    scale_x = (width - 2*margin) / (bbox.XLength or 1)
                    scale_y = (height - 2*margin) / (bbox.YLength or 1)
                    scale = min(scale_x, scale_y)
                    
                    # Calculate offset to center drawing
                    offset_x = (width - bbox.XLength * scale) / 2 - bbox.XMin * scale
                    offset_y = (height - bbox.YLength * scale) / 2 - bbox.YMin * scale
                    
                    # Create SVG content
                    svg_content = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
                                 '<svg xmlns="http://www.w3.org/2000/svg" version="1.1"',
                                 f'     width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                                 '<g stroke="black" stroke-width="1" fill="none">']
                    
                    # Convert edges to SVG paths with proper scaling
                    for edge in edges:
                        points = []
                        for vertex in edge.Vertexes:
                            x = vertex.X * scale + offset_x
                            y = height - (vertex.Y * scale + offset_y)  # Flip Y coordinate
                            points.append(f"{x:.1f},{y:.1f}")
                        path = f'M {points[0]} L {points[1]}'
                        svg_content.append(f'<path d="{path}"/>')
                    
                    svg_content.append('</g></svg>')
                    
                    # Write SVG file
                    with open(svg_path, 'w') as f:
                        f.write('\n'.join(svg_content))
                    
                    size = os.path.getsize(svg_path)
                    print(f"SVG file created: {size} bytes")
                    FreeCAD.closeDocument("ExportDoc")
                    return True
                    
                except Exception as e:
                    print(f"Error creating SVG: {str(e)}")
                    FreeCAD.closeDocument("ExportDoc")
                    return False
            except Exception as e:
                print(f"Error during SVG export: {str(e)}")
                if "ExportDoc" in FreeCAD.listDocuments():
                    FreeCAD.closeDocument("ExportDoc")
                return False
                
        except Exception as e:
            print(f"Error exporting to SVG: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        # Scale if needed
        if scale != 1.0:
            proj_obj.Shape.scale(scale)
        
        doc.recompute()
        
        print(f"\nProjection created with {len(proj_obj.Shape.Edges)} edges")
        
        # Create TechDraw page
        print("\nCreating TechDraw page...")
        page = doc.addObject('TechDraw::DrawPage', 'Page')
        template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
        
        # Find template
        template_paths = [
            "/usr/share/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg",
            "/usr/lib/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg",
            os.path.join(os.path.dirname(FreeCAD.getResourceDir()),
                        "Mod", "TechDraw", "Templates", "A3_Landscape_blank.svg")
        ]
        
        template_found = False
        for template_path in template_paths:
            if os.path.exists(template_path):
                print(f"Using template: {template_path}")
                template.Template = template_path
                page.Template = template
                template_found = True
                break
        
        if not template_found:
            print("Error: Could not find TechDraw template")
            return False
        
        # Create view
        view = doc.addObject('TechDraw::DrawViewPart', 'View')
        page.addView(view)
        
        # Set view properties
        view.Source = proj_obj
        view.Direction = FreeCAD.Vector(0,0,1)  # Top view for projected shape
        view.Scale = 1.0  # Already scaled in projection
        view.ScaleType = "Custom"
        view.X = 148.5  # Center on page
        view.Y = 210.0
        
        doc.recompute()
        
        # Export using Draft module
        print("\nExporting to SVG...")
        import Draft
        Draft.export([proj_obj], svg_path)
        
        if os.path.exists(svg_path):
            size = os.path.getsize(svg_path)
            print(f"SVG file created: {size} bytes")
            return True
        else:
            print("Failed to create SVG file")
            return False
            
    except Exception as e:
        print(f"Error in create_svg_from_shape: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
            
    except Exception as e:
        print(f"Error creating TechDraw page: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
            
        # Create TechDraw page
        print("\nCreating TechDraw page...")
        page = doc.addObject('TechDraw::DrawPage', 'Page')
        template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
        
        # Use blank template
        template_paths = [
            os.path.join(os.path.dirname(FreeCAD.getResourceDir()),
                        "Mod", "TechDraw", "Templates", "A3_Landscape_blank.svg"),
            "/usr/share/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg",
            "/usr/lib/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg"
        ]
        
        template_found = False
        for template_path in template_paths:
            if os.path.exists(template_path):
                print(f"Using template: {template_path}")
                template.Template = template_path
                page.Template = template
                template_found = True
                break
                
        if not template_found:
            print("Error: Could not find TechDraw template")
            return False
        
        # Create view
        view = doc.addObject('TechDraw::DrawViewPart', 'View')
        page.addView(view)
        
        # Set view properties
        view.Source = shape  # Use the input shape directly
        view.Direction = projection_vector
        view.Scale = scale
        view.ScaleType = "Custom"
        view.Perspective = False  # Orthographic projection
        view.Focus = 0  # Auto focus
        view.IsoCount = 0  # No isometric lines
        view.SmoothVisible = False  # Don't smooth visible lines
        view.SeamVisible = True  # Show seam lines
        view.HardHidden = False  # Don't show hidden lines
        
        print("\nChecking source shape...")
        print(f"Shape type: {type(working_shape)}")
        print(f"Shape valid: {working_shape.isValid()}")
        print(f"Shape faces: {len(working_shape.Faces)}")
        print(f"Shape edges: {len(working_shape.Edges)}")
        
        # Create projection using Draft module
        print("\nCreating projection with vector:", projection_vector)
        
        # Create temporary object for shape
        temp_obj = doc.addObject("Part::Feature", "TempObject")
        temp_obj.Shape = working_shape
        
        # Try different methods to create 2D view
        print("Creating 2D view...")
        import Draft
        
        # Method 1: Try makeShapeView2D
        try:
            print("Trying Draft.makeShapeView2D...")
            proj_obj = Draft.makeShapeView2D(temp_obj, projection_vector)
        except Exception as e1:
            print(f"makeShapeView2D failed: {str(e1)}")
            try:
                # Method 2: Try Draft.makeShape2DView
                print("Trying Draft.makeShape2DView...")
                proj_obj = Draft.makeShape2DView(temp_obj, projection_vector)
            except Exception as e2:
                print(f"makeShape2DView failed: {str(e2)}")
                try:
                    # Method 3: Use Part projection
                    print("Trying Part projection...")
                    # Get the shape to project
                    shape_to_project = temp_obj if isinstance(temp_obj, Part.Shape) else temp_obj.Shape
                    # Create projection
                    edges = [edge for edge in shape_to_project.Edges]
                    projection = Part.makeProjection(edges, projection_vector)[0]
                    proj_obj = doc.addObject("Part::Feature", "Projection")
                    proj_obj.Shape = projection
                except Exception as e3:
                    print(f"Part projection failed: {str(e3)}")
                    return False
        
        if not proj_obj or not hasattr(proj_obj, 'Shape'):
            print("Error: Failed to create 2D view")
            return False
            
        # Scale if needed
        if scale != 1.0:
            print(f"Scaling projection by {scale}")
            proj_obj.Scale = scale
        
        doc.recompute()
        
        print("\nProjection created successfully")
        print(f"Projection valid: {proj_obj.Shape.isValid()}")
        print(f"Projection edges: {len(proj_obj.Shape.Edges)}")
        
        if not proj_obj.Shape.Edges:
            print("Error: No edges in projection")
            return False
                    
        # Create TechDraw page and template
        print("\nCreating TechDraw page...")
        page = doc.addObject('TechDraw::DrawPage', 'Page')
        template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
        
        # Use blank template
        template_paths = [
            os.path.join(os.path.dirname(FreeCAD.getResourceDir()),
                        "Mod", "TechDraw", "Templates", "A3_Landscape_blank.svg"),
            "/usr/share/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg",
            "/usr/lib/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg"
        ]
                    
        # Find template
        template_found = False
        for template_path in template_paths:
            if os.path.exists(template_path):
                print(f"Using template: {template_path}")
                template.Template = template_path
                page.Template = template
                template_found = True
                break
                
        if not template_found:
            print("Error: Could not find TechDraw template")
            return False
                    
        # Set up view properties
        view.Source = proj_obj
        view.Direction = FreeCAD.Vector(0,0,1)  # Top view for projected shape
        view.Scale = scale
        view.ScaleType = "Custom"
        view.Perspective = False  # Orthographic projection
        view.Focus = 0  # Auto focus
        view.IsoCount = 0  # No isometric lines
        view.SmoothVisible = False  # Don't smooth visible lines
        view.SeamVisible = True  # Show seam lines
        view.HardHidden = False  # Don't show hidden lines
        
        # Center view on page (A3 dimensions)
        view.X = 148.5  # Half of A3 width (297mm)
        view.Y = 210.0  # Half of A3 height (420mm)
        
        # Update document
        doc.recompute()
        
        # Export page to SVG
        try:
            # Try multiple export methods
            svg_content = None
            
            # Method 1: Try ViewObject.save
            if hasattr(page.ViewObject, 'save'):
                try:
                    print("\nTrying ViewObject.save method...")
                    page.ViewObject.save(svg_path)
                    if os.path.exists(svg_path):
                        with open(svg_path, 'r') as f:
                            svg_content = f.read()
                        print("Got content using ViewObject.save")
                except Exception as e:
                    print(f"ViewObject.save failed: {str(e)}")
            
            # Method 2: Try Draft export
            if not svg_content:
                try:
                    print("\nTrying Draft export method...")
                    import Draft
                    Draft.export([proj_obj], svg_path)
                    if os.path.exists(svg_path):
                        with open(svg_path, 'r') as f:
                            svg_content = f.read()
                        print("Got content using Draft export")
                except Exception as e:
                    print(f"Draft export failed: {str(e)}")
            
            if not svg_content:
                print("Failed to get SVG content using any method")
                return False
            
            # Write SVG content
            with open(svg_path, 'w') as f:
                f.write(svg_content)
            print(f"SVG file created: {os.path.getsize(svg_path)} bytes")
            return True
            
        except Exception as e:
            print(f"Error exporting to SVG: {str(e)}")
            return False
        
        print("\nChecking view after recompute...")
        if hasattr(view, 'Shape'):
            print(f"View shape type: {type(view.Shape)}")
            print(f"View shape valid: {view.Shape.isValid()}")
            print(f"View shape faces: {len(view.Shape.Faces)}")
            print(f"View shape edges: {len(view.Shape.Edges)}")
        else:
            print("View has no Shape property")
            
        print("\nAvailable view properties:", dir(view))
        
        # Clean up and return
        return True
            
    except Exception as e:
        print(f"Error creating TechDraw page: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
            
    # End of create_svg_from_shape function

def convert_svg_to_png(svg_path, png_path):
    """Convert SVG to PNG using ImageMagick with high quality settings"""
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
        
        if os.path.exists(png_path):
            size = os.path.getsize(png_path)
            if size < 1000:
                print(f"Warning: PNG file is small ({size} bytes)")
                return False
            print(f"PNG file created: {size} bytes")
            return True
        else:
            print("Failed to create PNG file")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error converting to PNG: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def export_drawing(doc, objects, name, scale, projection_vector):
    """Export a drawing with given objects and settings"""
    print(f"\nExporting {name}...")
    print(f"Scale: 1:{int(1/scale)}")
    print(f"Projection vector: {projection_vector}")
    print(f"Number of objects: {len(objects)}")
    try:
        # Create compound from shapes
        shapes = []
        print(f"\nProcessing {len(objects)} objects for {name}...")
        for obj in objects:
            if hasattr(obj, 'Shape'):
                print(f"Adding shape from {obj.Name}")
                print(f"Shape type: {type(obj.Shape)}")
                print(f"Shape valid: {obj.Shape.isValid()}")
                print(f"Shape faces: {len(obj.Shape.Faces)}")
                print(f"Shape edges: {len(obj.Shape.Edges)}")
                shapes.append(obj.Shape)
        
        if not shapes:
            print("No valid shapes found")
            return False
            
        # Create compound using Part.makeCompound
        print("\nCreating compound shape...")
        compound_shape = Part.makeCompound(shapes)
        
        # Create compound object
        compound = doc.addObject("Part::Feature", f"Compound_{name}")
        compound.Shape = compound_shape
        doc.recompute()
        
        print(f"\nChecking compound...")
        print(f"Compound valid: {compound_shape.isValid()}")
        print(f"Compound faces: {len(compound_shape.Faces)}")
        print(f"Compound edges: {len(compound_shape.Edges)}")
        
        # Set up paths
        export_dir = "/home/ubuntu/cad_project/exports"
        screenshot_dir = os.path.join(export_dir, "screenshots")
        temp_dir = os.path.join(export_dir, "temp")
        os.makedirs(screenshot_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        
        svg_path = os.path.join(temp_dir, f"{name}.svg")
        png_path = os.path.join(screenshot_dir, f"{name}.png")
        
        # Create SVG using TechDraw
        if not create_svg_from_shape(doc, compound, svg_path, scale, projection_vector):
            return False
            
        # Convert to PNG
        if not convert_svg_to_png(svg_path, png_path):
            return False
            
        # Clean up SVG
        if os.path.exists(svg_path):
            os.remove(svg_path)
            
        # Verify PNG was created with proper size
        if os.path.exists(png_path):
            size = os.path.getsize(png_path)
            if size < 1000:
                print(f"Warning: Generated PNG file is too small ({size} bytes)")
                return False
            print(f"Successfully exported {name} ({size} bytes)")
            return True
        else:
            print(f"Error: Failed to create PNG file at {png_path}")
            return False
        
    except Exception as e:
        print(f"Error exporting {name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    try:
        print("\nStarting drawing export...")
        
        # Create test document
        doc = FreeCAD.newDocument("TestDoc")
        
        # Create vertical projection shapes
        # Wall
        wall = doc.addObject("Part::Feature", "Wall")
        wall.Shape = Part.makeBox(220, 2500, 10)  # 220mm thick, 2.5m high
        
        # Column
        column = doc.addObject("Part::Feature", "Column")
        column.Shape = Part.makeBox(150, 2500, 150)  # 150x150mm column, 2.5m high
        
        # Roof (triangular face)
        roof_points = [
            FreeCAD.Vector(0, 2500, 0),
            FreeCAD.Vector(3600, 3000, 0),  # Peak at center
            FreeCAD.Vector(7200, 2500, 0)
        ]
        roof_wire = Part.makePolygon(roof_points + [roof_points[0]])
        roof_face = Part.Face(Part.Wire(roof_wire))
        roof = doc.addObject("Part::Feature", "Roof")
        roof.Shape = roof_face
        
        # Export vertical projection (1:50)
        if not export_drawing(doc, [wall, column, roof], "vertical_projection", 1/50, FreeCAD.Vector(0,0,1)):
            return False
        
        # Create horizontal projection shapes
        # Building outline
        outline = doc.addObject("Part::Feature", "Building")
        outline.Shape = Part.makeBox(7200, 10800, 10)  # Full building footprint
        
        # Purlins
        purlins = []
        spacing = 1100  # 1.1m spacing
        for i in range(int(10800/spacing)):
            purlin = doc.addObject("Part::Feature", f"Purlin_{i}")
            y_pos = i * spacing
            purlin.Shape = Part.makeBox(7200, 100, 160, FreeCAD.Vector(0, y_pos, 0))
            purlins.append(purlin)
        
        # Export horizontal projection (1:50)
        if not export_drawing(doc, [outline] + purlins, "horizontal_projection", 1/50, FreeCAD.Vector(0,1,0)):
            return False
        
        # Create detail drawing shapes
        # Column-foundation connection detail
        detail = doc.addObject("Part::Feature", "Detail")
        base = Part.makeBox(500, 500, 500)  # Base block
        bolt = Part.makeCylinder(25, 200)  # Bolt representation
        detail.Shape = base.fuse(bolt)
        
        # Export detail drawings (1:10)
        if not export_drawing(doc, [detail], "detail_drawings", 1/10, FreeCAD.Vector(0,0,1)):
            return False
        
        print("\nAll drawings exported successfully")
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if main():
        print("\nExport completed successfully")
        sys.exit(0)
    else:
        print("\nExport failed")
        sys.exit(1)
