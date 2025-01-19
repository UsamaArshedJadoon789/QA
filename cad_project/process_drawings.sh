#!/bin/bash

# Create output directory
mkdir -p exports/screenshots

# Function to process a DXF file
process_dxf() {
    local input_file=$1
    local output_name=$2
    local scale=$3
    
    echo "Processing: $input_file"
    
    # Convert DXF to SVG using LibreCAD CLI
    librecad-cli -o "exports/screenshots/${output_name}.svg" "$input_file"
    
    # Convert SVG to high-quality PNG
    convert -density 300 "exports/screenshots/${output_name}.svg" \
            -resize 2048x1536 \
            -background white \
            -flatten \
            "exports/screenshots/${output_name}.png"
    
    echo "Generated: ${output_name}.png"
}

# Process each drawing
if [ -f "exports/dataset5_vertical.dxf" ]; then
    process_dxf "exports/dataset5_vertical.dxf" "vertical_projection" "1:50"
fi

if [ -f "exports/dataset5_horizontal.dxf" ]; then
    process_dxf "exports/dataset5_horizontal.dxf" "horizontal_projection" "1:50"
fi

if [ -f "exports/dataset5_details.dxf" ]; then
    process_dxf "exports/dataset5_details.dxf" "detail_drawings" "1:10"
fi
