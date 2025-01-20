import sys

def check_dependencies():
    required_modules = ['FreeCAD', 'Draft', 'Part', 'importDXF']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f'Successfully imported {module}')
        except ImportError as e:
            missing_modules.append(module)
            print(f'Failed to import {module}: {e}')
    
    if missing_modules:
        print('\nMissing required modules:', ', '.join(missing_modules))
        return False
    
    print('\nAll required modules are available')
    return True

if __name__ == '__main__':
    success = check_dependencies()
    sys.exit(0 if success else 1)
