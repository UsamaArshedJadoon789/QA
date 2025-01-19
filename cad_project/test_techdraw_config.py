#!/usr/bin/env python3
import os
import sys

# Set environment variables
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['COIN_GL_NO_WINDOW'] = '1'

try:
    import FreeCAD
    import TechDraw
    
    print('\nFreeCAD paths:')
    print('\n'.join(sys.path))
    
    print('\nFreeCAD Version:', FreeCAD.Version())
    
    # Check TechDraw templates
    template_dir = os.path.join(FreeCAD.getResourceDir(), 'Mod', 'TechDraw', 'Templates')
    print('\nTechDraw templates directory:', template_dir)
    
    print('\nAvailable templates:')
    if os.path.exists(template_dir):
        templates = os.listdir(template_dir)
        for template in templates:
            print(f"- {template}")
    else:
        print('Template directory not found')
        
    # Test TechDraw functionality
    print('\nTesting TechDraw functionality:')
    doc = FreeCAD.newDocument('TechDrawTest')
    
    # Create a test page
    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    
    # Try to load a template
    template_file = os.path.join(template_dir, 'A3_Landscape_blank.svg')
    if os.path.exists(template_file):
        template.Template = template_file
        print(f"Template loaded: {template_file}")
    else:
        print(f"Template not found: {template_file}")
    
    page.Template = template
    
    # Create a simple shape
    import Part
    box = Part.makeBox(10, 10, 10)
    shape = doc.addObject("Part::Feature", "Box")
    shape.Shape = box
    
    # Create view
    view = doc.addObject('TechDraw::DrawViewPart', 'View')
    page.addView(view)
    view.Source = shape
    
    doc.recompute()
    
    print('\nTechDraw test completed successfully')
    
except Exception as e:
    print('\nError:', str(e))
    print('Exception type:', type(e))
    sys.exit(1)
