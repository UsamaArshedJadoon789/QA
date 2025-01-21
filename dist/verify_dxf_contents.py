import os
import ezdxf

def verify_dxf_contents():
    """Verify contents of DXF files"""
    dxf_files = []
    # Check projections
    proj_dir = 'dist/drawings/projections'
    dxf_files.extend([os.path.join(proj_dir, f) for f in os.listdir(proj_dir) if f.endswith('.dxf')])
    
    # Check details
    details_dir = 'dist/drawings/details'
    dxf_files.extend([os.path.join(details_dir, f) for f in os.listdir(details_dir) if f.endswith('.dxf')])
    
    for dxf_file in dxf_files:
        print(f"\n=== {dxf_file} ===")
        doc = ezdxf.readfile(dxf_file)
        msp = doc.modelspace()
        
        # Count entities
        entities = list(msp)
        dimensions = list(msp.query('DIMENSION'))
        lines = list(msp.query('LINE'))
        polylines = list(msp.query('LWPOLYLINE'))
        
        print(f"Total entities: {len(entities)}")
        print(f"Dimensions: {len(dimensions)}")
        print(f"Lines: {len(lines)}")
        print(f"Polylines: {len(polylines)}")
        
        # Check dimension properties
        if dimensions:
            print("\nDimension Properties:")
            for i, dim in enumerate(dimensions, 1):
                text = dim.get_dxf_attrib('text', '')
                if not text:
                    text = getattr(dim.dxf, 'text', '')
                if not text:
                    text = dim.get_dxf_attrib('dimtext', '')
                print(f"Dimension {i} - Text: {text}")

if __name__ == "__main__":
    verify_dxf_contents()
