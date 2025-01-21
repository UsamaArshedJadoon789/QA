import os
import fitz  # PyMuPDF
from PIL import Image
import io
import struct  # For unpacking pHYs chunk data

def analyze_pdf_content(pdf_path):
    """Analyze PDF content including text and images"""
    print("Performing comprehensive PDF verification...")
    doc = fitz.open(pdf_path)
    
    # Enhanced section tracking with page numbers and multiple patterns
    required_sections = {
        "Building Specifications": {"found": False, "page": None, "patterns": ["Building Specifications", "I. BUILDING SPECIFICATIONS"]},
        "Material Properties": {"found": False, "page": None, "patterns": ["Material Properties", "II. MATERIAL PROPERTIES"]},
        "Design Strength": {"found": False, "page": None, "patterns": ["Design Strength", "III. DESIGN STRENGTH"]},
        "Load Analysis": {"found": False, "page": None, "patterns": ["Load Analysis", "III.2 Load Analysis"]},
        "Structural Analysis": {"found": False, "page": None, "patterns": ["IV. STRUCTURAL ANALYSIS", "Structural Analysis"]},
        "Thermal Analysis": {"found": False, "page": None, "patterns": ["V. THERMAL ANALYSIS", "Thermal Analysis"]},
        "Cross-Section Analysis": {"found": False, "page": None, "patterns": ["Cross-Section Analysis", "4.2 Cross-Section Analysis"]},
        "Ultimate Limit State": {"found": False, "page": None, "patterns": ["Ultimate Limit State", "4.3 Ultimate Limit State"]}
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
        
        # Check sections with page tracking and multiple patterns
        for section, info in required_sections.items():
            if not info["found"]:  # Only check if not already found
                for pattern in info["patterns"]:
                    if pattern in text or pattern.upper() in text:  # Case-insensitive check
                        info["found"] = True
                        info["page"] = page_num + 1
                        print(f"\nFound section '{section}' on page {page_num + 1} (matched: {pattern})")
                        break
                
        # Verify margins and spacing using cropbox and mediabox
        mediabox = page.mediabox
        cropbox = page.cropbox
        
        # Calculate margins by analyzing content placement
        # Get all content boxes (text and images)
        content_areas = []
        for block in page.get_text("dict")["blocks"]:
            bbox = block.get("bbox", [])
            if bbox:
                content_areas.append(bbox)
        
        # Add image areas
        for img in page.get_images():
            for rect in page.get_image_rects(img[0]):
                content_areas.append((rect.x0, rect.y0, rect.x1, rect.y1))
        
        if content_areas:
            # Find content boundaries
            content_left = min(area[0] for area in content_areas)
            content_right = max(area[2] for area in content_areas)
            content_bottom = min(area[1] for area in content_areas)
            content_top = max(area[3] for area in content_areas)
            
            # Calculate margins relative to page size (A4: 595 x 842 points)
            margin_left = content_left
            margin_right = 595 - content_right
            margin_bottom = content_bottom
            margin_top = 842 - content_top
        else:
            # Default to 0 if no content found
            margin_left = margin_right = margin_top = margin_bottom = 0
        
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
    pdf_path = "output/documentation/structural_analysis_report.pdf"
    if os.path.exists(pdf_path):
        analyze_pdf_content(pdf_path)
    else:
        print(f"Error: PDF file not found at {pdf_path}")
