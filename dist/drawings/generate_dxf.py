import ezdxf
import math
from ezdxf import units
from pathlib import Path

class DXFGenerator:
    def __init__(self):
        # Dataset 5 specifications (all dimensions in mm for 1:50 scale)
        self.width = 7200
        self.length1 = 6600
        self.length2 = 10800
        self.height1 = 2500
        self.height2 = 2650
        self.angle = 16
        self.spacing = 1100
        self.ground_level = -1400
        
        # Scale factor (1:50)
        self.scale = 50
        
        # Create new DXF document
        self.doc = ezdxf.new('R2010')
        self.doc.units = units.MM  # Set units to millimeters
        self.msp = self.doc.modelspace()
        
    def create_horizontal_projection(self):
        """Create horizontal projection (top view) DXF file"""
        # Create new DXF document for horizontal projection
        doc = ezdxf.new('R2010')
        doc.units = units.MM
        msp = doc.modelspace()
        
        # Main outline
        points = [(0, 0), (self.length1, 0), (self.length1, self.width), (0, self.width), (0, 0)]
        msp.add_lwpolyline(points)
        
        # Add rafters (200mm wide)
        rafter_count = int(self.length1 / self.spacing) + 1
        for i in range(rafter_count):
            x = i * self.spacing
            if x <= self.length1:
                # Draw rafter centerline
                msp.add_line((x, 0), (x, self.width))
                # Draw rafter width (100mm each side)
                msp.add_line((x-100, 0), (x-100, self.width))
                msp.add_line((x+100, 0), (x+100, self.width))
        
        # Add purlins (150mm wide)
        purlin_spacing = 1500  # 1.5m spacing
        purlin_count = int(self.width / purlin_spacing) + 1
        for i in range(purlin_count):
            y = i * purlin_spacing
            if y <= self.width:
                # Draw purlin centerline
                msp.add_line((0, y), (self.length1, y))
                # Draw purlin width (75mm each side)
                msp.add_line((0, y-75), (self.length1, y-75))
                msp.add_line((0, y+75), (self.length1, y+75))
        
        # Add dimensions with actual measurements
        # Create text style
        doc.styles.new('DIMENSION')
        
        # Create and configure dimension style
        dimstyle = doc.dimstyles.new('50')
        # Basic dimension settings
        dimstyle.dxf.dimscale = 50.0
        dimstyle.dxf.dimasz = 100
        dimstyle.dxf.dimtxt = 100
        dimstyle.dxf.dimexe = 50
        dimstyle.dxf.dimexo = 25
        # Text settings
        dimstyle.dxf.dimtxsty = 'DIMENSION'  # Set text style
        dimstyle.dxf.dimtad = 1  # Text above line
        dimstyle.dxf.dimtoh = 0  # Text horizontal
        dimstyle.dxf.dimjust = 0  # Text centered
        # Color settings
        dimstyle.dxf.dimclrt = 7  # Text color
        dimstyle.dxf.dimclrd = 7  # Dimension line color
        dimstyle.dxf.dimclre = 7  # Extension line color
        # Line settings
        dimstyle.dxf.dimsd1 = 1  # First arrow
        dimstyle.dxf.dimsd2 = 1  # Second arrow
        dimstyle.dxf.dimse1 = 1  # First extension line
        dimstyle.dxf.dimse2 = 1  # Second extension line
        dimstyle.dxf.dimtofl = 1  # Force text outside if no fit
        # Number settings
        dimstyle.dxf.dimdsep = 46  # Decimal separator
        dimstyle.dxf.dimzin = 0  # Zero suppression
        dimstyle.dxf.dimdec = 0  # Decimal places
        dimstyle.dxf.dimpost = '<> mm'  # Units suffix with required placeholder

        # Add dimensions with explicit measurements
        # Width dimension
        width_dim = msp.add_linear_dim(
            base=(0, -500),
            p1=(0, 0),
            p2=(self.length1, 0),
            dimstyle='50',
            text=str(self.length1),  # Explicit measurement
            override={
                'dimscale': 50,
                'dimtxt': 100,
                'dimasz': 100,
                'dimclrt': 7,
                'dimtad': 1,
                'dimtoh': 0,
                'dimexe': 50,
                'dimexo': 25,
                'dimjust': 0,
                'dimpost': ' mm',
                'dimzin': 0,  # Suppress leading/trailing zeros
                'dimdec': 0,  # No decimal places
                'dimrnd': 1,  # Round to nearest mm
                'dimlfac': 50,  # Scale factor for linear dimensions
                'dimtix': 0,  # Force text inside
                'dimtofl': 1,  # Force text outside if it doesn't fit
                'dimgap': 50,  # Text gap
                'dimtfill': 0  # No text background
            }
        )
        
        # Height dimension
        msp.add_linear_dim(
            base=(-500, 0),
            p1=(0, 0),
            p2=(0, self.width),
            dimstyle='50',
            text=f"{self.width}",
            angle=90,
            override={
                'dimscale': 50,
                'dimtxt': 100,
                'dimasz': 100,
                'dimclrt': 7,
                'dimclrd': 7,
                'dimclre': 7,
                'dimtad': 1,
                'dimtoh': 0,
                'dimexe': 50,
                'dimexo': 25,
                'dimtix': 1,
                'dimtmove': 0,
                'dimjust': 0,
                'dimsd1': 1,
                'dimsd2': 1,
                'dimse1': 1,
                'dimse2': 1,
                'dimtofl': 1,
                'dimdsep': 46,
                'dimzin': 0,
                'dimtol': 0,
                'dimupt': 0,
                'dimtxt': 100,
                'dimasz': 100,
                'dimclrt': 7,
                'dimtad': 1,
                'dimtoh': 0,
                'dimexe': 50,
                'dimexo': 25,
                'dimjust': 0,
                'dimdsep': 46,
                'dimzin': 0,
                'dimdec': 0,
                'dimlfac': 1.0,
                'dimpost': ' mm'
            }
        )
        
        # Save the DXF file with proper scale
        doc.header['$MEASUREMENT'] = 1
        doc.header['$LUNITS'] = 2
        doc.header['$INSUNITS'] = 4
        doc.header['$DIMSCALE'] = 50.0
        doc.saveas('horizontal_projection.dxf')
        
    def create_vertical_projection(self):
        """Create vertical projection (side view) DXF file"""
        # Create new DXF document for vertical projection
        doc = ezdxf.new('R2010')
        doc.units = units.MM
        msp = doc.modelspace()
        
        # Create dimension style for 1:50 scale
        dimstyle = doc.dimstyles.new('50')
        # Basic dimension settings
        dimstyle.dxf.dimscale = 50.0
        dimstyle.dxf.dimlfac = 1.0
        dimstyle.dxf.dimrnd = 1
        dimstyle.dxf.dimpost = '<> mm'  # Use placeholder for actual measurement
        dimstyle.dxf.dimtxt = 100
        dimstyle.dxf.dimasz = 100
        dimstyle.dxf.dimexe = 50
        dimstyle.dxf.dimexo = 25
        # Text settings
        dimstyle.dxf.dimtad = 1  # Text above line
        dimstyle.dxf.dimtoh = 0  # Text horizontal
        dimstyle.dxf.dimjust = 0  # Text centered
        dimstyle.dxf.dimgap = 25  # Text gap
        # Color settings
        dimstyle.dxf.dimclrt = 7  # Text color (white)
        dimstyle.dxf.dimclrd = 7  # Dimension line color
        dimstyle.dxf.dimclre = 7  # Extension line color
        # Line settings
        dimstyle.dxf.dimsd1 = 1  # First arrow
        dimstyle.dxf.dimsd2 = 1  # Second arrow
        dimstyle.dxf.dimse1 = 1  # First extension line
        dimstyle.dxf.dimse2 = 1  # Second extension line
        dimstyle.dxf.dimtofl = 1  # Force text outside if no fit
        dimstyle.dxf.dimtsz = 0  # Size for dimension line terminators
        # Number settings
        dimstyle.dxf.dimdsep = 46  # Decimal separator
        dimstyle.dxf.dimzin = 0  # Zero suppression
        dimstyle.dxf.dimdec = 0  # Decimal places
        dimstyle.dxf.dimtfill = 0  # No background
        
        # Main outline
        points = [
            (0, self.ground_level),
            (0, self.height1),
            (self.width, self.height2),
            (self.width, self.ground_level),
            (0, self.ground_level)
        ]
        msp.add_lwpolyline(points)
        
        # Add columns (200mm wide)
        column_spacing = 2000  # 2m spacing
        column_count = int(self.width / column_spacing) + 1
        for i in range(column_count):
            x = i * column_spacing
            if x <= self.width:
                h = self.height1 + (x/self.width)*(self.height2-self.height1)
                # Draw column centerline
                msp.add_line((x, self.ground_level), (x, h))
                # Draw column width (100mm each side)
                msp.add_line((x-100, self.ground_level), (x-100, h))
                msp.add_line((x+100, self.ground_level), (x+100, h))
        
        # Add thermal insulation layer (200mm thick)
        insulation_thickness = 200
        insulation_points = [
            (0, self.height1),
            (self.width, self.height2),
            (self.width, self.height2-insulation_thickness),
            (0, self.height1-insulation_thickness),
            (0, self.height1)
        ]
        msp.add_lwpolyline(insulation_points)
        # Add hatching for insulation
        msp.add_hatch(color=3).paths.add_polyline_path(insulation_points, is_closed=True)
        
        # Add rafters in side view (200mm deep)
        angle_rad = math.radians(self.angle)
        rafter_count = int(self.width / self.spacing) + 1
        for i in range(rafter_count):
            x = i * self.spacing
            if x <= self.width:
                h = self.height1 + (x/self.width)*(self.height2-self.height1)
                # Draw rafter outline
                rafter_points = [
                    (x-100, h),
                    (x+100, h),
                    (x+100, h-200),
                    (x-100, h-200),
                    (x-100, h)
                ]
                msp.add_lwpolyline(rafter_points)
        
        # Add vertical dimensions with explicit measurements
        # Height dimension
        height_dim = msp.add_linear_dim(
            base=(-500, 0),
            p1=(0, self.ground_level),
            p2=(0, self.height1),
            dimstyle='50',
            text=str(abs(self.height1)),  # Explicit measurement, absolute value
            angle=90,
            override={
                'dimscale': 50,
                'dimtxt': 100,
                'dimasz': 100,
                'dimclrt': 7,
                'dimtad': 1,
                'dimtoh': 0,
                'dimexe': 50,
                'dimexo': 25,
                'dimjust': 0,
                'dimpost': ' mm',
                'dimzin': 0,  # Suppress leading/trailing zeros
                'dimdec': 0,  # No decimal places
                'dimrnd': 1,  # Round to nearest mm
                'dimlfac': 50,  # Scale factor for linear dimensions
                'dimtix': 0,  # Force text inside
                'dimtofl': 1,  # Force text outside if it doesn't fit
                'dimgap': 50,  # Text gap
                'dimtfill': 0  # No text background
            }
        )
        
        # Width dimension
        width_dim = msp.add_linear_dim(
            base=(self.width + 500, 0),
            p1=(self.width, self.ground_level),
            p2=(self.width, self.height2),
            dimstyle='50',
            text=str(self.width),  # Explicit measurement
            angle=90,
            override={
                'dimscale': 50,
                'dimtxt': 100,
                'dimasz': 100,
                'dimclrt': 7,
                'dimtad': 1,
                'dimtoh': 0,
                'dimexe': 50,
                'dimexo': 25,
                'dimjust': 0,
                'dimpost': ' mm',
                'dimzin': 0,  # Suppress leading/trailing zeros
                'dimdec': 0,  # No decimal places
                'dimrnd': 1,  # Round to nearest mm
                'dimlfac': 50,  # Scale factor for linear dimensions
                'dimtix': 0,  # Force text inside
                'dimtofl': 1,  # Force text outside if it doesn't fit
                'dimgap': 50,  # Text gap
                'dimtfill': 0  # No text background
            }
        )
        
        # Save the DXF file
        doc.saveas('vertical_projection.dxf')

    def add_dimensions(self, msp, horizontal=True):
        """Add dimensions to the drawing with proper scale"""
        # Set up dimension style for 1:50 scale
        dimstyle = self.doc.dimstyles.get('Standard')
        
        # Set dimension style variables for proper scaling
        dimstyle.dxf.dimscale = 50.0  # Overall scale factor
        dimstyle.dxf.dimlfac = 50.0   # Linear measurements scale
        dimstyle.dxf.dimrnd = 0.0     # Rounding
        dimstyle.dxf.dimzin = 0       # Zero suppression
        dimstyle.dxf.dimexe = 50.0    # Extension line size
        dimstyle.dxf.dimexo = 25.0    # Extension line offset
        dimstyle.dxf.dimasz = 100.0   # Arrow size
        dimstyle.dxf.dimtxt = 100.0   # Text size
        
        # Set drawing units and scale
        self.doc.header['$MEASUREMENT'] = 1     # Set to metric measurement
        self.doc.header['$LUNITS'] = 2         # Set to decimal
        self.doc.header['$INSUNITS'] = 4       # Set to millimeters
        self.doc.header['$DIMSCALE'] = 50.0    # Global dimension scale
        self.doc.header['$DIMLFAC'] = 50.0     # Global linear scale
        self.doc.header['$DIMALT'] = 0         # Disable alternate units
        self.doc.header['$DIMTIX'] = 1         # Force text inside
        
        if horizontal:
            # Add width dimension with actual measurements
            dim1 = msp.add_linear_dim(
                base=(0, -500),
                p1=(0, 0),
                p2=(self.length1, 0),
                override={
                    'dimscale': 50,
                    'measurement_scale': 1.0/50,
                    'dimrnd': 1,
                    'dimpost': '<> mm'
                }
            ).render()
            
            # Add length dimension with actual measurements
            dim2 = msp.add_linear_dim(
                base=(self.length1 + 500, 0),
                p1=(self.length1, 0),
                p2=(self.length1, self.width),
                angle=90,
                override={
                    'dimscale': 50,
                    'measurement_scale': 1.0/50,
                    'dimrnd': 1,
                    'dimpost': '<> mm'
                }
            ).render()
        else:
            # Add height dimensions with actual measurements
            dim3 = msp.add_linear_dim(
                base=(-500, 0),
                p1=(0, self.ground_level),
                p2=(0, self.height1),
                angle=90,
                override={
                    'dimscale': 50,
                    'measurement_scale': 1.0/50,
                    'dimrnd': 1,
                    'dimpost': '<> mm'
                }
            ).render()
            
            dim4 = msp.add_linear_dim(
                base=(self.width + 500, 0),
                p1=(self.width, self.ground_level),
                p2=(self.width, self.height2),
                angle=90,
                override={
                    'dimscale': 50,
                    'measurement_scale': 1.0/50,
                    'dimrnd': 1,
                    'dimpost': '<> mm'
                }
            ).render()
            # Add angle dimension using linear dimensions instead
            dx = self.width
            dy = self.height2 - self.height1
            angle_text = f"{self.angle}°"
            
            # Create angle indicator arc
            center = (0, self.height1)
            radius = 1000
            start_angle = 0
            end_angle = math.degrees(math.atan2(dy, dx))
            
            # Draw arc for angle visualization
            msp.add_arc(
                center=center,
                radius=radius,
                start_angle=start_angle,
                end_angle=end_angle
            )
            
            # Add text for angle
            text_x = radius * math.cos(math.radians(end_angle/2))
            text_y = radius * math.sin(math.radians(end_angle/2)) + self.height1
            msp.add_text(
                angle_text,
                dxfattribs={
                    'height': 200,
                    'rotation': end_angle/2,
                    'insert': (text_x, text_y)
                }
            )

def main():
    generator = DXFGenerator()
    generator.create_horizontal_projection()
    generator.create_vertical_projection()
    
    print("DXF files generated successfully:")
    print("1. horizontal_projection.dxf")
    print("2. vertical_projection.dxf")

if __name__ == "__main__":
    main()
