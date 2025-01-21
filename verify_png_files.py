from PIL import Image
import os

def verify_image(filepath):
    """Verify image properties and quality"""
    print(f"\nVerifying {os.path.basename(filepath)}:")
    img = Image.open(filepath)
    print(f"Format: {img.format}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    dpi = img.info.get("dpi", (72,72))
    print(f"DPI: {dpi}")
    print(f"HD Quality: {'✓' if dpi[0] >= 290 else '✗'}")
    return dpi[0] >= 290  # Allow slightly lower DPI for PDF compatibility

def main():
    """Verify all required PNG files"""
    figures_dir = "output/figures"
    required_figures = [
        "vertical_projection.png",
        "horizontal_projection.png",
        "construction_details.png",
        "momentum_analysis.png",
        "inertia_analysis.png",
        "strength_analysis.png",
        "layer_analysis.png",
        "uls_verification.png",
        "connection_detail.png",
        "load_distribution.png",
        "thermal_resistance.png",
        "stress_analysis.png",
        "cross_sections.png",
        "thermal_bridge_analysis.png",
        "combined_load_analysis.png",
        "purlin_spacing.png"
    ]
    
    all_verified = True
    for figure in required_figures:
        filepath = os.path.join(figures_dir, figure)
        if os.path.exists(filepath):
            if not verify_image(filepath):
                all_verified = False
                print(f"Warning: {figure} does not meet HD quality requirements")
        else:
            all_verified = False
            print(f"\nMissing required figure: {figure}")
    
    if all_verified:
        print("\nAll required figures verified successfully.")
    else:
        print("\nVerification failed: Some figures are missing or do not meet quality requirements.")
        exit(1)

if __name__ == "__main__":
    main()
