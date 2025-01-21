import ezdxf
from PIL import Image, ImageDraw, PngImagePlugin
import math
import os
import struct
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def dxf_to_png(dxf_path, png_path, scale=1.0):
    """Convert DXF to PNG with proper scaling and 300 DPI"""
    try:
        # Load DXF
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        
        # Initialize bounds
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        # Track whether we found any entities
        entities_found = False
        
        # Process all entity types
        for entity in msp:
            try:
                if entity.dxftype() == "LINE":
                    start = entity.dxf.start
                    end = entity.dxf.end
                    min_x = min(min_x, start[0], end[0])
                    min_y = min(min_y, start[1], end[1])
                    max_x = max(max_x, start[0], end[0])
                    max_y = max(max_y, start[1], end[1])
                    entities_found = True
                    
                elif entity.dxftype() == "LWPOLYLINE":
                    for point in entity.get_points():
                        min_x = min(min_x, point[0])
                        min_y = min(min_y, point[1])
                        max_x = max(max_x, point[0])
                        max_y = max(max_y, point[1])
                    entities_found = True
                    
                elif entity.dxftype() == "CIRCLE":
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    min_x = min(min_x, center[0] - radius)
                    min_y = min(min_y, center[1] - radius)
                    max_x = max(max_x, center[0] + radius)
                    max_y = max(max_y, center[1] + radius)
                    entities_found = True
                    
                elif entity.dxftype() in ["TEXT", "MTEXT"]:
                    pos = entity.dxf.insert
                    min_x = min(min_x, pos[0])
                    min_y = min(min_y, pos[1])
                    max_x = max(max_x, pos[0])
                    max_y = max(max_y, pos[1])
                    entities_found = True
                    
                elif entity.dxftype() == "DIMENSION":
                    defpoints = [
                        entity.dxf.defpoint,
                        entity.dxf.defpoint2,
                        entity.dxf.defpoint3,
                        entity.dxf.defpoint4
                    ]
                    for point in defpoints:
                        if point:
                            min_x = min(min_x, point[0])
                            min_y = min(min_y, point[1])
                            max_x = max(max_x, point[0])
                            max_y = max(max_y, point[1])
                    entities_found = True
                    
            except Exception as e:
                print(f"Warning: Could not process entity {entity.dxftype()}: {e}")
                continue
        
        if not entities_found:
            print(f"Error: No valid entities found in {dxf_path}")
            return False
            
        # Add margin and handle infinite bounds
        margin = 500
        if min_x == float('inf'):
            min_x = -margin
        if min_y == float('inf'):
            min_y = -margin
        if max_x == float('-inf'):
            max_x = margin
        if max_y == float('-inf'):
            max_y = margin
            
        min_x -= margin
        min_y -= margin
        max_x += margin
        max_y += margin
        
        print(f"Drawing bounds: ({min_x}, {min_y}) -> ({max_x}, {max_y})")
        
        # Calculate dimensions with minimum size guarantee
        width = max(1000, int((max_x - min_x) * scale))
        height = max(1000, int((max_y - min_y) * scale))
        
        # Create image with white background
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        
        # Define transform function to map DXF coordinates to image coordinates
        def transform_point(x, y):
            img_x = int((x - min_x) * scale)
            img_y = height - int((y - min_y) * scale)  # Flip Y axis
            return img_x, img_y
        
        # Track whether anything was actually drawn
        elements_drawn = 0
        
        # Draw entities with error handling
        for entity in msp:
            try:
                if entity.dxftype() == "LINE":
                    start = entity.dxf.start
                    end = entity.dxf.end
                    x1, y1 = transform_point(start[0], start[1])
                    x2, y2 = transform_point(end[0], end[1])
                    draw.line([(x1, y1), (x2, y2)], fill="black", width=2)
                    elements_drawn += 1
                    
                elif entity.dxftype() == "LWPOLYLINE":
                    points = []
                    for point in entity.get_points():
                        x, y = transform_point(point[0], point[1])
                        points.append((x, y))
                    if points:
                        draw.line(points + [points[0]], fill="black", width=2)
                        elements_drawn += 1
                        
                elif entity.dxftype() == "CIRCLE":
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    cx, cy = transform_point(center[0], center[1])
                    r = int(radius * scale)
                    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline="black", width=2)
                    elements_drawn += 1
                    
                elif entity.dxftype() in ["TEXT", "MTEXT"]:
                    pos = entity.dxf.insert if entity.dxftype() == "TEXT" else entity.dxf.insert
                    text = entity.dxf.text if entity.dxftype() == "TEXT" else entity.text
                    x, y = transform_point(pos[0], pos[1])
                    draw.text((x, y), text, fill="black")
                    elements_drawn += 1
                    
                elif entity.dxftype() == "ARC":
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    start_angle = math.radians(entity.dxf.start_angle)
                    end_angle = math.radians(entity.dxf.end_angle)
                    cx, cy = transform_point(center[0], center[1])
                    r = int(radius * scale)
                    bbox = [cx-r, cy-r, cx+r, cy+r]
                    draw.arc(bbox, -math.degrees(end_angle), -math.degrees(start_angle), fill="black", width=2)
                    elements_drawn += 1
                    
                elif entity.dxftype() == "DIMENSION":
                    # Draw dimension lines
                    if hasattr(entity, "geometry"):
                        for line in entity.geometry.lines:
                            start = line.start
                            end = line.end
                            x1, y1 = transform_point(start[0], start[1])
                            x2, y2 = transform_point(end[0], end[1])
                            draw.line([(x1, y1), (x2, y2)], fill="black", width=2)
                            elements_drawn += 1
                    
            except Exception as e:
                print(f"Warning: Could not draw entity: {e}")
                continue
        
        if elements_drawn == 0:
            print(f"Error: No elements were drawn for {dxf_path}")
            return False
            
        # Create high quality output with proper DPI metadata
        # Calculate physical size for 300 DPI
        physical_width = width / 300 * 25.4  # mm
        physical_height = height / 300 * 25.4  # mm
        
        # Add DPI information
        dpi = (300, 300)
        ppm = int(300 / 25.4 * 1000)  # pixels per meter
        
        # Create PNG info with physical size metadata
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text('dpi', f'{dpi[0]},{dpi[1]}')
        
        # Pack pHYs data as big-endian
        phys_data = struct.pack('>IIB', ppm, ppm, 1)
        pnginfo.add(b'pHYs', phys_data)
        
        # Save with all metadata
        img.save(png_path, "PNG", 
                dpi=dpi,
                pnginfo=pnginfo,
                optimize=True,
                quality=95)
        
        print(f"Generated {png_path} ({width}x{height} px @ {dpi[0]} DPI)")
        return True
        
    except Exception as e:
        print(f"Error converting {dxf_path}: {str(e)}")
        return False

def main():
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert DXF files to PNG with high DPI')
    parser.add_argument('--input', required=True, help='Input DXF file path')
    parser.add_argument('--output', required=True, help='Output PNG file path')
    parser.add_argument('--dpi', type=int, default=300, help='Output DPI (default: 300)')
    parser.add_argument('--scale', type=float, default=0.8, help='Scale factor (default: 0.8)')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Verify input file exists
    if not os.path.exists(args.input):
        print(f"\nError: Input file not found: {args.input}")
        return False
    
    try:
        # Convert drawing with proper scaling for high quality output
        print(f"\nConverting {os.path.basename(args.input)}...")
        success = dxf_to_png(args.input, args.output, scale=args.scale)
        
        if success and os.path.exists(args.output):
            print(f"\nSuccessfully generated: {args.output}")
            return True
        else:
            print(f"\nError: Failed to generate output file: {args.output}")
            return False
            
    except Exception as e:
        print(f"\nError during conversion: {str(e)}")
        return False

if __name__ == "__main__":
    main()
