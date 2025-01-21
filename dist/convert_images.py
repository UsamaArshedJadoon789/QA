from PIL import Image
import os

# Map attachment filenames to our expected names
image_mapping = {
    'WhatsApp+Image+2025-01-19+at+12.51.25_99437b83.jpg': 'extracted_image_p8_1.png',
    'WhatsApp+Image+2025-01-19+at+12.51.25_68a2f4a7.jpg': 'extracted_image_p9_1.png',
    'WhatsApp+Image+2025-01-19+at+12.51.25_14fbe49e.jpg': 'extracted_image_p10_1.png'
}

attachments_dir = os.path.expanduser('~/attachments')
output_dir = 'output/images'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each image
for dirpath, dirnames, filenames in os.walk(attachments_dir):
    for filename in filenames:
        if filename in image_mapping:
            input_path = os.path.join(dirpath, filename)
            output_path = os.path.join(output_dir, image_mapping[filename])
            
            # Convert and save as PNG
            img = Image.open(input_path)
            img = img.convert('RGB')  # Ensure RGB mode
            img.save(output_path, 'PNG', quality=95, optimize=True)
            print(f"Converted and saved: {output_path}")

print("\nImage conversion complete")
