import ezdxf

def verify_drawing_scale(doc, drawing_name):
    """Verify scale of a single drawing"""
    print(f"\nChecking {drawing_name}...")
    msp = doc.modelspace()
    dimensions = list(msp.query('DIMENSION'))
    
    if not dimensions:
        print(f"Warning: No dimensions found in {drawing_name}")
        return False
    
    scale_verified = False
    for dim in dimensions:
        # Get dimension measurement
        p1 = dim.get_dxf_attrib('defpoint', (0,0,0))
        p2 = dim.get_dxf_attrib('defpoint4', None)  # Try defpoint4 for actual endpoint
        if not p2:
            p2 = dim.get_dxf_attrib('defpoint2', None)  # Fallback to defpoint2
        
        if p2:
            # Calculate actual measurement in drawing units
            actual = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5
            
            # Get dimension style
            dimstyle = doc.dimstyles.get(dim.get_dxf_attrib('dimstyle', '50'))
            if dimstyle:
                # Get scale factor from style
                scale = dimstyle.dxf.dimscale
                
                # Get dimension text
                text = dim.get_dxf_attrib('text', '')
                if not text:  # If no override text, use measurement
                    text = str(int(actual * scale))
                else:
                    # Clean up text
                    text = text.replace('<>', '').replace('mm', '').strip()
                
                try:
                    value = float(text)
                    print(f"Dimension found:")
                    print(f"- Text value: {text}mm")
                    print(f"- Actual measurement: {actual:.1f}")
                    print(f"- Scale factor: {scale:.1f}")
                    print(f"- Calculated scale: 1:{value/actual:.1f}")
                    
                    # Verify scale is 1:50 (within tolerance)
                    if abs(value/actual - 50) <= 1:
                        print(f"✓ Scale verified: 1:50")
                        scale_verified = True
                    else:
                        print(f"✗ Warning: Scale {value/actual:.0f} differs from required 1:50")
                except ValueError:
                    continue
    
    return scale_verified

def check_dxf_scale():
    """Verify that DXF files are at 1:50 scale"""
    print("Checking DXF files for 1:50 scale...")
    
    # Check horizontal projection
    doc_h = ezdxf.readfile('dist/drawings/projections/horizontal_projection.dxf')
    h_verified = verify_drawing_scale(doc_h, "horizontal projection")
    
    # Check vertical projection
    doc_v = ezdxf.readfile('dist/drawings/projections/vertical_projection.dxf')
    v_verified = verify_drawing_scale(doc_v, "vertical projection")
    
    return h_verified and v_verified

if __name__ == "__main__":
    check_dxf_scale()
