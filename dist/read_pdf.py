import fitz  # PyMuPDF
import os
from PIL import Image
import io

def analyze_pdf(pdf_path):
    """Analyze PDF content including text and images"""
    print(f"\nAnalyzing PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    doc = fitz.open(pdf_path)
    print(f"\nDocument has {len(doc)} pages")
    
    # Extract and analyze content
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"\n=== Page {page_num + 1} ===")
        
        # Get text
        text = page.get_text()
        print("\nText content:")
        print(text)
        
        # Get images
        image_list = page.get_images()
        print(f"\nFound {len(image_list)} images on page {page_num + 1}")
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert to PIL Image for analysis
            image = Image.open(io.BytesIO(image_bytes))
            print(f"\nImage {img_index + 1}:")
            print(f"Format: {image.format}")
            print(f"Size: {image.size}")
            print(f"Mode: {image.mode}")
            
            # Save image for later use
            ext = image.format.lower() if image.format else 'png'  # Default to png if format is None
            image_filename = f"extracted_image_p{page_num + 1}_{img_index + 1}.{ext}"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            print(f"Saved as: {image_filename}")

if __name__ == "__main__":
    pdf_path = os.path.expanduser("~/attachments/ad93d7f9-8ad0-4a68-9e64-4cf2b135e276/DOC-20250119-WA0109..pdf")
    analyze_pdf(pdf_path)
