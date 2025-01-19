#!/usr/bin/python3
import os
import sys

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

try:
    import FreeCAD
    import TechDraw
    print("FreeCAD Version:", FreeCAD.Version())
    
    # Create test document and page
    doc = FreeCAD.newDocument("TestDoc")
    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    page.Template = template
    
    # Get detailed property information
    print("\nChecking ProjectionType property...")
    
    # Try different methods to get enumeration values
    print("Method 1: Direct property access")
    try:
        prop = page.getPropertyByName("ProjectionType")
        print("Property type:", type(prop))
        print("Property dir:", dir(prop))
        if hasattr(prop, "getEnumeration"):
            valid_values = prop.getEnumeration()
            print("Valid values:", valid_values)
    except Exception as e:
        print("Error:", str(e))
    
    print("\nMethod 2: Property info")
    try:
        prop_info = page.PropertiesList
        print("All properties:", prop_info)
        if "ProjectionType" in prop_info:
            print("Current ProjectionType value:", page.ProjectionType)
    except Exception as e:
        print("Error:", str(e))
    
    print("\nMethod 3: Try setting different values")
    test_values = ["First", "FIRST", "Third", "THIRD", "Document", "DOCUMENT"]
    for value in test_values:
        try:
            page.ProjectionType = value
            print(f"Successfully set ProjectionType to: {value}")
        except Exception as e:
            print(f"Failed to set ProjectionType to {value}: {str(e)}")
            
    print("\nMethod 4: Property documentation")
    try:
        doc_str = page.getDocumentationOfProperty("ProjectionType")
        print("Property documentation:", doc_str)
    except Exception as e:
        print("Error getting documentation:", str(e))
    
except Exception as e:
    print("Error:", str(e))
    print("Exception type:", type(e))
    sys.exit(1)
