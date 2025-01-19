#!/usr/bin/env python3
import os
import sys
import subprocess

def test_platform(platform):
    """Test FreeCAD with specific Qt platform"""
    print(f"\nTesting Qt platform: {platform}")
    
    # Set environment variables
    os.environ['DISPLAY'] = ''
    os.environ['QT_QPA_PLATFORM'] = platform
    os.environ['COIN_GL_NO_WINDOW'] = '1'
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
        print("FreeCAD imported successfully")
        print("FreeCAD version:", FreeCAD.Version())
        
        # Create test document
        doc = FreeCAD.newDocument('TestDoc')
        print("Document created successfully")
        
        # Try to create a simple shape
        import Part
        box = Part.makeBox(10, 10, 10)
        obj = doc.addObject("Part::Feature", "Box")
        obj.Shape = box
        print("Shape created successfully")
        
        # Try to export
        doc.saveAs("/home/ubuntu/cad_project/test.FCStd")
        print("File saved successfully")
        return True
        
    except Exception as e:
        print(f"Error with {platform}:", str(e))
        print("Exception type:", type(e))
        return False

def main():
    # Test all available platforms
    platforms = ['offscreen', 'minimal', 'minimalegl', 'eglfs', 'linuxfb', 'vnc']
    results = {}
    
    for platform in platforms:
        results[platform] = test_platform(platform)
    
    # Print summary
    print("\nResults Summary:")
    print("-" * 40)
    for platform, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{platform:12} : {status}")

if __name__ == "__main__":
    main()
