import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import math

def create_connection_details():
    """Create DXF file with connection details at 1:10 scale"""
    doc = ezdxf.new('R2010')
    doc.units = units.MM
    msp = doc.modelspace()
    
    # Create dimension style for 1:10 scale
    dimstyle = doc.dimstyles.new('10')
    dimstyle.dxf.dimscale = 10.0
    dimstyle.dxf.dimlfac = 10.0
    dimstyle.dxf.dimrnd = 1
    dimstyle.dxf.dimpost = '<>'  # Standard dimension text format without units  # Standard dimension text format
    dimstyle.dxf.dimtxt = 50
    dimstyle.dxf.dimasz = 50
    dimstyle.dxf.dimclrd = 256  # Dimension line color (black)
    dimstyle.dxf.dimclre = 256  # Extension line color (black)
    dimstyle.dxf.dimgap = 25    # Gap from dimension line to text
    dimstyle.dxf.dimexe = 50    # Extension line extension
    dimstyle.dxf.dimexo = 25    # Extension line offset
    dimstyle.dxf.dimtad = 1     # Text above dimension line
    dimstyle.dxf.dimzin = 8     # Suppress trailing zeros
    
    # Rafter-Purlin Connection Detail (1:10 scale)
    # Rafter outline
    rafter_points = [(0, 0), (200, 0), (200, 240), (0, 240), (0, 0)]
    msp.add_lwpolyline(rafter_points)
    
    # Purlin outline
    purlin_points = [(50, 240), (150, 240), (150, 390), (50, 390), (50, 240)]
    msp.add_lwpolyline(purlin_points)
    
    # Add bolt holes
    bolt_radius = 6  # 12mm diameter bolts
    msp.add_circle((75, 290), bolt_radius)
    msp.add_circle((125, 290), bolt_radius)
    
    # Add dimensions
    msp.add_linear_dim(
        base=(-50, 0),
        p1=(0, 0),
        p2=(0, 240),
        dimstyle='10',
        angle=90,
        override={'dimscale': 10, 'dimlfac': 10}
    ).render()
    
    msp.add_linear_dim(
        base=(200, -50),
        p1=(0, 0),
        p2=(200, 0),
        dimstyle='10',
        override={'dimscale': 10, 'dimlfac': 10}
    ).render()
    
    # Column-Rafter Connection Detail
    # Offset for second detail
    offset_x = 500
    
    # Column outline
    column_points = [
        (offset_x, 0),
        (offset_x + 200, 0),
        (offset_x + 200, 300),
        (offset_x, 300),
        (offset_x, 0)
    ]
    msp.add_lwpolyline(column_points)
    
    # Rafter at angle
    angle = math.radians(16)
    rafter_start = (offset_x + 200, 300)
    rafter_end = (offset_x + 200 + 300 * math.cos(angle), 300 + 300 * math.sin(angle))
    
    # Add rafter
    rafter_points = [
        rafter_start,
        rafter_end,
        (rafter_end[0], rafter_end[1] - 240 * math.cos(angle)),
        (rafter_start[0], rafter_start[1] - 240),
        rafter_start
    ]
    msp.add_lwpolyline(rafter_points)
    
    # Add steel plate
    plate_points = [
        (offset_x + 150, 250),
        (offset_x + 250, 250),
        (offset_x + 250, 350),
        (offset_x + 150, 350),
        (offset_x + 150, 250)
    ]
    msp.add_lwpolyline(plate_points)
    
    # Add bolt holes
    msp.add_circle((offset_x + 175, 275), bolt_radius)
    msp.add_circle((offset_x + 225, 275), bolt_radius)
    msp.add_circle((offset_x + 175, 325), bolt_radius)
    msp.add_circle((offset_x + 225, 325), bolt_radius)
    
    # Set proper scale in header
    doc.header['$MEASUREMENT'] = 1
    doc.header['$LUNITS'] = 2
    doc.header['$INSUNITS'] = 4
    doc.header['$DIMSCALE'] = 10.0
    
    # Save the file
    doc.saveas('connection_details.dxf')
    print("Connection details created successfully")

if __name__ == "__main__":
    create_connection_details()
