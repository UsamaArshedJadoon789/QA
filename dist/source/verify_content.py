import os
import json
from PIL import Image

def verify_content_completeness():
    """Verify that all content from PDF has been properly extracted and organized"""
    print("Verifying content completeness...")
    
    # Create output directory if it doesn't exist
    os.makedirs('output/images', exist_ok=True)
    
    # Load document structure
    document_path = 'output/document_structure.json'
    if not os.path.exists(document_path):
        # Try to create document structure
        from document_structure import create_document_structure
        document = create_document_structure()
    else:
        with open(document_path, 'r') as f:
            document = json.load(f)
    
    # Required content checklist
    required_sections = {
        "Load Analysis": False,
        "Thermal Analysis": False,
        "Technical Drawings": False,
        "Structural Details": False,
        "Calculations": False
    }
    
    required_calculations = {
        "Load Distribution": False,
        "Momentum Analysis": False,
        "Stress Analysis": False,
        "Thermal Performance": False,
        "ULS Verification": False
    }
    
    required_figures = {
        "Load Distribution": False,
        "Thermal Bridge": False,
        "Vertical Projection": False,
        "Horizontal Projection": False,
        "Construction Details": False,
        "Thermal Envelope": False,
        "Connection Details": False
    }
    
    def check_content_recursively(data, path=""):
        """Recursively check content in nested dictionary structure"""
        if isinstance(data, dict):
            # Check title and type at current level
            title = data.get('title', '')
            type_value = data.get('type', '')
            current_path = f"{path}/{title}" if path else title
            
            # Check sections by title or type
            for req_section in required_sections:
                if (req_section.lower() in title.lower() or 
                    (type_value and req_section.lower() == type_value.lower())):
                    required_sections[req_section] = True
            
            # Check calculations by type or content
            for calc in required_calculations:
                # Check by type
                if type_value and calc.lower() == type_value.lower():
                    required_calculations[calc] = True
                # Check by title
                if calc.lower() in title.lower():
                    required_calculations[calc] = True
                # Check in calculations content
                if 'calculations' in data:
                    calc_content = str(data['calculations'])
                    if calc.lower() in calc_content.lower():
                        required_calculations[calc] = True
                # Check in verification content
                if 'verification' in data:
                    verif_content = str(data['verification'])
                    if calc.lower() in verif_content.lower():
                        required_calculations[calc] = True
            
            # Check figures
            if 'image' in data:
                image_path = os.path.join('output/images', data['image'])
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    print(f"\nVerified image: {data['image']}")
                    print(f"Resolution: {img.size}")
                    print(f"Mode: {img.mode}")
                    # Check figure type in path and description
                    for fig_type in required_figures:
                        # Check in path
                        if fig_type.lower() in current_path.lower():
                            required_figures[fig_type] = True
                            continue
                            
                        # Check in description
                        description = data.get('description', '')
                        if isinstance(description, str) and fig_type.lower() in description.lower():
                            required_figures[fig_type] = True
                            continue
                            
                        # Check in technical details
                        tech_details = data.get('technical_details', '')
                        if isinstance(tech_details, str):
                            if fig_type.lower() in tech_details.lower():
                                required_figures[fig_type] = True
                        elif isinstance(tech_details, dict):
                            if fig_type.lower() in str(tech_details).lower():
                                required_figures[fig_type] = True
            
            # Recursively check all nested dictionaries
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    check_content_recursively(value, current_path)
            
            # Recursively check all nested dictionaries
            for key, value in data.items():
                new_path = f"{path}/{title}" if path else title
                if isinstance(value, (dict, list)):
                    check_content_recursively(value, new_path)
        elif isinstance(data, list):
            for item in data:
                check_content_recursively(item, path)
    
    # Start recursive check from root
    for section in document['sections'].values():
        check_content_recursively(section)
    
    # Print verification results
    print("\nContent Verification Results:")
    print("\nRequired Sections:")
    for section, found in required_sections.items():
        status = "✓" if found else "✗"
        print(f"{section}: {status}")
    
    print("\nRequired Calculations:")
    for calc, found in required_calculations.items():
        status = "✓" if found else "✗"
        print(f"{calc}: {status}")
    
    print("\nRequired Figures:")
    for fig, found in required_figures.items():
        status = "✓" if found else "✗"
        print(f"{fig}: {status}")
    
    # Check for missing content
    missing_sections = [s for s, found in required_sections.items() if not found]
    missing_calcs = [c for c, found in required_calculations.items() if not found]
    missing_figs = [f for f, found in required_figures.items() if not found]
    
    if missing_sections or missing_calcs or missing_figs:
        print("\nMissing Content:")
        if missing_sections:
            print("\nMissing Sections:", ", ".join(missing_sections))
        if missing_calcs:
            print("Missing Calculations:", ", ".join(missing_calcs))
        if missing_figs:
            print("Missing Figures:", ", ".join(missing_figs))
        return False
    
    print("\nAll required content has been properly extracted and organized.")
    return True

if __name__ == "__main__":
    success = verify_content_completeness()
    exit(0 if success else 1)
