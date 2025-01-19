#!/bin/bash
set -e

# Create output directory
mkdir -p exports/screenshots

# Start FreeCAD in background
DISPLAY=:0 freecad &
FREECAD_PID=$!

# Wait for FreeCAD to start
sleep 5

# For each DXF file
for dxf in exports/dataset5_*.dxf; do
    name=$(basename "$dxf" .dxf)
    echo "Processing $name..."
    
    # Open DXF file
    xdotool key ctrl+o
    sleep 1
    xdotool type "$dxf"
    xdotool key Return
    sleep 2
    
    # Fit view to content
    xdotool key v
    xdotool key f
    sleep 1
    
    # Take screenshot
    import -window root -resize 2048x1536 "exports/screenshots/${name}.png"
    sleep 1
done

# Close FreeCAD
kill $FREECAD_PID

echo "Screenshots captured successfully"
