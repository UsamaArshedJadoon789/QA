import os
import fitz  # PyMuPDF
from PIL import Image
import io
import struct  # For unpacking pHYs chunk data

def analyze_pdf_content(pdf_path):
    """Analyze PDF content including text and images"""
    print("Performing comprehensive PDF verification...")
    doc = fitz.open(pdf_path)
    
    # Enhanced section tracking with page numbers
    required_sections = {
        "Building Specifications": {"found": False, "page": None},
        "Material Properties": {"found": False, "page": None},
        "Design Strength": {"found": False, "page": None},
        "Load Analysis": {"found": False, "page": None},
        "Structural Analysis": {"found": False, "page": None},
        "Thermal Analysis": {"found": False, "page": None},
        "Cross-Section Analysis": {"found": False, "page": None},
        "Ultimate Limit State": {"found": False, "page": None}
    }
    
    # Track required calculations with multiple possible matches
    calculation_patterns = {
        "Momentum": ["Momentum", "moment", "M = q × l²", "maximum moment"],
        "Bending": ["Bending", "bending moment", "M = (q × l²)", "maximum moment"],
        "Building stress": ["Stress Analysis", "stress distribution", "von Mises", "combined stress"],
        "ULS verification": ["Ultimate Limit State", "ULS verification", "limit state"],
        "Actions": ["Load Analysis", "load combination", "actions", "design load"],
        "Cross section": ["Cross-Section Analysis", "section properties", "cross-sectional"],
        "Inertia": ["moment of inertia", "Movement of inertia", "second moment"],
        "Angle brace": ["Angle Brace Analysis", "brace configuration", "brace connection"],
        "Stress": ["stress", "σ", "normal stress", "shear stress"],
        "Strength": ["strength", "characteristic strength", "design strength"],
        "Thermal resistance": ["Thermal Analysis", "thermal resistance", "R = d / λ", "U-value"]
    }
    
    # Initialize calculation status
    required_calculations = {calc: False for calc in calculation_patterns.keys()}
    
    # Image quality metrics
    images_found = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Check text content
        text = page.get_text()
        
        # Check sections with page tracking
        for section in required_sections:
            if section in text:
                required_sections[section]["found"] = True
                required_sections[section]["page"] = page_num + 1
                print(f"\nFound section '{section}' on page {page_num + 1}")
                
        # Verify margins and spacing
        mediabox = page.mediabox
        margin_left = mediabox[0]
        margin_right = mediabox[2] - 595  # A4 width in points
        margin_top = mediabox[3] - 842  # A4 height in points
        margin_bottom = mediabox[1]
        
        print(f"\nPage {page_num + 1} margins:")
        print(f"Left: {margin_left:.1f} pts")
        print(f"Right: {margin_right:.1f} pts")
        print(f"Top: {margin_top:.1f} pts")
        print(f"Bottom: {margin_bottom:.1f} pts")
        
        # Check calculations with multiple possible matches
        for calc, patterns in calculation_patterns.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    required_calculations[calc] = True
                    break
        
        # Extract and analyze images
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            
            # Convert to PIL Image for analysis
            img_obj = Image.open(io.BytesIO(image_data))
            width, height = img_obj.size
            
            # Get physical size from PDF
            image_rects = page.get_image_rects(xref)
            if image_rects:
                rect = image_rects[0]  # Get the first rectangle for this image
                # Convert PDF points to inches (72 points = 1 inch)
                width_inch = rect.width / 72
                height_inch = rect.height / 72
                
                # Calculate effective DPI (pixels / physical size in inches)
                effective_dpi_w = width / width_inch
                effective_dpi_h = height / height_inch
                effective_dpi = (effective_dpi_w, effective_dpi_h)
            else:
                effective_dpi = (72, 72)  # Default if no rect found
            
            images_found.append({
                'page': page_num + 1,
                'size': (width, height),
                'physical_size': (rect.width if image_rects else 0, rect.height if image_rects else 0),
                'effective_dpi': effective_dpi
            })
    
    # Print analysis results
    print("\nDocument Analysis Results:")
    print("=========================")
    
    print("\nDocument Structure Verification:")
    print("\nRequired Sections:")
    for section, info in required_sections.items():
        status = "✓" if info["found"] else "✗"
        page_info = f"(Page {info['page']})" if info["found"] else "(Not found)"
        print(f"{section}: {status} {page_info}")
    
    print("\nRequired Calculations:")
    for calc, found in required_calculations.items():
        status = "✓" if found else "✗"
        print(f"{calc}: {status}")
    
    print("\nImages Found:")
    for idx, img in enumerate(images_found, 1):
        print(f"\nImage {idx}:")
        print(f"Page: {img['page']}")
        print(f"Size: {img['size'][0]}x{img['size'][1]} pixels")
        print(f"Physical size: {img['physical_size'][0]:.1f}x{img['physical_size'][1]:.1f} points")
        print(f"Effective DPI: {img['effective_dpi'][0]:.1f}x{img['effective_dpi'][1]:.1f}")
        if img['effective_dpi'][0] >= 290:  # Allow small margin of error
            print("HD Quality: ✓")
        else:
            print("HD Quality: ✗")

if __name__ == "__main__":
    pdf_path = "dist/documentation/structural_analysis_report.pdf"
    if os.path.exists(pdf_path):
        analyze_pdf_content(pdf_path)
    else:
        print(f"Error: PDF file not found at {pdf_path}")
