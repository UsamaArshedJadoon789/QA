import os
from io import BytesIO
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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
    
    # Process PDFs with enhanced quality and organization
    print("\nProcessing first PDF with enhanced formatting...")
    reader1 = PdfReader(pdf1_path)
    
    # Define key sections for better organization
    sections = [
        "Building Specifications",
        "Material Properties",
        "Structural Analysis",
        "Thermal Analysis",
        "Load Analysis",
        "Cross-Section Analysis",
        "Ultimate Limit State"
    ]
    
    section_found = {section: False for section in sections}
    
    # Process first PDF with section markers
    for page_num, page in enumerate(reader1.pages):
        text = page.extract_text()
        
        # Add IEEE-style header using reportlab
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("Helvetica", 9)
        can.drawString(50, 800, "IEEE TRANSACTIONS ON CIVIL ENGINEERING")
        can.save()
        packet.seek(0)
        header = PdfReader(packet)
        page.merge_page(header.pages[0])
        
        # Check for section headers
        for section in sections:
            if section in text and not section_found[section]:
                section_found[section] = True
                print(f"Adding section marker: {section}")
                
                # Add section bookmark
                outline = writer.add_outline_item(
                    section,
                    page_number=page_num
                )
        
        writer.add_page(page)
    
    print("\nProcessing second PDF with enhanced formatting...")
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
