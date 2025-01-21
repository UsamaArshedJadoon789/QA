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
    
    # Define figure captions
    figure_captions = [
        "Figure 3: Vertical projection (Scale 1:50) showing building elevations and structural configuration. The drawing illustrates the primary heights (h1=2.5m, h2=2.65m), roof angle (16°), and ground level (-1.4 m.a.s.l). Wall construction utilizes MAX 220 block with mineral wool insulation for optimal thermal performance.",
        "Figure 4: Horizontal projection (Scale 1:50) detailing building layout and dimensions. The plan shows primary measurements: width (b=7.2m), lengths (L1=6.6m, L2=10.8m), and purlin spacing (s=1.1m). Structural grid and member placement are indicated for precise construction reference.",
        "Figure 5: Construction details (Scale 1:10) illustrating critical structural connections and assemblies. Key components include C27 timber elements (columns 150×150mm, purlins 80×160mm, rafters 100×200mm) and wall assembly (MAX 220 block + 150mm mineral wool). Details show precise connection methods and thermal envelope integration for optimal performance."
    ]
    
    # Process first PDF with section markers
    for page_num, page in enumerate(reader1.pages):
        text = page.extract_text()
        
        # Add IEEE-style header using reportlab
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("Helvetica", 9)
        can.drawString(50, 800, "IEEE TRANSACTIONS ON CIVIL ENGINEERING")
        
        # Handle references page
        if "References" in text:
            from reportlab.lib import colors
            from reportlab.platypus import Table, TableStyle
            from reportlab.lib.units import mm
            
            # Define references with wrapped text
            references = [
                ["[1]", "EN 1995-1-1:2004", "Eurocode 5: Design of timber structures - Part 1-1: General - Common rules and rules for buildings"],
                ["[2]", "EN 1990:2002", "Eurocode: Basis of structural design"],
                ["[3]", "EN 1991-1-3:2003", "Eurocode 1: Actions on structures - Part 1-3: General actions - Snow loads"],
                ["[4]", "EN 1991-1-4:2005", "Eurocode 1: Actions on structures - Part 1-4: General actions - Wind actions"],
                ["[5]", "EN ISO 6946:2017", "Building components and building elements - Thermal resistance and thermal transmittance"],
                ["[6]", "EN ISO 13788:2012", "Hygrothermal performance of building components and building elements"]
            ]
            
            # Calculate available width (A4 width = 210mm, margins = 25mm each side)
            available_width = 160 * mm  # 210mm - 2 * 25mm
            
            # Define column widths (in mm)
            col_widths = [10*mm, 45*mm, 105*mm]  # Total = 160mm
            
            # Create table with wrapped text
            table = Table(references, colWidths=col_widths, repeatRows=1)
            
            # Style the table
            table_style = TableStyle([
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('WORDWRAP', (0,0), (-1,-1)),
            ])
            table.setStyle(table_style)
            
            # Draw table
            table.wrapOn(can, available_width, 700)
            table.drawOn(can, 25*mm, 500)
        
        # Add figure caption if this is a diagram page (pages 8-10 for our new diagrams)
        if page_num in [7, 8, 9]:  # 0-based indexing
            caption_idx = page_num - 7
            if caption_idx < len(figure_captions):
                can.setFont("Helvetica", 10)
                # Split caption into multiple lines if needed
                caption = figure_captions[caption_idx]
                words = caption.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    if len(' '.join(current_line)) > 80:  # Max line length
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw caption lines
                y_pos = 100  # Start from bottom
                for line in lines:
                    can.drawString(50, y_pos, line)
                    y_pos += 15  # Line spacing
        
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
