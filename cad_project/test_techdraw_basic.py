#!/usr/bin/python3
import os
import sys
import traceback

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
    print("Importing FreeCAD...")
    import FreeCAD
    print("FreeCAD Version:", FreeCAD.Version())
    
    print("\nImporting Part...")
    import Part
    print("Part module imported successfully")
    
    print("\nImporting TechDraw...")
    import TechDraw
    print("TechDraw module imported successfully")
    
    print("\nCreating test document...")
    doc = FreeCAD.newDocument("TestDoc")
    
    print("\nCreating simple shape...")
    box = Part.makeBox(100, 100, 100)
    obj = doc.addObject("Part::Feature", "Box")
    obj.Shape = box
    
    print("\nCreating TechDraw page...")
    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    
    print("\nSetting up template...")
    template_path = os.path.join(os.path.dirname(FreeCAD.getResourceDir()),
                               "Mod", "TechDraw", "Templates", "A3_Landscape_blank.svg")
    print("Template path:", template_path)
    template.Template = template_path
    page.Template = template
    
    print("\nCreating view...")
    view = doc.addObject('TechDraw::DrawViewPart', 'View')
    page.addView(view)
    view.Source = obj
    view.Scale = 1
    view.Direction = FreeCAD.Vector(0,0,1)
    view.X = 148.5
    view.Y = 210.0
    
    print("\nRecomputing document...")
    doc.recompute()
    
    print("\nChecking page ViewObject...")
    if hasattr(page, 'ViewObject'):
        print("Page has ViewObject")
        if hasattr(page.ViewObject, 'save'):
            print("ViewObject has save method")
        else:
            print("ViewObject does not have save method")
            print("Available ViewObject attributes:", dir(page.ViewObject))
    else:
        print("Page does not have ViewObject")
        print("Available page attributes:", dir(page))
    
    print("\nTrying to export...")
    export_path = "/home/ubuntu/cad_project/exports/temp/test.svg"
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    try:
        page.ViewObject.save(export_path)
        print(f"Successfully exported to {export_path}")
    except Exception as e:
        print(f"Error during export: {str(e)}")
        print("Exception details:")
        traceback.print_exc()
    
    print("\nTest completed")
    
except Exception as e:
    print(f"\nError: {str(e)}")
    print("Exception details:")
    traceback.print_exc()
    sys.exit(1)
