#!/usr/bin/env python3
import os
import subprocess
import sys

def create_scad_file(dxf_path, output_name, scale):
    """Create OpenSCAD file for rendering"""
    scad_content = f'''
    scale([{scale}, {scale}, 1])
    linear_extrude(height=0.1)
    import(file="../{dxf_path}", layer="0");
    '''
    
    scad_file = f"exports/screenshots/{output_name}.scad"
    os.makedirs(os.path.dirname(scad_file), exist_ok=True)
    with open(scad_file, 'w') as f:
        f.write(scad_content)
    return scad_file

def render_drawing(dxf_path, output_name, scale_factor):
    """Render DXF to PNG using OpenSCAD with xvfb"""
    try:
        # Create output directory
        os.makedirs("exports/screenshots", exist_ok=True)
        
        # Create OpenSCAD file
        scad_file = create_scad_file(dxf_path, output_name, scale_factor)
        output_png = f"exports/screenshots/{output_name}.png"
        
        # Render using OpenSCAD with xvfb-run
        cmd = [
            'xvfb-run',
            '--auto-servernum',
            '--server-args=-screen 0 2048x1536x24',
            'openscad',
            '-o', output_png,
            '--imgsize=2048,1536',
            '--projection=ortho',
            '--colorscheme=Tomorrow Night',
            '--camera=0,0,0,0,0,0,500',  # Fixed camera position
            scad_file
        ]
        
        print(f"Rendering {output_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Generated: {output_png}")
            return True
        else:
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error rendering {output_name}: {str(e)}")
        return False

def main():
    drawings = [
        ("dataset5_vertical.dxf", "vertical_projection", 1.0),
        ("dataset5_horizontal.dxf", "horizontal_projection", 1.0),
        ("dataset5_details.dxf", "detail_drawings", 5.0)  # Larger scale for details
    ]
    
    success = True
    for dxf_path, name, scale in drawings:
        full_path = os.path.join("exports", dxf_path)
        if os.path.exists(full_path):
            if not render_drawing(full_path, name, scale):
                success = False
        else:
            print(f"DXF file not found: {full_path}")
            success = False
    
    return success

if __name__ == "__main__":
    if main():
        print("\nAll drawings rendered successfully")
    else:
        print("\nSome drawings failed to render")
        sys.exit(1)
