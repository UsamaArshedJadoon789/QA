import fitz
import os

def verify_diagrams():
    """Verify specific diagrams and captions in the PDF"""
    print("\nVerifying specific diagrams and captions...")
    pdf_path = "output/documentation/final_structural_analysis_report.pdf"
    doc = fitz.open(pdf_path)
    
    # Keywords to look for in each diagram/caption
    diagram_keywords = {
        "Vertical projection": ["Scale 1:50", "h1=2.5m", "h2=2.65m", "16°", "-1.4 m.a.s.l"],
        "Horizontal projection": ["Scale 1:50", "7.2m", "6.6m", "10.8m", "1.1m"],
        "Construction details": ["Scale 1:10", "150×150mm", "80×160mm", "100×200mm"]
    }
    
    found_diagrams = {name: {"found": False, "page": None} for name in diagram_keywords}
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        images = doc[page_num].get_images()
        
        if images:
            print(f"\nPage {page_num + 1} contains {len(images)} image(s)")
            
            # Check for diagram keywords in text
            for diagram_name, keywords in diagram_keywords.items():
                if not found_diagrams[diagram_name]["found"]:
                    keyword_count = sum(1 for kw in keywords if kw.lower() in text.lower())
                    if keyword_count >= 3:  # Match if at least 3 keywords are found
                        found_diagrams[diagram_name] = {
                            "found": True,
                            "page": page_num + 1,
                            "keywords_matched": keyword_count
                        }
                        print(f"Found {diagram_name} on page {page_num + 1}")
                        print(f"Matched {keyword_count}/{len(keywords)} keywords")
                        
                        # Verify image quality
                        for img in images:
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_rect = doc[page_num].get_image_rects(xref)[0]
                            width_inch = image_rect.width / 72
                            height_inch = image_rect.height / 72
                            effective_dpi = (
                                base_image["width"] / width_inch,
                                base_image["height"] / height_inch
                            )
                            print(f"Image quality: {effective_dpi[0]:.1f} x {effective_dpi[1]:.1f} DPI")
                            if effective_dpi[0] < 290 or effective_dpi[1] < 290:
                                print(f"Warning: Image DPI below 290 on page {page_num + 1}")
    
    print("\nDiagram Verification Results:")
    print("============================")
    all_found = True
    for name, info in found_diagrams.items():
        status = "✓" if info["found"] else "✗"
        location = f"Page {info['page']}" if info["found"] else "Not found"
        print(f"{name}: {status} ({location})")
        if not info["found"]:
            all_found = False
    
    if all_found:
        print("\nAll required diagrams verified successfully!")
    else:
        print("\nWarning: Some diagrams could not be verified!")
    
    doc.close()

if __name__ == "__main__":
    verify_diagrams()
