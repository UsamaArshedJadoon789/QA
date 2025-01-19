#!/usr/bin/env python3
from PIL import Image
import os
import subprocess

def standardize_image(input_path, output_path=None):
    """Standardize image to HD resolution (2048x1536) with 300 DPI"""
    if output_path is None:
        output_path = input_path
        
    # Open and resize image
    with Image.open(input_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to exact HD resolution
        img_resized = img.resize((2048, 1536), Image.Resampling.LANCZOS)
        
        # Save with 300 DPI resolution
        dpi_value = 300
        
        # Save initial version with PIL
        img_resized.save(output_path, 'PNG', dpi=(dpi_value, dpi_value))
        
        try:
            # Use ImageMagick to properly set DPI metadata
            subprocess.run([
                'convert',
                output_path,
                '-units', 'PixelsPerInch',
                '-density', str(dpi_value),
                '-set', 'units', 'PixelsPerInch',
                '-set', 'resolution', f'{dpi_value}x{dpi_value}',
                output_path
            ], check=True, capture_output=True, text=True)
            
            # Verify DPI setting
            result = subprocess.run([
                'identify',
                '-format', '%x',
                output_path
            ], check=True, capture_output=True, text=True)
            
            actual_dpi = float(result.stdout.strip())
            print(f"Standardized {input_path} -> {output_path} ({actual_dpi} DPI)")
            
        except subprocess.CalledProcessError as e:
            print(f"Warning: Error setting DPI metadata: {e.stderr}")
            print(f"Standardized {input_path} -> {output_path} (DPI metadata may be incorrect)")

def main():
    # Directory containing screenshots
    screenshot_dir = "/home/ubuntu/cad_project/enhanced_exports/screenshots"
    
    # Process all PNG files
    for filename in os.listdir(screenshot_dir):
        if filename.endswith('.png'):
            input_path = os.path.join(screenshot_dir, filename)
            standardize_image(input_path)

if __name__ == "__main__":
    main()
