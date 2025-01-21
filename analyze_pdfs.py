import fitz
import os

def analyze_pdf(path, name):
    """Analyze PDF content and structure"""
    print(f"\nAnalyzing {name}:")
    print("=" * 50)
    doc = fitz.open(path)
    
    print(f"Total Pages: {len(doc)}")
    
    # Track sections and figures
    sections = []
    figures = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # Look for section headings
        lines = text.split("\n")
        for line in lines:
            if any(keyword in line.lower() for keyword in ["section", "chapter", "analysis", "calculation"]):
                sections.append(f"Page {page_num + 1}: {line.strip()}")
        
        # Count images
        images = page.get_images()
        if images:
            figures.append(f"Page {page_num + 1}: {len(images)} image(s)")
    
    print("\nSections Found:")
    for section in sections:
        print(f"- {section}")
    
    print("\nFigures Found:")
    for figure in figures:
        print(f"- {figure}")
    
    doc.close()
    return sections, figures

def main():
    """Analyze both PDFs"""
    # Analyze both PDFs
    pdf1_path = os.path.expanduser("~/attachments/fae87636-3c95-4431-8d44-15c54ea2c3a0/report.pdf")
    pdf2_path = os.path.expanduser("~/attachments/badb8161-83c7-4456-b975-d557bb723def/structural_analysis_report+6+1.pdf")

    print("Starting PDF Analysis...")
    analyze_pdf(pdf1_path, "First PDF")
    analyze_pdf(pdf2_path, "Second PDF")

if __name__ == "__main__":
    main()
