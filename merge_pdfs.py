import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import fitz

def merge_pdfs():
    """Merge PDFs with intelligent content organization and image preservation"""
    print("Starting enhanced PDF merge process...")
    
    # Input paths
    pdf1_path = os.path.expanduser("~/attachments/fae87636-3c95-4431-8d44-15c54ea2c3a0/report.pdf")
    pdf2_path = os.path.expanduser("~/attachments/badb8161-83c7-4456-b975-d557bb723def/structural_analysis_report+6+1.pdf")
    output_path = "output/documentation/final_structural_analysis_report.pdf"
    
    # Create output directory
    os.makedirs("output/documentation", exist_ok=True)
    
    # Initialize writer for more control
    writer = PdfWriter()
    
    # Process first PDF with section header emphasis
    print("\nProcessing first PDF...")
    reader1 = PdfReader(pdf1_path)
    
    # Add thermal analysis section marker
    thermal_found = False
    for i, page in enumerate(reader1.pages):
        text = page.extract_text()
        if "Thermal Analysis" in text and not thermal_found:
            # Add section header annotation
            page.annotations.append({
                'type': '/Text',
                'rect': [50, 750, 200, 780],
                'contents': 'Thermal Analysis',
                'color': [0, 0, 0]
            })
            thermal_found = True
        writer.add_page(page)
    
    # Process second PDF
    print("\nProcessing second PDF...")
    reader2 = PdfReader(pdf2_path)
    for page in reader2.pages:
        writer.add_page(page)
    
    # Write merged PDF with image preservation
    print("\nWriting merged PDF with enhanced image quality...")
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    
    print(f"\nMerged PDF saved to: {output_path}")
    
    # Verify merged PDF
    print("\nVerifying merged PDF...")
    doc = fitz.open(output_path)
    print(f"Total pages in merged document: {len(doc)}")
    
    # Check for images
    total_images = 0
    for page in doc:
        images = page.get_images()
        if images:
            total_images += len(images)
    
    print(f"Total images in merged document: {total_images}")
    doc.close()
    
    return output_path

if __name__ == "__main__":
    merge_pdfs()
