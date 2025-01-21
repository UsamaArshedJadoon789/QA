import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import math

def create_projections():
    """Create DXF files with vertical and horizontal projections at 1:50 scale"""
    # Create new DXF document
    doc = ezdxf.new('R2010')
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Create dimension style for 1:50 scale
    dimstyle = doc.dimstyles.new('50')
    dimstyle.dxf.dimscale = 50.0
    dimstyle.dxf.dimlfac = 50.0
    dimstyle.dxf.dimrnd = 1
    dimstyle.dxf.dimpost = '<>'  # Standard dimension text format without units
    dimstyle.dxf.dimtxt = 50
    dimstyle.dxf.dimasz = 50
    dimstyle.dxf.dimclrd = 256  # Dimension line color (black)
    dimstyle.dxf.dimclre = 256  # Extension line color (black)
    dimstyle.dxf.dimgap = 25    # Gap from dimension line to text
    dimstyle.dxf.dimexe = 50    # Extension line extension
    dimstyle.dxf.dimexo = 25    # Extension line offset
    dimstyle.dxf.dimtad = 1     # Text above dimension line
    dimstyle.dxf.dimzin = 8     # Suppress trailing zeros
    
    # Dataset 5 specifications
    width = 7200
    length1 = 6600
    length2 = 10800
    height1 = 2500
    height2 = 2650
    angle = 16  # degrees
    spacing = 1100
    ground_level = -1400
    
    # Create horizontal projection
    # Main outline
    points = [(0, 0), (length1, 0), (length1, width), (0, width), (0, 0)]
    msp.add_lwpolyline(points)
    
    # Add dimensions
    msp.add_linear_dim(
        base=(0, -200),
        p1=(0, 0),
        p2=(length1, 0),
        dimstyle='50',
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    msp.add_linear_dim(
        base=(-200, 0),
        p1=(0, 0),
        p2=(0, width),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    # Add rafters
    rafter_count = int(length1 / spacing) + 1
    for i in range(rafter_count):
        pos = i * spacing
        if pos <= length1:
            points = [(pos, 0), (pos+200, 0), (pos+200, width), (pos, width), (pos, 0)]
            msp.add_lwpolyline(points)
    
    # Add text annotations
    text = msp.add_text(
        'Rafter spacing: 1100mm',
        dxfattribs={'height': 100, 'style': 'Standard'}
    )
    text.set_placement((length1/2, -500), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # Save horizontal projection
    doc.saveas('dist/drawings/projections/horizontal_projection.dxf')
    
    # Create new document for vertical projection
    doc = ezdxf.new('R2010')
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Add dimension style
    dimstyle = doc.dimstyles.new('50')
    dimstyle.dxf.dimscale = 50.0
    dimstyle.dxf.dimlfac = 50.0
    dimstyle.dxf.dimrnd = 1
    dimstyle.dxf.dimpost = '<>'  # Standard dimension text format without units
    dimstyle.dxf.dimtxt = 50
    dimstyle.dxf.dimasz = 50
    dimstyle.dxf.dimclrd = 256
    dimstyle.dxf.dimclre = 256
    dimstyle.dxf.dimgap = 25
    dimstyle.dxf.dimexe = 50
    dimstyle.dxf.dimexo = 25
    dimstyle.dxf.dimtad = 1
    dimstyle.dxf.dimzin = 8
    
    # Main outline
    points = [
        (0, ground_level),
        (0, height1),
        (width, height2),
        (width, ground_level),
        (0, ground_level)
    ]
    msp.add_lwpolyline(points)
    
    # Add dimensions
    msp.add_linear_dim(
        base=(-200, ground_level),
        p1=(0, ground_level),
        p2=(0, height1),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    msp.add_linear_dim(
        base=(width+200, ground_level),
        p1=(width, ground_level),
        p2=(width, height2),
        dimstyle='50',
        angle=90,
        override={'dimscale': 50, 'dimlfac': 50}
    ).render()
    
    # Add roof angle annotation
    angle_text = f'Roof angle: {angle}°'
    text = msp.add_text(
        angle_text,
        dxfattribs={'height': 100, 'style': 'Standard'}
    )
    text.set_placement((width/2, height2+200), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # Add ground level annotation
    ground_text = 'Ground level: -1.4 m.a.s.l'
    text = msp.add_text(
        ground_text,
        dxfattribs={'height': 100, 'style': 'Standard'}
    )
    text.set_placement((0, ground_level-200), align=TextEntityAlignment.LEFT)
    
    # Save vertical projection
    doc.saveas('dist/drawings/projections/vertical_projection.dxf')

if __name__ == "__main__":
    import os
    os.makedirs('dist/drawings/projections', exist_ok=True)
    create_projections()
